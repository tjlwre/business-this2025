"""
Admin dashboard for BusinessThis
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from core.services.auth_service import AuthService
from core.services.financial_service import FinancialService
from core.services.subscription_service import SubscriptionService
from config.supabase_config import get_supabase_client

class AdminDashboard:
    """Admin dashboard for BusinessThis"""
    
    def __init__(self):
        self.auth_service = AuthService()
        self.financial_service = FinancialService()
        self.subscription_service = SubscriptionService()
        self.supabase = get_supabase_client()
    
    def run(self):
        """Run the admin dashboard"""
        st.set_page_config(
            page_title="BusinessThis Admin",
            page_icon="📊",
            layout="wide"
        )
        
        st.title("📊 BusinessThis Admin Dashboard")
        
        # Sidebar navigation
        page = st.sidebar.selectbox(
            "Navigation",
            ["Overview", "Users", "Subscriptions", "Financial Data", "System Health"]
        )
        
        if page == "Overview":
            self.show_overview()
        elif page == "Users":
            self.show_users()
        elif page == "Subscriptions":
            self.show_subscriptions()
        elif page == "Financial Data":
            self.show_financial_data()
        elif page == "System Health":
            self.show_system_health()
    
    def show_overview(self):
        """Show overview metrics"""
        st.header("📈 Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_users = self.get_total_users()
            st.metric("Total Users", total_users)
        
        with col2:
            active_subscriptions = self.get_active_subscriptions()
            st.metric("Active Subscriptions", active_subscriptions)
        
        with col3:
            mrr = self.get_monthly_recurring_revenue()
            st.metric("Monthly Recurring Revenue", f"${mrr:,.2f}")
        
        with col4:
            churn_rate = self.get_churn_rate()
            st.metric("Churn Rate", f"{churn_rate:.1f}%")
        
        # Recent activity
        st.subheader("Recent Activity")
        recent_activity = self.get_recent_activity()
        if recent_activity:
            df = pd.DataFrame(recent_activity)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No recent activity")
    
    def show_users(self):
        """Show user management"""
        st.header("👥 Users")
        
        # User filters
        col1, col2, col3 = st.columns(3)
        with col1:
            subscription_filter = st.selectbox("Subscription Tier", ["All", "Free", "Premium", "Pro"])
        with col2:
            status_filter = st.selectbox("Status", ["All", "Active", "Inactive"])
        with col3:
            search_term = st.text_input("Search by email")
        
        # Get users
        users = self.get_users(subscription_filter, status_filter, search_term)
        
        if users:
            df = pd.DataFrame(users)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No users found")
    
    def show_subscriptions(self):
        """Show subscription management"""
        st.header("💳 Subscriptions")
        
        # Subscription metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            free_users = self.get_subscription_count('free')
            st.metric("Free Users", free_users)
        
        with col2:
            premium_users = self.get_subscription_count('premium')
            st.metric("Premium Users", premium_users)
        
        with col3:
            pro_users = self.get_subscription_count('pro')
            st.metric("Pro Users", pro_users)
        
        # Subscription details
        subscriptions = self.get_subscription_details()
        if subscriptions:
            df = pd.DataFrame(subscriptions)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No subscription data")
    
    def show_financial_data(self):
        """Show financial data insights"""
        st.header("💰 Financial Data")
        
        # Financial health distribution
        st.subheader("Financial Health Distribution")
        health_scores = self.get_financial_health_distribution()
        if health_scores:
            df = pd.DataFrame(health_scores)
            st.bar_chart(df.set_index('health_level')['count'])
        else:
            st.info("No financial health data")
        
        # Average financial metrics
        st.subheader("Average Financial Metrics")
        metrics = self.get_average_financial_metrics()
        if metrics:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Avg Monthly Income", f"${metrics.get('avg_income', 0):,.2f}")
            with col2:
                st.metric("Avg Savings Rate", f"{metrics.get('avg_savings_rate', 0):.1f}%")
            with col3:
                st.metric("Avg Debt-to-Income", f"{metrics.get('avg_debt_ratio', 0):.2f}")
    
    def show_system_health(self):
        """Show system health metrics"""
        st.header("🔧 System Health")
        
        # Database status
        st.subheader("Database Status")
        db_status = self.check_database_status()
        if db_status:
            st.success("✅ Database connection healthy")
        else:
            st.error("❌ Database connection failed")
        
        # API status
        st.subheader("External Services")
        services = self.check_external_services()
        for service, status in services.items():
            if status:
                st.success(f"✅ {service} - Connected")
            else:
                st.error(f"❌ {service} - Failed")
    
    def get_total_users(self):
        """Get total user count"""
        try:
            result = self.supabase.table('users').select('id', count='exact').execute()
            return result.count
        except:
            return 0
    
    def get_active_subscriptions(self):
        """Get active subscription count"""
        try:
            result = self.supabase.table('users').select('id', count='exact').neq('subscription_tier', 'free').execute()
            return result.count
        except:
            return 0
    
    def get_monthly_recurring_revenue(self):
        """Calculate monthly recurring revenue"""
        try:
            # This would need to be calculated based on actual subscription data
            # For now, return a placeholder
            return 0.0
        except:
            return 0.0
    
    def get_churn_rate(self):
        """Calculate churn rate"""
        try:
            # This would need to be calculated based on historical data
            # For now, return a placeholder
            return 0.0
        except:
            return 0.0
    
    def get_recent_activity(self):
        """Get recent user activity"""
        try:
            result = self.supabase.table('users').select('email, created_at, last_login').order('created_at', desc=True).limit(10).execute()
            return result.data
        except:
            return []
    
    def get_users(self, subscription_filter, status_filter, search_term):
        """Get filtered users"""
        try:
            query = self.supabase.table('users').select('*')
            
            if subscription_filter != "All":
                query = query.eq('subscription_tier', subscription_filter.lower())
            
            if status_filter != "All":
                is_active = status_filter == "Active"
                query = query.eq('is_active', is_active)
            
            if search_term:
                query = query.ilike('email', f'%{search_term}%')
            
            result = query.execute()
            return result.data
        except:
            return []
    
    def get_subscription_count(self, tier):
        """Get subscription count by tier"""
        try:
            result = self.supabase.table('users').select('id', count='exact').eq('subscription_tier', tier).execute()
            return result.count
        except:
            return 0
    
    def get_subscription_details(self):
        """Get subscription details"""
        try:
            result = self.supabase.table('subscriptions').select('*').execute()
            return result.data
        except:
            return []
    
    def get_financial_health_distribution(self):
        """Get financial health score distribution"""
        try:
            result = self.supabase.table('financial_health_scores').select('overall_score').execute()
            if not result.data:
                return []
            
            # Group scores into ranges
            ranges = {
                'Excellent (90-100)': 0,
                'Good (75-89)': 0,
                'Fair (60-74)': 0,
                'Poor (40-59)': 0,
                'Critical (0-39)': 0
            }
            
            for score_data in result.data:
                score = score_data['overall_score']
                if score >= 90:
                    ranges['Excellent (90-100)'] += 1
                elif score >= 75:
                    ranges['Good (75-89)'] += 1
                elif score >= 60:
                    ranges['Fair (60-74)'] += 1
                elif score >= 40:
                    ranges['Poor (40-59)'] += 1
                else:
                    ranges['Critical (0-39)'] += 1
            
            return [{'health_level': k, 'count': v} for k, v in ranges.items()]
        except:
            return []
    
    def get_average_financial_metrics(self):
        """Get average financial metrics"""
        try:
            result = self.supabase.table('financial_profiles').select('monthly_income, fixed_expenses, variable_expenses, total_debt').execute()
            if not result.data:
                return {}
            
            total_income = sum(float(p['monthly_income']) for p in result.data)
            total_expenses = sum(float(p['fixed_expenses']) + float(p['variable_expenses']) for p in result.data)
            total_debt = sum(float(p['total_debt']) for p in result.data)
            count = len(result.data)
            
            return {
                'avg_income': total_income / count,
                'avg_savings_rate': ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0,
                'avg_debt_ratio': (total_debt / total_income) if total_income > 0 else 0
            }
        except:
            return {}
    
    def check_database_status(self):
        """Check database connection status"""
        try:
            result = self.supabase.table('users').select('id').limit(1).execute()
            return True
        except:
            return False
    
    def check_external_services(self):
        """Check external service connections"""
        services = {
            'Supabase': self.check_database_status(),
            'Stripe': False,  # Would need to implement
            'OpenAI': False,  # Would need to implement
            'SendGrid': False  # Would need to implement
        }
        return services

def main():
    """Main function to run admin dashboard"""
    dashboard = AdminDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
