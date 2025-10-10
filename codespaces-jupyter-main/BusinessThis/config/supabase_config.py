"""
Supabase configuration for BusinessThis
"""
import os
from supabase import create_client, Client
from typing import Optional

class SupabaseConfig:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_ANON_KEY')
        self.service_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables")
    
    def get_client(self) -> Client:
        """Get Supabase client for regular operations"""
        return create_client(self.url, self.key)
    
    def get_service_client(self) -> Client:
        """Get Supabase client with service key for admin operations"""
        if not self.service_key:
            raise ValueError("SUPABASE_SERVICE_KEY must be set for admin operations")
        return create_client(self.url, self.service_key)

# Global instance
supabase_config = SupabaseConfig()

def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    return supabase_config.get_client()

def get_supabase_service_client() -> Client:
    """Get Supabase service client for admin operations"""
    return supabase_config.get_service_client()
