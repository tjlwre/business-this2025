#!/usr/bin/env python3
"""
Verify Vercel LLM Integration Structure
Tests the integration structure without external API calls
"""
import os
import sys
from pathlib import Path

def verify_file_structure():
    """Verify that all required files exist"""
    print("Verifying File Structure...")
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

def verify_ollama_removal():
    """Verify that Ollama files have been removed"""
    print("\nVerifying Ollama Removal...")
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

def verify_ai_service_structure():
    """Verify AI service structure"""
    print("\nVerifying AI Service Structure...")
    print("=" * 50)
    
    try:
        # Read AI service file
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
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading AI service: {e}")
        return False

def verify_environment_config():
    """Verify environment configuration"""
    print("\nVerifying Environment Configuration...")
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
    """Main verification function"""
    print("Vercel LLM Integration Verification")
    print("=" * 50)
    
    success = True
    
    # Verify file structure
    if not verify_file_structure():
        success = False
    
    # Verify Ollama removal
    if not verify_ollama_removal():
        success = False
    
    # Verify AI service structure
    if not verify_ai_service_structure():
        success = False
    
    # Verify environment config
    if not verify_environment_config():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All verifications passed!")
        print("\nVercel LLM integration is ready for testing.")
        print("\nNext steps:")
        print("1. Set VERCEL_LLM_API_KEY environment variable")
        print("2. Run: python scripts/test_vercel_llm.py")
        print("3. Test AI features in your application")
    else:
        print("❌ Some verifications failed.")
        print("Please check the issues above and fix them.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
