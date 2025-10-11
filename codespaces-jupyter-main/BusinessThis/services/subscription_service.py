"""
Subscription service for BusinessThis
"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import stripe
import os
from config.supabase_config import get_supabase_client

class SubscriptionService:
    """Subscription service for managing user subscriptions"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        
        # Initialize Stripe
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        self.stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
    
    def get_subscription_status(self, user_id: str) -> Dict[str, Any]:
        """Get user's subscription status"""
        try:
            # Get user data
            user_result = self.supabase.table('users').select('*').eq('id', user_id).execute()
            if not user_result.data:
                return {'error': 'User not found'}
            
            user_data = user_result.data[0]
            
            # Get subscription details
            subscription_result = self.supabase.table('subscriptions').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            
            subscription_data = None
            if subscription_result.data:
                subscription_data = subscription_result.data[0]
            
            return {
                'user_id': user_id,
                'subscription_tier': user_data.get('subscription_tier', 'free'),
                'subscription_status': user_data.get('subscription_status', 'active'),
                'subscription_expires_at': user_data.get('subscription_expires_at'),
                'ai_usage_count': user_data.get('ai_usage_count', 0),
                'ai_usage_limit': user_data.get('ai_usage_limit', 0),
                'subscription_details': subscription_data
            }
            
        except Exception as e:
            return {'error': f'Error getting subscription status: {str(e)}'}
    
    def create_subscription(self, user_id: str, plan: str) -> Dict[str, Any]:
        """Create a new subscription"""
        try:
            # Define plan details
            plan_details = {
                'premium': {
                    'price_id': os.getenv('STRIPE_PREMIUM_PRICE_ID'),
                    'amount': 999,  # $9.99 in cents
                    'interval': 'month'
                },
                'pro': {
                    'price_id': os.getenv('STRIPE_PRO_PRICE_ID'),
                    'amount': 1999,  # $19.99 in cents
                    'interval': 'month'
                }
            }
            
            if plan not in plan_details:
                return {'error': 'Invalid plan'}
            
            # Get user email for Stripe customer
            user_result = self.supabase.table('users').select('email').eq('id', user_id).execute()
            if not user_result.data:
                return {'error': 'User not found'}
            
            user_email = user_result.data[0]['email']
            
            # Create or get Stripe customer
            customers = stripe.Customer.list(email=user_email, limit=1)
            if customers.data:
                customer_id = customers.data[0].id
            else:
                customer = stripe.Customer.create(
                    email=user_email,
                    metadata={'user_id': user_id}
                )
                customer_id = customer.id
            
            # Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': plan_details[plan]['price_id'],
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{os.getenv('FRONTEND_URL', 'http://localhost:8501')}/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{os.getenv('FRONTEND_URL', 'http://localhost:8501')}/cancel",
                metadata={
                    'user_id': user_id,
                    'plan': plan
                }
            )
            
            return {
                'success': True,
                'checkout_url': checkout_session.url,
                'session_id': checkout_session.id
            }
            
        except Exception as e:
            return {'error': f'Error creating subscription: {str(e)}'}
    
    def handle_stripe_webhook(self, payload: str, signature: str) -> Dict[str, Any]:
        """Handle Stripe webhook events"""
        try:
            webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
            event = stripe.Webhook.construct_event(payload, signature, webhook_secret)
            
            if event['type'] == 'checkout.session.completed':
                session = event['data']['object']
                user_id = session['metadata']['user_id']
                plan = session['metadata']['plan']
                
                # Update user subscription
                self.update_user_subscription(user_id, plan, 'active')
                
                # Create subscription record
                self.create_subscription_record(user_id, session['subscription'], plan)
                
            elif event['type'] == 'customer.subscription.updated':
                subscription = event['data']['object']
                customer_id = subscription['customer']
                
                # Get user by customer ID
                user_id = self.get_user_id_by_customer_id(customer_id)
                if user_id:
                    status = subscription['status']
                    plan = self.get_plan_from_subscription(subscription)
                    self.update_user_subscription(user_id, plan, status)
            
            elif event['type'] == 'customer.subscription.deleted':
                subscription = event['data']['object']
                customer_id = subscription['customer']
                
                # Get user by customer ID
                user_id = self.get_user_id_by_customer_id(customer_id)
                if user_id:
                    self.update_user_subscription(user_id, 'free', 'cancelled')
            
            return {'success': True}
            
        except Exception as e:
            return {'error': f'Error handling webhook: {str(e)}'}
    
    def update_user_subscription(self, user_id: str, tier: str, status: str) -> bool:
        """Update user's subscription in database"""
        try:
            # Calculate expiration date
            expires_at = None
            if tier != 'free' and status == 'active':
                expires_at = (datetime.utcnow() + timedelta(days=30)).isoformat()
            
            # Set AI usage limits
            # Set AI usage limits based on tier (Ollama is free to run)
            ai_usage_limit = 25  # Free tier gets 25 queries per month
            if tier == 'premium':
                ai_usage_limit = 100  # Premium gets 100 queries per month
            elif tier == 'pro':
                ai_usage_limit = -1  # Pro gets unlimited queries
            
            update_data = {
                'subscription_tier': tier,
                'subscription_status': status,
                'subscription_expires_at': expires_at,
                'ai_usage_limit': ai_usage_limit
            }
            
            result = self.supabase.table('users').update(update_data).eq('id', user_id).execute()
            return len(result.data) > 0
            
        except Exception as e:
            print(f"Error updating user subscription: {e}")
            return False
    
    def create_subscription_record(self, user_id: str, stripe_subscription_id: str, plan: str) -> bool:
        """Create subscription record in database"""
        try:
            subscription_data = {
                'user_id': user_id,
                'stripe_subscription_id': stripe_subscription_id,
                'plan_name': plan,
                'status': 'active'
            }
            
            result = self.supabase.table('subscriptions').insert(subscription_data).execute()
            return len(result.data) > 0
            
        except Exception as e:
            print(f"Error creating subscription record: {e}")
            return False
    
    def get_user_id_by_customer_id(self, customer_id: str) -> Optional[str]:
        """Get user ID by Stripe customer ID"""
        try:
            customer = stripe.Customer.retrieve(customer_id)
            user_id = customer.metadata.get('user_id')
            return user_id
        except Exception as e:
            print(f"Error getting user ID by customer ID: {e}")
            return None
    
    def get_plan_from_subscription(self, subscription: Dict[str, Any]) -> str:
        """Get plan name from Stripe subscription"""
        try:
            # This would need to be implemented based on your Stripe price IDs
            # For now, return a default
            return 'premium'
        except Exception as e:
            print(f"Error getting plan from subscription: {e}")
            return 'free'
    
    def cancel_subscription(self, user_id: str) -> Dict[str, Any]:
        """Cancel user's subscription"""
        try:
            # Get subscription record
            subscription_result = self.supabase.table('subscriptions').select('*').eq('user_id', user_id).eq('status', 'active').execute()
            
            if not subscription_result.data:
                return {'error': 'No active subscription found'}
            
            subscription_data = subscription_result.data[0]
            stripe_subscription_id = subscription_data['stripe_subscription_id']
            
            # Cancel in Stripe
            stripe.Subscription.modify(stripe_subscription_id, cancel_at_period_end=True)
            
            # Update in database
            self.update_user_subscription(user_id, 'free', 'cancelled')
            
            return {'success': True, 'message': 'Subscription cancelled successfully'}
            
        except Exception as e:
            return {'error': f'Error cancelling subscription: {str(e)}'}
    
    def get_subscription_plans(self) -> Dict[str, Any]:
        """Get available subscription plans"""
        return {
            'free': {
                'name': 'Free',
                'price': 0,
                'features': [
                    'Basic calculator',
                    '1 savings goal',
                    'Financial health score',
                    'Basic reports'
                ],
                'ai_usage_limit': 25  # Free tier gets 25 queries per month
            },
            'premium': {
                'name': 'Premium',
                'price': 9.99,
                'features': [
                    'Everything in Free',
                    '5 savings goals',
                    'Advanced analytics',
                    'PDF exports',
                    'Email notifications',
                    '50 AI interactions/month'
                ],
                'ai_usage_limit': 100  # Premium gets 100 queries per month
            },
            'pro': {
                'name': 'Pro',
                'price': 19.99,
                'features': [
                    'Everything in Premium',
                    'Unlimited savings goals',
                    'AI financial coaching',
                    'Investment tracking',
                    'API access',
                    'White-label options',
                    'Unlimited AI interactions'
                ],
                'ai_usage_limit': -1  # Pro gets unlimited queries
            }
        }
