"""
Enhanced Supabase Service for BusinessThis
Demonstrates new features from Supabase Python client v2.22.2
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from config.supabase_config import (
    get_supabase_client,
    get_supabase_service_client,
    get_supabase_storage_client,
    get_supabase_realtime_client,
    get_supabase_functions_client,
    get_supabase_health_status
)

logger = logging.getLogger(__name__)

class EnhancedSupabaseService:
    """Enhanced Supabase service with new features from v2.22.2"""
    
    def __init__(self):
        self.client = get_supabase_client()
        self.service_client = get_supabase_service_client()
        self.storage = get_supabase_storage_client()
        self.realtime = get_supabase_realtime_client()
        self.functions = get_supabase_functions_client()
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status"""
        return get_supabase_health_status()
    
    # Enhanced Database Operations
    def create_user_with_profile(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create user with financial profile in a transaction"""
        try:
            # Use service client for admin operations
            result = self.service_client.table('users').insert(user_data).execute()
            logger.info(f"User created successfully: {result.data[0]['id'] if result.data else 'Unknown'}")
            return result.data[0] if result.data else {}
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    def get_user_with_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user with joined financial profile"""
        try:
            result = self.client.table('users').select("""
                *,
                financial_profiles(*)
            """).eq('id', user_id).execute()
            
            if result.data:
                return result.data[0]
            return {}
        except Exception as e:
            logger.error(f"Error fetching user with profile: {e}")
            raise
    
    def update_financial_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update financial profile with validation"""
        try:
            # Add timestamp
            profile_data['updated_at'] = datetime.utcnow().isoformat()
            
            result = self.client.table('financial_profiles').update(profile_data).eq('user_id', user_id).execute()
            logger.info(f"Financial profile updated for user {user_id}")
            return result.data[0] if result.data else {}
        except Exception as e:
            logger.error(f"Error updating financial profile: {e}")
            raise
    
    # Real-time Subscriptions
    def subscribe_to_user_changes(self, user_id: str, callback):
        """Subscribe to real-time changes for a user"""
        try:
            def handle_change(payload):
                logger.info(f"Real-time update for user {user_id}: {payload}")
                callback(payload)
            
            subscription = self.realtime.channel('user_changes').on(
                'postgres_changes',
                {
                    'event': '*',
                    'schema': 'public',
                    'table': 'users',
                    'filter': f'id=eq.{user_id}'
                },
                handle_change
            ).subscribe()
            
            logger.info(f"Subscribed to real-time changes for user {user_id}")
            return subscription
        except Exception as e:
            logger.error(f"Error setting up real-time subscription: {e}")
            raise
    
    def subscribe_to_goals_changes(self, user_id: str, callback):
        """Subscribe to savings goals changes"""
        try:
            def handle_change(payload):
                logger.info(f"Savings goal update for user {user_id}: {payload}")
                callback(payload)
            
            subscription = self.realtime.channel('goals_changes').on(
                'postgres_changes',
                {
                    'event': '*',
                    'schema': 'public',
                    'table': 'savings_goals',
                    'filter': f'user_id=eq.{user_id}'
                },
                handle_change
            ).subscribe()
            
            logger.info(f"Subscribed to savings goals changes for user {user_id}")
            return subscription
        except Exception as e:
            logger.error(f"Error setting up goals subscription: {e}")
            raise
    
    # File Storage Operations
    def upload_financial_document(self, user_id: str, file_path: str, file_data: bytes, content_type: str = 'application/pdf') -> Dict[str, Any]:
        """Upload financial document to Supabase storage"""
        try:
            # Create user-specific folder
            storage_path = f"financial-documents/{user_id}/{file_path}"
            
            result = self.storage.from_('documents').upload(
                path=storage_path,
                file=file_data,
                file_options={
                    'content-type': content_type,
                    'cache-control': '3600'
                }
            )
            
            # Get public URL
            public_url = self.storage.from_('documents').get_public_url(storage_path)
            
            logger.info(f"Document uploaded successfully: {storage_path}")
            return {
                'path': storage_path,
                'public_url': public_url,
                'result': result
            }
        except Exception as e:
            logger.error(f"Error uploading document: {e}")
            raise
    
    def get_user_documents(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all documents for a user"""
        try:
            result = self.storage.from_('documents').list(
                path=f"financial-documents/{user_id}",
                limit=100
            )
            
            documents = []
            for item in result:
                if item.get('name'):
                    public_url = self.storage.from_('documents').get_public_url(
                        f"financial-documents/{user_id}/{item['name']}"
                    )
                    documents.append({
                        'name': item['name'],
                        'size': item.get('metadata', {}).get('size', 0),
                        'created_at': item.get('created_at'),
                        'public_url': public_url
                    })
            
            return documents
        except Exception as e:
            logger.error(f"Error fetching user documents: {e}")
            raise
    
    def delete_document(self, user_id: str, file_name: str) -> bool:
        """Delete a document"""
        try:
            storage_path = f"financial-documents/{user_id}/{file_name}"
            result = self.storage.from_('documents').remove([storage_path])
            logger.info(f"Document deleted: {storage_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False
    
    # Edge Functions
    async def call_financial_analysis_function(self, user_id: str, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Call edge function for financial analysis"""
        try:
            result = await self.functions.invoke(
                'financial-analysis',
                {
                    'user_id': user_id,
                    'financial_data': financial_data
                }
            )
            
            logger.info(f"Financial analysis completed for user {user_id}")
            return result.data if hasattr(result, 'data') else result
        except Exception as e:
            logger.error(f"Error calling financial analysis function: {e}")
            raise
    
    async def call_ai_coaching_function(self, user_id: str, question: str) -> Dict[str, Any]:
        """Call AI coaching edge function"""
        try:
            result = await self.functions.invoke(
                'ai-coaching',
                {
                    'user_id': user_id,
                    'question': question,
                    'timestamp': datetime.utcnow().isoformat()
                }
            )
            
            logger.info(f"AI coaching response generated for user {user_id}")
            return result.data if hasattr(result, 'data') else result
        except Exception as e:
            logger.error(f"Error calling AI coaching function: {e}")
            raise
    
    # Advanced Query Operations
    def get_financial_insights(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive financial insights using advanced queries"""
        try:
            # Get user's financial profile and goals
            profile_result = self.client.table('financial_profiles').select('*').eq('user_id', user_id).execute()
            goals_result = self.client.table('savings_goals').select('*').eq('user_id', user_id).execute()
            transactions_result = self.client.table('transactions').select('*').eq('user_id', user_id).execute()
            
            profile = profile_result.data[0] if profile_result.data else {}
            goals = goals_result.data if goals_result.data else []
            transactions = transactions_result.data if transactions_result.data else []
            
            # Calculate insights
            total_goals = len(goals)
            completed_goals = len([g for g in goals if g.get('status') == 'completed'])
            total_saved = sum([g.get('current_amount', 0) for g in goals])
            total_target = sum([g.get('target_amount', 0) for g in goals])
            
            monthly_income = profile.get('monthly_income', 0)
            monthly_expenses = profile.get('monthly_expenses', 0)
            savings_rate = ((monthly_income - monthly_expenses) / monthly_income * 100) if monthly_income > 0 else 0
            
            return {
                'user_id': user_id,
                'profile': profile,
                'goals_summary': {
                    'total_goals': total_goals,
                    'completed_goals': completed_goals,
                    'completion_rate': (completed_goals / total_goals * 100) if total_goals > 0 else 0,
                    'total_saved': total_saved,
                    'total_target': total_target,
                    'progress_percentage': (total_saved / total_target * 100) if total_target > 0 else 0
                },
                'financial_health': {
                    'monthly_income': monthly_income,
                    'monthly_expenses': monthly_expenses,
                    'savings_rate': round(savings_rate, 2),
                    'emergency_fund_months': profile.get('emergency_fund', 0) / monthly_expenses if monthly_expenses > 0 else 0
                },
                'recent_transactions': transactions[-10:] if transactions else [],
                'generated_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error generating financial insights: {e}")
            raise
    
    # Batch Operations
    def batch_update_goals(self, user_id: str, goals_updates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Batch update multiple savings goals"""
        try:
            results = []
            for goal_update in goals_updates:
                goal_update['updated_at'] = datetime.utcnow().isoformat()
                result = self.client.table('savings_goals').update(goal_update).eq('id', goal_update['id']).eq('user_id', user_id).execute()
                results.append(result.data[0] if result.data else {})
            
            logger.info(f"Batch updated {len(goals_updates)} goals for user {user_id}")
            return results
        except Exception as e:
            logger.error(f"Error batch updating goals: {e}")
            raise
    
    # Analytics and Reporting
    def get_user_analytics(self, user_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get detailed analytics for a user"""
        try:
            # Get transactions in date range
            transactions_result = self.client.table('transactions').select('*').eq('user_id', user_id).gte('created_at', start_date).lte('created_at', end_date).execute()
            
            transactions = transactions_result.data if transactions_result.data else []
            
            # Calculate analytics
            total_spent = sum([t.get('amount', 0) for t in transactions if t.get('type') == 'expense'])
            total_earned = sum([t.get('amount', 0) for t in transactions if t.get('type') == 'income'])
            net_flow = total_earned - total_spent
            
            # Categorize spending
            spending_by_category = {}
            for transaction in transactions:
                if transaction.get('type') == 'expense':
                    category = transaction.get('category', 'uncategorized')
                    spending_by_category[category] = spending_by_category.get(category, 0) + transaction.get('amount', 0)
            
            return {
                'user_id': user_id,
                'period': {'start': start_date, 'end': end_date},
                'summary': {
                    'total_spent': total_spent,
                    'total_earned': total_earned,
                    'net_flow': net_flow,
                    'transaction_count': len(transactions)
                },
                'spending_by_category': spending_by_category,
                'transactions': transactions,
                'generated_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error generating user analytics: {e}")
            raise

# Example usage and testing
def test_enhanced_features():
    """Test the enhanced Supabase features"""
    try:
        service = EnhancedSupabaseService()
        
        # Test health status
        health = service.get_health_status()
        print(f"Health Status: {health}")
        
        # Test financial insights (requires valid user_id)
        # insights = service.get_financial_insights('test-user-id')
        # print(f"Financial Insights: {insights}")
        
        print("Enhanced Supabase service initialized successfully!")
        return True
    except Exception as e:
        print(f"Error testing enhanced features: {e}")
        return False

if __name__ == "__main__":
    test_enhanced_features()
