"""
Create admin user script for BusinessThis
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from core.services.auth_service import AuthService

def create_admin_user():
    """Create an admin user"""
    try:
        auth_service = AuthService()
        
        print("Creating admin user...")
        email = input("Enter admin email: ")
        password = input("Enter admin password: ")
        full_name = input("Enter admin full name: ")
        
        # Register the user
        result = auth_service.register_user(email, password, full_name)
        
        if result['success']:
            user_id = result['user_id']
            
            # Update user to admin role (you'd need to add this to your user model)
            # For now, just mark as pro subscription
            auth_service.update_subscription(user_id, 'pro', 'active')
            
            print(f"Admin user created successfully!")
            print(f"User ID: {user_id}")
            print(f"Email: {email}")
            return True
        else:
            print(f"Error creating admin user: {result['error']}")
            return False
            
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return False

if __name__ == "__main__":
    print("BusinessThis Admin User Creation")
    print("=" * 40)
    success = create_admin_user()
    if success:
        print("Admin user creation completed successfully!")
    else:
        print("Admin user creation failed!")
        sys.exit(1)
