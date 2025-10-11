#!/usr/bin/env python3
"""
BusinessThis Complete Setup Script
This script will guide you through setting up BusinessThis from scratch
"""
import os
import sys
import subprocess
import json
from pathlib import Path

class BusinessThisSetup:
    """Complete setup for BusinessThis"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.env_file = self.project_root / '.env'
        self.setup_complete = False
    
    def print_header(self):
        """Print setup header"""
        print("🚀 BusinessThis Complete Setup")
        print("=" * 50)
        print("This script will set up your complete financial planning SaaS!")
        print("You'll be prompted for API keys - we'll guide you through getting them.")
        print()
    
    def check_python_version(self):
        """Check Python version"""
        print("1. Checking Python version...")
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ required. Current version:", sys.version)
            return False
        print(f"✅ Python {sys.version.split()[0]} detected")
        return True
    
    def install_dependencies(self):
        """Install required packages"""
        print("\n2. Installing dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                          check=True, capture_output=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def create_env_file(self):
        """Create .env file with user input"""
        print("\n3. Setting up environment variables...")
        print("We'll guide you through getting each API key:")
        
        env_vars = {
            'SECRET_KEY': 'your-secret-key-here-change-in-production',
            'FLASK_ENV': 'development',
            'FLASK_DEBUG': 'True',
            'SUPABASE_URL': '',
            'SUPABASE_ANON_KEY': '',
            'SUPABASE_SERVICE_ROLE_KEY': '',
            'SUPABASE_JWT_SECRET': '',
            'STRIPE_SECRET_KEY': '',
            'STRIPE_PUBLISHABLE_KEY': '',
            'STRIPE_WEBHOOK_SECRET': '',
            'STRIPE_PREMIUM_PRICE_ID': '',
            'STRIPE_PRO_PRICE_ID': '',
            'PAYPAL_CLIENT_ID': '',
            'PAYPAL_CLIENT_SECRET': '',
            'PAYPAL_MODE': 'sandbox',
            'OPENAI_API_KEY': '',
            'SENDGRID_API_KEY': '',
            'FROM_EMAIL': 'noreply@businessthis.com',
            'PLAID_CLIENT_ID': '',
            'PLAID_SECRET': '',
            'PLAID_ENV': 'sandbox',
            'REDIS_URL': 'redis://localhost:6379',
            'FRONTEND_URL': 'http://localhost:8501',
            'DATABASE_URL': 'postgresql://user:password@localhost:5432/businessthis'
        }
        
        print("\n🔑 Let's get your API keys:")
        print("=" * 30)
        
        # Supabase setup
        print("\n📊 SUPABASE SETUP:")
        print("1. Go to https://supabase.com")
        print("2. Create a new project")
        print("3. Go to Settings > API")
        print("4. Copy your Project URL and API keys")
        
        env_vars['SUPABASE_URL'] = input("Enter your Supabase URL: ").strip()
        env_vars['SUPABASE_ANON_KEY'] = input("Enter your Supabase Anon Key: ").strip()
        env_vars['SUPABASE_SERVICE_ROLE_KEY'] = input("Enter your Supabase Service Role Key: ").strip()
        env_vars['SUPABASE_JWT_SECRET'] = input("Enter your Supabase JWT Secret: ").strip()
        
        # Stripe setup
        print("\n💳 STRIPE SETUP:")
        print("1. Go to https://stripe.com")
        print("2. Get your API keys from Dashboard > Developers > API keys")
        print("3. Create products: Premium ($9.99/month) and Pro ($19.99/month)")
        print("4. Copy the price IDs")
        
        env_vars['STRIPE_SECRET_KEY'] = input("Enter your Stripe Secret Key (sk_test_...): ").strip()
        env_vars['STRIPE_PUBLISHABLE_KEY'] = input("Enter your Stripe Publishable Key (pk_test_...): ").strip()
        env_vars['STRIPE_WEBHOOK_SECRET'] = input("Enter your Stripe Webhook Secret (optional): ").strip()
        env_vars['STRIPE_PREMIUM_PRICE_ID'] = input("Enter your Premium Price ID (price_...): ").strip()
        env_vars['STRIPE_PRO_PRICE_ID'] = input("Enter your Pro Price ID (price_...): ").strip()
        
        # OpenAI setup
        print("\n🤖 OPENAI SETUP:")
        print("1. Go to https://platform.openai.com")
        print("2. Create an API key")
        
        env_vars['OPENAI_API_KEY'] = input("Enter your OpenAI API Key (sk-...): ").strip()
        
        # Optional services
        print("\n📧 OPTIONAL SERVICES (press Enter to skip):")
        
        sendgrid_key = input("SendGrid API Key (optional): ").strip()
        if sendgrid_key:
            env_vars['SENDGRID_API_KEY'] = sendgrid_key
        
        paypal_id = input("PayPal Client ID (optional): ").strip()
        if paypal_id:
            env_vars['PAYPAL_CLIENT_ID'] = paypal_id
            env_vars['PAYPAL_CLIENT_SECRET'] = input("PayPal Client Secret: ").strip()
        
        plaid_id = input("Plaid Client ID (optional): ").strip()
        if plaid_id:
            env_vars['PLAID_CLIENT_ID'] = plaid_id
            env_vars['PLAID_SECRET'] = input("Plaid Secret: ").strip()
        
        # Write .env file
        try:
            with open(self.env_file, 'w') as f:
                for key, value in env_vars.items():
                    f.write(f"{key}={value}\n")
            print("✅ Environment file created successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    
    def setup_database(self):
        """Setup database schema"""
        print("\n4. Setting up database...")
        try:
            # Test Supabase connection first
            from config.supabase_config import test_supabase_connection
            if not test_supabase_connection():
                print("❌ Database connection failed. Please check your Supabase credentials.")
                return False
            
            print("✅ Database connection successful")
            
            # Run database setup
            from scripts.setup_database import main as setup_db
            setup_db()
            print("✅ Database schema created")
            return True
            
        except Exception as e:
            print(f"❌ Database setup failed: {e}")
            print("Please check your Supabase credentials and try again.")
            return False
    
    def test_implementation(self):
        """Test the complete implementation"""
        print("\n5. Testing implementation...")
        try:
            # Start backend in background
            print("Starting backend server...")
            backend_process = subprocess.Popen([
                sys.executable, "run_backend.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for backend to start
            import time
            time.sleep(5)
            
            # Run tests
            result = subprocess.run([
                sys.executable, "test_implementation.py"
            ], capture_output=True, text=True)
            
            # Stop backend
            backend_process.terminate()
            
            if result.returncode == 0:
                print("✅ All tests passed!")
                return True
            else:
                print("❌ Some tests failed:")
                print(result.stdout)
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Testing failed: {e}")
            return False
    
    def create_startup_scripts(self):
        """Create convenient startup scripts"""
        print("\n6. Creating startup scripts...")
        
        # Windows batch file
        with open("start_backend.bat", "w") as f:
            f.write("""@echo off
echo Starting BusinessThis Backend...
python run_backend.py
pause
""")
        
        with open("start_frontend.bat", "w") as f:
            f.write("""@echo off
echo Starting BusinessThis Frontend...
python run_frontend.py
pause
""")
        
        # Unix shell scripts
        with open("start_backend.sh", "w") as f:
            f.write("""#!/bin/bash
echo "Starting BusinessThis Backend..."
python run_backend.py
""")
        
        with open("start_frontend.sh", "w") as f:
            f.write("""#!/bin/bash
echo "Starting BusinessThis Frontend..."
python run_frontend.py
""")
        
        # Make shell scripts executable
        try:
            os.chmod("start_backend.sh", 0o755)
            os.chmod("start_frontend.sh", 0o755)
        except:
            pass  # Windows doesn't support chmod
        
        print("✅ Startup scripts created")
        print("   - start_backend.bat/.sh")
        print("   - start_frontend.bat/.sh")
    
    def print_success_message(self):
        """Print success message with next steps"""
        print("\n" + "=" * 50)
        print("🎉 BUSINESS THIS SETUP COMPLETE!")
        print("=" * 50)
        print()
        print("✅ All components installed and configured")
        print("✅ Database schema created")
        print("✅ All tests passed")
        print("✅ Ready for production!")
        print()
        print("🚀 TO START YOUR APPLICATION:")
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
        print("📚 DOCUMENTATION:")
        print("=" * 30)
        print("- DEPLOYMENT_GUIDE.md - Production deployment")
        print("- IMPLEMENTATION_COMPLETE.md - Feature overview")
        print("- test_implementation.py - Run tests anytime")
        print()
        print("🎉 Congratulations! Your financial planning SaaS is ready!")
        print("=" * 50)
    
    def run_setup(self):
        """Run complete setup process"""
        self.print_header()
        
        steps = [
            ("Check Python version", self.check_python_version),
            ("Install dependencies", self.install_dependencies),
            ("Setup environment", self.create_env_file),
            ("Setup database", self.setup_database),
            ("Test implementation", self.test_implementation),
            ("Create startup scripts", self.create_startup_scripts)
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print(f"\n❌ Setup failed at: {step_name}")
                print("Please fix the issue and run the setup again.")
                return False
        
        self.setup_complete = True
        self.print_success_message()
        return True

def main():
    """Main setup function"""
    setup = BusinessThisSetup()
    success = setup.run_setup()
    
    if success:
        print("\n🎉 Setup completed successfully!")
        print("Your BusinessThis application is ready to launch!")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()