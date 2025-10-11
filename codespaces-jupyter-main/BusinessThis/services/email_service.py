"""
Email service for BusinessThis
Handles SendGrid integration, automated email sequences, and newsletters
"""
import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, TemplateId, DynamicTemplateData
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

class EmailService:
    """Email service for marketing and notifications"""
    
    def __init__(self):
        self.sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        if self.sendgrid_api_key:
            self.sg = sendgrid.SendGridAPIClient(api_key=self.sendgrid_api_key)
        else:
            self.sg = None
            print("Warning: SendGrid API key not found")
        
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@businessthis.com')
    
    def send_welcome_email(self, user_email: str, user_name: str) -> Dict[str, Any]:
        """Send welcome email to new users"""
        try:
            if not self.sg:
                return {'error': 'Email service not configured'}
            
            message = Mail(
                from_email=Email(self.from_email, "BusinessThis Team"),
                to_emails=To(user_email),
                subject="Welcome to BusinessThis! 🎉",
                html_content=self._get_welcome_email_html(user_name)
            )
            
            response = self.sg.send(message)
            
            return {
                'success': True,
                'status_code': response.status_code,
                'message': 'Welcome email sent successfully'
            }
            
        except Exception as e:
            return {'error': f'Failed to send welcome email: {str(e)}'}
    
    def send_onboarding_sequence(self, user_email: str, user_name: str, 
                                financial_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Send onboarding email sequence"""
        try:
            if not self.sg:
                return {'error': 'Email service not configured'}
            
            # Day 1: Welcome and setup
            self._send_onboarding_email(user_email, user_name, 1)
            
            # Day 3: Financial profile completion
            self._send_onboarding_email(user_email, user_name, 3)
            
            # Day 7: First goal setting
            self._send_onboarding_email(user_email, user_name, 7)
            
            # Day 14: Advanced features
            self._send_onboarding_email(user_email, user_name, 14)
            
            return {'success': True, 'message': 'Onboarding sequence initiated'}
            
        except Exception as e:
            return {'error': f'Failed to send onboarding sequence: {str(e)}'}
    
    def send_weekly_newsletter(self, user_email: str, user_name: str, 
                              financial_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Send weekly financial newsletter"""
        try:
            if not self.sg:
                return {'error': 'Email service not configured'}
            
            message = Mail(
                from_email=Email(self.from_email, "BusinessThis Team"),
                to_emails=To(user_email),
                subject="Your Weekly Financial Update 📊",
                html_content=self._get_newsletter_html(user_name, financial_summary)
            )
            
            response = self.sg.send(message)
            
            return {
                'success': True,
                'status_code': response.status_code,
                'message': 'Newsletter sent successfully'
            }
            
        except Exception as e:
            return {'error': f'Failed to send newsletter: {str(e)}'}
    
    def send_goal_achievement_email(self, user_email: str, user_name: str, 
                                   goal_name: str, goal_amount: float) -> Dict[str, Any]:
        """Send goal achievement celebration email"""
        try:
            if not self.sg:
                return {'error': 'Email service not configured'}
            
            message = Mail(
                from_email=Email(self.from_email, "BusinessThis Team"),
                to_emails=To(user_email),
                subject="🎉 Congratulations! You've achieved your goal!",
                html_content=self._get_goal_achievement_html(user_name, goal_name, goal_amount)
            )
            
            response = self.sg.send(message)
            
            return {
                'success': True,
                'status_code': response.status_code,
                'message': 'Goal achievement email sent successfully'
            }
            
        except Exception as e:
            return {'error': f'Failed to send goal achievement email: {str(e)}'}
    
    def send_subscription_upgrade_email(self, user_email: str, user_name: str, 
                                       new_tier: str) -> Dict[str, Any]:
        """Send subscription upgrade confirmation email"""
        try:
            if not self.sg:
                return {'error': 'Email service not configured'}
            
            message = Mail(
                from_email=Email(self.from_email, "BusinessThis Team"),
                to_emails=To(user_email),
                subject=f"Welcome to BusinessThis {new_tier.title()}! 🚀",
                html_content=self._get_upgrade_email_html(user_name, new_tier)
            )
            
            response = self.sg.send(message)
            
            return {
                'success': True,
                'status_code': response.status_code,
                'message': 'Upgrade email sent successfully'
            }
            
        except Exception as e:
            return {'error': f'Failed to send upgrade email: {str(e)}'}
    
    def send_daily_tip_email(self, user_email: str, user_name: str, 
                            tip: str, tip_category: str) -> Dict[str, Any]:
        """Send daily financial tip email"""
        try:
            if not self.sg:
                return {'error': 'Email service not configured'}
            
            message = Mail(
                from_email=Email(self.from_email, "BusinessThis Team"),
                to_emails=To(user_email),
                subject=f"💡 Daily Financial Tip: {tip_category}",
                html_content=self._get_daily_tip_html(user_name, tip, tip_category)
            )
            
            response = self.sg.send(message)
            
            return {
                'success': True,
                'status_code': response.status_code,
                'message': 'Daily tip email sent successfully'
            }
            
        except Exception as e:
            return {'error': f'Failed to send daily tip email: {str(e)}'}
    
    def send_engagement_email(self, user_email: str, user_name: str, 
                             days_since_last_login: int) -> Dict[str, Any]:
        """Send re-engagement email to inactive users"""
        try:
            if not self.sg:
                return {'error': 'Email service not configured'}
            
            if days_since_last_login < 7:
                return {'message': 'User is still active, no engagement email needed'}
            
            message = Mail(
                from_email=Email(self.from_email, "BusinessThis Team"),
                to_emails=To(user_email),
                subject="We miss you! Let's get back on track 💪",
                html_content=self._get_engagement_email_html(user_name, days_since_last_login)
            )
            
            response = self.sg.send(message)
            
            return {
                'success': True,
                'status_code': response.status_code,
                'message': 'Engagement email sent successfully'
            }
            
        except Exception as e:
            return {'error': f'Failed to send engagement email: {str(e)}'}
    
    def _send_onboarding_email(self, user_email: str, user_name: str, day: int):
        """Send specific onboarding email"""
        subjects = {
            1: "Welcome to BusinessThis! Let's get started 🚀",
            3: "Complete your financial profile for better insights 📊",
            7: "Set your first savings goal and start building wealth 💰",
            14: "Unlock advanced features with BusinessThis Premium ⭐"
        }
        
        subject = subjects.get(day, "Your BusinessThis Journey Continues")
        
        message = Mail(
            from_email=Email(self.from_email, "BusinessThis Team"),
            to_emails=To(user_email),
            subject=subject,
            html_content=self._get_onboarding_email_html(user_name, day)
        )
        
        self.sg.send(message)
    
    def _get_welcome_email_html(self, user_name: str) -> str:
        """Generate welcome email HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Welcome to BusinessThis</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #1e3a8a; text-align: center;">Welcome to BusinessThis! 🎉</h1>
                
                <p>Hi {user_name},</p>
                
                <p>Welcome to BusinessThis, your personal financial planning assistant! We're excited to help you take control of your finances and achieve your financial goals.</p>
                
                <h2 style="color: #1e3a8a;">What you can do with BusinessThis:</h2>
                <ul>
                    <li>📊 Calculate your safe daily spending amount</li>
                    <li>🎯 Set and track multiple savings goals</li>
                    <li>🏥 Get your financial health score</li>
                    <li>💰 Plan for retirement and investments</li>
                    <li>🤖 Get AI-powered financial coaching</li>
                </ul>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://businessthis.com/dashboard" 
                       style="background: #1e3a8a; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        Get Started Now
                    </a>
                </div>
                
                <p>If you have any questions, feel free to reach out to our support team.</p>
                
                <p>Best regards,<br>The BusinessThis Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_newsletter_html(self, user_name: str, financial_summary: Dict[str, Any]) -> str:
        """Generate newsletter HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Weekly Financial Update</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #1e3a8a; text-align: center;">Your Weekly Financial Update 📊</h1>
                
                <p>Hi {user_name},</p>
                
                <p>Here's your weekly financial summary:</p>
                
                <div style="background: #f8fafc; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #1e3a8a;">This Week's Highlights</h3>
                    <ul>
                        <li>Monthly Income: ${financial_summary.get('monthly_income', 0):,.2f}</li>
                        <li>Monthly Expenses: ${financial_summary.get('monthly_expenses', 0):,.2f}</li>
                        <li>Monthly Savings: ${financial_summary.get('monthly_savings', 0):,.2f}</li>
                        <li>Savings Rate: {financial_summary.get('savings_rate', 0):.1f}%</li>
                    </ul>
                </div>
                
                <h3 style="color: #1e3a8a;">Key Insights</h3>
                <ul>
                    {''.join([f'<li>{insight}</li>' for insight in financial_summary.get('insights', [])])}
                </ul>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://businessthis.com/dashboard" 
                       style="background: #1e3a8a; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        View Full Dashboard
                    </a>
                </div>
                
                <p>Keep up the great work with your financial goals!</p>
                
                <p>Best regards,<br>The BusinessThis Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_goal_achievement_html(self, user_name: str, goal_name: str, goal_amount: float) -> str:
        """Generate goal achievement email HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Goal Achievement</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #1e3a8a; text-align: center;">🎉 Congratulations! 🎉</h1>
                
                <p>Hi {user_name},</p>
                
                <p>Amazing news! You've successfully achieved your savings goal:</p>
                
                <div style="background: #f0f9ff; padding: 20px; border-radius: 5px; margin: 20px 0; text-align: center;">
                    <h2 style="color: #1e3a8a; margin: 0;">{goal_name}</h2>
                    <p style="font-size: 24px; font-weight: bold; color: #059669; margin: 10px 0;">${goal_amount:,.2f}</p>
                </div>
                
                <p>This is a significant milestone in your financial journey. Your dedication and discipline have paid off!</p>
                
                <h3 style="color: #1e3a8a;">What's Next?</h3>
                <ul>
                    <li>Set a new savings goal to keep the momentum going</li>
                    <li>Consider investing your savings for long-term growth</li>
                    <li>Celebrate this achievement (responsibly!)</li>
                </ul>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://businessthis.com/goals" 
                       style="background: #1e3a8a; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        Set Your Next Goal
                    </a>
                </div>
                
                <p>Keep up the excellent work!</p>
                
                <p>Best regards,<br>The BusinessThis Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_upgrade_email_html(self, user_name: str, new_tier: str) -> str:
        """Generate upgrade email HTML"""
        tier_features = {
            'premium': [
                '5 savings goals',
                'Advanced analytics',
                'PDF exports',
                'AI financial coaching',
                'Email notifications'
            ],
            'pro': [
                'Unlimited savings goals',
                'Full AI access',
                'Investment tracking',
                'API access',
                'White-label options'
            ]
        }
        
        features = tier_features.get(new_tier, [])
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Welcome to {new_tier.title()}</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #1e3a8a; text-align: center;">Welcome to BusinessThis {new_tier.title()}! 🚀</h1>
                
                <p>Hi {user_name},</p>
                
                <p>Thank you for upgrading to BusinessThis {new_tier.title()}! You now have access to powerful features that will help you achieve your financial goals faster.</p>
                
                <h2 style="color: #1e3a8a;">Your New Features:</h2>
                <ul>
                    {''.join([f'<li>✅ {feature}</li>' for feature in features])}
                </ul>
                
                <div style="background: #f0f9ff; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #1e3a8a; margin-top: 0;">Pro Tip</h3>
                    <p>Make the most of your {new_tier.title()} subscription by exploring all the advanced features. Our AI coach is ready to provide personalized financial advice!</p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://businessthis.com/dashboard" 
                       style="background: #1e3a8a; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        Explore Your New Features
                    </a>
                </div>
                
                <p>If you have any questions about your new features, our support team is here to help!</p>
                
                <p>Best regards,<br>The BusinessThis Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_daily_tip_html(self, user_name: str, tip: str, tip_category: str) -> str:
        """Generate daily tip email HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Daily Financial Tip</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #1e3a8a; text-align: center;">💡 Daily Financial Tip</h1>
                
                <p>Hi {user_name},</p>
                
                <div style="background: #f0f9ff; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #1e3a8a; margin-top: 0;">Today's Focus: {tip_category}</h3>
                    <p style="font-size: 16px; margin: 0;">{tip}</p>
                </div>
                
                <p>Small daily actions lead to big financial improvements over time. Keep up the great work!</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://businessthis.com/dashboard" 
                       style="background: #1e3a8a; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        Track Your Progress
                    </a>
                </div>
                
                <p>Best regards,<br>The BusinessThis Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_engagement_email_html(self, user_name: str, days_since_last_login: int) -> str:
        """Generate engagement email HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>We Miss You</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #1e3a8a; text-align: center;">We Miss You! 💪</h1>
                
                <p>Hi {user_name},</p>
                
                <p>We noticed you haven't logged into BusinessThis in {days_since_last_login} days. Your financial goals are waiting for you!</p>
                
                <div style="background: #f0f9ff; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #1e3a8a; margin-top: 0;">Quick Check-in</h3>
                    <p>Just 5 minutes can help you:</p>
                    <ul>
                        <li>Update your financial profile</li>
                        <li>Check your savings goal progress</li>
                        <li>Get your latest financial health score</li>
                        <li>Receive personalized recommendations</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://businessthis.com/dashboard" 
                       style="background: #1e3a8a; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        Get Back on Track
                    </a>
                </div>
                
                <p>Your financial future is worth the investment. Let's get back to building your wealth!</p>
                
                <p>Best regards,<br>The BusinessThis Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_onboarding_email_html(self, user_name: str, day: int) -> str:
        """Generate onboarding email HTML"""
        content = {
            1: {
                'title': 'Welcome to BusinessThis! Let\'s get started 🚀',
                'content': 'Welcome to your financial planning journey! Let\'s start by setting up your financial profile.',
                'cta': 'Complete Your Profile',
                'link': 'https://businessthis.com/profile'
            },
            3: {
                'title': 'Complete your financial profile for better insights 📊',
                'content': 'Your financial profile helps us provide personalized recommendations and accurate calculations.',
                'cta': 'Update Your Profile',
                'link': 'https://businessthis.com/profile'
            },
            7: {
                'title': 'Set your first savings goal and start building wealth 💰',
                'content': 'Goals give you direction and motivation. Let\'s set your first savings target!',
                'cta': 'Set Your First Goal',
                'link': 'https://businessthis.com/goals'
            },
            14: {
                'title': 'Unlock advanced features with BusinessThis Premium ⭐',
                'content': 'Ready for more? Upgrade to Premium for advanced analytics, AI coaching, and unlimited goals.',
                'cta': 'Upgrade to Premium',
                'link': 'https://businessthis.com/upgrade'
            }
        }
        
        email_content = content.get(day, content[1])
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{email_content['title']}</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #1e3a8a; text-align: center;">{email_content['title']}</h1>
                
                <p>Hi {user_name},</p>
                
                <p>{email_content['content']}</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{email_content['link']}" 
                       style="background: #1e3a8a; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        {email_content['cta']}
                    </a>
                </div>
                
                <p>Best regards,<br>The BusinessThis Team</p>
            </div>
        </body>
        </html>
        """
