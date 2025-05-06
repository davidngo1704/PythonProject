import requests
import time
import hmac
import hashlib
import json
from typing import Dict, Optional, Union

class MEXCFuturesAPI:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://contract.mexc.com"
        
    def _generate_signature(self, params: Dict) -> str:
        """Generate HMAC SHA256 signature for API requests"""
        query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _get_headers(self, params: Dict) -> Dict:
        """Generate headers for API requests"""
        timestamp = str(int(time.time() * 1000))
        params['timestamp'] = timestamp
        signature = self._generate_signature(params)
        
        return {
            'ApiKey': self.api_key,
            'Request-Time': timestamp,
            'Signature': signature,
            'Content-Type': 'application/json'
        }

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        leverage: Optional[int] = None,
        position_mode: str = "isolated"
    ) -> Dict:
        """
        Place a futures order on MEXC
        
        Args:
            symbol: Trading pair (e.g., "BTC_USDT")
            side: "BUY" or "SELL"
            order_type: "LIMIT" or "MARKET"
            quantity: Order quantity
            price: Price for limit orders
            leverage: Leverage value (1-125)
            position_mode: "isolated" or "cross"
            
        Returns:
            Dict containing order response
        """
        endpoint = "/api/v1/private/order/submit"
        url = f"{self.base_url}{endpoint}"
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "volume": str(quantity),
            "position_mode": position_mode
        }
        
        if price is not None:
            params["price"] = str(price)
            
        if leverage is not None:
            params["leverage"] = str(leverage)
            
        headers = self._get_headers(params)
        
        try:
            response = requests.post(url, headers=headers, json=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error placing order: {e}")
            return {"error": str(e)}

    def get_order_status(self, order_id: str, symbol: str) -> Dict:
        """
        Get status of a specific order
        
        Args:
            order_id: Order ID to check
            symbol: Trading pair
            
        Returns:
            Dict containing order status
        """
        endpoint = "/api/v1/private/order/get"
        url = f"{self.base_url}{endpoint}"
        
        params = {
            "order_id": order_id,
            "symbol": symbol
        }
        
        headers = self._get_headers(params)
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting order status: {e}")
            return {"error": str(e)}

    def cancel_order(self, order_id: str, symbol: str) -> Dict:
        """
        Cancel a specific order
        
        Args:
            order_id: Order ID to cancel
            symbol: Trading pair
            
        Returns:
            Dict containing cancellation response
        """
        endpoint = "/api/v1/private/order/cancel"
        url = f"{self.base_url}{endpoint}"
        
        params = {
            "order_id": order_id,
            "symbol": symbol
        }
        
        headers = self._get_headers(params)
        
        try:
            response = requests.post(url, headers=headers, json=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error canceling order: {e}")
            return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    # Replace with your actual API credentials
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"
    
    # Initialize the API client
    mexc = MEXCFuturesAPI(api_key, api_secret)
    
    # Example: Place a limit order
    order_response = mexc.place_order(
        symbol="BTC_USDT",
        side="BUY",
        order_type="LIMIT",
        quantity=0.01,
        price=30000,
        leverage=10
    )
    print("Order Response:", order_response)
    
    # Example: Check order status
    if "order_id" in order_response:
        status = mexc.get_order_status(
            order_id=order_response["order_id"],
            symbol="BTC_USDT"
        )
        print("Order Status:", status)
