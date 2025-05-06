import ccxt
import time
from typing import Optional, Dict, Any

class OKXSpotTrader:
    def __init__(self, api_key: str, api_secret: str, password: str):
        """
        Initialize OKX spot trader
        
        Args:
            api_key (str): Your OKX API key
            api_secret (str): Your OKX API secret
            password (str): Your OKX API password
        """
        self.exchange = ccxt.okx({
            'apiKey': api_key,
            'secret': api_secret,
            'password': password,
            'enableRateLimit': True,
        })
        
    def place_spot_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        amount: float,
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Place a spot order on OKX
        
        Args:
            symbol (str): Trading pair (e.g., 'BTC/USDT')
            side (str): 'buy' or 'sell'
            order_type (str): 'limit' or 'market'
            amount (float): Amount to buy/sell
            price (float, optional): Price for limit orders
            
        Returns:
            Dict[str, Any]: Order response from OKX
        """
        try:
            params = {}
            if order_type == 'limit':
                if price is None:
                    raise ValueError("Price is required for limit orders")
                params['price'] = price
                
            order = self.exchange.create_order(
                symbol=symbol,
                type=order_type,
                side=side,
                amount=amount,
                params=params
            )
            
            return order
            
        except Exception as e:
            print(f"Error placing order: {str(e)}")
            raise
            
    def get_order_status(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """
        Get the status of an order
        
        Args:
            order_id (str): Order ID to check
            symbol (str): Trading pair
            
        Returns:
            Dict[str, Any]: Order status information
        """
        try:
            return self.exchange.fetch_order(order_id, symbol)
        except Exception as e:
            print(f"Error getting order status: {str(e)}")
            raise
            
    def cancel_order(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """
        Cancel an order
        
        Args:
            order_id (str): Order ID to cancel
            symbol (str): Trading pair
            
        Returns:
            Dict[str, Any]: Cancellation response
        """
        try:
            return self.exchange.cancel_order(order_id, symbol)
        except Exception as e:
            print(f"Error canceling order: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    # Replace with your actual API credentials
    API_KEY = "your_api_key"
    API_SECRET = "your_api_secret"
    API_PASSWORD = "your_api_password"
    
    # Initialize trader
    trader = OKXSpotTrader(API_KEY, API_SECRET, API_PASSWORD)
    
    # Example: Place a limit buy order for 0.001 BTC at $50,000
    try:
        order = trader.place_spot_order(
            symbol="BTC/USDT",
            side="buy",
            order_type="limit",
            amount=0.001,
            price=50000
        )
        print(f"Order placed successfully: {order}")
        
        # Check order status
        time.sleep(2)  # Wait a bit before checking status
        status = trader.get_order_status(order['id'], "BTC/USDT")
        print(f"Order status: {status}")
        
    except Exception as e:
        print(f"Error in main execution: {str(e)}")
