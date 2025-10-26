#!/usr/bin/env python3
"""
Test Vercel LLM Integration Structure Only
Tests the integration without importing external dependencies
"""
import os
import sys
from pathlib import Path

def test_file_structure():
    """Test that all required files exist"""
    print("Testing File Structure...")
    print("=" * 50)
    
    required_files = [
        "integrations/vercel_llm_integration.py",
        "services/ai_service.py",
        "config/env.example",
        "scripts/test_vercel_llm.py",
        "VERCEL_LLM_INTEGRATION.md",
        "VERCEL_LLM_SETUP.md",
        "VERCEL_LLM_TESTING_GUIDE.md"
    ]
    
    all_good = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing!")
            all_good = False
    
    return all_good

def test_ollama_removal():
    """Test that Ollama files have been removed"""
    print("\nTesting Ollama Removal...")
    print("=" * 50)
    
    removed_files = [
        "integrations/ollama_integration.py",
        "OLLAMA_SETUP.md",
        "WINDOWS_OLLAMA_SETUP.md",
        "ollama-windows-amd64.exe"
    ]
    
    all_removed = True
    for file_path in removed_files:
        if not Path(file_path).exists():
            print(f"✅ {file_path} - Successfully removed")
        else:
            print(f"❌ {file_path} - Still exists!")
            all_removed = False
    
    return all_removed

def test_ai_service_content():
    """Test AI service content without importing"""
    print("\nTesting AI Service Content...")
    print("=" * 50)
    
    try:
        with open("services/ai_service.py", "r") as f:
            content = f.read()
        
        # Check for Vercel LLM usage
        if "VercelLLMIntegration" in content:
            print("✅ Vercel LLM integration found in AI service")
        else:
            print("❌ Vercel LLM integration not found in AI service")
            return False
        
        # Check for Ollama removal
        if "OllamaIntegration" not in content:
            print("✅ Ollama integration removed from AI service")
        else:
            print("❌ Ollama integration still present in AI service")
            return False
        
        # Check for required methods
        required_methods = [
            "get_financial_coaching",
            "get_spending_recommendations",
            "get_daily_financial_tip",
            "analyze_financial_goals",
            "get_investment_advice"
        ]
        
        for method in required_methods:
            if f"def {method}" in content:
                print(f"✅ {method} method found")
            else:
                print(f"❌ {method} method missing")
                return False
        
        # Check that methods use Vercel LLM
        if "self.vercel_llm." in content:
            print("✅ AI service methods use Vercel LLM")
        else:
            print("❌ AI service methods don't use Vercel LLM")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading AI service: {e}")
        return False

def test_vercel_llm_content():
    """Test Vercel LLM integration content"""
    print("\nTesting Vercel LLM Integration Content...")
    print("=" * 50)
    
    try:
        with open("integrations/vercel_llm_integration.py", "r") as f:
            content = f.read()
        
        # Check for required methods
        required_methods = [
            "generate_financial_advice",
            "analyze_spending_patterns",
            "generate_daily_tip",
            "analyze_financial_goals",
            "get_investment_advice",
            "health_check"
        ]
        
        for method in required_methods:
            if f"def {method}" in content:
                print(f"✅ {method} method found")
            else:
                print(f"❌ {method} method missing")
                return False
        
        # Check for API configuration
        if "VERCEL_LLM_API_KEY" in content:
            print("✅ API key configuration found")
        else:
            print("❌ API key configuration missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading Vercel LLM integration: {e}")
        return False

def test_environment_config():
    """Test environment configuration"""
    print("\nTesting Environment Configuration...")
    print("=" * 50)
    
    try:
        with open("config/env.example", "r") as f:
            content = f.read()
        
        # Check for Vercel LLM config
        vercel_configs = [
            "VERCEL_LLM_API_KEY",
            "VERCEL_LLM_BASE_URL",
            "VERCEL_LLM_MODEL",
            "VERCEL_LLM_MAX_TOKENS",
            "VERCEL_LLM_TEMPERATURE"
        ]
        
        for config in vercel_configs:
            if config in content:
                print(f"✅ {config} configuration found")
            else:
                print(f"❌ {config} configuration missing")
                return False
        
        # Check for Ollama removal
        if "OLLAMA_URL" not in content and "OLLAMA_MODEL" not in content:
            print("✅ Ollama configuration removed")
        else:
            print("❌ Ollama configuration still present")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading environment config: {e}")
        return False

def main():
    """Main test function"""
    print("Vercel LLM Integration Structure Test")
    print("=" * 50)
    
    success = True
    
    # Test file structure
    if not test_file_structure():
        success = False
    
    # Test Ollama removal
    if not test_ollama_removal():
        success = False
    
    # Test AI service content
    if not test_ai_service_content():
        success = False
    
    # Test Vercel LLM content
    if not test_vercel_llm_content():
        success = False
    
    # Test environment config
    if not test_environment_config():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All structure tests passed!")
        print("\nVercel LLM integration is properly structured and ready.")
        print("\nTo test with real API calls:")
        print("1. Install dependencies: pip install requests")
        print("2. Get Vercel API key from https://vercel.com/dashboard")
        print("3. Set VERCEL_LLM_API_KEY environment variable")
        print("4. Run: python scripts/test_vercel_llm.py")
    else:
        print("❌ Some structure tests failed.")
        print("Please check the issues above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
