from bitget import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Bitget client
api_key = os.getenv('BITGET_API_KEY')
api_secret = os.getenv('BITGET_API_SECRET')
api_passphrase = os.getenv('BITGET_API_PASSPHRASE')

client = Client(api_key, api_secret, api_passphrase)

def get_spot_balance():
    """Get spot account balance"""
    try:
        # Get spot account assets
        response = client.get_account_assets('spot')
        print("\n=== Spot Account Balance ===")
        for asset in response['data']:
            if float(asset['available']) > 0 or float(asset['frozen']) > 0:
                print(f"Asset: {asset['coin']}")
                print(f"Available: {asset['available']}")
                print(f"Frozen: {asset['frozen']}")
                print(f"Total: {float(asset['available']) + float(asset['frozen'])}")
                print("------------------------")
    except Exception as e:
        print(f"Error getting spot balance: {e}")

def get_futures_balance():
    """Get futures account balance"""
    try:
        # Get futures account assets
        response = client.get_account_assets('futures')
        print("\n=== Futures Account Balance ===")
        for asset in response['data']:
            if float(asset['available']) > 0 or float(asset['frozen']) > 0:
                print(f"Asset: {asset['coin']}")
                print(f"Available: {asset['available']}")
                print(f"Frozen: {asset['frozen']}")
                print(f"Total: {float(asset['available']) + float(asset['frozen'])}")
                print("------------------------")
    except Exception as e:
        print(f"Error getting futures balance: {e}")

if __name__ == "__main__":
    get_spot_balance()
    get_futures_balance()
