import requests
import time
import hmac
import hashlib
import json
from typing import Dict, Optional

class BybitSpotAPI:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api-testnet.bybit.com" if testnet else "https://api.bybit.com"
        
    def _generate_signature(self, params: Dict) -> str:
        """Generate signature for API request"""
        param_str = ""
        for key in sorted(params.keys()):
            param_str += f"{key}={params[key]}&"
        param_str = param_str[:-1]
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            param_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        qty: float,
        price: Optional[float] = None,
        time_in_force: str = "GTC"
    ) -> Dict:
        """
        Place a spot order on Bybit
        
        Args:
            symbol: Trading pair (e.g. "BTCUSDT")
            side: "Buy" or "Sell"
            order_type: "LIMIT" or "MARKET"
            qty: Order quantity
            price: Order price (required for LIMIT orders)
            time_in_force: Order time in force (default: "GTC")
            
        Returns:
            Dict containing order response
        """
        endpoint = "/spot/v3/private/order"
        timestamp = int(time.time() * 1000)
        
        params = {
            "api_key": self.api_key,
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "qty": str(qty),
            "timeInForce": time_in_force,
            "timestamp": timestamp
        }
        
        if order_type == "LIMIT" and price is not None:
            params["price"] = str(price)
            
        params["sign"] = self._generate_signature(params)
        
        response = requests.post(
            f"{self.base_url}{endpoint}",
            data=params
        )
        
        return response.json()

# Example usage
if __name__ == "__main__":
    # Replace with your actual API credentials
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"
    
    # Initialize API client
    client = BybitSpotAPI(api_key, api_secret, testnet=True)  # Set testnet=False for real trading
    
    # Example: Place a limit buy order for 0.001 BTC at $50,000
    try:
        response = client.place_order(
            symbol="BTCUSDT",
            side="Buy",
            order_type="LIMIT",
            qty=0.001,
            price=50000
        )
        print("Order response:", json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error placing order: {e}")
