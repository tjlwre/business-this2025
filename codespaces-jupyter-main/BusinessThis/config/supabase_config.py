"""
Supabase configuration for BusinessThis
"""
import os
from supabase import create_client, Client
from typing import Optional

def get_supabase_client() -> Client:
    """Get Supabase client for user operations"""
    try:
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_ANON_KEY')
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        
        return create_client(url, key)
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        raise

def get_supabase_service_client() -> Client:
    """Get Supabase service client for admin operations"""
    try:
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
        
        return create_client(url, key)
    except Exception as e:
        print(f"Error creating Supabase service client: {e}")
        raise

def test_supabase_connection() -> bool:
    """Test Supabase connection"""
    try:
        client = get_supabase_client()
        # Try to access a simple table
        result = client.table('users').select('id').limit(1).execute()
        return True
    except Exception as e:
        print(f"Supabase connection test failed: {e}")
        return False

def get_supabase_config() -> dict:
    """Get Supabase configuration"""
    return {
        'url': os.getenv('SUPABASE_URL'),
        'anon_key': os.getenv('SUPABASE_ANON_KEY'),
        'service_role_key': os.getenv('SUPABASE_SERVICE_KEY'),
        'jwt_secret': os.getenv('SUPABASE_JWT_SECRET')
    }