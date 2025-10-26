"""
Seed test data script for BusinessThis
"""
import os
import sys
from pathlib import Path
from datetime import datetime, date, timedelta
import random

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from core.services.auth_service import AuthService
from core.services.financial_service import FinancialService

def seed_test_data():
    """Seed the database with test data"""
    try:
        auth_service = AuthService()
        financial_service = FinancialService()
        
        print("Seeding test data...")
        
        # Create test users
        test_users = [
            {"email": "test1@example.com", "password": "password123", "name": "Test User 1"},
            {"email": "test2@example.com", "password": "password123", "name": "Test User 2"},
            {"email": "premium@example.com", "password": "password123", "name": "Premium User"},
        ]
        
        user_ids = []
        for user_data in test_users:
            result = auth_service.register_user(
                user_data["email"], 
                user_data["password"], 
                user_data["name"]
            )
            
            if result['success']:
                user_id = result['user_id']
                user_ids.append(user_id)
                print(f"Created user: {user_data['email']}")
                
                # Create financial profile
                profile_data = {
                    'monthly_income': random.randint(3000, 8000),
                    'fixed_expenses': random.randint(1000, 3000),
                    'variable_expenses': random.randint(500, 1500),
                    'emergency_fund_target': random.randint(5000, 15000),
                    'emergency_fund_current': random.randint(1000, 5000),
                    'total_debt': random.randint(0, 20000),
                    'credit_score': random.randint(600, 800),
                    'age': random.randint(25, 55)
                }
                
                financial_service.update_financial_profile(user_id, profile_data)
                
                # Create savings goals
                goals = [
                    {"name": "Emergency Fund", "target_amount": 10000, "priority": 1},
                    {"name": "Vacation", "target_amount": 3000, "priority": 2},
                    {"name": "New Car", "target_amount": 15000, "priority": 3}
                ]
                
                for goal_data in goals:
                    financial_service.create_savings_goal(user_id, goal_data)
        
        # Set premium user
        if len(user_ids) >= 3:
            auth_service.update_subscription(user_ids[2], 'premium', 'active')
            print("Set premium user subscription")
        
        print(f"Seeded {len(user_ids)} test users with financial data")
        return True
        
    except Exception as e:
        print(f"Error seeding test data: {e}")
        return False

if __name__ == "__main__":
    print("BusinessThis Test Data Seeding")
    print("=" * 40)
    success = seed_test_data()
    if success:
        print("Test data seeding completed successfully!")
    else:
        print("Test data seeding failed!")
        sys.exit(1)
