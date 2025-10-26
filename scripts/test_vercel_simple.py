#!/usr/bin/env python3
"""
Simple test script for Vercel LLM integration
Tests the integration without external dependencies
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_vercel_llm_import():
    """Test that Vercel LLM integration can be imported"""
    print("Testing Vercel LLM Integration Import...")
    print("=" * 50)
    
    try:
        from integrations.vercel_llm_integration import VercelLLMIntegration
        print("✅ Vercel LLM integration imported successfully")
        
        # Test initialization
        vercel_llm = VercelLLMIntegration()
        print("✅ Vercel LLM integration initialized successfully")
        
        # Test configuration
        api_key = os.getenv('VERCEL_LLM_API_KEY')
        if api_key:
            print("✅ Vercel LLM API key found")
        else:
            print("⚠️  Vercel LLM API key not found - set VERCEL_LLM_API_KEY environment variable")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import Vercel LLM integration: {e}")
        return False
    except Exception as e:
        print(f"❌ Error initializing Vercel LLM integration: {e}")
        return False

def test_ai_service_import():
    """Test that AI service can be imported"""
    print("\nTesting AI Service Import...")
    print("=" * 50)
    
    try:
        from services.ai_service import AIService
        print("✅ AI service imported successfully")
        
        # Test initialization
        ai_service = AIService()
        print("✅ AI service initialized successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import AI service: {e}")
        return False
    except Exception as e:
        print(f"❌ Error initializing AI service: {e}")
        return False

def test_environment_config():
    """Test environment configuration"""
    print("\nTesting Environment Configuration...")
    print("=" * 50)
    
    required_vars = [
        'VERCEL_LLM_API_KEY',
        'VERCEL_LLM_BASE_URL',
        'VERCEL_LLM_MODEL'
    ]
    
    all_good = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:20]}..." if len(value) > 20 else f"✅ {var}: {value}")
        else:
            print(f"⚠️  {var}: Not set")
            all_good = False
    
    return all_good

def main():
    """Main test function"""
    print("Vercel LLM Integration Simple Test")
    print("=" * 50)
    
    success = True
    
    # Test imports
    if not test_vercel_llm_import():
        success = False
    
    if not test_ai_service_import():
        success = False
    
    # Test environment
    if not test_environment_config():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All basic tests passed! Vercel LLM integration is ready.")
        print("\nTo test with actual API calls:")
        print("1. Set VERCEL_LLM_API_KEY environment variable")
        print("2. Run: python scripts/test_vercel_llm.py")
    else:
        print("❌ Some tests failed. Please check the configuration.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

