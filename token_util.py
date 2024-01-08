import os
from dotenv import load_dotenv

load_dotenv()

def get_plaid_access_token():
    return os.getenv('PLAID_ACCESS_TOKEN')

def set_plaid_access_token(token):
    # In a real-world scenario, you'd store this token in a more secure place
    # like a database or a secure environment variable system
    os.environ['PLAID_ACCESS_TOKEN'] = token
    # You should also update the .env file or your secure storage with the new token
