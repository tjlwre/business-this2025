"""
Environment variable validation for BusinessThis
"""
import os
from typing import List, Tuple

def validate_required_env_vars() -> Tuple[bool, List[str]]:
    """
    Validate that all required environment variables are set
    Returns: (is_valid, missing_vars)
    """
    required_vars = [
        'SECRET_KEY',
        'SUPABASE_URL', 
        'SUPABASE_SERVICE_KEY',
        'SUPABASE_ANON_KEY'
    ]
    
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    return len(missing_vars) == 0, missing_vars

def validate_optional_env_vars() -> Tuple[bool, List[str]]:
    """
    Validate optional environment variables and warn if missing
    Returns: (all_present, missing_vars)
    """
    optional_vars = [
        'STRIPE_SECRET_KEY',
        'STRIPE_PUBLISHABLE_KEY', 
        'OPENAI_API_KEY',
        'SENDGRID_API_KEY',
        'PLAID_CLIENT_ID',
        'PLAID_SECRET',
        'PAYPAL_CLIENT_ID',
        'PAYPAL_CLIENT_SECRET'
    ]
    
    missing_vars = []
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    return len(missing_vars) == 0, missing_vars

def validate_environment() -> bool:
    """
    Validate the entire environment configuration
    Raises ValueError if critical variables are missing
    """
    # Check required variables
    required_valid, missing_required = validate_required_env_vars()
    if not required_valid:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_required)}")
    
    # Check optional variables
    optional_valid, missing_optional = validate_optional_env_vars()
    if not optional_valid:
        print(f"Warning: Missing optional environment variables: {', '.join(missing_optional)}")
        print("Optional features may not work without these variables.")
    
    return True

def get_env_with_validation(var_name: str, default: str = None, required: bool = True) -> str:
    """
    Get environment variable with validation
    """
    value = os.getenv(var_name, default)
    
    if required and not value:
        raise ValueError(f"Required environment variable {var_name} is not set")
    
    return value
