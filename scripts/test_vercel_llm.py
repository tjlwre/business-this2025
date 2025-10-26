#!/usr/bin/env python3
"""
Test script for Vercel LLM integration
"""
import os
import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from integrations.vercel_llm_integration import VercelLLMIntegration
from services.ai_service import AIService

def test_vercel_llm_integration():
    """Test Vercel LLM integration"""
    print("Testing Vercel LLM Integration...")
    print("=" * 50)
    
    # Test 1: Health Check
    print("1. Testing health check...")
    vercel_llm = VercelLLMIntegration()
    health_status = vercel_llm.health_check()
    print(f"   Health check: {'✅ PASS' if health_status else '❌ FAIL'}")
    
    if not health_status:
        print("   ⚠️  Vercel LLM is not available. Check your API key and configuration.")
        return False
    
    # Test 2: Available Models
    print("2. Testing available models...")
    models = vercel_llm.get_available_models()
    print(f"   Available models: {models}")
    
    # Test 3: Financial Advice
    print("3. Testing financial advice generation...")
    user_context = "Age: 30, Monthly Income: $5000, Fixed Expenses: $3000, Risk Tolerance: moderate"
    question = "How should I start investing?"
    
    advice = vercel_llm.generate_financial_advice(user_context, question)
    if advice:
        print("   ✅ Financial advice generated successfully")
        print(f"   Advice: {advice[:100]}...")
    else:
        print("   ❌ Failed to generate financial advice")
        return False
    
    # Test 4: Spending Analysis
    print("4. Testing spending analysis...")
    transactions = [
        {"date": "2024-01-15", "category": "Food", "amount": 45.50},
        {"date": "2024-01-14", "category": "Transportation", "amount": 25.00},
        {"date": "2024-01-13", "category": "Entertainment", "amount": 80.00},
        {"date": "2024-01-12", "category": "Food", "amount": 32.75},
        {"date": "2024-01-11", "category": "Shopping", "amount": 120.00}
    ]
    
    analysis = vercel_llm.analyze_spending_patterns(transactions)
    if analysis:
        print("   ✅ Spending analysis generated successfully")
        print(f"   Analysis: {analysis[:100]}...")
    else:
        print("   ❌ Failed to generate spending analysis")
        return False
    
    # Test 5: Daily Tip
    print("5. Testing daily tip generation...")
    tip = vercel_llm.generate_daily_tip(user_context)
    if tip:
        print("   ✅ Daily tip generated successfully")
        print(f"   Tip: {tip}")
    else:
        print("   ❌ Failed to generate daily tip")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All Vercel LLM integration tests passed!")
    return True

def test_ai_service_integration():
    """Test AI service with Vercel LLM"""
    print("\nTesting AI Service Integration...")
    print("=" * 50)
    
    # Test AI Service
    ai_service = AIService()
    
    # Sample user profile
    profile = {
        "age": 28,
        "monthly_income": 6000,
        "fixed_expenses": 3000,
        "variable_expenses": 1500,
        "emergency_fund_current": 2000,
        "risk_tolerance": "moderate"
    }
    
    # Test financial coaching
    print("1. Testing AI service financial coaching...")
    result = ai_service.get_financial_coaching(profile, "I want to save for a house down payment")
    
    if result['success']:
        print("   ✅ AI service coaching successful")
        print(f"   Provider: {result.get('provider', 'unknown')}")
        print(f"   Advice: {result['advice'][:100]}...")
    else:
        print("   ❌ AI service coaching failed")
        print(f"   Error: {result.get('error', 'Unknown error')}")
        return False
    
    # Test spending recommendations
    print("2. Testing AI service spending recommendations...")
    transactions = [
        {"category": "Food", "amount": 45.50},
        {"category": "Transportation", "amount": 25.00},
        {"category": "Entertainment", "amount": 80.00}
    ]
    
    result = ai_service.get_spending_recommendations(profile, transactions)
    if result['success']:
        print("   ✅ AI service spending analysis successful")
        print(f"   Provider: {result.get('provider', 'unknown')}")
    else:
        print("   ❌ AI service spending analysis failed")
        return False
    
    print("\n" + "=" * 50)
    print("✅ AI Service integration tests passed!")
    return True

def main():
    """Main test function"""
    print("Vercel LLM Integration Test Suite")
    print("=" * 50)
    
    # Check environment variables
    required_vars = ['VERCEL_LLM_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        print("Please set up your environment variables before running tests.")
        return False
    
    # Run tests
    success = True
    
    # Test Vercel LLM integration
    if not test_vercel_llm_integration():
        success = False
    
    # Test AI service integration
    if not test_ai_service_integration():
        success = False
    
    if success:
        print("\n🎉 All tests passed! Vercel LLM integration is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the configuration and try again.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
