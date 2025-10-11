#!/usr/bin/env python3
"""
Test script for Ollama integration
Verifies that all AI features work correctly with Ollama
"""
import sys
import os
import requests
import json
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ollama_connection():
    """Test basic Ollama connection"""
    print("🔍 Testing Ollama connection...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running and accessible!")
            return True
        else:
            print(f"❌ Ollama returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
        return False

def test_mistral_model():
    """Test Mistral model with a simple query"""
    print("🔍 Testing Mistral model...")
    
    try:
        payload = {
            "model": "mistral",
            "prompt": "Hello, are you working? Please respond with 'Yes, I am working correctly.'",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 50
            }
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response', '').strip()
            print(f"✅ Mistral model is working!")
            print(f"📝 Response: {response_text}")
            return True
        else:
            print(f"❌ Mistral model test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Mistral model test failed: {e}")
        return False

def test_ollama_integration():
    """Test the OllamaIntegration class"""
    print("🔍 Testing OllamaIntegration class...")
    
    try:
        from integrations.ollama_integration import OllamaIntegration
        
        # Initialize integration
        ollama = OllamaIntegration()
        
        # Test health check
        is_healthy = ollama.health_check()
        print(f"📊 Health check: {'✅ Healthy' if is_healthy else '❌ Unhealthy'}")
        
        # Test available models
        models = ollama.get_available_models()
        print(f"📋 Available models: {models}")
        
        # Test financial advice generation
        print("🔍 Testing financial advice generation...")
        advice = ollama.generate_financial_advice(
            user_context="Age: 30, Monthly Income: $5000, Fixed Expenses: $3000",
            question="How can I save more money?"
        )
        
        if advice:
            print("✅ Financial advice generation works!")
            print(f"📝 Advice: {advice[:100]}...")
        else:
            print("❌ Financial advice generation failed")
            return False
        
        # Test spending analysis
        print("🔍 Testing spending pattern analysis...")
        transactions = [
            {"category": "Food", "amount": 500},
            {"category": "Transportation", "amount": 200},
            {"category": "Entertainment", "amount": 300}
        ]
        
        analysis = ollama.analyze_spending_patterns(transactions)
        
        if analysis:
            print("✅ Spending analysis works!")
            print(f"📝 Analysis: {analysis[:100]}...")
        else:
            print("❌ Spending analysis failed")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import OllamaIntegration: {e}")
        return False
    except Exception as e:
        print(f"❌ OllamaIntegration test failed: {e}")
        return False

def test_ai_service():
    """Test the AIService class"""
    print("🔍 Testing AIService class...")
    
    try:
        from services.ai_service import AIService
        
        # Initialize AI service
        ai_service = AIService()
        
        # Test with mock profile
        mock_profile = {
            "age": 30,
            "monthly_income": 5000,
            "fixed_expenses": 3000,
            "variable_expenses": 1000,
            "emergency_fund_current": 2000,
            "risk_tolerance": "moderate"
        }
        
        # Test financial coaching
        print("🔍 Testing financial coaching...")
        coaching_result = ai_service.get_financial_coaching(
            profile=mock_profile,
            question="How can I improve my financial health?"
        )
        
        if coaching_result.get('success'):
            print("✅ Financial coaching works!")
            print(f"📝 Coaching: {coaching_result.get('advice', '')[:100]}...")
        else:
            print("❌ Financial coaching failed")
            print(f"Error: {coaching_result.get('error', 'Unknown error')}")
            return False
        
        # Test daily tip
        print("🔍 Testing daily tip generation...")
        tip_result = ai_service.get_daily_financial_tip(profile=mock_profile)
        
        if tip_result.get('success'):
            print("✅ Daily tip generation works!")
            print(f"📝 Tip: {tip_result.get('tip', '')[:100]}...")
        else:
            print("❌ Daily tip generation failed")
            print(f"Error: {tip_result.get('error', 'Unknown error')}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import AIService: {e}")
        return False
    except Exception as e:
        print(f"❌ AIService test failed: {e}")
        return False

def test_backend_health_endpoint():
    """Test the backend health endpoint"""
    print("🔍 Testing backend health endpoint...")
    
    try:
        # Test if backend is running
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend is not running")
            print("💡 Start the backend: python run_backend.py")
            return False
        
        print("✅ Backend is running")
        
        # Test Ollama health endpoint
        response = requests.get("http://localhost:5000/api/health/ollama", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Ollama health endpoint works!")
            print(f"📊 Status: {data.get('ollama_status')}")
            print(f"📋 Models: {data.get('available_models')}")
            return True
        else:
            print(f"❌ Ollama health endpoint failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("💡 Make sure the backend is running: python run_backend.py")
        return False

def main():
    """Run all tests"""
    print("🚀 BusinessThis Ollama Integration Test Suite")
    print("=" * 60)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Ollama Connection", test_ollama_connection),
        ("Mistral Model", test_mistral_model),
        ("OllamaIntegration Class", test_ollama_integration),
        ("AIService Class", test_ai_service),
        ("Backend Health Endpoint", test_backend_health_endpoint)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
        
        print()
    
    # Summary
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ollama integration is working correctly.")
        print("\n🚀 Your BusinessThis app is ready to use with Ollama!")
        print("\nNext steps:")
        print("1. Start your frontend: python run_frontend.py")
        print("2. Test AI features in the web interface")
        print("3. Monitor usage with the health endpoint")
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the issues above.")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Make sure Mistral model is installed: ollama pull mistral")
        print("3. Make sure backend is running: python run_backend.py")
        print("4. Check the OLLAMA_SETUP.md guide for detailed instructions")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
