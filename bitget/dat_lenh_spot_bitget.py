import requests
import time
import hmac
import hashlib
import base64
import json
from typing import Optional, Dict, Any

class BitgetSpotAPI:
    def __init__(self, api_key: str, api_secret: str, passphrase: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.base_url = "https://api.bitget.com"
        
    def _generate_signature(self, timestamp: str, method: str, endpoint: str, body: str = "") -> str:
        message = timestamp + method.upper() + endpoint + body
        mac = hmac.new(
            bytes(self.api_secret, 'utf-8'),
            bytes(message, 'utf-8'),
            hashlib.sha256
        )
        return base64.b64encode(mac.digest()).decode('utf-8')
    
    def _get_headers(self, method: str, endpoint: str, body: str = "") -> Dict[str, str]:
        timestamp = str(int(time.time() * 1000))
        signature = self._generate_signature(timestamp, method, endpoint, body)
        
        return {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        size: float,
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Place a spot order on Bitget
        
        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            side: "buy" or "sell"
            order_type: "limit" or "market"
            size: Order size
            price: Price for limit orders (required for limit orders)
            
        Returns:
            Dict containing order response
        """
        endpoint = "/api/spot/v1/trade/orders"
        url = self.base_url + endpoint
        
        order_data = {
            "symbol": symbol,
            "side": side,
            "orderType": order_type,
            "force": "normal",
            "size": str(size)
        }
        
        if order_type == "limit":
            if price is None:
                raise ValueError("Price is required for limit orders")
            order_data["price"] = str(price)
        
        body = json.dumps(order_data)
        headers = self._get_headers("POST", endpoint, body)
        
        response = requests.post(url, headers=headers, data=body)
        return response.json()
    
    def get_order_status(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """
        Get the status of an order
        
        Args:
            order_id: Order ID to check
            symbol: Trading pair (e.g., "BTCUSDT")
            
        Returns:
            Dict containing order status
        """
        endpoint = f"/api/spot/v1/trade/orderInfo?orderId={order_id}&symbol={symbol}"
        url = self.base_url + endpoint
        
        headers = self._get_headers("GET", endpoint)
        response = requests.get(url, headers=headers)
        return response.json()

# Example usage
if __name__ == "__main__":
    # Replace with your actual API credentials
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"
    passphrase = "YOUR_PASSPHRASE"
    
    # Initialize the API client
    client = BitgetSpotAPI(api_key, api_secret, passphrase)
    
    try:
        # Example: Place a limit buy order for 0.001 BTC at $30,000
        order_response = client.place_order(
            symbol="BTCUSDT",
            side="buy",
            order_type="limit",
            size=0.001,
            price=30000
        )
        print("Order placed:", order_response)
        
        # Example: Place a market sell order for 0.001 BTC
        market_order = client.place_order(
            symbol="BTCUSDT",
            side="sell",
            order_type="market",
            size=0.001
        )
        print("Market order placed:", market_order)
        
    except Exception as e:
        print(f"Error placing order: {str(e)}")
