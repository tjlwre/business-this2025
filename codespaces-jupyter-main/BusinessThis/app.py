import streamlit as st
import pandas as pd
from calculations import get_all_safe_spends

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
    
    /* Animated background pattern */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(30, 58, 138, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(30, 64, 175, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(6, 95, 70, 0.05) 0%, transparent 50%);
        z-index: -1;
        animation: backgroundShift 20s ease-in-out infinite;
    }
    
    @keyframes backgroundShift {
        0%, 100% { transform: translateX(0) translateY(0); }
        25% { transform: translateX(-10px) translateY(-5px); }
        50% { transform: translateX(5px) translateY(-10px); }
        75% { transform: translateX(-5px) translateY(5px); }
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #1e3a8a 100%);
        color: white;
        padding: 3rem 1.5rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 1.5rem 1.5rem;
        box-shadow: 
            0 10px 25px -5px rgba(30, 58, 138, 0.3),
            0 4px 6px -1px rgba(0, 0, 0, 0.1);
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
        background: 
            radial-gradient(circle at 30% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 70% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
        animation: headerShimmer 3s ease-in-out infinite;
    }
    
    @keyframes headerShimmer {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        margin: 0;
        letter-spacing: -0.025em;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        animation: titleGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        0% { text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
        100% { text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1), 0 0 20px rgba(255, 255, 255, 0.1); }
    }
    
    .main-header p {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 1.25rem;
        margin: 1rem 0 0 0;
        opacity: 0.95;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    .main-header .icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
        animation: iconPulse 2s ease-in-out infinite;
    }
    
    @keyframes iconPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 
            0 10px 25px -5px rgba(0, 0, 0, 0.1),
            0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(30, 58, 138, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .sidebar .sidebar-content::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1e3a8a, #1e40af, #065f46);
        border-radius: 1rem 1rem 0 0;
    }
    
    .sidebar h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #1e3a8a;
        font-size: 1.5rem;
        margin-bottom: 2rem;
        border-bottom: 3px solid transparent;
        background: linear-gradient(90deg, #1e3a8a, #1e40af) bottom;
        background-size: 100% 3px;
        background-repeat: no-repeat;
        padding-bottom: 1rem;
        position: relative;
    }
    
    .sidebar h3::before {
        content: '💰';
        font-size: 1.25rem;
        margin-right: 0.5rem;
        animation: iconBounce 2s ease-in-out infinite;
    }
    
    @keyframes iconBounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-3px); }
    }
    
    /* Input styling */
    .stNumberInput > div > div > input {
        border: 2px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1rem;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        box-shadow: 
            inset 0 1px 3px rgba(0, 0, 0, 0.1),
            0 1px 2px rgba(0, 0, 0, 0.05);
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #1e40af;
        box-shadow: 
            0 0 0 4px rgba(30, 64, 175, 0.1),
            inset 0 1px 3px rgba(0, 0, 0, 0.1),
            0 4px 12px rgba(30, 64, 175, 0.15);
        transform: translateY(-1px);
    }
    
    .stNumberInput > div > div > input:hover {
        border-color: #1e40af;
        box-shadow: 
            0 2px 8px rgba(30, 64, 175, 0.1),
            inset 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .stNumberInput label {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #1e3a8a;
        font-size: 0.875rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .stNumberInput label::before {
        content: '💵';
        font-size: 1rem;
        animation: iconFloat 3s ease-in-out infinite;
    }
    
    @keyframes iconFloat {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        25% { transform: translateY(-2px) rotate(5deg); }
        50% { transform: translateY(-1px) rotate(0deg); }
        75% { transform: translateY(-2px) rotate(-5deg); }
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
        box-shadow: 
            0 8px 25px -5px rgba(30, 58, 138, 0.3),
            0 4px 6px -1px rgba(0, 0, 0, 0.1);
        width: 100%;
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 
            0 15px 35px -5px rgba(30, 58, 138, 0.4),
            0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98);
    }
    
    .stButton > button::after {
        content: '🚀';
        margin-left: 0.5rem;
        animation: rocketBoost 2s ease-in-out infinite;
    }
    
    @keyframes rocketBoost {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(3px); }
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #065f46 0%, #047857 50%, #059669 100%);
        border: none;
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 
            0 10px 25px -5px rgba(6, 95, 70, 0.3),
            0 4px 6px -1px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
        animation: successPulse 2s ease-in-out infinite;
    }
    
    @keyframes successPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .stSuccess::before {
        content: '✨';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.5rem;
        animation: sparkle 1.5s ease-in-out infinite;
    }
    
    @keyframes sparkle {
        0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.7; }
        50% { transform: scale(1.2) rotate(180deg); opacity: 1; }
    }
    
    .stSuccess > div {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.25rem;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Error message styling */
    .stError {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 50%, #991b1b 100%);
        border: none;
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 
            0 10px 25px -5px rgba(220, 38, 38, 0.3),
            0 4px 6px -1px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
        animation: errorShake 0.5s ease-in-out;
    }
    
    @keyframes errorShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .stError::before {
        content: '⚠️';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.5rem;
        animation: warningBlink 1s ease-in-out infinite;
    }
    
    @keyframes warningBlink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .stError > div {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.25rem;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Chart container */
    .chart-container {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 1rem;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 
            0 10px 25px -5px rgba(0, 0, 0, 0.1),
            0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(30, 58, 138, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1e3a8a, #1e40af, #065f46);
        border-radius: 1rem 1rem 0 0;
    }
    
    /* Footer styling */
    .footer {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #1e3a8a 100%);
        color: white;
        padding: 2rem;
        margin: 2rem -1rem -1rem -1rem;
        border-radius: 1.5rem 1.5rem 0 0;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        font-weight: 400;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 -10px 25px -5px rgba(30, 58, 138, 0.3),
            0 -4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 50%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
        animation: footerShimmer 4s ease-in-out infinite;
    }
    
    @keyframes footerShimmer {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.8; }
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom spacing */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1><span class="icon">💼</span>BusinessThis</h1>
    <p>Input your financial data to calculate your safe daily spending amount without risking your goals.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar inputs
st.sidebar.header("Financial Inputs")
monthly_income = st.sidebar.number_input("Monthly Income ($)", min_value=0.0, step=100.0)
fixed_expenses = st.sidebar.number_input("Fixed Expenses ($)", min_value=0.0, step=50.0)
variable_expenses_estimate = st.sidebar.number_input("Variable Expenses Estimate ($)", min_value=0.0, step=50.0)
savings_goal = st.sidebar.number_input("Savings Goal ($)", min_value=0.0, step=1000.0)
months_for_goal = st.sidebar.number_input("Months for Goal", min_value=1, step=1, value=12)

if st.button("Calculate Safe Daily Spend"):
    try:
        safe_spends = get_all_safe_spends(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal)
        
        # Display results in a nice format
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Daily Safe Spend",
                value=f"${safe_spends['daily']:.2f}",
                help="Amount you can safely spend per day"
            )
        
        with col2:
            st.metric(
                label="Weekly Safe Spend", 
                value=f"${safe_spends['weekly']:.2f}",
                help="Amount you can safely spend per week"
            )
        
        with col3:
            st.metric(
                label="Monthly Safe Spend",
                value=f"${safe_spends['monthly']:.2f}",
                help="Amount you can safely spend per month"
            )

        # Breakdown chart
        savings_contribution = savings_goal / months_for_goal
        
        # Create chart data
        chart_data = pd.DataFrame({
            'Fixed Expenses': [fixed_expenses],
            'Savings Contribution': [savings_contribution],
            'Variable Expenses': [variable_expenses_estimate],
            'Safe Monthly Spend': [safe_spends['monthly']]
        })
        
        st.bar_chart(chart_data)
    except ValueError as e:
        st.error(str(e))

# Footer
st.markdown("""
<div class="footer">
    2025. BusinessThis(c). Created by Ontiqua LLC. All Rights Reserved.
</div>
""", unsafe_allow_html=True)
