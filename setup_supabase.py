#!/usr/bin/env python3
"""
Supabase Setup Script for BusinessThis
This script helps you set up your Supabase configuration
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file with Supabase configuration"""
    env_content = """# Supabase Configuration
# Get these from your Supabase project dashboard: https://supabase.com/dashboard
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
STRIPE_PREMIUM_PRICE_ID=price_your_premium_price_id
STRIPE_PRO_PRICE_ID=price_your_pro_price_id

# PayPal Configuration
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
PAYPAL_MODE=sandbox  # or 'live' for production

# OpenAI Configuration
OPENAI_API_KEY=sk-your_openai_api_key

# Vercel LLM Configuration
VERCEL_LLM_API_KEY=your_vercel_llm_api_key
VERCEL_LLM_BASE_URL=https://api.vercel.com/v1/llm
VERCEL_LLM_MODEL=gpt-3.5-turbo
VERCEL_LLM_MAX_TOKENS=1000
VERCEL_LLM_TEMPERATURE=0.7

# SendGrid Configuration
SENDGRID_API_KEY=SG.your_sendgrid_api_key
FROM_EMAIL=noreply@businessthis.com

# Plaid Configuration (for bank integration)
PLAID_CLIENT_ID=your_plaid_client_id
PLAID_SECRET=your_plaid_secret
PLAID_ENV=sandbox  # or 'development', 'production'

# Application Configuration
SECRET_KEY=your_secret_key_for_sessions
DEBUG=True
ENVIRONMENT=development
API_BASE_URL=http://localhost:5000/api
FRONTEND_URL=http://localhost:8501

# Database Configuration (if using direct PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/businessthis

# Redis Configuration (for caching)
REDIS_URL=redis://localhost:6379/0

# File Storage
UPLOAD_FOLDER=uploads/
MAX_CONTENT_LENGTH=16777216  # 16MB
"""
    
    env_file = Path('.env')
    if env_file.exists():
        print("⚠️  .env file already exists. Backing up to .env.backup")
        env_file.rename('.env.backup')
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with template configuration")
    return True

def test_supabase_connection():
    """Test Supabase connection with current environment variables"""
    try:
        from config.supabase_config import test_supabase_connection
        print("🔍 Testing Supabase connection...")
        result = test_supabase_connection()
        if result:
            print("✅ Supabase connection successful!")
            return True
        else:
            print("❌ Supabase connection failed. Please check your credentials.")
            return False
    except Exception as e:
        print(f"❌ Error testing Supabase connection: {e}")
        return False

def interactive_setup():
    """Interactive setup for Supabase credentials"""
    print("🚀 BusinessThis Supabase Setup")
    print("=" * 50)
    print()
    print("To get your Supabase credentials:")
    print("1. Go to https://supabase.com/dashboard")
    print("2. Create a new project or select existing one")
    print("3. Go to Settings > API")
    print("4. Copy the Project URL and API keys")
    print()
    
    # Load existing .env if it exists
    env_vars = {}
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    
    # Get Supabase credentials
    supabase_url = input(f"Enter your Supabase URL [{env_vars.get('SUPABASE_URL', 'your_supabase_project_url')}]: ").strip()
    if not supabase_url or supabase_url == 'your_supabase_project_url':
        supabase_url = env_vars.get('SUPABASE_URL', 'your_supabase_project_url')
    
    supabase_anon_key = input(f"Enter your Supabase Anon Key [{env_vars.get('SUPABASE_ANON_KEY', 'your_supabase_anon_key')}]: ").strip()
    if not supabase_anon_key or supabase_anon_key == 'your_supabase_anon_key':
        supabase_anon_key = env_vars.get('SUPABASE_ANON_KEY', 'your_supabase_anon_key')
    
    supabase_service_key = input(f"Enter your Supabase Service Key [{env_vars.get('SUPABASE_SERVICE_KEY', 'your_supabase_service_key')}]: ").strip()
    if not supabase_service_key or supabase_service_key == 'your_supabase_service_key':
        supabase_service_key = env_vars.get('SUPABASE_SERVICE_KEY', 'your_supabase_service_key')
    
    # Generate a secret key if needed
    import secrets
    secret_key = secrets.token_urlsafe(32)
    
    # Update .env file
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            content = f.read()
        
        content = content.replace('your_supabase_project_url', supabase_url)
        content = content.replace('your_supabase_anon_key', supabase_anon_key)
        content = content.replace('your_supabase_service_key', supabase_service_key)
        content = content.replace('your_secret_key_for_sessions', secret_key)
        
        with open('.env', 'w') as f:
            f.write(content)
        
        print("✅ Updated .env file with your credentials")
    else:
        print("❌ .env file not found. Please run create_env_file() first.")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🔧 BusinessThis Supabase Setup")
    print("=" * 50)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        create_env_file()
        print()
        print("⚠️  Please edit the .env file with your actual Supabase credentials")
        print("   Then run this script again to test the connection.")
        return
    
    # Test current configuration
    print("🔍 Testing current Supabase configuration...")
    if test_supabase_connection():
        print("🎉 Setup complete! Your Supabase integration is working.")
    else:
        print()
        print("❌ Supabase connection failed.")
        print("   Please check your .env file and ensure your credentials are correct.")
        print()
        print("To fix this:")
        print("1. Edit the .env file with your correct Supabase credentials")
        print("2. Run this script again to test the connection")
        print()
        print("Or run the interactive setup:")
        print("   python setup_supabase.py --interactive")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_setup()
    else:
        main()
