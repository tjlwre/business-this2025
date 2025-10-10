"""
Validation utilities for BusinessThis
"""
import re
from typing import Dict, Any

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
    
    # Validate monthly income
    if 'monthly_income' in data:
        try:
            income = float(data['monthly_income'])
            if income < 0:
                errors.append("Monthly income cannot be negative")
        except (ValueError, TypeError):
            errors.append("Monthly income must be a valid number")
    
    # Validate fixed expenses
    if 'fixed_expenses' in data:
        try:
            expenses = float(data['fixed_expenses'])
            if expenses < 0:
                errors.append("Fixed expenses cannot be negative")
        except (ValueError, TypeError):
            errors.append("Fixed expenses must be a valid number")
    
    # Validate variable expenses
    if 'variable_expenses' in data:
        try:
            expenses = float(data['variable_expenses'])
            if expenses < 0:
                errors.append("Variable expenses cannot be negative")
        except (ValueError, TypeError):
            errors.append("Variable expenses must be a valid number")
    
    # Validate emergency fund
    if 'emergency_fund_target' in data:
        try:
            fund = float(data['emergency_fund_target'])
            if fund < 0:
                errors.append("Emergency fund target cannot be negative")
        except (ValueError, TypeError):
            errors.append("Emergency fund target must be a valid number")
    
    # Validate total debt
    if 'total_debt' in data:
        try:
            debt = float(data['total_debt'])
            if debt < 0:
                errors.append("Total debt cannot be negative")
        except (ValueError, TypeError):
            errors.append("Total debt must be a valid number")
    
    # Validate credit score
    if 'credit_score' in data and data['credit_score'] is not None:
        try:
            score = int(data['credit_score'])
            if score < 300 or score > 850:
                errors.append("Credit score must be between 300 and 850")
        except (ValueError, TypeError):
            errors.append("Credit score must be a valid integer")
    
    # Validate risk tolerance
    if 'risk_tolerance' in data:
        valid_tolerances = ['conservative', 'moderate', 'aggressive']
        if data['risk_tolerance'] not in valid_tolerances:
            errors.append(f"Risk tolerance must be one of: {', '.join(valid_tolerances)}")
    
    # Validate age
    if 'age' in data and data['age'] is not None:
        try:
            age = int(data['age'])
            if age < 18 or age > 120:
                errors.append("Age must be between 18 and 120")
        except (ValueError, TypeError):
            errors.append("Age must be a valid integer")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_savings_goal_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate savings goal data"""
    errors = []
    
    # Validate name
    if not data.get('name') or not data['name'].strip():
        errors.append("Goal name is required")
    
    # Validate target amount
    if 'target_amount' not in data:
        errors.append("Target amount is required")
    else:
        try:
            amount = float(data['target_amount'])
            if amount <= 0:
                errors.append("Target amount must be greater than 0")
        except (ValueError, TypeError):
            errors.append("Target amount must be a valid number")
    
    # Validate current amount
    if 'current_amount' in data:
        try:
            amount = float(data['current_amount'])
            if amount < 0:
                errors.append("Current amount cannot be negative")
        except (ValueError, TypeError):
            errors.append("Current amount must be a valid number")
    
    # Validate monthly contribution
    if 'monthly_contribution' in data and data['monthly_contribution'] is not None:
        try:
            contribution = float(data['monthly_contribution'])
            if contribution < 0:
                errors.append("Monthly contribution cannot be negative")
        except (ValueError, TypeError):
            errors.append("Monthly contribution must be a valid number")
    
    # Validate priority
    if 'priority' in data:
        try:
            priority = int(data['priority'])
            if priority < 1:
                errors.append("Priority must be at least 1")
        except (ValueError, TypeError):
            errors.append("Priority must be a valid integer")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_transaction_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate transaction data"""
    errors = []
    
    # Validate amount
    if 'amount' not in data:
        errors.append("Amount is required")
    else:
        try:
            amount = float(data['amount'])
            if amount == 0:
                errors.append("Amount cannot be zero")
        except (ValueError, TypeError):
            errors.append("Amount must be a valid number")
    
    # Validate transaction type
    if 'transaction_type' in data:
        valid_types = ['income', 'expense', 'transfer']
        if data['transaction_type'] not in valid_types:
            errors.append(f"Transaction type must be one of: {', '.join(valid_types)}")
    
    # Validate date
    if 'date' in data:
        try:
            from datetime import datetime
            datetime.fromisoformat(data['date'])
        except (ValueError, TypeError):
            errors.append("Date must be in valid ISO format")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', 'script', 'javascript']
    
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()

def validate_currency_amount(amount: Any) -> bool:
    """Validate currency amount"""
    try:
        value = float(amount)
        return value >= 0 and value <= 999999999.99  # Max $999,999,999.99
    except (ValueError, TypeError):
        return False
