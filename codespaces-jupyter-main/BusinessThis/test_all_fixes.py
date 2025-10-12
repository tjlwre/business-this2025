#!/usr/bin/env python3
"""
Comprehensive test script for all bug fixes
"""
import sys
import os
import traceback

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing Critical Imports...")
    
    critical_imports = [
        ("backend.app", "Flask app"),
        ("frontend.app", "Streamlit app"),
        ("config.supabase_config", "Supabase config"),
        ("config.validation", "Environment validation"),
        ("core.utils.validators", "Validators"),
        ("core.utils.error_handler", "Error handler"),
        ("core.utils.security", "Security utils"),
        ("services.auth_service", "Auth service"),
        ("services.financial_service", "Financial service"),
    ]
    
    failed_imports = []
    
    for module, description in critical_imports:
        try:
            __import__(module)
            print(f"✅ {description}")
        except Exception as e:
            print(f"❌ {description}: {e}")
            failed_imports.append((module, str(e)))
    
    return failed_imports

def test_environment_validation():
    """Test environment validation"""
    print("\n🔧 Testing Environment Validation...")
    
    try:
        from config.validation import validate_environment
        # This will fail if required env vars are missing, which is expected
        validate_environment()
        print("✅ Environment validation passed")
        return True
    except ValueError as e:
        print(f"⚠️  Environment validation failed (expected): {e}")
        return True  # This is expected behavior
    except Exception as e:
        print(f"❌ Environment validation error: {e}")
        return False

def test_security_features():
    """Test security features"""
    print("\n🔒 Testing Security Features...")
    
    try:
        from core.utils.security import rate_limit, add_security_headers, hash_password, verify_password
        
        # Test password hashing
        password = "test_password_123"
        hashed = hash_password(password)
        is_valid = verify_password(password, hashed)
        
        if is_valid:
            print("✅ Password hashing works")
        else:
            print("❌ Password hashing failed")
            return False
        
        print("✅ Security features imported successfully")
        return True
    except Exception as e:
        print(f"❌ Security features error: {e}")
        return False

def test_error_handling():
    """Test error handling"""
    print("\n🛡️  Testing Error Handling...")
    
    try:
        from core.utils.error_handler import handle_errors, ValidationError, AuthenticationError
        
        # Test error classes
        try:
            raise ValidationError("Test validation error")
        except ValidationError as e:
            if e.status_code == 400:
                print("✅ Validation error handling works")
            else:
                print("❌ Validation error status code incorrect")
                return False
        
        print("✅ Error handling imported successfully")
        return True
    except Exception as e:
        print(f"❌ Error handling error: {e}")
        return False

def test_validation_functions():
    """Test validation functions"""
    print("\n✅ Testing Validation Functions...")
    
    try:
        from core.utils.validators import validate_email, validate_user_input, validate_financial_data
        
        # Test email validation
        if validate_email("test@example.com"):
            print("✅ Email validation works")
        else:
            print("❌ Email validation failed")
            return False
        
        # Test user input validation
        test_data = {"name": "Test User", "email": "test@example.com"}
        result = validate_user_input(test_data, ["name", "email"])
        
        if result.get('valid'):
            print("✅ User input validation works")
        else:
            print(f"❌ User input validation failed: {result.get('errors')}")
            return False
        
        print("✅ Validation functions work correctly")
        return True
    except Exception as e:
        print(f"❌ Validation functions error: {e}")
        return False

def test_hardcoded_secrets_removed():
    """Test that hardcoded secrets are removed"""
    print("\n🔐 Testing Hardcoded Secrets Removal...")
    
    files_to_check = [
        'backend/app.py',
        'core/utils/decorators.py', 
        'config/settings.py'
    ]
    
    issues = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if 'dev-secret-key-change-in-production' in content:
                    issues.append(f"Hardcoded secret still found in {file_path}")
                    print(f"❌ Hardcoded secret in {file_path}")
                else:
                    print(f"✅ No hardcoded secrets in {file_path}")
    
    return len(issues) == 0

def test_todo_items_removed():
    """Test that TODO items are completed"""
    print("\n📝 Testing TODO Items Completion...")
    
    try:
        with open('backend/app.py', 'r') as f:
            content = f.read()
            
        todo_count = content.count('TODO:')
        if todo_count == 0:
            print("✅ All TODO items completed")
            return True
        else:
            print(f"⚠️  {todo_count} TODO items still remain")
            return False
    except Exception as e:
        print(f"❌ Error checking TODO items: {e}")
        return False

def main():
    """Run comprehensive test suite"""
    print("🐛 BusinessThis Bug Fix Test Suite")
    print("=" * 50)
    
    all_tests = [
        ("Critical Imports", test_imports),
        ("Environment Validation", test_environment_validation),
        ("Security Features", test_security_features),
        ("Error Handling", test_error_handling),
        ("Validation Functions", test_validation_functions),
        ("Hardcoded Secrets", test_hardcoded_secrets_removed),
        ("TODO Items", test_todo_items_removed),
    ]
    
    results = []
    
    for test_name, test_func in all_tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Bug fixes are working correctly.")
    else:
        print(f"⚠️  {total - passed} tests failed. Some issues remain.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
