"""
Run the Streamlit frontend
"""
import os
import sys
import subprocess

# Add the frontend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'frontend'))

if __name__ == "__main__":
    print("Starting BusinessThis Streamlit Frontend...")
    print("Frontend will be available at: http://localhost:8501")
    print("Make sure the Flask backend is running on port 5000")
    
    # Change to the frontend directory and run streamlit
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    os.chdir(frontend_dir)
    
    # Run streamlit
    subprocess.run(["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"])
