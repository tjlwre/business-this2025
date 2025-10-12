#!/usr/bin/env python3
"""
Simple test script for bug fixes
"""
import sys
import os

def test_basic_imports():
    """Test basic imports without external dependencies"""
    print("🔍 Testing Basic Imports...")
    
    try:
        from core.utils.validators import validate_email, validate_user_input
        print("✅ Validators imported successfully")
        
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
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_error_handling():
    """Test error handling classes"""
    print("\n🛡️  Testing Error Handling...")
    
    try:
        from core.utils.error_handler import ValidationError, AuthenticationError
        
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

def test_security_utils():
    """Test security utilities"""
    print("\n🔒 Testing Security Utils...")
    
    try:
        from core.utils.security import hash_password, verify_password
        
        # Test password hashing
        password = "test_password_123"
        hashed = hash_password(password)
        is_valid = verify_password(password, hashed)
        
        if is_valid:
            print("✅ Password hashing works")
        else:
            print("❌ Password hashing failed")
            return False
        
        print("✅ Security utils work correctly")
        return True
    except Exception as e:
        print(f"❌ Security utils error: {e}")
        return False

def test_environment_validation():
    """Test environment validation"""
    print("\n🔧 Testing Environment Validation...")
    
    try:
        from config.validation import validate_required_env_vars
        
        # This should return missing vars since we don't have env vars set
        is_valid, missing = validate_required_env_vars()
        
        if not is_valid and len(missing) > 0:
            print(f"✅ Environment validation correctly identified missing vars: {missing}")
            return True
        else:
            print("❌ Environment validation not working correctly")
            return False
    except Exception as e:
        print(f"❌ Environment validation error: {e}")
        return False

def test_hardcoded_secrets():
    """Test that hardcoded secrets are removed"""
    print("\n🔐 Testing Hardcoded Secrets...")
    
    files_to_check = [
        'backend/app.py',
        'core/utils/decorators.py', 
        'config/settings.py'
    ]
    
    issues = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'dev-secret-key-change-in-production' in content:
                        issues.append(f"Hardcoded secret still found in {file_path}")
                        print(f"❌ Hardcoded secret in {file_path}")
                    else:
                        print(f"✅ No hardcoded secrets in {file_path}")
            except Exception as e:
                print(f"⚠️  Could not check {file_path}: {e}")
    
    return len(issues) == 0

def main():
    """Run simple test suite"""
    print("🐛 BusinessThis Simple Bug Fix Test")
    print("=" * 40)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Error Handling", test_error_handling),
        ("Security Utils", test_security_utils),
        ("Environment Validation", test_environment_validation),
        ("Hardcoded Secrets", test_hardcoded_secrets),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"✅ {test_name}: PASS")
                passed += 1
            else:
                print(f"❌ {test_name}: FAIL")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Bug fixes are working.")
    else:
        print(f"⚠️  {total - passed} tests failed.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
