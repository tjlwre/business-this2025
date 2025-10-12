#!/usr/bin/env python3
"""
Verify BusinessThis deployment is working correctly
"""
import requests
import json
import sys
import os
from datetime import datetime

def test_backend_health(backend_url):
    """Test backend health endpoint"""
    try:
        response = requests.get(f"{backend_url}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend health check passed: {data}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False

def test_user_registration(backend_url):
    """Test user registration endpoint"""
    try:
        test_data = {
            "email": f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
            "password": "TestPass123!",
            "full_name": "Test User"
        }
        
        response = requests.post(
            f"{backend_url}/api/auth/register",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ User registration test passed")
            return True
        else:
            print(f"❌ User registration test failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ User registration test error: {e}")
        return False

def test_frontend_accessibility(frontend_url):
    """Test if frontend is accessible"""
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend accessibility test passed")
            return True
        else:
            print(f"❌ Frontend accessibility test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend accessibility test error: {e}")
        return False

def main():
    """Run all deployment verification tests"""
    print("🚀 BusinessThis Deployment Verification")
    print("=" * 50)
    
    # Get URLs from environment or prompt user
    backend_url = os.getenv('BACKEND_URL')
    frontend_url = os.getenv('FRONTEND_URL')
    
    if not backend_url:
        backend_url = input("Enter your backend URL (e.g., https://businessthis-backend.vercel.app): ").strip()
    
    if not frontend_url:
        frontend_url = input("Enter your frontend URL (e.g., https://businessthis.streamlit.app): ").strip()
    
    print(f"\nTesting Backend: {backend_url}")
    print(f"Testing Frontend: {frontend_url}")
    print("-" * 50)
    
    # Run tests
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Backend health
    if test_backend_health(backend_url):
        tests_passed += 1
    
    # Test 2: User registration
    if test_user_registration(backend_url):
        tests_passed += 1
    
    # Test 3: Frontend accessibility
    if test_frontend_accessibility(frontend_url):
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 50)
    print(f"Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your deployment is working correctly.")
        print("\nNext steps:")
        print("1. Test the full user flow in your browser")
        print("2. Test payment flow with Stripe test card")
        print("3. Monitor your dashboards (Vercel, Supabase, Stripe)")
        print("4. Start marketing and user acquisition!")
    else:
        print("❌ Some tests failed. Please check the errors above and fix them.")
        sys.exit(1)

if __name__ == "__main__":
    main()
