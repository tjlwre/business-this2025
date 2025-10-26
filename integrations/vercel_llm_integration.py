"""
Vercel LLM API integration for BusinessThis
Provides AI capabilities using Vercel's LLM API
"""
import os
import requests
import json
from typing import Dict, Any, Optional, List
import logging

class VercelLLMIntegration:
    """Vercel LLM API integration for financial AI services"""
    
    def __init__(self):
        self.api_key = os.getenv('VERCEL_LLM_API_KEY')
        self.base_url = os.getenv('VERCEL_LLM_BASE_URL', 'https://api.vercel.com/v1/llm')
        self.model = os.getenv('VERCEL_LLM_MODEL', 'gpt-3.5-turbo')
        self.max_tokens = int(os.getenv('VERCEL_LLM_MAX_TOKENS', '1000'))
        self.temperature = float(os.getenv('VERCEL_LLM_TEMPERATURE', '0.7'))
        
        if not self.api_key:
            logging.warning("VERCEL_LLM_API_KEY not found in environment variables")
    
    def _make_api_call(self, messages: List[Dict[str, str]], max_tokens: int = None, temperature: float = None) -> Optional[str]:
        """Make API call to Vercel LLM"""
        try:
            if not self.api_key:
                logging.error("Vercel LLM API key not configured")
                return None
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.model,
                'messages': messages,
                'max_tokens': max_tokens or self.max_tokens,
                'temperature': temperature or self.temperature,
                'stream': False
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            else:
                logging.error(f"Vercel LLM API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Error calling Vercel LLM API: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error in Vercel LLM call: {e}")
            return None
    
    def generate_financial_advice(self, user_context: str, question: str) -> Optional[str]:
        """Generate financial advice using Vercel LLM"""
        system_prompt = """You are a professional financial advisor with expertise in personal finance, budgeting, and investment strategies. 
        Provide helpful, personalized financial advice based on the user's context. Be specific, actionable, and encouraging. 
        Keep responses concise but informative. Focus on practical steps the user can take to improve their financial situation."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context: {user_context}\n\nQuestion: {question}\n\nPlease provide specific financial advice:"}
        ]
        
        return self._make_api_call(messages, max_tokens=500, temperature=0.7)
    
    def analyze_spending_patterns(self, transactions: List[Dict[str, Any]]) -> Optional[str]:
        """Analyze spending patterns using Vercel LLM"""
        system_prompt = """You are a financial analyst specializing in spending pattern analysis. 
        Analyze the provided transactions and provide actionable insights about spending habits, 
        potential savings opportunities, and financial health indicators. Focus on trends, 
        categories that might need attention, and practical recommendations for improvement."""
        
        transaction_summary = self._format_transactions(transactions)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze these recent transactions and provide insights:\n\n{transaction_summary}\n\nPlease provide your analysis:"}
        ]
        
        return self._make_api_call(messages, max_tokens=400, temperature=0.5)
    
    def generate_daily_tip(self, user_context: str) -> Optional[str]:
        """Generate a personalized daily financial tip"""
        system_prompt = """You are a financial coach providing daily tips. Generate a specific, 
        actionable financial tip based on the user's profile. Make it practical and immediately applicable. 
        Keep it concise (1-2 sentences) and encouraging."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"User profile: {user_context}\n\nProvide a specific, actionable financial tip for today:"}
        ]
        
        return self._make_api_call(messages, max_tokens=200, temperature=0.8)
    
    def analyze_financial_goals(self, goals_context: str, user_profile: str) -> Optional[str]:
        """Analyze financial goals and provide recommendations"""
        system_prompt = """You are a financial planning expert. Analyze the user's financial goals 
        and provide specific recommendations for achieving them. Consider the user's financial situation, 
        timeline, and priorities. Provide actionable steps and realistic timelines."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"User Profile: {user_profile}\n\nFinancial Goals: {goals_context}\n\nPlease analyze these goals and provide recommendations:"}
        ]
        
        return self._make_api_call(messages, max_tokens=600, temperature=0.6)
    
    def get_investment_advice(self, user_context: str, portfolio_info: str) -> Optional[str]:
        """Get investment advice based on user profile and portfolio"""
        system_prompt = """You are an investment advisor with expertise in portfolio management and asset allocation. 
        Provide specific investment advice based on the user's financial situation and current portfolio. 
        Consider risk tolerance, time horizon, and financial goals. Be practical and educational."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"User Context: {user_context}\n\nPortfolio Information: {portfolio_info}\n\nPlease provide investment advice:"}
        ]
        
        return self._make_api_call(messages, max_tokens=700, temperature=0.6)
    
    def _format_transactions(self, transactions: List[Dict[str, Any]]) -> str:
        """Format transactions for AI analysis"""
        if not transactions:
            return "No recent transactions available"
        
        formatted = []
        for tx in transactions[:15]:  # Limit to recent 15 transactions
            amount = tx.get('amount', 0)
            category = tx.get('category', 'Unknown')
            date = tx.get('date', 'Unknown date')
            formatted.append(f"{date}: {category} - ${amount:,.2f}")
        
        return "\n".join(formatted)
    
    def health_check(self) -> bool:
        """Check if Vercel LLM API is accessible"""
        try:
            if not self.api_key:
                return False
            
            headers = {'Authorization': f'Bearer {self.api_key}'}
            response = requests.get(f"{self.base_url}/models", headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        try:
            if not self.api_key:
                return []
            
            headers = {'Authorization': f'Bearer {self.api_key}'}
            response = requests.get(f"{self.base_url}/models", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return [model.get('id', '') for model in data.get('data', [])]
            return []
        except:
            return []
    
    def set_model(self, model_name: str) -> bool:
        """Set the model to use for API calls"""
        try:
            available_models = self.get_available_models()
            if model_name in available_models:
                self.model = model_name
                return True
            return False
        except:
            return False
