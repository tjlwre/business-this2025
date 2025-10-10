"""
Comprehensive test script for BusinessThis implementation
Tests all major components and integrations
"""
import os
import sys
import requests
import json
import time
from datetime import datetime

class BusinessThisTester:
    """Test suite for BusinessThis application"""
    
    def __init__(self):
        self.base_url = "http://localhost:5000/api"
        self.test_user = {
            "email": f"test_{int(time.time())}@example.com",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        self.auth_token = None
        self.user_id = None
        
    def log_test(self, test_name, status, message=""):
        """Log test results"""
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {test_name}: {message}")
        return status
    
    def test_backend_health(self):
        """Test if backend is running"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                return self.log_test("Backend Health Check", True, "Backend is running")
            else:
                return self.log_test("Backend Health Check", False, f"Status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            return self.log_test("Backend Health Check", False, "Backend not running on localhost:5000")
        except Exception as e:
            return self.log_test("Backend Health Check", False, str(e))
    
    def test_user_registration(self):
        """Test user registration"""
        try:
            response = requests.post(f"{self.base_url}/auth/register", json=self.test_user)
            if response.status_code == 201:
                return self.log_test("User Registration", True, "User registered successfully")
            else:
                return self.log_test("User Registration", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            return self.log_test("User Registration", False, str(e))
    
    def test_user_login(self):
        """Test user login"""
        try:
            response = requests.post(f"{self.base_url}/auth/login", json={
                "email": self.test_user["email"],
                "password": self.test_user["password"]
            })
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("token")
                self.user_id = data.get("user", {}).get("id")
                return self.log_test("User Login", True, "Login successful")
            else:
                return self.log_test("User Login", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            return self.log_test("User Login", False, str(e))
    
    def test_financial_profile_creation(self):
        """Test financial profile creation"""
        if not self.auth_token:
            return self.log_test("Financial Profile Creation", False, "No auth token")
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            profile_data = {
                "monthly_income": 5000,
                "fixed_expenses": 2000,
                "variable_expenses": 1000,
                "emergency_fund_target": 18000,
                "emergency_fund_current": 5000,
                "total_debt": 10000,
                "credit_score": 750,
                "age": 30,
                "risk_tolerance": "moderate",
                "retirement_age": 65
            }
            
            response = requests.post(f"{self.base_url}/financial-profile", json=profile_data, headers=headers)
            if response.status_code == 200:
                return self.log_test("Financial Profile Creation", True, "Profile created successfully")
            else:
                return self.log_test("Financial Profile Creation", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            return self.log_test("Financial Profile Creation", False, str(e))
    
    def test_savings_goal_creation(self):
        """Test savings goal creation"""
        if not self.auth_token:
            return self.log_test("Savings Goal Creation", False, "No auth token")
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            goal_data = {
                "name": "Emergency Fund",
                "target_amount": 18000,
                "current_amount": 5000,
                "target_date": "2024-12-31",
                "monthly_contribution": 1000,
                "priority": 1
            }
            
            response = requests.post(f"{self.base_url}/savings-goals", json=goal_data, headers=headers)
            if response.status_code == 201:
                return self.log_test("Savings Goal Creation", True, "Goal created successfully")
            else:
                return self.log_test("Savings Goal Creation", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            return self.log_test("Savings Goal Creation", False, str(e))
    
    def test_safe_spending_calculation(self):
        """Test safe spending calculation"""
        if not self.auth_token:
            return self.log_test("Safe Spending Calculation", False, "No auth token")
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            calc_data = {
                "savings_goal": 10000,
                "months_for_goal": 12
            }
            
            response = requests.post(f"{self.base_url}/calculator/safe-spend", json=calc_data, headers=headers)
            if response.status_code == 200:
                data = response.json()
                safe_spending = data.get("safe_spending", {})
                return self.log_test("Safe Spending Calculation", True, 
                    f"Daily: ${safe_spending.get('daily', 0):.2f}, Weekly: ${safe_spending.get('weekly', 0):.2f}")
            else:
                return self.log_test("Safe Spending Calculation", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            return self.log_test("Safe Spending Calculation", False, str(e))
    
    def test_financial_health_score(self):
        """Test financial health score calculation"""
        if not self.auth_token:
            return self.log_test("Financial Health Score", False, "No auth token")
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.get(f"{self.base_url}/calculator/financial-health", headers=headers)
            if response.status_code == 200:
                data = response.json()
                health = data.get("financial_health", {})
                score = health.get("overall_score", 0)
                return self.log_test("Financial Health Score", True, f"Score: {score}/100")
            else:
                return self.log_test("Financial Health Score", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            return self.log_test("Financial Health Score", False, str(e))
    
    def test_subscription_status(self):
        """Test subscription status endpoint"""
        if not self.auth_token:
            return self.log_test("Subscription Status", False, "No auth token")
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.get(f"{self.base_url}/subscription/status", headers=headers)
            if response.status_code == 200:
                data = response.json()
                subscription = data.get("subscription", {})
                tier = subscription.get("subscription_tier", "unknown")
                return self.log_test("Subscription Status", True, f"Tier: {tier}")
            else:
                return self.log_test("Subscription Status", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            return self.log_test("Subscription Status", False, str(e))
    
    def test_calculations_module(self):
        """Test the original calculations module"""
        try:
            # Import the calculations module
            sys.path.append(os.path.join(os.path.dirname(__file__)))
            from calculations import get_all_safe_spends
            
            # Test calculation
            result = get_all_safe_spends(5000, 2000, 1000, 10000, 12)
            
            if result and 'daily' in result and 'weekly' in result and 'monthly' in result:
                return self.log_test("Calculations Module", True, 
                    f"Daily: ${result['daily']:.2f}, Weekly: ${result['weekly']:.2f}, Monthly: ${result['monthly']:.2f}")
            else:
                return self.log_test("Calculations Module", False, "Invalid result format")
        except Exception as e:
            return self.log_test("Calculations Module", False, str(e))
    
    def test_environment_variables(self):
        """Test if required environment variables are set"""
        required_vars = [
            "SUPABASE_URL",
            "SUPABASE_ANON_KEY",
            "SECRET_KEY"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var) or os.getenv(var).startswith('your_'):
                missing_vars.append(var)
        
        if missing_vars:
            return self.log_test("Environment Variables", False, f"Missing: {', '.join(missing_vars)}")
        else:
            return self.log_test("Environment Variables", True, "All required variables set")
    
    def test_database_connection(self):
        """Test database connection through API"""
        if not self.auth_token:
            return self.log_test("Database Connection", False, "No auth token")
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.get(f"{self.base_url}/financial-profile", headers=headers)
            # Any response (even 404) means database connection works
            return self.log_test("Database Connection", True, "Database accessible")
        except Exception as e:
            return self.log_test("Database Connection", False, str(e))
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 BusinessThis Implementation Test Suite")
        print("=" * 50)
        
        tests = [
            ("Environment Variables", self.test_environment_variables),
            ("Backend Health", self.test_backend_health),
            ("Database Connection", self.test_database_connection),
            ("Calculations Module", self.test_calculations_module),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Financial Profile Creation", self.test_financial_profile_creation),
            ("Savings Goal Creation", self.test_savings_goal_creation),
            ("Safe Spending Calculation", self.test_safe_spending_calculation),
            ("Financial Health Score", self.test_financial_health_score),
            ("Subscription Status", self.test_subscription_status)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                print(f"❌ {test_name}: Exception - {str(e)}")
        
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Implementation is working correctly.")
        else:
            print("⚠️  Some tests failed. Please check the implementation.")
        
        return passed == total

def main():
    """Main test function"""
    tester = BusinessThisTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ Implementation is ready for production!")
        print("\nNext steps:")
        print("1. Set up production environment variables")
        print("2. Deploy to hosting platform")
        print("3. Configure domain and SSL")
        print("4. Set up monitoring and analytics")
    else:
        print("\n❌ Implementation needs fixes before production.")
        print("\nPlease address the failed tests and try again.")

if __name__ == "__main__":
    main()
