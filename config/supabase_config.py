"""
Supabase configuration for BusinessThis
Enhanced with latest Supabase Python client features (v2.22.2)
"""
import os
import asyncio
from supabase import create_client, Client
from supabase.client import ClientOptions
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_supabase_client() -> Client:
    """Get Supabase client for user operations with enhanced configuration"""
    try:
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_ANON_KEY')
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        
        # Enhanced client options for better performance and reliability
        options = ClientOptions(
            auto_refresh_token=True,
            persist_session=True,
            detect_session_in_url=True,
            headers={
                'X-Client-Info': 'BusinessThis/1.0.0',
                'User-Agent': 'BusinessThis-Python-Client'
            }
        )
        
        client = create_client(url, key, options)
        logger.info("Supabase client created successfully")
        return client
    except Exception as e:
        logger.error(f"Error creating Supabase client: {e}")
        raise

def get_supabase_service_client() -> Client:
    """Get Supabase service client for admin operations with enhanced configuration"""
    try:
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
        
        # Service client options for admin operations
        options = ClientOptions(
            auto_refresh_token=False,  # Service key doesn't need token refresh
            persist_session=False,
            detect_session_in_url=False,
            headers={
                'X-Client-Info': 'BusinessThis-Admin/1.0.0',
                'User-Agent': 'BusinessThis-Admin-Python-Client'
            }
        )
        
        client = create_client(url, key, options)
        logger.info("Supabase service client created successfully")
        return client
    except Exception as e:
        logger.error(f"Error creating Supabase service client: {e}")
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

def get_supabase_config() -> Dict[str, Any]:
    """Get Supabase configuration"""
    return {
        'url': os.getenv('SUPABASE_URL'),
        'anon_key': os.getenv('SUPABASE_ANON_KEY'),
        'service_role_key': os.getenv('SUPABASE_SERVICE_KEY'),
        'jwt_secret': os.getenv('SUPABASE_JWT_SECRET')
    }

def get_supabase_storage_client():
    """Get Supabase storage client for file operations"""
    try:
        client = get_supabase_client()
        return client.storage
    except Exception as e:
        logger.error(f"Error creating Supabase storage client: {e}")
        raise

def get_supabase_realtime_client():
    """Get Supabase realtime client for real-time subscriptions"""
    try:
        client = get_supabase_client()
        return client.realtime
    except Exception as e:
        logger.error(f"Error creating Supabase realtime client: {e}")
        raise

def get_supabase_functions_client():
    """Get Supabase functions client for edge functions"""
    try:
        client = get_supabase_client()
        return client.functions
    except Exception as e:
        logger.error(f"Error creating Supabase functions client: {e}")
        raise

async def test_supabase_async() -> bool:
    """Test Supabase connection asynchronously"""
    try:
        client = get_supabase_client()
        # Test with a simple async query
        result = await client.table('users').select('id').limit(1).execute()
        logger.info("Async Supabase connection test successful")
        return True
    except Exception as e:
        logger.error(f"Async Supabase connection test failed: {e}")
        return False

def get_supabase_health_status() -> Dict[str, Any]:
    """Get comprehensive Supabase health status"""
    try:
        client = get_supabase_client()
        
        # Test basic connection
        basic_test = test_supabase_connection()
        
        # Test storage
        storage_test = False
        try:
            storage = get_supabase_storage_client()
            storage_test = True
        except:
            pass
        
        # Test realtime
        realtime_test = False
        try:
            realtime = get_supabase_realtime_client()
            realtime_test = True
        except:
            pass
        
        return {
            'status': 'healthy' if basic_test else 'unhealthy',
            'basic_connection': basic_test,
            'storage_available': storage_test,
            'realtime_available': realtime_test,
            'version': '2.22.2',
            'timestamp': asyncio.get_event_loop().time() if asyncio.get_event_loop().is_running() else None
        }
    except Exception as e:
        logger.error(f"Error checking Supabase health: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'version': '2.22.2'
        }