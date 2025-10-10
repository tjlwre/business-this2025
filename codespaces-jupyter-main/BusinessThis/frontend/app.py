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

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Import professional fonts and icons */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Global styles */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        min-height: 100vh;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #1e3a8a 100%);
        color: white;
        padding: 3rem 1.5rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 1.5rem 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.3);
    }
    
    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        margin: 0;
        letter-spacing: -0.025em;
    }
    
    .main-header p {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 1.25rem;
        margin: 1rem 0 0 0;
        opacity: 0.95;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(30, 58, 138, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #065f46 100%);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 1rem 2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.125rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px -5px rgba(30, 58, 138, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 15px 35px -5px rgba(30, 58, 138, 0.4);
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #065f46 0%, #047857 50%, #059669 100%);
        border: none;
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 0 10px 25px -5px rgba(6, 95, 70, 0.3);
    }
    
    .stSuccess > div {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.25rem;
    }
    
    /* Error message styling */
    .stError {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 50%, #991b1b 100%);
        border: none;
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 0 10px 25px -5px rgba(220, 38, 38, 0.3);
    }
    
    .stError > div {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.25rem;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Configuration
API_BASE_URL = "http://localhost:5000/api"

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
        """Login/Register page"""
        st.markdown("""
        <div class="main-header">
            <h1><span class="icon">💼</span>BusinessThis</h1>
            <p>Your personal financial planning assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.subheader("Login to Your Account")
            
            with st.form("login_form"):
                email = st.text_input("Email", type="default")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    if email and password:
                        data = {"email": email, "password": password}
                        response, status = self.make_api_request("/auth/login", method='POST', data=data)
                        
                        if status == 200:
                            self.session_state.authenticated = True
                            self.session_state.user = response['user']
                            self.session_state.token = response['token']
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error(response.get('error', 'Login failed'))
                    else:
                        st.error("Please fill in all fields")
        
        with tab2:
            st.subheader("Create New Account")
            
            with st.form("register_form"):
                full_name = st.text_input("Full Name")
                email = st.text_input("Email", type="default")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit = st.form_submit_button("Register", use_container_width=True)
                
                if submit:
                    if email and password and password == confirm_password:
                        data = {
                            "email": email,
                            "password": password,
                            "full_name": full_name
                        }
                        response, status = self.make_api_request("/auth/register", method='POST', data=data)
                        
                        if status == 201:
                            st.success("Registration successful! Please login.")
                        else:
                            st.error(response.get('error', 'Registration failed'))
                    else:
                        st.error("Please fill in all fields and ensure passwords match")
    
    def dashboard(self):
        """Main dashboard"""
        # Header
        st.markdown("""
        <div class="main-header">
            <h1><span class="icon">💼</span>BusinessThis</h1>
            <p>Welcome back, {}!</p>
        </div>
        """.format(self.session_state.user.get('full_name', 'User')), unsafe_allow_html=True)
        
        # Sidebar
        with st.sidebar:
            st.header("Navigation")
            
            if st.button("🏠 Dashboard", use_container_width=True):
                st.session_state.current_page = "dashboard"
                st.rerun()
            
            if st.button("💰 Financial Profile", use_container_width=True):
                st.session_state.current_page = "profile"
                st.rerun()
            
            if st.button("🎯 Savings Goals", use_container_width=True):
                st.session_state.current_page = "goals"
                st.rerun()
            
            if st.button("📊 Calculator", use_container_width=True):
                st.session_state.current_page = "calculator"
                st.rerun()
            
            if st.button("📈 Analytics", use_container_width=True):
                st.session_state.current_page = "analytics"
                st.rerun()
            
            if st.button("⚙️ Settings", use_container_width=True):
                st.session_state.current_page = "settings"
                st.rerun()
            
            st.divider()
            
            if st.button("🚪 Logout", use_container_width=True):
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
        """Dashboard main content"""
        st.header("📊 Financial Overview")
        
        # Get financial profile
        profile_response, status = self.make_api_request("/financial-profile")
        
        if status == 200:
            profile = profile_response['profile']
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Monthly Income",
                    f"${profile.get('monthly_income', 0):,.2f}",
                    help="Your monthly income"
                )
            
            with col2:
                st.metric(
                    "Fixed Expenses",
                    f"${profile.get('fixed_expenses', 0):,.2f}",
                    help="Monthly fixed expenses"
                )
            
            with col3:
                st.metric(
                    "Variable Expenses",
                    f"${profile.get('variable_expenses', 0):,.2f}",
                    help="Monthly variable expenses"
                )
            
            with col4:
                st.metric(
                    "Emergency Fund",
                    f"${profile.get('emergency_fund_current', 0):,.2f}",
                    help="Current emergency fund"
                )
            
            # Financial health score
            health_response, health_status = self.make_api_request("/calculator/financial-health")
            
            if health_status == 200:
                health = health_response['financial_health']
                
                st.subheader("🏥 Financial Health Score")
                
                # Create gauge chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = health['overall_score'],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Financial Health"},
                    delta = {'reference': 70},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 40], 'color': "lightgray"},
                            {'range': [40, 70], 'color': "yellow"},
                            {'range': [70, 100], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                # Health level and recommendations
                st.info(f"**Health Level:** {health['health_level']}")
                
                if health.get('recommendations'):
                    st.subheader("💡 Recommendations")
                    for rec in health['recommendations']:
                        st.write(f"• {rec}")
        
        else:
            st.warning("Please complete your financial profile to see your dashboard.")
    
    def profile_page(self):
        """Financial profile page"""
        st.header("💰 Financial Profile")
        
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
        st.header("🎯 Savings Goals")
        
        # Get current goals
        goals_response, status = self.make_api_request("/savings-goals")
        
        if status == 200:
            goals = goals_response['goals']
            
            # Display goals
            if goals:
                for goal in goals:
                    with st.expander(f"🎯 {goal['name']} - ${goal['target_amount']:,.2f}"):
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
        st.header("📊 Safe Spending Calculator")
        
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
                        st.subheader("📊 Results")
                        
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
                            st.success("✅ Budget is perfectly balanced!")
                        elif remaining > 0:
                            st.warning(f"⚠️ You have ${remaining:.2f} unallocated each month")
                        else:
                            st.error(f"❌ You're overspending by ${abs(remaining):.2f} each month")
                    
                    else:
                        st.error(response.get('error', 'Failed to calculate safe spending'))
                else:
                    st.error("Please enter a valid monthly income")
    
    def analytics_page(self):
        """Analytics page"""
        st.header("📈 Financial Analytics")
        
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
        st.header("⚙️ Settings")
        
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
