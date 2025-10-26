"""
OpenAI integration for BusinessThis
"""
import openai
import os
from typing import Dict, Any, Optional

class OpenAIIntegration:
    """OpenAI API integration"""
    
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
    
    def generate_financial_advice(self, user_context: str, question: str) -> Optional[str]:
        """Generate financial advice using OpenAI"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial advisor. Provide helpful, personalized financial advice."},
                    {"role": "user", "content": f"Context: {user_context}\nQuestion: {question}"}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating financial advice: {e}")
            return None
    
    def analyze_spending_patterns(self, transactions: list) -> Optional[str]:
        """Analyze spending patterns using AI"""
        try:
            transaction_summary = self._format_transactions(transactions)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Analyze spending patterns and provide insights."},
                    {"role": "user", "content": f"Transactions: {transaction_summary}"}
                ],
                max_tokens=300,
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error analyzing spending patterns: {e}")
            return None
    
    def _format_transactions(self, transactions: list) -> str:
        """Format transactions for AI analysis"""
        formatted = []
        for tx in transactions[:10]:  # Limit to recent 10 transactions
            formatted.append(f"{tx.get('category', 'Unknown')}: ${tx.get('amount', 0)}")
        return "\n".join(formatted)
