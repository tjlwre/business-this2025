"""
PayPal integration for BusinessThis
"""
import paypalrestsdk
import os
from typing import Dict, Any, Optional

class PayPalIntegration:
    """PayPal payment integration"""
    
    def __init__(self):
        paypalrestsdk.configure({
            "mode": os.getenv('PAYPAL_MODE', 'sandbox'),
            "client_id": os.getenv('PAYPAL_CLIENT_ID'),
            "client_secret": os.getenv('PAYPAL_CLIENT_SECRET')
        })
    
    def create_subscription(self, plan_id: str, user_id: str) -> Optional[str]:
        """Create PayPal subscription"""
        try:
            subscription = paypalrestsdk.Subscription({
                "plan_id": plan_id,
                "subscriber": {
                    "email_address": "user@example.com"  # Get from user data
                },
                "custom_id": user_id
            })
            
            if subscription.create():
                return subscription.id
            return None
        except Exception as e:
            print(f"Error creating PayPal subscription: {e}")
            return None
    
    def cancel_subscription(self, subscription_id: str) -> bool:
        """Cancel PayPal subscription"""
        try:
            subscription = paypalrestsdk.Subscription.find(subscription_id)
            return subscription.cancel()
        except Exception as e:
            print(f"Error cancelling PayPal subscription: {e}")
            return False
