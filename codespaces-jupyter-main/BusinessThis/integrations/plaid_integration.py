"""
Plaid integration for BusinessThis
"""
import plaid
from plaid.api import plaid_api
import os
from typing import Dict, Any, Optional, List

class PlaidIntegration:
    """Plaid bank integration"""
    
    def __init__(self):
        configuration = plaid.Configuration(
            host=plaid.Environment[os.getenv('PLAID_ENV', 'sandbox')],
            api_key={
                'clientId': os.getenv('PLAID_CLIENT_ID'),
                'secret': os.getenv('PLAID_SECRET')
            }
        )
        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)
    
    def create_link_token(self, user_id: str) -> Optional[str]:
        """Create Plaid link token"""
        try:
            request = plaid.LinkTokenCreateRequest(
                user=plaid.LinkTokenCreateRequestUser(client_user_id=user_id),
                client_name="BusinessThis",
                products=['transactions', 'accounts'],
                country_codes=['US'],
                language='en'
            )
            response = self.client.link_token_create(request)
            return response['link_token']
        except Exception as e:
            print(f"Error creating link token: {e}")
            return None
    
    def exchange_public_token(self, public_token: str) -> Optional[str]:
        """Exchange public token for access token"""
        try:
            request = plaid.ItemPublicTokenExchangeRequest(public_token=public_token)
            response = self.client.item_public_token_exchange(request)
            return response['access_token']
        except Exception as e:
            print(f"Error exchanging public token: {e}")
            return None
    
    def get_accounts(self, access_token: str) -> List[Dict[str, Any]]:
        """Get user's bank accounts"""
        try:
            request = plaid.AccountsGetRequest(access_token=access_token)
            response = self.client.accounts_get(request)
            return response['accounts']
        except Exception as e:
            print(f"Error getting accounts: {e}")
            return []
    
    def get_transactions(self, access_token: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get user's transactions"""
        try:
            request = plaid.TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date,
                end_date=end_date
            )
            response = self.client.transactions_get(request)
            return response['transactions']
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []
