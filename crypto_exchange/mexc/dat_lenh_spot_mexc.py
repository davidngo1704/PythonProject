import hmac
import hashlib
import time
import requests
import json
from typing import Optional, Dict, Any

class MEXCSpotAPI:
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize MEXC Spot API client
        
        Args:
            api_key (str): Your MEXC API key
            api_secret (str): Your MEXC API secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.mexc.com"
        
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """
        Generate HMAC SHA256 signature for API requests
        
        Args:
            params (dict): Request parameters
            
        Returns:
            str: Generated signature
        """
        query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
        
    def _get_headers(self, params: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate headers for API requests
        
        Args:
            params (dict): Request parameters
            
        Returns:
            dict: Headers for the request
        """
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self._generate_signature(params)
        return {
            'Content-Type': 'application/json',
            'X-MEXC-APIKEY': self.api_key
        }
        
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Place a spot order on MEXC
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): Order side ('BUY' or 'SELL')
            order_type (str): Order type ('LIMIT' or 'MARKET')
            quantity (float): Order quantity
            price (float, optional): Order price (required for LIMIT orders)
            
        Returns:
            dict: Order response from MEXC
        """
        endpoint = "/api/v3/order"
        url = f"{self.base_url}{endpoint}"
        
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }
        
        if order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            params['price'] = price
            
        headers = self._get_headers(params)
        
        try:
            response = requests.post(
                url,
                params=params,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error placing order: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Replace with your actual API credentials
    API_KEY = "your_api_key"
    API_SECRET = "your_api_secret"
    
    # Initialize the API client
    mexc = MEXCSpotAPI(API_KEY, API_SECRET)
    
    # Example: Place a limit buy order for 0.001 BTC at $50,000
    order = mexc.place_order(
        symbol="BTCUSDT",
        side="BUY",
        order_type="LIMIT",
        quantity=0.001,
        price=50000
    )
    
    if order:
        print("Order placed successfully:")
        print(json.dumps(order, indent=2))
    else:
        print("Failed to place order")
