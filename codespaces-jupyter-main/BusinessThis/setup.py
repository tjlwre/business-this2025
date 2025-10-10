"""
Setup script for BusinessThis
"""
import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. Current version:", f"{version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor} is compatible")
    return True

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def create_directories():
    """Create necessary directories"""
    directories = [
        "logs",
        "uploads",
        "temp"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")

def setup_environment():
    """Set up environment file"""
    env_file = ".env"
    env_example = "env.example"
    
    if not os.path.exists(env_file):
        if os.path.exists(env_example):
            shutil.copy(env_example, env_file)
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your actual credentials")
        else:
            print("❌ env.example file not found")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def check_environment_variables():
    """Check if required environment variables are set"""
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY",
        "SECRET_KEY"
    ]
    
    missing_vars = []
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        for var in required_vars:
            if not os.getenv(var) or os.getenv(var).startswith('your_'):
                missing_vars.append(var)
        
        if missing_vars:
            print("⚠️  Missing or placeholder environment variables:")
            for var in missing_vars:
                print(f"   - {var}")
            print("Please update your .env file with actual values")
            return False
        else:
            print("✅ All required environment variables are set")
            return True
            
    except ImportError:
        print("❌ python-dotenv not installed")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    modules = [
        "streamlit",
        "flask",
        "pandas",
        "requests",
        "plotly",
        "supabase",
        "stripe",
        "jwt"
    ]
    
    failed_imports = []
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError:
            failed_imports.append(module)
            print(f"❌ {module} import failed")
    
    if failed_imports:
        print(f"❌ Failed to import: {', '.join(failed_imports)}")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 BusinessThis Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Setup environment
    if not setup_environment():
        print("❌ Setup failed at environment setup")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("❌ Setup failed at import testing")
        sys.exit(1)
    
    # Check environment variables
    check_environment_variables()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Update your .env file with actual credentials")
    print("2. Set up your Supabase database using database/schema.sql")
    print("3. Run the backend: python run_backend.py")
    print("4. Run the frontend: python run_frontend.py")
    print("\nFor detailed instructions, see README.md")

if __name__ == "__main__":
    main()
