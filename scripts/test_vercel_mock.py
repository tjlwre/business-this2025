#!/usr/bin/env python3
"""
Mock test for Vercel LLM integration structure
Tests the integration without requiring actual API calls
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_vercel_llm_structure():
    """Test Vercel LLM integration structure"""
    print("Testing Vercel LLM Integration Structure...")
    print("=" * 50)
    
    try:
        # Set mock environment variables
        os.environ['VERCEL_LLM_API_KEY'] = 'mock_api_key_for_testing'
        os.environ['VERCEL_LLM_BASE_URL'] = 'https://api.vercel.com/v1/llm'
        os.environ['VERCEL_LLM_MODEL'] = 'gpt-3.5-turbo'
        os.environ['VERCEL_LLM_MAX_TOKENS'] = '1000'
        os.environ['VERCEL_LLM_TEMPERATURE'] = '0.7'
        
        # Test Vercel LLM integration import
        from integrations.vercel_llm_integration import VercelLLMIntegration
        print("✅ Vercel LLM integration imported successfully")
        
        # Test initialization
        vercel_llm = VercelLLMIntegration()
        print("✅ Vercel LLM integration initialized successfully")
        
        # Test configuration
        print(f"✅ API Key: {vercel_llm.api_key[:10]}...")
        print(f"✅ Base URL: {vercel_llm.base_url}")
        print(f"✅ Model: {vercel_llm.model}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import Vercel LLM integration: {e}")
        return False
    except Exception as e:
        print(f"❌ Error with Vercel LLM integration: {e}")
        return False

def test_ai_service_structure():
    """Test AI service structure"""
    print("\nTesting AI Service Structure...")
    print("=" * 50)
    
    try:
        from services.ai_service import AIService
        print("✅ AI service imported successfully")
        
        # Test initialization
        ai_service = AIService()
        print("✅ AI service initialized successfully")
        
        # Test that it has Vercel LLM integration
        if hasattr(ai_service, 'vercel_llm'):
            print("✅ AI service has Vercel LLM integration")
        else:
            print("❌ AI service missing Vercel LLM integration")
            return False
        
        # Test that it doesn't have Ollama
        if not hasattr(ai_service, 'ollama'):
            print("✅ AI service no longer has Ollama integration")
        else:
            print("❌ AI service still has Ollama integration")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import AI service: {e}")
        return False
    except Exception as e:
        print(f"❌ Error with AI service: {e}")
        return False

def test_method_signatures():
    """Test that all required methods exist"""
    print("\nTesting Method Signatures...")
    print("=" * 50)
    
    try:
        from services.ai_service import AIService
        
        ai_service = AIService()
        
        # Test required methods exist
        required_methods = [
            'get_financial_coaching',
            'get_spending_recommendations',
            'get_daily_financial_tip',
            'analyze_financial_goals',
            'get_investment_advice'
        ]
        
        for method_name in required_methods:
            if hasattr(ai_service, method_name):
                print(f"✅ {method_name} method exists")
            else:
                print(f"❌ {method_name} method missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing method signatures: {e}")
        return False

def test_vercel_llm_methods():
    """Test Vercel LLM integration methods"""
    print("\nTesting Vercel LLM Methods...")
    print("=" * 50)
    
    try:
        from integrations.vercel_llm_integration import VercelLLMIntegration
        
        vercel_llm = VercelLLMIntegration()
        
        # Test required methods exist
        required_methods = [
            'generate_financial_advice',
            'analyze_spending_patterns',
            'generate_daily_tip',
            'analyze_financial_goals',
            'get_investment_advice',
            'health_check'
        ]
        
        for method_name in required_methods:
            if hasattr(vercel_llm, method_name):
                print(f"✅ {method_name} method exists")
            else:
                print(f"❌ {method_name} method missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Vercel LLM methods: {e}")
        return False

def main():
    """Main test function"""
    print("Vercel LLM Integration Mock Test")
    print("=" * 50)
    
    success = True
    
    # Test structure
    if not test_vercel_llm_structure():
        success = False
    
    # Test AI service
    if not test_ai_service_structure():
        success = False
    
    # Test method signatures
    if not test_method_signatures():
        success = False
    
    # Test Vercel LLM methods
    if not test_vercel_llm_methods():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All structure tests passed!")
        print("\nThe Vercel LLM integration is properly structured.")
        print("\nTo test with real API calls:")
        print("1. Get a Vercel API key from https://vercel.com/dashboard")
        print("2. Set VERCEL_LLM_API_KEY environment variable")
        print("3. Run: python scripts/test_vercel_llm.py")
    else:
        print("❌ Some structure tests failed.")
        print("Please check the issues above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
