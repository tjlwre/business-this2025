"""
Authentication service for BusinessThis
"""
from typing import Optional, Dict, Any
from datetime import datetime
from config.supabase_config import get_supabase_client, get_supabase_service_client
from core.models.user import User

class AuthService:
    """Authentication service"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self.supabase_service = get_supabase_service_client()
    
    def register_user(self, email: str, password: str, full_name: str = '') -> Dict[str, Any]:
        """Register a new user"""
        try:
            # Register with Supabase Auth
            auth_response = self.supabase.auth.sign_up({
                'email': email,
                'password': password,
                'options': {
                    'data': {
                        'full_name': full_name
                    }
                }
            })
            
            if auth_response.user:
                user_id = auth_response.user.id
                
                # Create user record in our users table
                user_data = {
                    'id': user_id,
                    'email': email,
                    'full_name': full_name,
                    'subscription_tier': 'free',
                    'subscription_status': 'active',
                    'ai_usage_count': 0,
                    'ai_usage_limit': 0,
                    'is_active': True
                }
                
                result = self.supabase.table('users').insert(user_data).execute()
                
                if result.data:
                    return {
                        'success': True,
                        'user_id': user_id,
                        'message': 'User registered successfully'
                    }
                else:
                    return {
                        'success': False,
                        'error': 'Failed to create user record'
                    }
            else:
                return {
                    'success': False,
                    'error': 'Failed to register user with Supabase Auth'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Registration failed: {str(e)}'
            }
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Login user"""
        try:
            # Authenticate with Supabase Auth
            auth_response = self.supabase.auth.sign_in_with_password({
                'email': email,
                'password': password
            })
            
            if auth_response.user:
                user_id = auth_response.user.id
                
                # Get user data from our users table
                user_data = self.get_user_by_id(user_id)
                
                if user_data:
                    # Update last login
                    self.update_last_login(user_id)
                    
                    return {
                        'success': True,
                        'user_id': user_id,
                        'user': user_data.to_dict()
                    }
                else:
                    return {
                        'success': False,
                        'error': 'User not found in database'
                    }
            else:
                return {
                    'success': False,
                    'error': 'Invalid email or password'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Login failed: {str(e)}'
            }
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            result = self.supabase.table('users').select('*').eq('id', user_id).execute()
            
            if result.data:
                user_data = result.data[0]
                return User.from_dict(user_data)
            else:
                return None
                
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            result = self.supabase.table('users').select('*').eq('email', email).execute()
            
            if result.data:
                user_data = result.data[0]
                return User.from_dict(user_data)
            else:
                return None
                
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def update_user(self, user_id: str, data: Dict[str, Any]) -> bool:
        """Update user data"""
        try:
            result = self.supabase.table('users').update(data).eq('id', user_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def update_last_login(self, user_id: str) -> bool:
        """Update user's last login timestamp"""
        try:
            result = self.supabase.table('users').update({
                'last_login': datetime.utcnow().isoformat()
            }).eq('id', user_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error updating last login: {e}")
            return False
    
    def update_subscription(self, user_id: str, tier: str, status: str, expires_at: Optional[str] = None) -> bool:
        """Update user's subscription"""
        try:
            update_data = {
                'subscription_tier': tier,
                'subscription_status': status
            }
            
            if expires_at:
                update_data['subscription_expires_at'] = expires_at
            
            # Set AI usage limits based on tier
            if tier == 'free':
                update_data['ai_usage_limit'] = 0
            elif tier == 'premium':
                update_data['ai_usage_limit'] = 50
            else:  # pro
                update_data['ai_usage_limit'] = -1  # Unlimited
            
            result = self.supabase.table('users').update(update_data).eq('id', user_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error updating subscription: {e}")
            return False
    
    def increment_ai_usage(self, user_id: str) -> bool:
        """Increment AI usage count for user"""
        try:
            # Get current usage
            user = self.get_user_by_id(user_id)
            if not user:
                return False
            
            new_count = user.ai_usage_count + 1
            
            result = self.supabase.table('users').update({
                'ai_usage_count': new_count
            }).eq('id', user_id).execute()
            
            return len(result.data) > 0
        except Exception as e:
            print(f"Error incrementing AI usage: {e}")
            return False
    
    def reset_ai_usage(self, user_id: str) -> bool:
        """Reset AI usage count (typically done monthly)"""
        try:
            result = self.supabase.table('users').update({
                'ai_usage_count': 0
            }).eq('id', user_id).execute()
            
            return len(result.data) > 0
        except Exception as e:
            print(f"Error resetting AI usage: {e}")
            return False
    
    def logout_user(self, user_id: str) -> bool:
        """Logout user (invalidate session)"""
        try:
            # Supabase handles session invalidation automatically
            # We can add any cleanup logic here if needed
            return True
        except Exception as e:
            print(f"Error logging out user: {e}")
            return False
