import requests
import time
import hmac
import hashlib
import json
from typing import Optional, Dict, Any

class BitgetFuturesAPI:
    def __init__(self, api_key: str, api_secret: str, passphrase: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.base_url = "https://api.bitget.com"
        self.futures_url = f"{self.base_url}/api/mix/v1"

    def _generate_signature(self, timestamp: str, method: str, endpoint: str, body: str = "") -> str:
        message = timestamp + method + endpoint + body
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

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

    def place_market_order(
        self,
        symbol: str,
        side: str,
        size: float,
        margin_mode: str = "isolated",
        reduce_only: bool = False
    ) -> Dict[str, Any]:
        """
        Place a market order for futures trading
        
        Args:
            symbol: Trading pair (e.g., "BTCUSDT_UMCBL")
            side: "buy" or "sell"
            size: Order size
            margin_mode: "isolated" or "cross"
            reduce_only: Whether the order is reduce-only
        
        Returns:
            Order response from Bitget
        """
        endpoint = "/order/placeOrder"
        url = f"{self.futures_url}{endpoint}"
        
        body = {
            "symbol": symbol,
            "marginMode": margin_mode,
            "side": side,
            "orderType": "market",
            "size": str(size),
            "reduceOnly": reduce_only
        }
        
        headers = self._get_headers("POST", endpoint, json.dumps(body))
        response = requests.post(url, headers=headers, json=body)
        return response.json()

    def place_limit_order(
        self,
        symbol: str,
        side: str,
        size: float,
        price: float,
        margin_mode: str = "isolated",
        reduce_only: bool = False
    ) -> Dict[str, Any]:
        """
        Place a limit order for futures trading
        
        Args:
            symbol: Trading pair (e.g., "BTCUSDT_UMCBL")
            side: "buy" or "sell"
            size: Order size
            price: Order price
            margin_mode: "isolated" or "cross"
            reduce_only: Whether the order is reduce-only
        
        Returns:
            Order response from Bitget
        """
        endpoint = "/order/placeOrder"
        url = f"{self.futures_url}{endpoint}"
        
        body = {
            "symbol": symbol,
            "marginMode": margin_mode,
            "side": side,
            "orderType": "limit",
            "size": str(size),
            "price": str(price),
            "reduceOnly": reduce_only
        }
        
        headers = self._get_headers("POST", endpoint, json.dumps(body))
        response = requests.post(url, headers=headers, json=body)
        return response.json()

    def place_stop_order(
        self,
        symbol: str,
        side: str,
        size: float,
        trigger_price: float,
        margin_mode: str = "isolated",
        reduce_only: bool = False
    ) -> Dict[str, Any]:
        """
        Place a stop order for futures trading
        
        Args:
            symbol: Trading pair (e.g., "BTCUSDT_UMCBL")
            side: "buy" or "sell"
            size: Order size
            trigger_price: Price at which the order will be triggered
            margin_mode: "isolated" or "cross"
            reduce_only: Whether the order is reduce-only
        
        Returns:
            Order response from Bitget
        """
        endpoint = "/order/placeOrder"
        url = f"{self.futures_url}{endpoint}"
        
        body = {
            "symbol": symbol,
            "marginMode": margin_mode,
            "side": side,
            "orderType": "market",
            "size": str(size),
            "triggerPrice": str(trigger_price),
            "triggerType": "market_price",
            "reduceOnly": reduce_only
        }
        
        headers = self._get_headers("POST", endpoint, json.dumps(body))
        response = requests.post(url, headers=headers, json=body)
        return response.json()

    def cancel_order(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """
        Cancel an existing order
        
        Args:
            symbol: Trading pair (e.g., "BTCUSDT_UMCBL")
            order_id: ID of the order to cancel
        
        Returns:
            Cancellation response from Bitget
        """
        endpoint = "/order/cancel-order"
        url = f"{self.futures_url}{endpoint}"
        
        body = {
            "symbol": symbol,
            "orderId": order_id
        }
        
        headers = self._get_headers("POST", endpoint, json.dumps(body))
        response = requests.post(url, headers=headers, json=body)
        return response.json()

    def get_order_status(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """
        Get the status of an order
        
        Args:
            symbol: Trading pair (e.g., "BTCUSDT_UMCBL")
            order_id: ID of the order to check
        
        Returns:
            Order status from Bitget
        """
        endpoint = "/order/detail"
        url = f"{self.futures_url}{endpoint}"
        
        params = {
            "symbol": symbol,
            "orderId": order_id
        }
        
        headers = self._get_headers("GET", endpoint)
        response = requests.get(url, headers=headers, params=params)
        return response.json()
