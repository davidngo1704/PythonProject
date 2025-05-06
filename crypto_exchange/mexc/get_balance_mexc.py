import requests
import time
import hmac
import hashlib
import base64
from urllib.parse import urlencode

class MEXCAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.mexc.com"
        
    def _get_signature(self, params):
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def get_spot_balance(self):
        endpoint = "/api/v3/account"
        timestamp = int(time.time() * 1000)
        
        params = {
            "timestamp": timestamp
        }
        
        signature = self._get_signature(params)
        headers = {
            "X-MEXC-APIKEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        params["signature"] = signature
        url = f"{self.base_url}{endpoint}?{urlencode(params)}"
        
        response = requests.get(url, headers=headers)
        return response.json()

    def get_futures_balance(self):
        endpoint = "/api/v3/private/account"
        timestamp = int(time.time() * 1000)
        
        params = {
            "timestamp": timestamp
        }
        
        signature = self._get_signature(params)
        headers = {
            "X-MEXC-APIKEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        params["signature"] = signature
        url = f"{self.base_url}{endpoint}?{urlencode(params)}"
        
        response = requests.get(url, headers=headers)
        return response.json()

def main():
    # Replace with your actual API credentials
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"
    
    mexc = MEXCAPI(api_key, api_secret)
    
    try:
        # Get spot balance
        spot_balance = mexc.get_spot_balance()
        print("Spot Account Balance:")
        for asset in spot_balance.get('balances', []):
            if float(asset['free']) > 0 or float(asset['locked']) > 0:
                print(f"Asset: {asset['asset']}")
                print(f"Free: {asset['free']}")
                print(f"Locked: {asset['locked']}")
                print("---")
        
        # Get futures balance
        futures_balance = mexc.get_futures_balance()
        print("\nFutures Account Balance:")
        print(f"Total Wallet Balance: {futures_balance.get('totalWalletBalance', '0')}")
        print(f"Available Balance: {futures_balance.get('availableBalance', '0')}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
