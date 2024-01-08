import plaid
from plaid.api import plaid_api
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Removed from main

# from plaid_services import PlaidServices
# from token_util import get_plaid_access_token, set_plaid_access_token

    # plaid_service = PlaidServices()

    # access_token = get_plaid_access_token()

    # if not access_token:
    #     email_service.send_email("your_email@example.com", "Re-authentication Required", 
    #                              "Please re-authenticate to obtain a new Plaid access token.")
    #     return

    # try:
    #     balances = plaid_service.get_account_balances(access_token)
    #     transactions = plaid_service.get_transactions(access_token)
    #     report = f"Balances: {balances}\nTransactions: {transactions}"
    #     email_service.send_email("your_email@example.com", "Daily Financial Report", "Your daily financial report is attached.", report)
    # except Exception as e:
    #     email_service.send_email("your_email@example.com", "Error", 
    #                              f"Failed to fetch data: {e}. Please re-authenticate.")
    #     set_plaid_access_token(None)


class PlaidServices:
    def __init__(self):
        self.client_id = os.getenv('PLAID_CLIENT_ID')
        self.secret = os.getenv('PLAID_SECRET')
        self.environment = plaid.Environment.Sandbox  # Change as needed

        configuration = plaid.Configuration(
            host=self.environment,
            api_key={
                'clientId': self.client_id,
                'secret': self.secret,
            }
        )
        self.client = plaid.ApiClient(configuration)
        self.api = plaid_api.PlaidApi(self.client)

    def create_link_token(self, user_id):
        request = plaid.LinkTokenCreateRequest(
            user=plaid.LinkTokenCreateRequestUser(client_user_id=user_id),
            client_name='Your App Name',
            products=['transactions'],
            country_codes=['US'],
            language='en'
        )
        response = self.api.link_token_create(request)
        return response['link_token']

    def exchange_public_token(self, public_token):
        exchange_request = plaid.ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = self.api.item_public_token_exchange(exchange_request)
        return exchange_response['access_token']

    def get_account_balances(self, access_token):
        accounts_request = plaid.AccountsBalanceGetRequest(access_token=access_token)
        accounts_response = self.api.accounts_balance_get(accounts_request)
        return accounts_response['accounts']

    def get_transactions(self, access_token, days_past=30):
        start_date = (datetime.now() - timedelta(days=days_past)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')

        transactions_request = plaid.TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date
        )
        transactions_response = self.api.transactions_get(transactions_request)
        return transactions_response['transactions']

# Example usage
if __name__ == "__main__":
    plaid_services = PlaidServices()
    user_id = "custom_1"
    link_token = plaid_services.create_link_token(user_id)
    print("Link Token:", link_token)

    # Public token would normally be obtained from the front-end after user logs in
    # public_token = "obtained-from-frontend"
    # access_token = plaid_services.exchange_public_token(public_token)
    # print("Access Token:", access_token)

    # Example, assuming you have an access token
    # balances = plaid_services.get_account_balances(access_token)
    # transactions = plaid_services.get_transactions(access_token)
    # print("Balances:", balances)
    # print("Transactions:", transactions)
