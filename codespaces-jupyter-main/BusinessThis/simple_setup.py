#!/usr/bin/env python3
"""
BusinessThis Simple Setup
Interactive setup for API keys and configuration
"""
import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file with user input"""
    print("🔑 BusinessThis Environment Setup")
    print("=" * 40)
    print("We'll guide you through getting your API keys:")
    print()
    
    # Get Supabase credentials
    print("📊 SUPABASE SETUP:")
    print("1. Go to https://supabase.com")
    print("2. Create a new project")
    print("3. Go to Settings > API")
    print("4. Copy your Project URL and API keys")
    print()
    
    supabase_url = input("Enter your Supabase URL: ").strip()
    supabase_anon = input("Enter your Supabase Anon Key: ").strip()
    supabase_service = input("Enter your Supabase Service Role Key: ").strip()
    supabase_jwt = input("Enter your Supabase JWT Secret: ").strip()
    
    print("\n💳 STRIPE SETUP:")
    print("1. Go to https://stripe.com")
    print("2. Get your API keys from Dashboard > Developers > API keys")
    print("3. Create products: Premium ($9.99/month) and Pro ($19.99/month)")
    print("4. Copy the price IDs")
    print()
    
    stripe_secret = input("Enter your Stripe Secret Key (sk_test_...): ").strip()
    stripe_publishable = input("Enter your Stripe Publishable Key (pk_test_...): ").strip()
    stripe_webhook = input("Enter your Stripe Webhook Secret (optional): ").strip()
    stripe_premium = input("Enter your Premium Price ID (price_...): ").strip()
    stripe_pro = input("Enter your Pro Price ID (price_...): ").strip()
    
    print("\n🤖 OPENAI SETUP:")
    print("1. Go to https://platform.openai.com")
    print("2. Create an API key")
    print()
    
    openai_key = input("Enter your OpenAI API Key (sk-...): ").strip()
    
    print("\n📧 OPTIONAL SERVICES (press Enter to skip):")
    sendgrid_key = input("SendGrid API Key (optional): ").strip()
    paypal_id = input("PayPal Client ID (optional): ").strip()
    paypal_secret = input("PayPal Client Secret (optional): ").strip()
    plaid_id = input("Plaid Client ID (optional): ").strip()
    plaid_secret = input("Plaid Secret (optional): ").strip()
    
    # Create .env file
    env_content = f"""# BusinessThis Environment Configuration
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# Supabase Configuration
SUPABASE_URL={supabase_url}
SUPABASE_ANON_KEY={supabase_anon}
SUPABASE_SERVICE_ROLE_KEY={supabase_service}
SUPABASE_JWT_SECRET={supabase_jwt}

# Stripe Configuration
STRIPE_SECRET_KEY={stripe_secret}
STRIPE_PUBLISHABLE_KEY={stripe_publishable}
STRIPE_WEBHOOK_SECRET={stripe_webhook}
STRIPE_PREMIUM_PRICE_ID={stripe_premium}
STRIPE_PRO_PRICE_ID={stripe_pro}

# PayPal Configuration
PAYPAL_CLIENT_ID={paypal_id}
PAYPAL_CLIENT_SECRET={paypal_secret}
PAYPAL_MODE=sandbox

# OpenAI Configuration
OPENAI_API_KEY={openai_key}

# SendGrid Configuration
SENDGRID_API_KEY={sendgrid_key}
FROM_EMAIL=noreply@businessthis.com

# Plaid Configuration
PLAID_CLIENT_ID={plaid_id}
PLAID_SECRET={plaid_secret}
PLAID_ENV=sandbox

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Frontend URL
FRONTEND_URL=http://localhost:8501

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/businessthis
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n✅ Environment file created successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Failed to create .env file: {e}")
        return False

def test_setup():
    """Test the setup"""
    print("\n🧪 Testing setup...")
    
    # Test imports
    try:
        import flask
        import supabase
        import stripe
        import openai
        print("✅ All required packages are installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        return False
    
    # Test environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY', 'STRIPE_SECRET_KEY', 'OPENAI_API_KEY']
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
            return False
        
        print("✅ Environment variables configured")
        return True
        
    except Exception as e:
        print(f"❌ Environment test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 BusinessThis Simple Setup")
    print("=" * 40)
    print("This will set up your complete financial planning SaaS!")
    print()
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Test setup
    if not test_setup():
        print("\n❌ Setup test failed. Please check your configuration.")
        return False
    
    print("\n🎉 Setup complete!")
    print("\n🚀 TO START YOUR APPLICATION:")
    print("=" * 30)
    print("1. Open TWO terminal windows")
    print("2. Terminal 1: python run_backend.py")
    print("3. Terminal 2: python run_frontend.py")
    print("4. Open http://localhost:8501 in your browser")
    print()
    print("📊 YOUR REVENUE POTENTIAL:")
    print("=" * 30)
    print("Month 1-3: $500-2K (early adopters)")
    print("Month 6: $5K-10K (marketing push)")
    print("Month 12: $15K-30K (scaled user base)")
    print("Year 2: $75K-150K/month (full monetization)")
    print()
    print("🎯 NEXT STEPS:")
    print("=" * 30)
    print("1. Test the application locally")
    print("2. Deploy to production (Railway/Heroku)")
    print("3. Start marketing and user acquisition")
    print("4. Monitor metrics and iterate")
    print()
    print("🎉 Congratulations! Your financial planning SaaS is ready!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

