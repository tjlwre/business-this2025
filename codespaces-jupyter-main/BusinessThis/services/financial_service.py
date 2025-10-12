"""
Financial service for BusinessThis
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from decimal import Decimal
from config.supabase_config import get_supabase_client
from models.financial_profile import FinancialProfile
from models.savings_goal import SavingsGoal
from models.transaction import Transaction
from core.calculations import get_all_safe_spends
import logging

class FinancialService:
    """Financial service for calculations and data management"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
    
    def get_financial_profile(self, user_id: str) -> Optional[FinancialProfile]:
        """Get user's financial profile"""
        try:
            result = self.supabase.table('financial_profiles').select('*').eq('user_id', user_id).execute()
            
            if result.data:
                profile_data = result.data[0]
                return FinancialProfile.from_dict(profile_data)
            else:
                return None
                
        except Exception as e:
            print(f"Error getting financial profile: {e}")
            return None
    
    def update_financial_profile(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update financial profile"""
        try:
            # Check if profile exists
            existing_profile = self.get_financial_profile(user_id)
            
            if existing_profile:
                # Update existing profile
                result = self.supabase.table('financial_profiles').update(data).eq('user_id', user_id).execute()
                
                if result.data:
                    updated_profile = FinancialProfile.from_dict(result.data[0])
                    return {
                        'success': True,
                        'profile': updated_profile.to_dict()
                    }
                else:
                    return {
                        'success': False,
                        'error': 'Failed to update financial profile'
                    }
            else:
                # Create new profile
                profile_data = {
                    'user_id': user_id,
                    **data
                }
                
                result = self.supabase.table('financial_profiles').insert(profile_data).execute()
                
                if result.data:
                    new_profile = FinancialProfile.from_dict(result.data[0])
                    return {
                        'success': True,
                        'profile': new_profile.to_dict()
                    }
                else:
                    return {
                        'success': False,
                        'error': 'Failed to create financial profile'
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'error': f'Error updating financial profile: {str(e)}'
            }
    
    def get_savings_goals(self, user_id: str) -> List[SavingsGoal]:
        """Get user's savings goals"""
        try:
            result = self.supabase.table('savings_goals').select('*').eq('user_id', user_id).order('priority', desc=False).execute()
            
            goals = []
            for goal_data in result.data:
                goal = SavingsGoal.from_dict(goal_data)
                goals.append(goal)
            
            return goals
            
        except Exception as e:
            print(f"Error getting savings goals: {e}")
            return []
    
    def create_savings_goal(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new savings goal"""
        try:
            goal_data = {
                'user_id': user_id,
                'name': data['name'],
                'target_amount': data['target_amount'],
                'current_amount': data.get('current_amount', 0),
                'target_date': data.get('target_date'),
                'monthly_contribution': data.get('monthly_contribution'),
                'priority': data.get('priority', 1),
                'is_achieved': False
            }
            
            result = self.supabase.table('savings_goals').insert(goal_data).execute()
            
            if result.data:
                goal = SavingsGoal.from_dict(result.data[0])
                return {
                    'success': True,
                    'goal': goal.to_dict()
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to create savings goal'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error creating savings goal: {str(e)}'
            }
    
    def update_savings_goal(self, user_id: str, goal_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a savings goal"""
        try:
            result = self.supabase.table('savings_goals').update(data).eq('id', goal_id).eq('user_id', user_id).execute()
            
            if result.data:
                goal = SavingsGoal.from_dict(result.data[0])
                return {
                    'success': True,
                    'goal': goal.to_dict()
                }
            else:
                return {
                    'success': False,
                    'error': 'Savings goal not found or update failed'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error updating savings goal: {str(e)}'
            }
    
    def delete_savings_goal(self, user_id: str, goal_id: str) -> Dict[str, Any]:
        """Delete a savings goal"""
        try:
            result = self.supabase.table('savings_goals').delete().eq('id', goal_id).eq('user_id', user_id).execute()
            
            return {
                'success': True,
                'message': 'Savings goal deleted successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error deleting savings goal: {str(e)}'
            }
    
    def calculate_safe_spending(self, user_id: str, savings_goal: Optional[float] = None, months_for_goal: Optional[int] = None) -> Dict[str, Any]:
        """Calculate safe spending amounts"""
        try:
            # Get financial profile
            profile = self.get_financial_profile(user_id)
            if not profile:
                return {
                    'error': 'Financial profile not found'
                }
            
            # Use provided values or get from profile
            monthly_income = float(profile.monthly_income)
            fixed_expenses = float(profile.fixed_expenses)
            variable_expenses = float(profile.variable_expenses)
            
            # Use provided savings goal or calculate from existing goals
            if savings_goal is None:
                goals = self.get_savings_goals(user_id)
                total_goal_amount = sum(float(goal.target_amount) for goal in goals)
                if total_goal_amount > 0:
                    savings_goal = total_goal_amount
                else:
                    savings_goal = 0
            
            if months_for_goal is None:
                months_for_goal = 12  # Default to 12 months
            
            # Calculate safe spending using existing function
            safe_spends = get_all_safe_spends(
                monthly_income,
                fixed_expenses,
                variable_expenses,
                savings_goal,
                months_for_goal
            )
            
            return safe_spends
            
        except Exception as e:
            return {
                'error': f'Error calculating safe spending: {str(e)}'
            }
    
    def calculate_financial_health_score(self, user_id: str) -> Dict[str, Any]:
        """Calculate comprehensive financial health score"""
        try:
            profile = self.get_financial_profile(user_id)
            if not profile:
                return {
                    'error': 'Financial profile not found'
                }
            
            scores = {}
            
            # Savings rate score (0-25 points)
            savings_rate = profile.calculate_savings_rate()
            if savings_rate >= 20:
                scores['savings_rate'] = 25
            elif savings_rate >= 15:
                scores['savings_rate'] = 20
            elif savings_rate >= 10:
                scores['savings_rate'] = 15
            elif savings_rate >= 5:
                scores['savings_rate'] = 10
            else:
                scores['savings_rate'] = max(0, int(savings_rate * 2))
            
            # Debt-to-income ratio score (0-25 points)
            debt_ratio = profile.calculate_debt_to_income_ratio()
            if debt_ratio <= 0.2:
                scores['debt_ratio'] = 25
            elif debt_ratio <= 0.3:
                scores['debt_ratio'] = 20
            elif debt_ratio <= 0.4:
                scores['debt_ratio'] = 15
            elif debt_ratio <= 0.5:
                scores['debt_ratio'] = 10
            else:
                scores['debt_ratio'] = max(0, 25 - int(debt_ratio * 50))
            
            # Emergency fund score (0-25 points)
            emergency_fund_progress = profile.calculate_emergency_fund_progress()
            if emergency_fund_progress >= 100:
                scores['emergency_fund'] = 25
            elif emergency_fund_progress >= 75:
                scores['emergency_fund'] = 20
            elif emergency_fund_progress >= 50:
                scores['emergency_fund'] = 15
            elif emergency_fund_progress >= 25:
                scores['emergency_fund'] = 10
            else:
                scores['emergency_fund'] = max(0, int(emergency_fund_progress / 4))
            
            # Investment score (0-25 points) - simplified for now
            # This would be more complex in a real implementation
            scores['investment'] = 10  # Default moderate score
            
            # Calculate overall score
            overall_score = sum(scores.values())
            
            # Determine health level
            if overall_score >= 90:
                health_level = 'Excellent'
            elif overall_score >= 75:
                health_level = 'Good'
            elif overall_score >= 60:
                health_level = 'Fair'
            elif overall_score >= 40:
                health_level = 'Poor'
            else:
                health_level = 'Critical'
            
            # Save score to database
            self.save_financial_health_score(user_id, overall_score, scores)
            
            return {
                'overall_score': overall_score,
                'health_level': health_level,
                'scores': scores,
                'recommendations': self.get_financial_recommendations(scores)
            }
            
        except Exception as e:
            return {
                'error': f'Error calculating financial health score: {str(e)}'
            }
    
    def save_financial_health_score(self, user_id: str, overall_score: int, scores: Dict[str, int]) -> bool:
        """Save financial health score to database"""
        try:
            score_data = {
                'user_id': user_id,
                'overall_score': overall_score,
                'savings_rate_score': scores.get('savings_rate', 0),
                'debt_ratio_score': scores.get('debt_ratio', 0),
                'emergency_fund_score': scores.get('emergency_fund', 0),
                'investment_score': scores.get('investment', 0)
            }
            
            result = self.supabase.table('financial_health_scores').insert(score_data).execute()
            return len(result.data) > 0
            
        except Exception as e:
            print(f"Error saving financial health score: {e}")
            return False
    
    def get_financial_recommendations(self, scores: Dict[str, int]) -> List[str]:
        """Get personalized financial recommendations based on scores"""
        recommendations = []
        
        if scores.get('savings_rate', 0) < 15:
            recommendations.append("Increase your savings rate by reducing expenses or increasing income")
        
        if scores.get('debt_ratio', 0) < 20:
            recommendations.append("Focus on paying down debt to improve your debt-to-income ratio")
        
        if scores.get('emergency_fund', 0) < 20:
            recommendations.append("Build your emergency fund to cover 3-6 months of expenses")
        
        if scores.get('investment', 0) < 15:
            recommendations.append("Consider starting an investment portfolio for long-term wealth building")
        
        if not recommendations:
            recommendations.append("Great job! Your financial health is in excellent shape")
        
        return recommendations
