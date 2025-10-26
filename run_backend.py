"""
Run the Flask backend server
"""
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Load environment variables
load_dotenv()

# Import and run the Flask app
from backend.app import app

if __name__ == "__main__":
    print("Starting BusinessThis Flask Backend...")
    print("Backend will be available at: http://localhost:5000")
    print("API Documentation: http://localhost:5000/api/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
