"""
Stripe integration for BusinessThis
"""
import stripe
import os
from typing import Dict, Any, Optional

class StripeIntegration:
    """Stripe payment integration"""
    
    def __init__(self):
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        self.publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
    
    def create_customer(self, email: str, user_id: str) -> Optional[str]:
        """Create Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                metadata={'user_id': user_id}
            )
            return customer.id
        except Exception as e:
            print(f"Error creating Stripe customer: {e}")
            return None
    
    def create_checkout_session(self, customer_id: str, price_id: str, user_id: str) -> Optional[str]:
        """Create Stripe checkout session"""
        try:
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{os.getenv('FRONTEND_URL')}/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{os.getenv('FRONTEND_URL')}/cancel",
                metadata={'user_id': user_id}
            )
            return session.url
        except Exception as e:
            print(f"Error creating checkout session: {e}")
            return None
    
    def handle_webhook(self, payload: str, signature: str) -> Dict[str, Any]:
        """Handle Stripe webhook events"""
        try:
            webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
            event = stripe.Webhook.construct_event(payload, signature, webhook_secret)
            return {'success': True, 'event': event}
        except Exception as e:
            return {'success': False, 'error': str(e)}
