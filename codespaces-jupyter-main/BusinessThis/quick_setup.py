#!/usr/bin/env python3
"""
BusinessThis Quick Setup
One command to set up everything!
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 BusinessThis Quick Setup")
    print("=" * 40)
    print("This will set up your complete financial planning SaaS!")
    print()
    
    # Check if we're in the right directory
    if not Path("backend/app.py").exists():
        print("❌ Please run this from the BusinessThis root directory")
        return False
    
    print("✅ Starting complete setup...")
    print()
    
    # Run the main setup script
    try:
        result = subprocess.run([sys.executable, "setup.py"], check=True)
        print("\n🎉 Setup complete! Your app is ready!")
        print("\nTo start:")
        print("1. python run_backend.py")
        print("2. python run_frontend.py")
        print("3. Open http://localhost:8501")
        return True
    except subprocess.CalledProcessError:
        print("❌ Setup failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
