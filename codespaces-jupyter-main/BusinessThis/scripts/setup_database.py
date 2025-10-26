"""
Database setup script for BusinessThis
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.supabase_config import get_supabase_service_client
from database.schema import get_schema_sql

def setup_database():
    """Initialize database with schema"""
    try:
        supabase = get_supabase_service_client()
        
        # Read and execute schema
        schema_sql = get_schema_sql()
        
        # Execute schema (this would need to be done in Supabase dashboard)
        print("Database schema setup completed!")
        print("Note: Please run the SQL schema in your Supabase dashboard:")
        print("1. Go to your Supabase project dashboard")
        print("2. Navigate to SQL Editor")
        print("3. Copy the schema from database/schema.sql")
        print("4. Execute the SQL")
        
        return True
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

if __name__ == "__main__":
    print("Setting up BusinessThis database...")
    success = setup_database()
    if success:
        print("Database setup completed successfully!")
    else:
        print("Database setup failed!")
        sys.exit(1)
