from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_spot_balance(client):
    """Get spot account balance"""
    try:
        account = client.get_account()
        balances = []
        
        for asset in account['balances']:
            free = float(asset['free'])
            locked = float(asset['locked'])
            total = free + locked
            
            if total > 0:  # Only show assets with balance
                balances.append({
                    'Asset': asset['asset'],
                    'Free': free,
                    'Locked': locked,
                    'Total': total
                })
        
        return pd.DataFrame(balances)
    except BinanceAPIException as e:
        print(f"Error getting spot balance: {e}")
        return None

def get_futures_balance(client):
    """Get futures account balance"""
    try:
        futures_account = client.futures_account_balance()
        balances = []
        
        for asset in futures_account:
            balance = float(asset['balance'])
            if balance > 0:  # Only show assets with balance
                balances.append({
                    'Asset': asset['asset'],
                    'Balance': balance
                })
        
        return pd.DataFrame(balances)
    except BinanceAPIException as e:
        print(f"Error getting futures balance: {e}")
        return None

def main():
    # Get API keys from environment variables
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        print("Please set BINANCE_API_KEY and BINANCE_API_SECRET in your .env file")
        return
    
    try:
        # Initialize Binance client
        client = Client(api_key, api_secret)
        
        print("\n=== Spot Account Balance ===")
        spot_balance = get_spot_balance(client)
        if spot_balance is not None and not spot_balance.empty:
            print(spot_balance.to_string(index=False))
        else:
            print("No spot balance found")
        
        print("\n=== Futures Account Balance ===")
        futures_balance = get_futures_balance(client)
        if futures_balance is not None and not futures_balance.empty:
            print(futures_balance.to_string(index=False))
        else:
            print("No futures balance found")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
