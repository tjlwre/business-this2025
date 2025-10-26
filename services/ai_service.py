"""
AI Service for BusinessThis
Handles all AI-related functionality using Vercel LLM
"""
import os
from typing import Dict, Any, Optional, List
from integrations.vercel_llm_integration import VercelLLMIntegration
import logging

class AIService:
    """AI service for financial coaching and analysis"""
    
    def __init__(self):
        self.vercel_llm = VercelLLMIntegration()
    
    def get_financial_coaching(self, profile: Dict[str, Any], question: str) -> Dict[str, Any]:
        """Get AI financial coaching based on user profile and question"""
        try:
            # Format user context from profile
            user_context = self._format_user_context(profile)
            
            # Get AI advice from Vercel LLM
            advice = self.vercel_llm.generate_financial_advice(user_context, question)
            
            if advice:
                return {
                    'success': True,
                    'advice': advice,
                    'provider': 'vercel_llm',
                    'timestamp': os.getenv('CURRENT_TIMESTAMP', '2024-01-01T00:00:00Z')
                }
            else:
                return {
                    'success': False,
                    'error': 'Unable to generate financial advice at this time',
                    'fallback_advice': self._get_fallback_advice(profile, question)
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'AI service error: {str(e)}',
                'fallback_advice': self._get_fallback_advice(profile, question)
            }
    
    def get_spending_recommendations(self, profile: Dict[str, Any], transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get AI-powered spending recommendations"""
        try:
            # Analyze spending patterns using Vercel LLM
            analysis = self.vercel_llm.analyze_spending_patterns(transactions)
            
            if analysis:
                return {
                    'success': True,
                    'recommendations': analysis,
                    'provider': 'vercel_llm',
                    'insights': self._extract_insights(analysis),
                    'action_items': self._generate_action_items(profile, analysis)
                }
            else:
                return {
                    'success': False,
                    'error': 'Unable to analyze spending patterns',
                    'fallback_recommendations': self._get_fallback_recommendations(profile)
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'AI analysis error: {str(e)}',
                'fallback_recommendations': self._get_fallback_recommendations(profile)
            }
    
    def get_daily_financial_tip(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get daily financial tip based on user profile"""
        try:
            # Generate personalized tip using Vercel LLM
            user_context = self._format_user_context(profile)
            tip = self.vercel_llm.generate_daily_tip(user_context)
            
            if tip:
                return {
                    'success': True,
                    'tip': tip,
                    'provider': 'vercel_llm',
                    'category': self._categorize_tip(tip),
                    'priority': self._assess_tip_priority(profile, tip)
                }
            else:
                return {
                    'success': False,
                    'error': 'Unable to generate daily tip',
                    'fallback_tip': self._get_fallback_tip(profile)
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'AI tip generation error: {str(e)}',
                'fallback_tip': self._get_fallback_tip(profile)
            }
    
    def analyze_financial_goals(self, profile: Dict[str, Any], goals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze financial goals and provide recommendations"""
        try:
            # Format goals for analysis
            goals_context = self._format_goals_context(goals)
            user_profile = self._format_user_context(profile)
            
            analysis = self.vercel_llm.analyze_financial_goals(goals_context, user_profile)
            
            if analysis:
                return {
                    'success': True,
                    'analysis': analysis,
                    'provider': 'vercel_llm',
                    'goal_priorities': self._prioritize_goals(goals, profile),
                    'timeline_recommendations': self._get_timeline_recommendations(goals, profile)
                }
            else:
                return {
                    'success': False,
                    'error': 'Unable to analyze financial goals',
                    'fallback_analysis': self._get_fallback_goal_analysis(goals, profile)
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'AI goal analysis error: {str(e)}',
                'fallback_analysis': self._get_fallback_goal_analysis(goals, profile)
            }
    
    def get_investment_advice(self, profile: Dict[str, Any], portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI investment advice"""
        try:
            # Format investment context
            user_context = self._format_user_context(profile)
            portfolio_info = self._format_investment_context(profile, portfolio)
            
            advice = self.vercel_llm.get_investment_advice(user_context, portfolio_info)
            
            if advice:
                return {
                    'success': True,
                    'advice': advice,
                    'provider': 'vercel_llm',
                    'risk_assessment': self._assess_investment_risk(profile, portfolio),
                    'allocation_recommendations': self._get_allocation_recommendations(profile, portfolio)
                }
            else:
                return {
                    'success': False,
                    'error': 'Unable to generate investment advice',
                    'fallback_advice': self._get_fallback_investment_advice(profile, portfolio)
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'AI investment advice error: {str(e)}',
                'fallback_advice': self._get_fallback_investment_advice(profile, portfolio)
            }
    
    def _format_user_context(self, profile: Dict[str, Any]) -> str:
        """Format user profile into context string"""
        context_parts = []
        
        if profile.get('age'):
            context_parts.append(f"Age: {profile['age']}")
        
        if profile.get('monthly_income'):
            context_parts.append(f"Monthly Income: ${profile['monthly_income']:,.2f}")
        
        if profile.get('fixed_expenses'):
            context_parts.append(f"Fixed Expenses: ${profile['fixed_expenses']:,.2f}")
        
        if profile.get('variable_expenses'):
            context_parts.append(f"Variable Expenses: ${profile['variable_expenses']:,.2f}")
        
        if profile.get('emergency_fund_current'):
            context_parts.append(f"Current Emergency Fund: ${profile['emergency_fund_current']:,.2f}")
        
        if profile.get('risk_tolerance'):
            context_parts.append(f"Risk Tolerance: {profile['risk_tolerance']}")
        
        return " | ".join(context_parts) if context_parts else "New user with minimal profile data"
    
    def _format_goals_context(self, goals: List[Dict[str, Any]]) -> str:
        """Format goals into context string"""
        if not goals:
            return "No financial goals set yet"
        
        goals_text = []
        for goal in goals:
            goal_text = f"Goal: {goal.get('name', 'Unnamed')} - Target: ${goal.get('target_amount', 0):,.2f}"
            if goal.get('target_date'):
                goal_text += f" by {goal['target_date']}"
            goals_text.append(goal_text)
        
        return " | ".join(goals_text)
    
    def _format_investment_context(self, profile: Dict[str, Any], portfolio: Dict[str, Any]) -> str:
        """Format investment context"""
        context_parts = [self._format_user_context(profile)]
        
        if portfolio:
            context_parts.append(f"Current Portfolio Value: ${portfolio.get('total_value', 0):,.2f}")
            context_parts.append(f"Stock Allocation: {portfolio.get('stock_percentage', 0)}%")
            context_parts.append(f"Bond Allocation: {portfolio.get('bond_percentage', 0)}%")
            context_parts.append(f"Cash Allocation: {portfolio.get('cash_percentage', 0)}%")
        
        return " | ".join(context_parts)
    
    def _get_fallback_advice(self, profile: Dict[str, Any], question: str) -> str:
        """Provide fallback advice when AI is unavailable"""
        return "I'm currently unable to provide personalized advice, but here are some general financial tips: 1) Build an emergency fund of 3-6 months expenses, 2) Pay down high-interest debt, 3) Start investing early for compound growth."
    
    def _get_fallback_recommendations(self, profile: Dict[str, Any]) -> List[str]:
        """Provide fallback spending recommendations"""
        recommendations = [
            "Review your monthly subscriptions and cancel unused services",
            "Consider cooking at home more often to reduce dining expenses",
            "Look for opportunities to negotiate bills like insurance or internet"
        ]
        
        if profile.get('variable_expenses', 0) > profile.get('fixed_expenses', 0):
            recommendations.append("Focus on reducing variable expenses which seem high")
        
        return recommendations
    
    def _get_fallback_tip(self, profile: Dict[str, Any]) -> str:
        """Provide fallback daily tip"""
        tips = [
            "Set up automatic transfers to your savings account",
            "Review your credit card statements for unnecessary charges",
            "Consider the 50/30/20 rule: 50% needs, 30% wants, 20% savings",
            "Track your spending for one week to identify patterns"
        ]
        
        # Return a tip based on profile
        if profile.get('emergency_fund_current', 0) < 1000:
            return "Build your emergency fund - aim for $1,000 as a starting goal"
        elif profile.get('risk_tolerance') == 'conservative':
            return "Consider high-yield savings accounts for your emergency fund"
        else:
            return tips[0]  # Default tip
    
    def _get_fallback_goal_analysis(self, goals: List[Dict[str, Any]], profile: Dict[str, Any]) -> str:
        """Provide fallback goal analysis"""
        if not goals:
            return "Start by setting your first financial goal - whether it's an emergency fund, vacation, or major purchase."
        
        return f"You have {len(goals)} financial goal(s). Focus on the most important one first and set up automatic savings to achieve it."
    
    def _get_fallback_investment_advice(self, profile: Dict[str, Any], portfolio: Dict[str, Any]) -> str:
        """Provide fallback investment advice"""
        return "Consider starting with low-cost index funds and gradually diversifying your portfolio based on your risk tolerance and time horizon."
    
    def _extract_insights(self, analysis: str) -> List[str]:
        """Extract key insights from AI analysis"""
        # Simple keyword extraction - could be enhanced
        insights = []
        if "spending" in analysis.lower():
            insights.append("Spending pattern analysis available")
        if "savings" in analysis.lower():
            insights.append("Savings opportunities identified")
        if "budget" in analysis.lower():
            insights.append("Budget optimization recommendations")
        return insights
    
    def _generate_action_items(self, profile: Dict[str, Any], analysis: str) -> List[str]:
        """Generate actionable items from analysis"""
        return [
            "Review your monthly budget",
            "Set up automatic savings transfers",
            "Track expenses for the next 30 days"
        ]
    
    def _categorize_tip(self, tip: str) -> str:
        """Categorize the financial tip"""
        tip_lower = tip.lower()
        if "emergency" in tip_lower or "savings" in tip_lower:
            return "Savings"
        elif "debt" in tip_lower or "pay" in tip_lower:
            return "Debt Management"
        elif "invest" in tip_lower or "portfolio" in tip_lower:
            return "Investing"
        else:
            return "General"
    
    def _assess_tip_priority(self, profile: Dict[str, Any], tip: str) -> str:
        """Assess tip priority based on user profile"""
        return "High"  # Default priority
    
    def _prioritize_goals(self, goals: List[Dict[str, Any]], profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize goals based on importance and timeline"""
        # Simple prioritization logic
        for goal in goals:
            goal['priority'] = "High" if goal.get('target_amount', 0) < 5000 else "Medium"
        return goals
    
    def _get_timeline_recommendations(self, goals: List[Dict[str, Any]], profile: Dict[str, Any]) -> List[str]:
        """Get timeline recommendations for goals"""
        return [
            "Focus on one goal at a time for maximum impact",
            "Set realistic timelines based on your income and expenses",
            "Consider breaking large goals into smaller milestones"
        ]
    
    def _assess_investment_risk(self, profile: Dict[str, Any], portfolio: Dict[str, Any]) -> str:
        """Assess investment risk level"""
        risk_tolerance = profile.get('risk_tolerance', 'moderate')
        return f"Risk Level: {risk_tolerance.title()}"
    
    def _get_allocation_recommendations(self, profile: Dict[str, Any], portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """Get asset allocation recommendations"""
        age = profile.get('age', 30)
        risk_tolerance = profile.get('risk_tolerance', 'moderate')
        
        if risk_tolerance == 'conservative':
            return {"stocks": 30, "bonds": 60, "cash": 10}
        elif risk_tolerance == 'aggressive':
            return {"stocks": 80, "bonds": 15, "cash": 5}
        else:  # moderate
            return {"stocks": 60, "bonds": 30, "cash": 10}