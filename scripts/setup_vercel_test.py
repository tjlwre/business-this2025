#!/usr/bin/env python3
"""
Setup script for Vercel LLM testing
Helps configure the environment for testing
"""
import os
import sys

def setup_environment():
    """Setup environment variables for testing"""
    print("Vercel LLM Test Setup")
    print("=" * 50)
    
    print("Please provide your Vercel API key:")
    api_key = input("Enter your Vercel API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return False
    
    # Set environment variables
    os.environ['VERCEL_LLM_API_KEY'] = api_key
    os.environ['VERCEL_LLM_BASE_URL'] = 'https://api.vercel.com/v1/llm'
    os.environ['VERCEL_LLM_MODEL'] = 'gpt-3.5-turbo'
    os.environ['VERCEL_LLM_MAX_TOKENS'] = '1000'
    os.environ['VERCEL_LLM_TEMPERATURE'] = '0.7'
    
    print("✅ Environment variables set")
    print(f"✅ API Key: {api_key[:10]}...")
    print(f"✅ Base URL: {os.environ['VERCEL_LLM_BASE_URL']}")
    print(f"✅ Model: {os.environ['VERCEL_LLM_MODEL']}")
    
    return True

def test_imports():
    """Test that we can import the modules"""
    print("\nTesting Imports...")
    print("=" * 50)
    
    try:
        # Try to import requests first
        import requests
        print("✅ requests module available")
    except ImportError:
        print("❌ requests module not available")
        print("Please install with: pip install requests")
        return False
    
    try:
        from integrations.vercel_llm_integration import VercelLLMIntegration
        print("✅ Vercel LLM integration imported")
    except ImportError as e:
        print(f"❌ Failed to import Vercel LLM integration: {e}")
        return False
    
    try:
        from services.ai_service import AIService
        print("✅ AI service imported")
    except ImportError as e:
        print(f"❌ Failed to import AI service: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality"""
    print("\nTesting Basic Functionality...")
    print("=" * 50)
    
    try:
        from integrations.vercel_llm_integration import VercelLLMIntegration
        from services.ai_service import AIService
        
        # Test Vercel LLM integration
        vercel_llm = VercelLLMIntegration()
        print("✅ Vercel LLM integration initialized")
        
        # Test AI service
        ai_service = AIService()
        print("✅ AI service initialized")
        
        # Test health check (this will fail without real API key, but structure is correct)
        print("⚠️  Health check will be tested with real API calls")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing functionality: {e}")
        return False

def main():
    """Main setup function"""
    print("Setting up Vercel LLM integration test...")
    
    # Setup environment
    if not setup_environment():
        return False
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install dependencies:")
        print("pip install requests")
        return False
    
    # Test basic functionality
    if not test_basic_functionality():
        print("\n❌ Functionality tests failed.")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Run: python scripts/test_vercel_llm.py")
    print("2. Test AI features in your application")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
