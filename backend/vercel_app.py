"""
Vercel-compatible Flask app entry point
"""
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(backend_dir.parent))

# Import the main Flask app
from app import app

# This is the entry point for Vercel
def handler(request):
    return app(request.environ, lambda *args: None)
