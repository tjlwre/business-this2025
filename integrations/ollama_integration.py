"""
Ollama integration for BusinessThis
"""
import requests
import json
import os
from typing import Dict, Any, Optional

class OllamaIntegration:
    """Ollama local AI integration"""
    
    def __init__(self):
        self.ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        self.model = os.getenv('OLLAMA_MODEL', 'mistral')
    
    def _call_ollama(self, prompt: str, system_prompt: str = None, max_tokens: int = 500, temperature: float = 0.7) -> Optional[str]:
        """Make API call to Ollama"""
        try:
            # Format prompt for Mistral instruction format
            if system_prompt:
                formatted_prompt = f"<s>[INST] {system_prompt}\n\n{prompt} [/INST]"
            else:
                formatted_prompt = f"<s>[INST] {prompt} [/INST]"
            
            payload = {
                "model": self.model,
                "prompt": formatted_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                print(f"Ollama API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in Ollama call: {e}")
            return None
    
    def generate_financial_advice(self, user_context: str, question: str) -> Optional[str]:
        """Generate financial advice using Ollama"""
        system_prompt = "You are a professional financial advisor. Provide helpful, personalized financial advice based on the user's context. Be specific, actionable, and encouraging. Keep responses concise but informative."
        
        prompt = f"User Context: {user_context}\n\nQuestion: {question}\n\nPlease provide specific financial advice:"
        
        return self._call_ollama(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=500,
            temperature=0.7
        )
    
    def analyze_spending_patterns(self, transactions: list) -> Optional[str]:
        """Analyze spending patterns using Ollama"""
        system_prompt = "You are a financial analyst. Analyze spending patterns and provide actionable insights. Focus on trends, potential savings opportunities, and financial health indicators."
        
        transaction_summary = self._format_transactions(transactions)
        prompt = f"Analyze these recent transactions and provide insights:\n\n{transaction_summary}\n\nAnalysis:"
        
        return self._call_ollama(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=300,
            temperature=0.5
        )
    
    def _format_transactions(self, transactions: list) -> str:
        """Format transactions for AI analysis"""
        formatted = []
        for tx in transactions[:10]:  # Limit to recent 10 transactions
            formatted.append(f"{tx.get('category', 'Unknown')}: ${tx.get('amount', 0)}")
        return "\n".join(formatted)
    
    def health_check(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self) -> list:
        """Get list of available Ollama models"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except:
            return []
