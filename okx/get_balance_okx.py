import ccxt
import pandas as pd
from datetime import datetime

def get_okx_balance(api_key, secret_key, passphrase):
    """
    Get spot and futures balance from OKX exchange
    
    Args:
        api_key (str): Your OKX API key
        secret_key (str): Your OKX secret key
        passphrase (str): Your OKX API passphrase
    
    Returns:
        tuple: (spot_balance_df, futures_balance_df)
    """
    # Initialize OKX exchange
    exchange = ccxt.okx({
        'apiKey': api_key,
        'secret': secret_key,
        'password': passphrase,
        'enableRateLimit': True,
    })
    
    # Get spot balance
    spot_balance = exchange.fetch_balance()
    spot_assets = []
    for currency, balance in spot_balance['total'].items():
        if balance > 0:
            spot_assets.append({
                'Currency': currency,
                'Total Balance': balance,
                'Available': spot_balance['free'][currency],
                'In Orders': spot_balance['used'][currency]
            })
    
    spot_balance_df = pd.DataFrame(spot_assets)
    
    # Get futures balance
    futures_balance = exchange.fetch_balance({'type': 'futures'})
    futures_assets = []
    for currency, balance in futures_balance['total'].items():
        if balance > 0:
            futures_assets.append({
                'Currency': currency,
                'Total Balance': balance,
                'Available': futures_balance['free'][currency],
                'In Orders': futures_balance['used'][currency]
            })
    
    futures_balance_df = pd.DataFrame(futures_assets)
    
    return spot_balance_df, futures_balance_df

if __name__ == "__main__":
    # Replace with your API credentials
    API_KEY = "your_api_key"
    SECRET_KEY = "your_secret_key"
    PASSPHRASE = "your_passphrase"
    
    try:
        spot_balance, futures_balance = get_okx_balance(API_KEY, SECRET_KEY, PASSPHRASE)
        
        print("\n=== Spot Account Balance ===")
        print(spot_balance)
        
        print("\n=== Futures Account Balance ===")
        print(futures_balance)
        
    except Exception as e:
        print(f"Error: {str(e)}")
