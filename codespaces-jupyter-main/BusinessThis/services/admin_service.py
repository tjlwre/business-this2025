"""
Admin service for BusinessThis
Handles admin dashboard, metrics, and user management
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from config.supabase_config import get_supabase_client, get_supabase_service_client

class AdminService:
    """Admin service for dashboard and user management"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self.supabase_service = get_supabase_service_client()
    
    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Get comprehensive dashboard metrics"""
        try:
            # Get user metrics
            user_metrics = self._get_user_metrics()
            
            # Get subscription metrics
            subscription_metrics = self._get_subscription_metrics()
            
            # Get financial metrics
            financial_metrics = self._get_financial_metrics()
            
            # Get AI usage metrics
            ai_metrics = self._get_ai_usage_metrics()
            
            return {
                'users': user_metrics,
                'subscriptions': subscription_metrics,
                'financial': financial_metrics,
                'ai_usage': ai_metrics,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {'error': f'Error getting dashboard metrics: {str(e)}'}
    
    def _get_user_metrics(self) -> Dict[str, Any]:
        """Get user-related metrics"""
        try:
            # Total users
            total_users_result = self.supabase.table('users').select('id', count='exact').execute()
            total_users = total_users_result.count if total_users_result.count else 0
            
            # New users this month
            month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            new_users_result = self.supabase.table('users').select('id', count='exact').gte('created_at', month_start.isoformat()).execute()
            new_users_this_month = new_users_result.count if new_users_result.count else 0
            
            # Active users (logged in within last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            active_users_result = self.supabase.table('users').select('id', count='exact').gte('last_login', thirty_days_ago.isoformat()).execute()
            active_users = active_users_result.count if active_users_result.count else 0
            
            # Users by subscription tier
            free_users_result = self.supabase.table('users').select('id', count='exact').eq('subscription_tier', 'free').execute()
            premium_users_result = self.supabase.table('users').select('id', count='exact').eq('subscription_tier', 'premium').execute()
            pro_users_result = self.supabase.table('users').select('id', count='exact').eq('subscription_tier', 'pro').execute()
            
            return {
                'total_users': total_users,
                'new_users_this_month': new_users_this_month,
                'active_users': active_users,
                'free_users': free_users_result.count if free_users_result.count else 0,
                'premium_users': premium_users_result.count if premium_users_result.count else 0,
                'pro_users': pro_users_result.count if pro_users_result.count else 0,
                'user_growth_rate': self._calculate_growth_rate(new_users_this_month, total_users)
            }
            
        except Exception as e:
            return {'error': f'Error getting user metrics: {str(e)}'}
    
    def _get_subscription_metrics(self) -> Dict[str, Any]:
        """Get subscription-related metrics"""
        try:
            # Monthly Recurring Revenue (MRR)
            premium_users_result = self.supabase.table('users').select('id', count='exact').eq('subscription_tier', 'premium').execute()
            pro_users_result = self.supabase.table('users').select('id', count='exact').eq('subscription_tier', 'pro').execute()
            
            premium_count = premium_users_result.count if premium_users_result.count else 0
            pro_count = pro_users_result.count if pro_users_result.count else 0
            
            mrr = (premium_count * 9.99) + (pro_count * 19.99)
            
            # Churn rate (users who cancelled in last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            churned_users_result = self.supabase.table('users').select('id', count='exact').eq('subscription_status', 'cancelled').gte('updated_at', thirty_days_ago.isoformat()).execute()
            churned_users = churned_users_result.count if churned_users_result.count else 0
            
            # Conversion rate (free to paid)
            total_paid_users = premium_count + pro_count
            total_users_result = self.supabase.table('users').select('id', count='exact').execute()
            total_users = total_users_result.count if total_users_result.count else 0
            
            conversion_rate = (total_paid_users / total_users * 100) if total_users > 0 else 0
            
            return {
                'mrr': mrr,
                'premium_subscribers': premium_count,
                'pro_subscribers': pro_count,
                'total_paid_users': total_paid_users,
                'churn_rate': (churned_users / total_paid_users * 100) if total_paid_users > 0 else 0,
                'conversion_rate': conversion_rate,
                'average_revenue_per_user': mrr / total_paid_users if total_paid_users > 0 else 0
            }
            
        except Exception as e:
            return {'error': f'Error getting subscription metrics: {str(e)}'}
    
    def _get_financial_metrics(self) -> Dict[str, Any]:
        """Get financial-related metrics"""
        try:
            # Users with financial profiles
            profiles_result = self.supabase.table('financial_profiles').select('id', count='exact').execute()
            users_with_profiles = profiles_result.count if profiles_result.count else 0
            
            # Average financial health score
            health_scores_result = self.supabase.table('financial_health_scores').select('overall_score').execute()
            if health_scores_result.data:
                avg_health_score = sum(score['overall_score'] for score in health_scores_result.data) / len(health_scores_result.data)
            else:
                avg_health_score = 0
            
            # Total savings goals
            goals_result = self.supabase.table('savings_goals').select('id', count='exact').execute()
            total_goals = goals_result.count if goals_result.count else 0
            
            # Achieved goals
            achieved_goals_result = self.supabase.table('savings_goals').select('id', count='exact').eq('is_achieved', True).execute()
            achieved_goals = achieved_goals_result.count if achieved_goals_result.count else 0
            
            return {
                'users_with_profiles': users_with_profiles,
                'average_health_score': round(avg_health_score, 1),
                'total_savings_goals': total_goals,
                'achieved_goals': achieved_goals,
                'goal_achievement_rate': (achieved_goals / total_goals * 100) if total_goals > 0 else 0
            }
            
        except Exception as e:
            return {'error': f'Error getting financial metrics: {str(e)}'}
    
    def _get_ai_usage_metrics(self) -> Dict[str, Any]:
        """Get AI usage metrics"""
        try:
            # Total AI usage
            ai_usage_result = self.supabase.table('ai_usage').select('id', count='exact').execute()
            total_ai_usage = ai_usage_result.count if ai_usage_result.count else 0
            
            # AI usage this month
            month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            monthly_ai_usage_result = self.supabase.table('ai_usage').select('id', count='exact').gte('created_at', month_start.isoformat()).execute()
            monthly_ai_usage = monthly_ai_usage_result.count if monthly_ai_usage_result.count else 0
            
            # Users using AI
            ai_users_result = self.supabase.table('ai_usage').select('user_id').execute()
            unique_ai_users = len(set(usage['user_id'] for usage in ai_users_result.data)) if ai_users_result.data else 0
            
            return {
                'total_ai_usage': total_ai_usage,
                'monthly_ai_usage': monthly_ai_usage,
                'unique_ai_users': unique_ai_users,
                'average_usage_per_user': total_ai_usage / unique_ai_users if unique_ai_users > 0 else 0
            }
            
        except Exception as e:
            return {'error': f'Error getting AI usage metrics: {str(e)}'}
    
    def _calculate_growth_rate(self, new_users: int, total_users: int) -> float:
        """Calculate user growth rate"""
        if total_users <= new_users:
            return 100.0
        return (new_users / (total_users - new_users)) * 100 if (total_users - new_users) > 0 else 0
    
    def get_user_list(self, page: int = 1, limit: int = 50, search: str = '') -> Dict[str, Any]:
        """Get paginated list of users"""
        try:
            offset = (page - 1) * limit
            
            query = self.supabase.table('users').select('*')
            
            if search:
                query = query.or_(f'email.ilike.%{search}%,full_name.ilike.%{search}%')
            
            result = query.range(offset, offset + limit - 1).execute()
            
            # Get total count
            count_result = self.supabase.table('users').select('id', count='exact').execute()
            total_count = count_result.count if count_result.count else 0
            
            return {
                'users': result.data,
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': total_count,
                    'pages': (total_count + limit - 1) // limit
                }
            }
            
        except Exception as e:
            return {'error': f'Error getting user list: {str(e)}'}
    
    def get_user_details(self, user_id: str) -> Dict[str, Any]:
        """Get detailed user information"""
        try:
            # Get user data
            user_result = self.supabase.table('users').select('*').eq('id', user_id).execute()
            if not user_result.data:
                return {'error': 'User not found'}
            
            user = user_result.data[0]
            
            # Get financial profile
            profile_result = self.supabase.table('financial_profiles').select('*').eq('user_id', user_id).execute()
            profile = profile_result.data[0] if profile_result.data else None
            
            # Get savings goals
            goals_result = self.supabase.table('savings_goals').select('*').eq('user_id', user_id).execute()
            goals = goals_result.data if goals_result.data else []
            
            # Get subscription details
            subscription_result = self.supabase.table('subscriptions').select('*').eq('user_id', user_id).execute()
            subscription = subscription_result.data[0] if subscription_result.data else None
            
            # Get AI usage
            ai_usage_result = self.supabase.table('ai_usage').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(10).execute()
            ai_usage = ai_usage_result.data if ai_usage_result.data else []
            
            return {
                'user': user,
                'profile': profile,
                'goals': goals,
                'subscription': subscription,
                'ai_usage': ai_usage
            }
            
        except Exception as e:
            return {'error': f'Error getting user details: {str(e)}'}
    
    def update_user_subscription(self, user_id: str, tier: str, status: str) -> Dict[str, Any]:
        """Update user subscription"""
        try:
            result = self.supabase.table('users').update({
                'subscription_tier': tier,
                'subscription_status': status
            }).eq('id', user_id).execute()
            
            if result.data:
                return {'success': True, 'message': 'Subscription updated successfully'}
            else:
                return {'error': 'Failed to update subscription'}
                
        except Exception as e:
            return {'error': f'Error updating subscription: {str(e)}'}
    
    def get_support_tickets(self, status: str = 'all') -> Dict[str, Any]:
        """Get support tickets"""
        try:
            query = self.supabase.table('support_tickets').select('*')
            
            if status != 'all':
                query = query.eq('status', status)
            
            result = query.order('created_at', desc=True).execute()
            
            return {'tickets': result.data}
            
        except Exception as e:
            return {'error': f'Error getting support tickets: {str(e)}'}
    
    def update_support_ticket(self, ticket_id: str, status: str, response: str = '') -> Dict[str, Any]:
        """Update support ticket"""
        try:
            update_data = {'status': status}
            if response:
                update_data['response'] = response
            
            result = self.supabase.table('support_tickets').update(update_data).eq('id', ticket_id).execute()
            
            if result.data:
                return {'success': True, 'message': 'Ticket updated successfully'}
            else:
                return {'error': 'Failed to update ticket'}
                
        except Exception as e:
            return {'error': f'Error updating ticket: {str(e)}'}
