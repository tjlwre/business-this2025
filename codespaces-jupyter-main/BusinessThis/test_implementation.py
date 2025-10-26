#!/usr/bin/env python3
"""
BusinessThis Implementation Test Suite
Comprehensive testing of all implemented features
"""
import os
import sys
import json
import requests
import time
from datetime import datetime
from typing import Dict, Any, List

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class BusinessThisTester:
    """Comprehensive test suite for BusinessThis"""
    
    def __init__(self):
        self.base_url = "http://localhost:5000/api"
        self.test_user = {
            "email": f"test_{int(time.time())}@example.com",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        self.auth_token = None
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if message:
            print(f"    {message}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def test_health_check(self) -> bool:
        """Test health check endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                self.log_test("Health Check", True, "API is responding")
                return True
            else:
                self.log_test("Health Check", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_user_registration(self) -> bool:
        """Test user registration"""
        try:
            response = requests.post(f"{self.base_url}/auth/register", json=self.test_user)
            if response.status_code == 201:
                self.log_test("User Registration", True, "User created successfully")
                return True
            else:
                self.log_test("User Registration", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("User Registration", False, f"Error: {str(e)}")
            return False
    
    def test_user_login(self) -> bool:
        """Test user login"""
        try:
            login_data = {
                "email": self.test_user["email"],
                "password": self.test_user["password"]
            }
            response = requests.post(f"{self.base_url}/auth/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("token")
                self.log_test("User Login", True, "Login successful")
                return True
            else:
                self.log_test("User Login", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("User Login", False, f"Error: {str(e)}")
            return False
    
    def test_financial_profile(self) -> bool:
        """Test financial profile creation"""
        if not self.auth_token:
            self.log_test("Financial Profile", False, "No auth token")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            profile_data = {
                "monthly_income": 5000,
                "fixed_expenses": 2000,
                "variable_expenses": 1000,
                "emergency_fund_target": 15000,
                "emergency_fund_current": 5000,
                "total_debt": 10000,
                "age": 30,
                "risk_tolerance": "moderate"
            }
            
            response = requests.post(f"{self.base_url}/financial-profile", 
                                   json=profile_data, headers=headers)
            if response.status_code == 200:
                self.log_test("Financial Profile", True, "Profile created successfully")
                return True
            else:
                self.log_test("Financial Profile", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Financial Profile", False, f"Error: {str(e)}")
            return False
    
    def test_savings_goals(self) -> bool:
        """Test savings goals functionality"""
        if not self.auth_token:
            self.log_test("Savings Goals", False, "No auth token")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            goal_data = {
                "name": "Emergency Fund",
                "target_amount": 15000,
                "current_amount": 5000,
                "monthly_contribution": 500,
                "priority": 1
            }
            
            response = requests.post(f"{self.base_url}/savings-goals", 
                                   json=goal_data, headers=headers)
            if response.status_code == 201:
                self.log_test("Savings Goals", True, "Goal created successfully")
                return True
            else:
                self.log_test("Savings Goals", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Savings Goals", False, f"Error: {str(e)}")
            return False
    
    def test_safe_spending_calculator(self) -> bool:
        """Test safe spending calculator"""
        if not self.auth_token:
            self.log_test("Safe Spending Calculator", False, "No auth token")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            calc_data = {
                "savings_goal": 10000,
                "months_for_goal": 12
            }
            
            response = requests.post(f"{self.base_url}/calculator/safe-spend", 
                                   json=calc_data, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if "safe_spending" in data:
                    self.log_test("Safe Spending Calculator", True, "Calculation successful")
                    return True
                else:
                    self.log_test("Safe Spending Calculator", False, "Invalid response format")
                    return False
            else:
                self.log_test("Safe Spending Calculator", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Safe Spending Calculator", False, f"Error: {str(e)}")
            return False
    
    def test_financial_health_score(self) -> bool:
        """Test financial health score calculation"""
        if not self.auth_token:
            self.log_test("Financial Health Score", False, "No auth token")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.get(f"{self.base_url}/calculator/financial-health", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if "financial_health" in data:
                    self.log_test("Financial Health Score", True, "Health score calculated")
                    return True
                else:
                    self.log_test("Financial Health Score", False, "Invalid response format")
                    return False
            else:
                self.log_test("Financial Health Score", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Financial Health Score", False, f"Error: {str(e)}")
            return False
    
    def test_investment_calculations(self) -> bool:
        """Test investment calculations"""
        if not self.auth_token:
            self.log_test("Investment Calculations", False, "No auth token")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            investment_data = {
                "age": 30,
                "risk_tolerance": "moderate",
                "investment_amount": 10000
            }
            
            response = requests.post(f"{self.base_url}/investment/asset-allocation", 
                                   json=investment_data, headers=headers)
            if response.status_code == 200:
                self.log_test("Investment Calculations", True, "Asset allocation calculated")
                return True
            else:
                self.log_test("Investment Calculations", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Investment Calculations", False, f"Error: {str(e)}")
            return False
    
    def test_subscription_status(self) -> bool:
        """Test subscription status endpoint"""
        if not self.auth_token:
            self.log_test("Subscription Status", False, "No auth token")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.get(f"{self.base_url}/subscription/status", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if "subscription" in data:
                    self.log_test("Subscription Status", True, "Subscription status retrieved")
                    return True
                else:
                    self.log_test("Subscription Status", False, "Invalid response format")
                    return False
            else:
                self.log_test("Subscription Status", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Subscription Status", False, f"Error: {str(e)}")
            return False
    
    def test_admin_dashboard(self) -> bool:
        """Test admin dashboard endpoint"""
        if not self.auth_token:
            self.log_test("Admin Dashboard", False, "No auth token")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.get(f"{self.base_url}/admin/dashboard", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if "dashboard" in data:
                    self.log_test("Admin Dashboard", True, "Dashboard metrics retrieved")
                    return True
                else:
                    self.log_test("Admin Dashboard", False, "Invalid response format")
                    return False
            else:
                self.log_test("Admin Dashboard", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Admin Dashboard", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return results"""
        print("🧪 BusinessThis Implementation Test Suite")
        print("=" * 50)
        
        # Test order matters - some tests depend on previous ones
        tests = [
            ("Health Check", self.test_health_check),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Financial Profile", self.test_financial_profile),
            ("Savings Goals", self.test_savings_goals),
            ("Safe Spending Calculator", self.test_safe_spending_calculator),
            ("Financial Health Score", self.test_financial_health_score),
            ("Investment Calculations", self.test_investment_calculations),
            ("Subscription Status", self.test_subscription_status),
            ("Admin Dashboard", self.test_admin_dashboard),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                self.log_test(test_name, False, f"Unexpected error: {str(e)}")
        
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! BusinessThis is ready for production!")
        else:
            print("⚠️ Some tests failed. Please check the configuration.")
        
        return {
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": total - passed,
            "success_rate": (passed / total) * 100,
            "test_results": self.test_results
        }

def main():
    """Main test function"""
    tester = BusinessThisTester()
    results = tester.run_all_tests()
    
    # Save results to file
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to test_results.json")
    
    return results["success_rate"] == 100

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)