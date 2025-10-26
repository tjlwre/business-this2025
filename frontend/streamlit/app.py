"""
BusinessThis Enhanced Frontend
Streamlit app with authentication and backend integration
"""
import streamlit as st
import requests
import json
from datetime import datetime, date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Ensure local components can be imported when running via `streamlit run frontend/app.py`
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)
from components.ui_components import UIComponents

# Modern CSS Design System
st.markdown("""
<style>
    /* Import modern fonts and icons */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');
    
    /* CSS Variables for Design System */
    :root {
        /* Colors */
        --primary-50: #eff6ff;
        --primary-100: #dbeafe;
        --primary-200: #bfdbfe;
        --primary-300: #93c5fd;
        --primary-400: #60a5fa;
        --primary-500: #3b82f6;
        --primary-600: #2563eb;
        --primary-700: #1d4ed8;
        --primary-800: #1e40af;
        --primary-900: #1e3a8a;
        
        --secondary-50: #f0fdf4;
        --secondary-100: #dcfce7;
        --secondary-200: #bbf7d0;
        --secondary-300: #86efac;
        --secondary-400: #4ade80;
        --secondary-500: #22c55e;
        --secondary-600: #16a34a;
        --secondary-700: #15803d;
        --secondary-800: #166534;
        --secondary-900: #14532d;
        
        --neutral-50: #f8fafc;
        --neutral-100: #f1f5f9;
        --neutral-200: #e2e8f0;
        --neutral-300: #cbd5e1;
        --neutral-400: #94a3b8;
        --neutral-500: #64748b;
        --neutral-600: #475569;
        --neutral-700: #334155;
        --neutral-800: #1e293b;
        --neutral-900: #0f172a;
        
        --success-50: #f0fdf4;
        --success-500: #22c55e;
        --success-600: #16a34a;
        --success-700: #15803d;
        
        --warning-50: #fffbeb;
        --warning-500: #f59e0b;
        --warning-600: #d97706;
        --warning-700: #b45309;
        
        --error-50: #fef2f2;
        --error-500: #ef4444;
        --error-600: #dc2626;
        --error-700: #b91c1c;
        
        /* Typography */
        --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
        
        /* Spacing */
        --space-1: 0.25rem;
        --space-2: 0.5rem;
        --space-3: 0.75rem;
        --space-4: 1rem;
        --space-5: 1.25rem;
        --space-6: 1.5rem;
        --space-8: 2rem;
        --space-10: 2.5rem;
        --space-12: 3rem;
        --space-16: 4rem;
        --space-20: 5rem;
        
        /* Border Radius */
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
        --radius-2xl: 1.5rem;
        --radius-full: 9999px;
        
        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
        --shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
        
        /* Transitions */
        --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-normal: 300ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 500ms cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Global Reset and Base Styles */
    * {
        box-sizing: border-box;
    }
    
    .main {
        background: linear-gradient(135deg, var(--neutral-50) 0%, var(--neutral-100) 100%);
        min-height: 100vh;
        font-family: var(--font-primary);
        line-height: 1.6;
        color: var(--neutral-800);
    }
    
    /* Modern Header with Glassmorphism */
    .main-header {
        background: linear-gradient(135deg, 
            rgba(30, 58, 138, 0.95) 0%, 
            rgba(30, 64, 175, 0.9) 50%, 
            rgba(30, 58, 138, 0.95) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        color: white;
        padding: var(--space-16) var(--space-6);
        margin: calc(-1 * var(--space-4)) calc(-1 * var(--space-4)) var(--space-8) calc(-1 * var(--space-4));
        border-radius: 0 0 var(--radius-2xl) var(--radius-2xl);
        box-shadow: var(--shadow-2xl);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, 
            rgba(255, 255, 255, 0.1) 0%, 
            transparent 50%, 
            rgba(255, 255, 255, 0.05) 100%);
        pointer-events: none;
    }
    
    .main-header h1 {
        font-family: var(--font-primary);
        font-weight: 800;
        font-size: clamp(2rem, 5vw, 3.5rem);
        margin: 0;
        letter-spacing: -0.025em;
        position: relative;
        z-index: 1;
        background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        font-family: var(--font-primary);
        font-weight: 400;
        font-size: 1.25rem;
        margin: var(--space-4) 0 0 0;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* Modern Sidebar with Card Design */
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: var(--radius-2xl);
        padding: var(--space-8);
        box-shadow: var(--shadow-xl);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: var(--space-4);
    }
    
    /* Modern Button System */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 50%, var(--secondary-600) 100%);
        color: white;
        border: none;
        border-radius: var(--radius-lg);
        padding: var(--space-4) var(--space-8);
        font-family: var(--font-primary);
        font-weight: 600;
        font-size: 1rem;
        transition: all var(--transition-normal);
        box-shadow: var(--shadow-lg);
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left var(--transition-normal);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: var(--shadow-2xl);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* Secondary Button Style */
    .stButton.secondary > button {
        background: linear-gradient(135deg, var(--neutral-100) 0%, var(--neutral-200) 100%);
        color: var(--neutral-700);
        border: 1px solid var(--neutral-300);
    }
    
    .stButton.secondary > button:hover {
        background: linear-gradient(135deg, var(--neutral-200) 0%, var(--neutral-300) 100%);
        color: var(--neutral-800);
    }
    
    /* Modern Card Components */
    .modern-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: var(--radius-2xl);
        padding: var(--space-8);
        box-shadow: var(--shadow-lg);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all var(--transition-normal);
        margin: var(--space-4) 0;
    }
    
    .modern-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-2xl);
    }
    
    /* Enhanced Success Messages */
    .stSuccess {
        background: linear-gradient(135deg, var(--success-50) 0%, var(--success-100) 100%);
        border: 1px solid var(--success-200);
        border-radius: var(--radius-xl);
        padding: var(--space-6);
        box-shadow: var(--shadow-lg);
        margin: var(--space-4) 0;
    }
    
    .stSuccess > div {
        color: var(--success-700);
        font-family: var(--font-primary);
        font-weight: 600;
        font-size: 1.125rem;
    }
    
    /* Enhanced Error Messages */
    .stError {
        background: linear-gradient(135deg, var(--error-50) 0%, var(--error-100) 100%);
        border: 1px solid var(--error-200);
        border-radius: var(--radius-xl);
        padding: var(--space-6);
        box-shadow: var(--shadow-lg);
        margin: var(--space-4) 0;
    }
    
    .stError > div {
        color: var(--error-700);
        font-family: var(--font-primary);
        font-weight: 600;
        font-size: 1.125rem;
    }
    
    /* Enhanced Warning Messages */
    .stWarning {
        background: linear-gradient(135deg, var(--warning-50) 0%, var(--warning-100) 100%);
        border: 1px solid var(--warning-200);
        border-radius: var(--radius-xl);
        padding: var(--space-6);
        box-shadow: var(--shadow-lg);
        margin: var(--space-4) 0;
    }
    
    .stWarning > div {
        color: var(--warning-700);
        font-family: var(--font-primary);
        font-weight: 600;
        font-size: 1.125rem;
    }
    
    /* Modern Form Elements */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: var(--radius-lg);
        border: 2px solid var(--neutral-200);
        padding: var(--space-3) var(--space-4);
        font-family: var(--font-primary);
        font-size: 1rem;
        transition: all var(--transition-fast);
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary-500);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        outline: none;
    }
    
    /* Modern Metrics */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: var(--radius-xl);
        padding: var(--space-6);
        box-shadow: var(--shadow-md);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all var(--transition-normal);
        text-align: center;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-600);
        margin: var(--space-2) 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--neutral-600);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(59, 130, 246, 0.3);
        border-radius: 50%;
        border-top-color: var(--primary-600);
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Progress Bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary-500) 0%, var(--secondary-500) 100%);
        border-radius: var(--radius-full);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            padding: var(--space-12) var(--space-4);
        }
        
        .main-header h1 {
            font-size: 2.5rem;
        }
        
        .sidebar .sidebar-content {
            margin: var(--space-2);
            padding: var(--space-6);
        }
    }
    
    /* Dark Mode Support */
    .dark-mode {
        --neutral-50: #0f172a;
        --neutral-100: #1e293b;
        --neutral-200: #334155;
        --neutral-300: #475569;
        --neutral-400: #64748b;
        --neutral-500: #94a3b8;
        --neutral-600: #cbd5e1;
        --neutral-700: #e2e8f0;
        --neutral-800: #f1f5f9;
        --neutral-900: #f8fafc;
        
        --primary-50: #0f172a;
        --primary-100: #1e293b;
        --primary-200: #334155;
        --primary-300: #475569;
        --primary-400: #64748b;
        --primary-500: #94a3b8;
        --primary-600: #cbd5e1;
        --primary-700: #e2e8f0;
        --primary-800: #f1f5f9;
        --primary-900: #f8fafc;
    }
    
    /* Theme Toggle Button */
    .theme-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--neutral-200);
        border-radius: var(--radius-full);
        padding: 0.75rem;
        cursor: pointer;
        transition: all var(--transition-normal);
        box-shadow: var(--shadow-lg);
    }
    
    .theme-toggle:hover {
        transform: scale(1.1);
        box-shadow: var(--shadow-xl);
    }
    
    .theme-toggle.dark {
        background: rgba(15, 23, 42, 0.9);
        border-color: var(--neutral-700);
        color: var(--neutral-200);
    }
    
    /* Dark mode specific styles */
    .dark-mode .main {
        background: linear-gradient(135deg, var(--neutral-50) 0%, var(--neutral-100) 100%);
        color: var(--neutral-800);
    }
    
    .dark-mode .main-header {
        background: linear-gradient(135deg, 
            rgba(15, 23, 42, 0.95) 0%, 
            rgba(30, 41, 59, 0.9) 50%, 
            rgba(15, 23, 42, 0.95) 100%);
    }
    
    .dark-mode .modern-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(71, 85, 105, 0.3);
        color: var(--neutral-200);
    }
    
    .dark-mode .metric-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(71, 85, 105, 0.3);
    }
    
    .dark-mode .sidebar .sidebar-content {
        background: rgba(30, 41, 59, 0.9);
        border: 1px solid rgba(71, 85, 105, 0.3);
    }
    
    /* Animation for theme transition */
    * {
        transition: background-color var(--transition-normal), 
                   color var(--transition-normal), 
                   border-color var(--transition-normal);
    }
</style>
""", unsafe_allow_html=True)

# Configuration
import os
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000/api')

class BusinessThisApp:
    """Main application class"""
    
    def __init__(self):
        self.session_state = st.session_state
        
        # Initialize session state
        if 'authenticated' not in self.session_state:
            self.session_state.authenticated = False
        if 'user' not in self.session_state:
            self.session_state.user = None
        if 'token' not in self.session_state:
            self.session_state.token = None
        if 'dark_mode' not in self.session_state:
            self.session_state.dark_mode = False
    
    def make_api_request(self, endpoint, method='GET', data=None, headers=None):
        """Make API request to backend"""
        url = f"{API_BASE_URL}{endpoint}"
        
        if headers is None:
            headers = {}
        
        if self.session_state.token:
            headers['Authorization'] = f"Bearer {self.session_state.token}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            st.error("Unable to connect to backend server. Please ensure the Flask backend is running.")
            return None, 500
        except Exception as e:
            st.error(f"API request failed: {str(e)}")
            return None, 500
    
    def login_page(self):
        """Modern Login/Register page"""
        st.markdown("""
        <div class="main-header">
            <h1><i class="fas fa-briefcase" style="margin-right: 1rem;"></i>BusinessThis</h1>
            <p>Your personal financial planning assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Center the login form
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="modern-card" style="margin: 2rem 0;">
                <div style="text-align: center; margin-bottom: 2rem;">
                    <h2 style="color: var(--neutral-800); font-weight: 700; margin: 0;">
                        <i class="fas fa-sign-in-alt" style="margin-right: 0.5rem; color: var(--primary-600);"></i>
                        Welcome Back
                    </h2>
                    <p style="color: var(--neutral-600); margin: 0.5rem 0 0 0;">Sign in to access your financial dashboard</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                st.markdown("""
                <div style="background: rgba(255, 255, 255, 0.8); border-radius: var(--radius-xl); padding: 2rem; margin: 1rem 0;">
                    <h3 style="color: var(--neutral-800); font-weight: 600; margin: 0 0 1.5rem 0;">
                        <i class="fas fa-user" style="margin-right: 0.5rem; color: var(--primary-600);"></i>
                        Login to Your Account
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                with st.form("login_form"):
                    email = st.text_input("Email Address", placeholder="Enter your email address", help="We'll never share your email")
                    password = st.text_input("Password", type="password", placeholder="Enter your password", help="Your password is encrypted and secure")
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        submit = st.form_submit_button("Login", use_container_width=True)
                    with col2:
                        if st.form_submit_button("Forgot Password?", use_container_width=True):
                            st.info("Password reset functionality coming soon!")
                    
                    if submit:
                        if email and password:
                            with st.spinner("Authenticating..."):
                                data = {"email": email, "password": password}
                                response, status = self.make_api_request("/auth/login", method='POST', data=data)
                                
                                if status == 200:
                                    self.session_state.authenticated = True
                                    self.session_state.user = response['user']
                                    self.session_state.token = response['token']
                                    st.success("Login successful! Redirecting to dashboard...")
                                    st.rerun()
                                else:
                                    st.error(f"Login failed: {(response or {}).get('error', 'Login failed')}")
                        else:
                            st.error("Please fill in all fields")
            
            with tab2:
                st.markdown("""
                <div style="background: rgba(255, 255, 255, 0.8); border-radius: var(--radius-xl); padding: 2rem; margin: 1rem 0;">
                    <h3 style="color: var(--neutral-800); font-weight: 600; margin: 0 0 1.5rem 0;">
                        <i class="fas fa-user-plus" style="margin-right: 0.5rem; color: var(--secondary-600);"></i>
                        Create New Account
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                with st.form("register_form"):
                    full_name = st.text_input("Full Name", placeholder="Enter your full name", help="This will be displayed in your dashboard")
                    email = st.text_input("Email Address", placeholder="Enter your email address", help="We'll use this for account verification")
                    password = st.text_input("Password", type="password", placeholder="Create a strong password", help="Use at least 8 characters with numbers and symbols")
                    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password", help="Must match the password above")
                    
                    # Terms and conditions
                    st.markdown("""
                    <div style="background: rgba(239, 246, 255, 0.5); border-radius: var(--radius-lg); padding: 1rem; margin: 1rem 0; border: 1px solid var(--primary-200);">
                        <div style="display: flex; align-items: flex-start;">
                            <input type="checkbox" id="terms" style="margin-right: 0.75rem; margin-top: 0.25rem;">
                            <label for="terms" style="color: var(--neutral-700); font-size: 0.875rem; line-height: 1.4;">
                                I agree to the <a href="#" style="color: var(--primary-600); text-decoration: none;">Terms of Service</a> 
                                and <a href="#" style="color: var(--primary-600); text-decoration: none;">Privacy Policy</a>
                            </label>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    submit = st.form_submit_button("Create Account", use_container_width=True)
                    
                    if submit:
                        if email and password and password == confirm_password:
                            with st.spinner("Creating your account..."):
                                data = {
                                    "email": email,
                                    "password": password,
                                    "full_name": full_name
                                }
                                response, status = self.make_api_request("/auth/register", method='POST', data=data)
                                
                                if status == 201:
                                    st.success("Registration successful! Please login with your credentials.")
                                else:
                                    st.error(f"Registration failed: {(response or {}).get('error', 'Registration failed')}")
                        else:
                            st.error("Please fill in all fields and ensure passwords match")
            
            # Footer with features
            st.markdown("""
            <div style="margin: 3rem 0; text-align: center;">
                <h4 style="color: var(--neutral-700); margin-bottom: 1.5rem;">Why Choose BusinessThis?</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div style="background: rgba(239, 246, 255, 0.5); border-radius: var(--radius-lg); padding: 1rem; border: 1px solid var(--primary-200);">
                        <i class="fas fa-shield-alt" style="color: var(--primary-600); font-size: 1.5rem; margin-bottom: 0.5rem;"></i>
                        <div style="font-weight: 600; color: var(--neutral-800);">Secure</div>
                        <div style="font-size: 0.875rem; color: var(--neutral-600);">Bank-level encryption</div>
                    </div>
                    <div style="background: rgba(240, 253, 244, 0.5); border-radius: var(--radius-lg); padding: 1rem; border: 1px solid var(--secondary-200);">
                        <i class="fas fa-chart-line" style="color: var(--secondary-600); font-size: 1.5rem; margin-bottom: 0.5rem;"></i>
                        <div style="font-weight: 600; color: var(--neutral-800);">Smart Analytics</div>
                        <div style="font-size: 0.875rem; color: var(--neutral-600);">AI-powered insights</div>
                    </div>
                    <div style="background: rgba(255, 251, 235, 0.5); border-radius: var(--radius-lg); padding: 1rem; border: 1px solid var(--warning-200);">
                        <i class="fas fa-mobile-alt" style="color: var(--warning-600); font-size: 1.5rem; margin-bottom: 0.5rem;"></i>
                        <div style="font-weight: 600; color: var(--neutral-800);">Mobile Ready</div>
                        <div style="font-size: 0.875rem; color: var(--neutral-600);">Access anywhere</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def dashboard(self):
        """Main dashboard"""
        # Theme toggle button
        st.markdown(f"""
        <div class="theme-toggle {'dark' if self.session_state.dark_mode else ''}" onclick="toggleTheme()">
            <i class="fas fa-{'moon' if not self.session_state.dark_mode else 'sun'}" style="font-size: 1.25rem;"></i>
        </div>
        """, unsafe_allow_html=True)
        
        # Theme toggle JavaScript
        st.markdown("""
        <script>
        function toggleTheme() {
            const body = document.body;
            const isDark = body.classList.contains('dark-mode');
            if (isDark) {
                body.classList.remove('dark-mode');
                localStorage.setItem('theme', 'light');
            } else {
                body.classList.add('dark-mode');
                localStorage.setItem('theme', 'dark');
            }
        }
        
        // Load saved theme
        document.addEventListener('DOMContentLoaded', function() {
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme === 'dark') {
                document.body.classList.add('dark-mode');
            }
        });
        </script>
        """, unsafe_allow_html=True)
        
        # Header
        st.markdown("""
        <div class="main-header">
            <h1>BusinessThis</h1>
            <p>Welcome back, {}!</p>
        </div>
        """.format(self.session_state.user.get('full_name', 'User')), unsafe_allow_html=True)
        
        # Modern Sidebar Navigation
        with st.sidebar:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h3 style="color: var(--neutral-800); font-weight: 700; margin: 0;">
                    <i class="fas fa-compass" style="color: var(--primary-600); margin-right: 0.5rem;"></i>
                    Navigation
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation items with modern styling
            nav_items = [
                ("Dashboard", "Dashboard", "dashboard", "Overview of your financial status"),
                ("Financial Profile", "Financial Profile", "profile", "Manage your financial information"),
                ("Savings Goals", "Savings Goals", "goals", "Track and manage your savings goals"),
                ("Calculator", "Calculator", "calculator", "Financial planning calculators"),
                ("Analytics", "Analytics", "analytics", "Detailed financial analytics"),
                ("Settings", "Settings", "settings", "Account and app settings")
            ]
            
            current_page = st.session_state.get('current_page', 'dashboard')
            
            for icon, label, page, description in nav_items:
                is_active = current_page == page
                button_style = """
                <style>
                .nav-button {
                    background: """ + ("linear-gradient(135deg, var(--primary-100) 0%, var(--primary-200) 100%)" if is_active else "linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(248, 250, 252, 0.8) 100%)") + """;
                    border: 1px solid """ + ("var(--primary-300)" if is_active else "var(--neutral-200)") + """;
                    border-radius: var(--radius-lg);
                    padding: 1rem;
                    margin: 0.5rem 0;
                    transition: all var(--transition-normal);
                    cursor: pointer;
                    text-align: left;
                }
                .nav-button:hover {
                    transform: translateY(-2px);
                    box-shadow: var(--shadow-lg);
                    background: linear-gradient(135deg, var(--primary-50) 0%, var(--primary-100) 100%);
                }
                .nav-button.active {
                    background: linear-gradient(135deg, var(--primary-100) 0%, var(--primary-200) 100%);
                    border-color: var(--primary-400);
                    box-shadow: var(--shadow-md);
                }
                .nav-icon {
                    font-size: 1.25rem;
                    margin-right: 0.75rem;
                    color: """ + ("var(--primary-600)" if is_active else "var(--neutral-500)") + """;
                }
                .nav-label {
                    font-weight: 600;
                    color: """ + ("var(--primary-700)" if is_active else "var(--neutral-700)") + """;
                    margin-bottom: 0.25rem;
                }
                .nav-description {
                    font-size: 0.875rem;
                    color: var(--neutral-500);
                    line-height: 1.4;
                }
                </style>
                """
                
                st.markdown(button_style, unsafe_allow_html=True)
                
                if st.button(f"{label}", key=f"nav_{page}", use_container_width=True):
                    st.session_state.current_page = page
                    st.rerun()
                
                # Add description tooltip
                st.markdown(f"""
                <div style="font-size: 0.75rem; color: var(--neutral-400); margin: -0.5rem 0 1rem 0; padding-left: 1rem;">
                    {description}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="margin: 2rem 0; padding: 1rem; background: rgba(239, 246, 255, 0.5); border-radius: var(--radius-lg); border: 1px solid var(--primary-200);">
                <div style="text-align: center; color: var(--primary-700); font-size: 0.875rem;">
                    <i class="fas fa-user-circle" style="margin-right: 0.5rem;"></i>
                    Welcome back!
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Logout", use_container_width=True, key="logout_btn"):
                self.session_state.authenticated = False
                self.session_state.user = None
                self.session_state.token = None
                st.rerun()
        
        # Main content based on current page
        current_page = st.session_state.get('current_page', 'dashboard')
        
        if current_page == "dashboard":
            self.dashboard_content()
        elif current_page == "profile":
            self.profile_page()
        elif current_page == "goals":
            self.goals_page()
        elif current_page == "calculator":
            self.calculator_page()
        elif current_page == "analytics":
            self.analytics_page()
        elif current_page == "settings":
            self.settings_page()
    
    def dashboard_content(self):
        """Dashboard main content with modern card layout"""
        UIComponents.modern_card("Financial Overview", "", "fas fa-chart-line", "primary")
        
        # Get financial profile
        profile_response, status = self.make_api_request("/financial-profile")
        
        if status == 200:
            profile = profile_response['profile']
            
            # Key metrics with modern card design
            st.markdown("""
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                UIComponents.metric_card(
                    "Monthly Income",
                    f"${profile.get('monthly_income', 0):,.2f}",
                    "fas fa-dollar-sign",
                    "Primary income source",
                    "success"
                )
            
            with col2:
                UIComponents.metric_card(
                    "Fixed Expenses",
                    f"${profile.get('fixed_expenses', 0):,.2f}",
                    "fas fa-home",
                    "Monthly recurring",
                    "warning"
                )
            
            with col3:
                UIComponents.metric_card(
                    "Variable Expenses",
                    f"${profile.get('variable_expenses', 0):,.2f}",
                    "fas fa-shopping-cart",
                    "Flexible spending",
                    "primary"
                )
            
            with col4:
                emergency_fund = profile.get('emergency_fund_current', 0)
                emergency_target = profile.get('emergency_fund_target', 1)
                emergency_progress = (emergency_fund / emergency_target * 100) if emergency_target > 0 else 0
                
                UIComponents.metric_card(
                    "Emergency Fund",
                    f"${emergency_fund:,.2f}",
                    "fas fa-shield-alt",
                    f"{emergency_progress:.1f}% of target",
                    "success" if emergency_progress >= 100 else "warning"
                )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Financial health score with modern design
            health_response, health_status = self.make_api_request("/calculator/financial-health")
            
            if health_status == 200:
                health = health_response['financial_health']
                
                UIComponents.modern_card("Financial Health Score", "", "fas fa-heartbeat", "primary")
                
                # Create modern gauge chart using component
                fig = UIComponents.financial_health_gauge(health['overall_score'])
                st.plotly_chart(fig, use_container_width=True)
                
                # Health level and recommendations with modern cards
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    health_level = health['health_level']
                    health_color = {
                        'Excellent': 'success',
                        'Good': 'primary', 
                        'Fair': 'warning',
                        'Poor': 'error'
                    }.get(health_level, 'info')
                    
                    UIComponents.metric_card(
                        "Health Level",
                        health_level,
                        f"fas fa-{'trophy' if health_level == 'Excellent' else 'star' if health_level == 'Good' else 'exclamation-triangle' if health_level == 'Fair' else 'exclamation-circle'}",
                        f"{health['overall_score']}/100",
                        health_color
                    )
                
                with col2:
                    if health.get('recommendations'):
                        UIComponents.modern_card("Recommendations", "", "fas fa-lightbulb", "warning")
                        
                        for i, rec in enumerate(health['recommendations'], 1):
                            st.markdown(f"""
                            <div style="background: rgba(255, 255, 255, 0.8); border-radius: var(--radius-lg); padding: 1rem; margin: 0.5rem 0; border-left: 4px solid var(--primary-500);">
                                <div style="display: flex; align-items: flex-start;">
                                    <span style="background: var(--primary-100); color: var(--primary-700); border-radius: 50%; width: 1.5rem; height: 1.5rem; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 600; margin-right: 0.75rem; flex-shrink: 0;">{i}</span>
                                    <span style="color: var(--neutral-700); line-height: 1.5;">{rec}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
        
        else:
            st.warning("Please complete your financial profile to see your dashboard.")
    
    def profile_page(self):
        """Financial profile page"""
        st.header("Financial Profile")
        
        # Get current profile
        profile_response, status = self.make_api_request("/financial-profile")
        
        if status == 200:
            profile = profile_response['profile']
        else:
            profile = {}
        
        with st.form("financial_profile_form"):
            st.subheader("Basic Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                monthly_income = st.number_input(
                    "Monthly Income ($)",
                    min_value=0.0,
                    step=100.0,
                    value=float(profile.get('monthly_income', 0))
                )
                
                fixed_expenses = st.number_input(
                    "Fixed Expenses ($)",
                    min_value=0.0,
                    step=50.0,
                    value=float(profile.get('fixed_expenses', 0))
                )
                
                variable_expenses = st.number_input(
                    "Variable Expenses ($)",
                    min_value=0.0,
                    step=50.0,
                    value=float(profile.get('variable_expenses', 0))
                )
            
            with col2:
                emergency_fund_target = st.number_input(
                    "Emergency Fund Target ($)",
                    min_value=0.0,
                    step=1000.0,
                    value=float(profile.get('emergency_fund_target', 0))
                )
                
                emergency_fund_current = st.number_input(
                    "Current Emergency Fund ($)",
                    min_value=0.0,
                    step=100.0,
                    value=float(profile.get('emergency_fund_current', 0))
                )
                
                total_debt = st.number_input(
                    "Total Debt ($)",
                    min_value=0.0,
                    step=100.0,
                    value=float(profile.get('total_debt', 0))
                )
            
            st.subheader("Additional Information")
            
            col3, col4 = st.columns(2)
            
            with col3:
                credit_score = st.number_input(
                    "Credit Score",
                    min_value=300,
                    max_value=850,
                    step=1,
                    value=profile.get('credit_score', 0) or None
                )
                
                age = st.number_input(
                    "Age",
                    min_value=18,
                    max_value=120,
                    step=1,
                    value=profile.get('age', 0) or None
                )
            
            with col4:
                risk_tolerance = st.selectbox(
                    "Risk Tolerance",
                    ["conservative", "moderate", "aggressive"],
                    index=["conservative", "moderate", "aggressive"].index(profile.get('risk_tolerance', 'moderate'))
                )
                
                retirement_age = st.number_input(
                    "Retirement Age",
                    min_value=50,
                    max_value=80,
                    step=1,
                    value=profile.get('retirement_age', 65)
                )
            
            submit = st.form_submit_button("Save Profile", use_container_width=True)
            
            if submit:
                data = {
                    "monthly_income": monthly_income,
                    "fixed_expenses": fixed_expenses,
                    "variable_expenses": variable_expenses,
                    "emergency_fund_target": emergency_fund_target,
                    "emergency_fund_current": emergency_fund_current,
                    "total_debt": total_debt,
                    "credit_score": credit_score,
                    "age": age,
                    "risk_tolerance": risk_tolerance,
                    "retirement_age": retirement_age
                }
                
                response, status = self.make_api_request("/financial-profile", method='POST', data=data)
                
                if status == 200:
                    st.success("Financial profile updated successfully!")
                    st.rerun()
                else:
                    st.error(response.get('error', 'Failed to update profile'))
    
    def goals_page(self):
        """Savings goals page"""
        st.header("Savings Goals")
        
        # Get current goals
        goals_response, status = self.make_api_request("/savings-goals")
        
        if status == 200:
            goals = goals_response['goals']
            
            # Display goals
            if goals:
                for goal in goals:
                    with st.expander(f"{goal['name']} - ${goal['target_amount']:,.2f}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Current Amount:** ${goal['current_amount']:,.2f}")
                            st.write(f"**Target Amount:** ${goal['target_amount']:,.2f}")
                            st.write(f"**Progress:** {goal['current_amount']/goal['target_amount']*100:.1f}%")
                        
                        with col2:
                            if goal.get('target_date'):
                                st.write(f"**Target Date:** {goal['target_date']}")
                            if goal.get('monthly_contribution'):
                                st.write(f"**Monthly Contribution:** ${goal['monthly_contribution']:,.2f}")
                        
                        # Progress bar
                        progress = goal['current_amount'] / goal['target_amount']
                        st.progress(progress)
                        
                        # Action buttons
                        col3, col4, col5 = st.columns(3)
                        
                        with col3:
                            if st.button(f"Edit {goal['name']}", key=f"edit_{goal['id']}"):
                                st.session_state.editing_goal = goal
                                st.rerun()
                        
                        with col4:
                            if st.button(f"Delete {goal['name']}", key=f"delete_{goal['id']}"):
                                delete_response, delete_status = self.make_api_request(f"/savings-goals/{goal['id']}", method='DELETE')
                                if delete_status == 200:
                                    st.success("Goal deleted successfully!")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete goal")
            else:
                st.info("No savings goals yet. Create your first goal below!")
        
        # Add new goal form
        st.subheader("Add New Goal")
        
        with st.form("new_goal_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                goal_name = st.text_input("Goal Name")
                target_amount = st.number_input("Target Amount ($)", min_value=0.0, step=100.0)
                current_amount = st.number_input("Current Amount ($)", min_value=0.0, step=100.0)
            
            with col2:
                target_date = st.date_input("Target Date", min_value=date.today())
                monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=0.0, step=50.0)
                priority = st.number_input("Priority (1-10)", min_value=1, max_value=10, value=1)
            
            submit = st.form_submit_button("Create Goal", use_container_width=True)
            
            if submit:
                if goal_name and target_amount > 0:
                    data = {
                        "name": goal_name,
                        "target_amount": target_amount,
                        "current_amount": current_amount,
                        "target_date": target_date.isoformat(),
                        "monthly_contribution": monthly_contribution,
                        "priority": priority
                    }
                    
                    response, status = self.make_api_request("/savings-goals", method='POST', data=data)
                    
                    if status == 201:
                        st.success("Goal created successfully!")
                        st.rerun()
                    else:
                        st.error(response.get('error', 'Failed to create goal'))
                else:
                    st.error("Please fill in goal name and target amount")
    
    def calculator_page(self):
        """Calculator page"""
        st.header("Safe Spending Calculator")
        
        # Get financial profile for default values
        profile_response, status = self.make_api_request("/financial-profile")
        
        if status == 200:
            profile = profile_response['profile']
        else:
            profile = {}
        
        with st.form("calculator_form"):
            st.subheader("Financial Inputs")
            
            col1, col2 = st.columns(2)
            
            with col1:
                monthly_income = st.number_input(
                    "Monthly Income ($)",
                    min_value=0.0,
                    step=100.0,
                    value=float(profile.get('monthly_income', 0))
                )
                
                fixed_expenses = st.number_input(
                    "Fixed Expenses ($)",
                    min_value=0.0,
                    step=50.0,
                    value=float(profile.get('fixed_expenses', 0))
                )
            
            with col2:
                variable_expenses = st.number_input(
                    "Variable Expenses ($)",
                    min_value=0.0,
                    step=50.0,
                    value=float(profile.get('variable_expenses', 0))
                )
                
                savings_goal = st.number_input(
                    "Savings Goal ($)",
                    min_value=0.0,
                    step=1000.0,
                    value=0.0
                )
            
            months_for_goal = st.number_input(
                "Months for Goal",
                min_value=1,
                step=1,
                value=12
            )
            
            submit = st.form_submit_button("Calculate Safe Spending", use_container_width=True)
            
            if submit:
                if monthly_income > 0:
                    data = {
                        "savings_goal": savings_goal,
                        "months_for_goal": months_for_goal
                    }
                    
                    response, status = self.make_api_request("/calculator/safe-spend", method='POST', data=data)
                    
                    if status == 200:
                        safe_spending = response['safe_spending']
                        
                        # Display results
                        st.subheader("Results")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                "Daily Safe Spend",
                                f"${safe_spending['daily']:.2f}",
                                help="Amount you can safely spend per day"
                            )
                        
                        with col2:
                            st.metric(
                                "Weekly Safe Spend",
                                f"${safe_spending['weekly']:.2f}",
                                help="Amount you can safely spend per week"
                            )
                        
                        with col3:
                            st.metric(
                                "Monthly Safe Spend",
                                f"${safe_spending['monthly']:.2f}",
                                help="Amount you can safely spend per month"
                            )
                        
                        # Breakdown chart
                        savings_contribution = savings_goal / months_for_goal
                        
                        chart_data = pd.DataFrame({
                            'Category': ['Fixed Expenses', 'Savings Contribution', 'Variable Expenses', 'Safe Monthly Spend'],
                            'Amount': [fixed_expenses, savings_contribution, variable_expenses, safe_spending['monthly']]
                        })
                        
                        fig = px.bar(chart_data, x='Category', y='Amount', title='Monthly Budget Breakdown')
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Validation
                        total_allocated = fixed_expenses + savings_contribution + variable_expenses + safe_spending['monthly']
                        remaining = monthly_income - total_allocated
                        
                        if abs(remaining) < 0.01:
                            st.success("Budget is perfectly balanced!")
                        elif remaining > 0:
                            st.warning(f"You have ${remaining:.2f} unallocated each month")
                        else:
                            st.error(f"You're overspending by ${abs(remaining):.2f} each month")
                    
                    else:
                        st.error(response.get('error', 'Failed to calculate safe spending'))
                else:
                    st.error("Please enter a valid monthly income")
    
    def analytics_page(self):
        """Analytics page"""
        st.header("Financial Analytics")
        
        # Get financial profile
        profile_response, status = self.make_api_request("/financial-profile")
        
        if status == 200:
            profile = profile_response['profile']
            
            # Key metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                savings_rate = ((profile.get('monthly_income', 0) - profile.get('fixed_expenses', 0) - profile.get('variable_expenses', 0)) / profile.get('monthly_income', 1)) * 100
                st.metric("Savings Rate", f"{savings_rate:.1f}%")
            
            with col2:
                debt_ratio = (profile.get('total_debt', 0) / profile.get('monthly_income', 1)) * 100
                st.metric("Debt-to-Income Ratio", f"{debt_ratio:.1f}%")
            
            with col3:
                emergency_fund_progress = (profile.get('emergency_fund_current', 0) / profile.get('emergency_fund_target', 1)) * 100
                st.metric("Emergency Fund Progress", f"{emergency_fund_progress:.1f}%")
            
            # Charts
            st.subheader("Financial Health Breakdown")
            
            # Create pie chart for expenses
            expense_data = pd.DataFrame({
                'Category': ['Fixed Expenses', 'Variable Expenses', 'Available for Spending'],
                'Amount': [
                    profile.get('fixed_expenses', 0),
                    profile.get('variable_expenses', 0),
                    profile.get('monthly_income', 0) - profile.get('fixed_expenses', 0) - profile.get('variable_expenses', 0)
                ]
            })
            
            fig = px.pie(expense_data, values='Amount', names='Category', title='Monthly Income Distribution')
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("Please complete your financial profile to see analytics.")
    
    def settings_page(self):
        """Settings page"""
        st.header("Settings")
        
        # User information
        st.subheader("Account Information")
        
        if self.session_state.user:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Email:** {self.session_state.user.get('email', 'N/A')}")
                st.write(f"**Full Name:** {self.session_state.user.get('full_name', 'N/A')}")
            
            with col2:
                st.write(f"**Subscription Tier:** {self.session_state.user.get('subscription_tier', 'free').title()}")
                st.write(f"**AI Usage:** {self.session_state.user.get('ai_usage_count', 0)} / {self.session_state.user.get('ai_usage_limit', 0)}")
        
        # Subscription management
        st.subheader("Subscription Management")
        
        subscription_response, status = self.make_api_request("/subscription/status")
        
        if status == 200:
            subscription = subscription_response['subscription']
            
            st.write(f"**Current Plan:** {subscription.get('subscription_tier', 'free').title()}")
            st.write(f"**Status:** {subscription.get('subscription_status', 'active').title()}")
            
            if subscription.get('subscription_tier') == 'free':
                st.info("Upgrade to Premium or Pro for advanced features!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Upgrade to Premium ($9.99/month)", use_container_width=True):
                        upgrade_response, upgrade_status = self.make_api_request("/subscription/upgrade", method='POST', data={"plan": "premium"})
                        if upgrade_status == 200:
                            st.success("Redirecting to payment...")
                            st.link_button("Complete Payment", upgrade_response['checkout_url'])
                        else:
                            st.error("Failed to start upgrade process")
                
                with col2:
                    if st.button("Upgrade to Pro ($19.99/month)", use_container_width=True):
                        upgrade_response, upgrade_status = self.make_api_request("/subscription/upgrade", method='POST', data={"plan": "pro"})
                        if upgrade_status == 200:
                            st.success("Redirecting to payment...")
                            st.link_button("Complete Payment", upgrade_response['checkout_url'])
                        else:
                            st.error("Failed to start upgrade process")
    
    def run(self):
        """Run the application"""
        if not self.session_state.authenticated:
            self.login_page()
        else:
            self.dashboard()

# Run the app
if __name__ == "__main__":
    app = BusinessThisApp()
    app.run()
