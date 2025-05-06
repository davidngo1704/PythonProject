from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Bybit client
def get_bybit_client():
    api_key = os.getenv('BYBIT_API_KEY')
    api_secret = os.getenv('BYBIT_API_SECRET')
    return HTTP(
        testnet=False,
        api_key=api_key,
        api_secret=api_secret
    )

def get_spot_balance():
    """Get spot account balance"""
    try:
        client = get_bybit_client()
        response = client.get_wallet_balance(accountType="SPOT")
        if response['retCode'] == 0:
            balances = response['result']['list'][0]['coin']
            print("\n=== Spot Account Balance ===")
            for coin in balances:
                if float(coin['walletBalance']) > 0:
                    print(f"{coin['coin']}: {coin['walletBalance']}")
        else:
            print(f"Error getting spot balance: {response['retMsg']}")
    except Exception as e:
        print(f"Error: {str(e)}")

def get_futures_balance():
    """Get futures account balance"""
    try:
        client = get_bybit_client()
        response = client.get_wallet_balance(accountType="CONTRACT")
        if response['retCode'] == 0:
            balances = response['result']['list'][0]['coin']
            print("\n=== Futures Account Balance ===")
            for coin in balances:
                if float(coin['walletBalance']) > 0:
                    print(f"{coin['coin']}: {coin['walletBalance']}")
        else:
            print(f"Error getting futures balance: {response['retMsg']}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    get_spot_balance()
    get_futures_balance()
