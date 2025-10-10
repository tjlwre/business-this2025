"""
SendGrid integration for BusinessThis
"""
import sendgrid
from sendgrid.helpers.mail import Mail
import os
from typing import Dict, Any, Optional

class SendGridIntegration:
    """SendGrid email integration"""
    
    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@businessthis.com')
    
    def send_welcome_email(self, to_email: str, user_name: str) -> bool:
        """Send welcome email to new user"""
        try:
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject='Welcome to BusinessThis!',
                html_content=f"""
                <h1>Welcome to BusinessThis, {user_name}!</h1>
                <p>Thank you for joining our financial planning platform.</p>
                <p>Get started by setting up your financial profile and creating your first savings goal.</p>
                <p>Best regards,<br>The BusinessThis Team</p>
                """
            )
            response = self.sg.send(message)
            return response.status_code == 202
        except Exception as e:
            print(f"Error sending welcome email: {e}")
            return False
    
    def send_financial_tip(self, to_email: str, tip: str) -> bool:
        """Send financial tip email"""
        try:
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject='Your Daily Financial Tip',
                html_content=f"""
                <h2>Daily Financial Tip</h2>
                <p>{tip}</p>
                <p>Keep up the great work with your financial goals!</p>
                <p>Best regards,<br>The BusinessThis Team</p>
                """
            )
            response = self.sg.send(message)
            return response.status_code == 202
        except Exception as e:
            print(f"Error sending financial tip: {e}")
            return False
    
    def send_subscription_confirmation(self, to_email: str, plan_name: str) -> bool:
        """Send subscription confirmation email"""
        try:
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=f'Welcome to {plan_name}!',
                html_content=f"""
                <h1>Thank you for upgrading to {plan_name}!</h1>
                <p>You now have access to all premium features.</p>
                <p>Start exploring advanced analytics and AI-powered insights.</p>
                <p>Best regards,<br>The BusinessThis Team</p>
                """
            )
            response = self.sg.send(message)
            return response.status_code == 202
        except Exception as e:
            print(f"Error sending subscription confirmation: {e}")
            return False
