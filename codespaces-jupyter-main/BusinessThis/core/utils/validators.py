"""
Validation utilities for BusinessThis
"""
import re
from typing import Dict, Any, List
from decimal import Decimal

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> Dict[str, Any]:
    """Validate password strength"""
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_financial_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate financial profile data"""
    errors = []
    
    # Required fields
    required_fields = ['monthly_income', 'fixed_expenses', 'variable_expenses']
    for field in required_fields:
        if field not in data or data[field] is None:
            errors.append(f"{field.replace('_', ' ').title()} is required")
    
    # Numeric validation
    numeric_fields = ['monthly_income', 'fixed_expenses', 'variable_expenses', 
                     'emergency_fund_target', 'emergency_fund_current', 'total_debt']
    
    for field in numeric_fields:
        if field in data and data[field] is not None:
            try:
                value = float(data[field])
                if value < 0:
                    errors.append(f"{field.replace('_', ' ').title()} must be non-negative")
            except (ValueError, TypeError):
                errors.append(f"{field.replace('_', ' ').title()} must be a valid number")
    
    # Credit score validation
    if 'credit_score' in data and data['credit_score'] is not None:
        try:
            score = int(data['credit_score'])
            if not (300 <= score <= 850):
                errors.append("Credit score must be between 300 and 850")
        except (ValueError, TypeError):
            errors.append("Credit score must be a valid number")
    
    # Age validation
    if 'age' in data and data['age'] is not None:
        try:
            age = int(data['age'])
            if not (18 <= age <= 120):
                errors.append("Age must be between 18 and 120")
        except (ValueError, TypeError):
            errors.append("Age must be a valid number")
    
    # Risk tolerance validation
    if 'risk_tolerance' in data and data['risk_tolerance'] is not None:
        valid_tolerances = ['conservative', 'moderate', 'aggressive']
        if data['risk_tolerance'] not in valid_tolerances:
            errors.append("Risk tolerance must be conservative, moderate, or aggressive")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_savings_goal(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate savings goal data"""
    errors = []
    
    # Required fields
    if 'name' not in data or not data['name']:
        errors.append("Goal name is required")
    
    if 'target_amount' not in data or data['target_amount'] is None:
        errors.append("Target amount is required")
    else:
        try:
            amount = float(data['target_amount'])
            if amount <= 0:
                errors.append("Target amount must be greater than 0")
        except (ValueError, TypeError):
            errors.append("Target amount must be a valid number")
    
    # Optional numeric fields
    optional_numeric_fields = ['current_amount', 'monthly_contribution', 'priority']
    for field in optional_numeric_fields:
        if field in data and data[field] is not None:
            try:
                value = float(data[field])
                if value < 0:
                    errors.append(f"{field.replace('_', ' ').title()} must be non-negative")
            except (ValueError, TypeError):
                errors.append(f"{field.replace('_', ' ').title()} must be a valid number")
    
    # Priority validation
    if 'priority' in data and data['priority'] is not None:
        try:
            priority = int(data['priority'])
            if not (1 <= priority <= 10):
                errors.append("Priority must be between 1 and 10")
        except (ValueError, TypeError):
            errors.append("Priority must be a valid number")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_transaction_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate transaction data"""
    errors = []
    
    # Required fields
    if 'amount' not in data or data['amount'] is None:
        errors.append("Amount is required")
    else:
        try:
            amount = float(data['amount'])
            if amount == 0:
                errors.append("Amount must not be zero")
        except (ValueError, TypeError):
            errors.append("Amount must be a valid number")
    
    if 'transaction_type' not in data or data['transaction_type'] not in ['income', 'expense', 'transfer']:
        errors.append("Transaction type must be income, expense, or transfer")
    
    if 'date' not in data or not data['date']:
        errors.append("Date is required")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS"""
    if not isinstance(text, str):
        return str(text)
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', 'script', 'javascript']
    sanitized = text
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()

def validate_api_key(api_key: str, service: str) -> bool:
    """Validate API key format for different services"""
    if not api_key:
        return False
    
    if service == 'stripe':
        return api_key.startswith('sk_') or api_key.startswith('pk_')
    elif service == 'openai':
        return api_key.startswith('sk-')
    elif service == 'sendgrid':
        return len(api_key) > 20 and 'SG.' in api_key
    elif service == 'plaid':
        return len(api_key) > 20
    
    return len(api_key) > 10

def validate_user_input(data: Dict[str, Any], required_fields: List[str] = None) -> Dict[str, Any]:
    """Comprehensive user input validation"""
    errors = []
    warnings = []
    
    # Check for required fields
    if required_fields:
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                errors.append(f"{field.replace('_', ' ').title()} is required")
    
    # Sanitize string inputs
    for key, value in data.items():
        if isinstance(value, str):
            # Check for potential XSS
            if any(char in value for char in ['<', '>', 'script', 'javascript']):
                errors.append(f"Invalid characters in {key}")
            
            # Check for SQL injection patterns
            if any(pattern in value.lower() for pattern in ['union', 'select', 'drop', 'delete', 'insert', 'update']):
                errors.append(f"Invalid input pattern in {key}")
            
            # Length validation
            if len(value) > 1000:
                warnings.append(f"{key} is very long")
    
    # Numeric validation
    numeric_fields = ['income', 'expenses', 'savings', 'amount', 'target_amount']
    for field in numeric_fields:
        if field in data and data[field] is not None:
            try:
                num_value = float(data[field])
                if num_value < 0:
                    errors.append(f"{field} cannot be negative")
                elif num_value > 10000000:
                    warnings.append(f"{field} seems unreasonably high")
            except (ValueError, TypeError):
                errors.append(f"{field} must be a valid number")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }