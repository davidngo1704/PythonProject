from pybit.unified_trading import HTTP
import time
from typing import Optional, Literal

class BybitFuturesTrader:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        """
        Initialize the Bybit futures trader
        
        Args:
            api_key (str): Your Bybit API key
            api_secret (str): Your Bybit API secret
            testnet (bool): Whether to use testnet (default: False)
        """
        self.session = HTTP(
            testnet=testnet,
            api_key=api_key,
            api_secret=api_secret
        )
        
    def place_market_order(
        self,
        symbol: str,
        side: Literal["Buy", "Sell"],
        qty: float,
        reduce_only: bool = False,
        close_on_trigger: bool = False
    ) -> dict:
        """
        Place a market order
        
        Args:
            symbol (str): Trading pair (e.g. "BTCUSDT")
            side (str): "Buy" or "Sell"
            qty (float): Order quantity
            reduce_only (bool): Whether to reduce position only
            close_on_trigger (bool): Whether to close position on trigger
            
        Returns:
            dict: Order response from Bybit
        """
        try:
            response = self.session.place_order(
                category="linear",
                symbol=symbol,
                side=side,
                orderType="Market",
                qty=str(qty),
                reduceOnly=reduce_only,
                closeOnTrigger=close_on_trigger
            )
            return response
        except Exception as e:
            print(f"Error placing market order: {e}")
            return None
            
    def place_limit_order(
        self,
        symbol: str,
        side: Literal["Buy", "Sell"],
        qty: float,
        price: float,
        reduce_only: bool = False,
        close_on_trigger: bool = False,
        time_in_force: str = "GoodTillCancel"
    ) -> dict:
        """
        Place a limit order
        
        Args:
            symbol (str): Trading pair (e.g. "BTCUSDT")
            side (str): "Buy" or "Sell"
            qty (float): Order quantity
            price (float): Order price
            reduce_only (bool): Whether to reduce position only
            close_on_trigger (bool): Whether to close position on trigger
            time_in_force (str): Order time in force (default: "GoodTillCancel")
            
        Returns:
            dict: Order response from Bybit
        """
        try:
            response = self.session.place_order(
                category="linear",
                symbol=symbol,
                side=side,
                orderType="Limit",
                qty=str(qty),
                price=str(price),
                reduceOnly=reduce_only,
                closeOnTrigger=close_on_trigger,
                timeInForce=time_in_force
            )
            return response
        except Exception as e:
            print(f"Error placing limit order: {e}")
            return None
            
    def place_stop_market_order(
        self,
        symbol: str,
        side: Literal["Buy", "Sell"],
        qty: float,
        stop_price: float,
        reduce_only: bool = False,
        close_on_trigger: bool = False
    ) -> dict:
        """
        Place a stop market order
        
        Args:
            symbol (str): Trading pair (e.g. "BTCUSDT")
            side (str): "Buy" or "Sell"
            qty (float): Order quantity
            stop_price (float): Stop price
            reduce_only (bool): Whether to reduce position only
            close_on_trigger (bool): Whether to close position on trigger
            
        Returns:
            dict: Order response from Bybit
        """
        try:
            response = self.session.place_order(
                category="linear",
                symbol=symbol,
                side=side,
                orderType="Market",
                qty=str(qty),
                stopPrice=str(stop_price),
                reduceOnly=reduce_only,
                closeOnTrigger=close_on_trigger,
                triggerDirection=1 if side == "Buy" else 2
            )
            return response
        except Exception as e:
            print(f"Error placing stop market order: {e}")
            return None
            
    def cancel_order(self, symbol: str, order_id: str) -> dict:
        """
        Cancel an order
        
        Args:
            symbol (str): Trading pair (e.g. "BTCUSDT")
            order_id (str): Order ID to cancel
            
        Returns:
            dict: Cancel response from Bybit
        """
        try:
            response = self.session.cancel_order(
                category="linear",
                symbol=symbol,
                orderId=order_id
            )
            return response
        except Exception as e:
            print(f"Error canceling order: {e}")
            return None
            
    def get_position(self, symbol: str) -> dict:
        """
        Get current position information
        
        Args:
            symbol (str): Trading pair (e.g. "BTCUSDT")
            
        Returns:
            dict: Position information from Bybit
        """
        try:
            response = self.session.get_positions(
                category="linear",
                symbol=symbol
            )
            return response
        except Exception as e:
            print(f"Error getting position: {e}")
            return None
