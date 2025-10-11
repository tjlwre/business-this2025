#!/usr/bin/env python3
"""
BusinessThis Environment Setup Script
This script helps set up the environment for BusinessThis
"""
import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file from template"""
    env_content = """# BusinessThis Environment Configuration
# Fill in your actual values below

# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
SUPABASE_JWT_SECRET=your-jwt-secret-here

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=pk_test_your-stripe-publishable-key
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret
STRIPE_PREMIUM_PRICE_ID=price_your-premium-price-id
STRIPE_PRO_PRICE_ID=price_your-pro-price-id

# PayPal Configuration
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
PAYPAL_MODE=sandbox

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key

# SendGrid Configuration
SENDGRID_API_KEY=SG.your-sendgrid-api-key
FROM_EMAIL=noreply@businessthis.com

# Plaid Configuration
PLAID_CLIENT_ID=your-plaid-client-id
PLAID_SECRET=your-plaid-secret
PLAID_ENV=sandbox

# Redis Configuration (Optional)
REDIS_URL=redis://localhost:6379

# Frontend URL
FRONTEND_URL=http://localhost:8501

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/businessthis
"""
    
    env_path = Path('.env')
    if env_path.exists():
        print("✅ .env file already exists")
        return True
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        'flask', 'supabase', 'stripe', 'openai', 'sendgrid', 
        'plaid-python', 'streamlit', 'pandas', 'plotly', 'reportlab'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed")
        return True

def test_database_connection():
    """Test database connection"""
    try:
        from config.supabase_config import test_supabase_connection
        if test_supabase_connection():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def setup_database():
    """Set up database schema"""
    try:
        from scripts.setup_database import main
        main()
        print("✅ Database schema created")
        return True
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 BusinessThis Environment Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('backend/app.py').exists():
        print("❌ Please run this script from the BusinessThis root directory")
        sys.exit(1)
    
    # Create .env file
    print("\n1. Creating environment file...")
    if not create_env_file():
        sys.exit(1)
    
    # Check requirements
    print("\n2. Checking requirements...")
    if not check_requirements():
        print("Please install missing packages and run again")
        sys.exit(1)
    
    # Test database connection
    print("\n3. Testing database connection...")
    if not test_database_connection():
        print("Please configure your Supabase credentials in .env file")
        print("Then run this script again")
        sys.exit(1)
    
    # Setup database
    print("\n4. Setting up database schema...")
    if not setup_database():
        print("Database setup failed. Please check your configuration.")
        sys.exit(1)
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Update .env file with your actual API keys")
    print("2. Run: python run_backend.py")
    print("3. Run: python run_frontend.py")
    print("4. Open http://localhost:8501 in your browser")

if __name__ == "__main__":
    main()
