"""
Centralized configuration for BusinessThis
"""
import os
from typing import Dict, Any

class Settings:
    """Application settings"""
    
    def __init__(self):
        self.load_from_env()
    
    def load_from_env(self):
        """Load configuration from environment variables"""
        
        # Database Configuration
        self.SUPABASE_URL = os.getenv('SUPABASE_URL')
        self.SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
        self.SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
        
        # Application Configuration
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
        self.DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
        self.ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
        
        # API Configuration
        self.API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000/api')
        self.FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:8501')
        
        # Payment Configuration
        self.STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
        self.STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
        self.STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
        self.STRIPE_PREMIUM_PRICE_ID = os.getenv('STRIPE_PREMIUM_PRICE_ID')
        self.STRIPE_PRO_PRICE_ID = os.getenv('STRIPE_PRO_PRICE_ID')
        
        # PayPal Configuration
        self.PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
        self.PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
        self.PAYPAL_MODE = os.getenv('PAYPAL_MODE', 'sandbox')
        
        # AI Configuration
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        
        # Email Configuration
        self.SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
        self.FROM_EMAIL = os.getenv('FROM_EMAIL', 'noreply@businessthis.com')
        
        # Bank Integration
        self.PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
        self.PLAID_SECRET = os.getenv('PLAID_SECRET')
        self.PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
        
        # Redis Configuration
        self.REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        
        # File Storage
        self.UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads/')
        self.MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', '16777216'))  # 16MB
    
    def get_database_config(self) -> Dict[str, str]:
        """Get database configuration"""
        return {
            'url': self.SUPABASE_URL,
            'anon_key': self.SUPABASE_ANON_KEY,
            'service_key': self.SUPABASE_SERVICE_KEY
        }
    
    def get_stripe_config(self) -> Dict[str, str]:
        """Get Stripe configuration"""
        return {
            'publishable_key': self.STRIPE_PUBLISHABLE_KEY,
            'secret_key': self.STRIPE_SECRET_KEY,
            'webhook_secret': self.STRIPE_WEBHOOK_SECRET,
            'premium_price_id': self.STRIPE_PREMIUM_PRICE_ID,
            'pro_price_id': self.STRIPE_PRO_PRICE_ID
        }
    
    def get_paypal_config(self) -> Dict[str, str]:
        """Get PayPal configuration"""
        return {
            'client_id': self.PAYPAL_CLIENT_ID,
            'client_secret': self.PAYPAL_CLIENT_SECRET,
            'mode': self.PAYPAL_MODE
        }
    
    def get_ai_config(self) -> Dict[str, str]:
        """Get AI configuration"""
        return {
            'openai_api_key': self.OPENAI_API_KEY
        }
    
    def get_email_config(self) -> Dict[str, str]:
        """Get email configuration"""
        return {
            'sendgrid_api_key': self.SENDGRID_API_KEY,
            'from_email': self.FROM_EMAIL
        }
    
    def get_plaid_config(self) -> Dict[str, str]:
        """Get Plaid configuration"""
        return {
            'client_id': self.PLAID_CLIENT_ID,
            'secret': self.PLAID_SECRET,
            'env': self.PLAID_ENV
        }
    
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT.lower() == 'production'
    
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.ENVIRONMENT.lower() == 'development'
    
    def validate_required_settings(self) -> list:
        """Validate that all required settings are present"""
        required_settings = [
            'SUPABASE_URL',
            'SUPABASE_ANON_KEY',
            'SUPABASE_SERVICE_KEY',
            'SECRET_KEY'
        ]
        
        missing = []
        for setting in required_settings:
            if not getattr(self, setting):
                missing.append(setting)
        
        return missing

# Global settings instance
settings = Settings()
