import os
from dotenv import load_dotenv

load_dotenv()

def get_plaid_access_token():
    return os.getenv('PLAID_ACCESS_TOKEN')

def set_plaid_access_token(token):
    # TODO
    return None
