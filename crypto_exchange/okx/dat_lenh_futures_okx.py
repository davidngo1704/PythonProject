import ccxt
import time
from typing import Dict, Optional

class OKXFuturesTrader:
    def __init__(self, api_key: str, api_secret: str, password: str):
        """
        Initialize OKX futures trader
        
        Args:
            api_key (str): OKX API key
            api_secret (str): OKX API secret
            password (str): OKX API password
        """
        self.exchange = ccxt.okx({
            'apiKey': api_key,
            'secret': api_secret,
            'password': password,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'swap',  # Use swap for futures trading
            }
        })
    
    def place_market_order(self, symbol: str, side: str, size: float) -> Dict:
        """
        Place a market order
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTC/USDT:USDT')
            side (str): 'buy' or 'sell'
            size (float): Order size
            
        Returns:
            Dict: Order response
        """
        try:
            order = self.exchange.create_order(
                symbol=symbol,
                type='market',
                side=side,
                amount=size
            )
            return order
        except Exception as e:
            print(f"Error placing market order: {e}")
            return None
    
    def place_limit_order(self, symbol: str, side: str, size: float, price: float) -> Dict:
        """
        Place a limit order
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTC/USDT:USDT')
            side (str): 'buy' or 'sell'
            size (float): Order size
            price (float): Order price
            
        Returns:
            Dict: Order response
        """
        try:
            order = self.exchange.create_order(
                symbol=symbol,
                type='limit',
                side=side,
                amount=size,
                price=price
            )
            return order
        except Exception as e:
            print(f"Error placing limit order: {e}")
            return None
    
    def get_position(self, symbol: str) -> Dict:
        """
        Get current position for a symbol
        
        Args:
            symbol (str): Trading pair symbol
            
        Returns:
            Dict: Position information
        """
        try:
            positions = self.exchange.fetch_positions([symbol])
            return positions[0] if positions else None
        except Exception as e:
            print(f"Error getting position: {e}")
            return None
    
    def close_position(self, symbol: str, side: Optional[str] = None) -> Dict:
        """
        Close current position
        
        Args:
            symbol (str): Trading pair symbol
            side (str, optional): 'buy' or 'sell'. If None, will close in opposite direction of current position
            
        Returns:
            Dict: Order response
        """
        try:
            position = self.get_position(symbol)
            if not position:
                print("No position found")
                return None
                
            if not side:
                side = 'sell' if position['side'] == 'long' else 'buy'
                
            return self.place_market_order(symbol, side, abs(float(position['contracts'])))
        except Exception as e:
            print(f"Error closing position: {e}")
            return None

# Example usage:
if __name__ == "__main__":
    # Initialize with your API credentials
    trader = OKXFuturesTrader(
        api_key="YOUR_API_KEY",
        api_secret="YOUR_API_SECRET",
        password="YOUR_API_PASSWORD"
    )
    
    # Example: Place a market buy order
    order = trader.place_market_order('BTC/USDT:USDT', 'buy', 0.01)
    print(order)
    
    # Example: Place a limit sell order
    order = trader.place_limit_order('BTC/USDT:USDT', 'sell', 0.01, 50000)
    print(order)
    
    # Example: Get current position
    position = trader.get_position('BTC/USDT:USDT')
    print(position)
    
    # Example: Close position
    close_order = trader.close_position('BTC/USDT:USDT')
    print(close_order)
