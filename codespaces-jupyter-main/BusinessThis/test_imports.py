#!/usr/bin/env python3
"""
Test script to check for import issues in BusinessThis
"""
import sys
import os

def test_import(module_path, class_name=None):
    """Test importing a module and optionally a class"""
    try:
        if class_name:
            exec(f"from {module_path} import {class_name}")
            print(f"✅ {module_path}.{class_name} - OK")
        else:
            exec(f"import {module_path}")
            print(f"✅ {module_path} - OK")
        return True
    except Exception as e:
        print(f"❌ {module_path} - ERROR: {e}")
        return False

def main():
    print("🔍 Testing BusinessThis Imports")
    print("=" * 50)
    
    # Test core services
    core_services = [
        ("core.services.auth_service", "AuthService"),
        ("core.services.financial_service", "FinancialService"),
        ("core.services.subscription_service", "SubscriptionService"),
        ("core.services.investment_service", "InvestmentService"),
        ("core.services.ai_service", "AIService"),
        ("core.services.admin_service", "AdminService"),
        ("core.services.reports_service", "ReportsService"),
        ("core.services.email_service", "EmailService"),
        ("core.services.affiliate_service", "AffiliateService"),
        ("core.services.course_service", "CourseService"),
        ("core.services.multi_user_service", "MultiUserService"),
        ("core.services.advisor_service", "AdvisorService"),
    ]
    
    # Test models
    models = [
        ("core.models.user", "User"),
        ("core.models.financial_profile", "FinancialProfile"),
        ("core.models.savings_goal", "SavingsGoal"),
        ("core.models.transaction", "Transaction"),
    ]
    
    # Test integrations
    integrations = [
        ("integrations.stripe_integration", "StripeIntegration"),
        ("integrations.paypal_integration", "PayPalIntegration"),
        ("integrations.openai_integration", "OpenAIIntegration"),
        ("integrations.plaid_integration", "PlaidIntegration"),
        ("integrations.sendgrid_integration", "SendGridIntegration"),
        ("integrations.ollama_integration", "OllamaIntegration"),
    ]
    
    # Test config
    config_modules = [
        ("config.supabase_config", None),
        ("config.settings", "Settings"),
    ]
    
    # Test utils
    utils = [
        ("core.utils.validators", None),
        ("core.utils.decorators", None),
    ]
    
    all_tests = [
        ("Core Services", core_services),
        ("Models", models),
        ("Integrations", integrations),
        ("Config", config_modules),
        ("Utils", utils),
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for category, tests in all_tests:
        print(f"\n📁 {category}")
        print("-" * 30)
        
        for module_path, class_name in tests:
            total_tests += 1
            if test_import(module_path, class_name):
                passed_tests += 1
    
    print(f"\n📊 Results: {passed_tests}/{total_tests} imports successful")
    
    if passed_tests == total_tests:
        print("🎉 All imports working correctly!")
    else:
        print(f"⚠️  {total_tests - passed_tests} imports failed")
        print("\n🔧 Common fixes:")
        print("1. Check if files exist in the expected locations")
        print("2. Verify import paths are correct")
        print("3. Check for missing dependencies")
        print("4. Ensure __init__.py files exist in directories")

if __name__ == "__main__":
    main()
