from binance.client import Client
from binance.exceptions import BinanceAPIException
import logging
from typing import Optional, Literal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BinanceFuturesTrader:
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize the Binance Futures trader
        
        Args:
            api_key (str): Your Binance API key
            api_secret (str): Your Binance API secret
        """
        self.client = Client(api_key, api_secret)
        self.client.futures_change_leverage(symbol='BTCUSDT', leverage=1)  # Default leverage
        
    def set_leverage(self, symbol: str, leverage: int):
        """
        Set leverage for a trading pair
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            leverage (int): Leverage value
        """
        try:
            self.client.futures_change_leverage(symbol=symbol, leverage=leverage)
            logger.info(f"Leverage set to {leverage}x for {symbol}")
        except BinanceAPIException as e:
            logger.error(f"Error setting leverage: {e}")
            
    def place_order(self, 
                   symbol: str, 
                   side: Literal['BUY', 'SELL'], 
                   quantity: float,
                   order_type: Literal['MARKET', 'LIMIT'] = 'MARKET',
                   price: Optional[float] = None,
                   stop_price: Optional[float] = None,
                   take_profit: Optional[float] = None,
                   stop_loss: Optional[float] = None):
        """
        Place a futures order
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): 'BUY' for long, 'SELL' for short
            quantity (float): Order quantity
            order_type (str): 'MARKET' or 'LIMIT'
            price (float, optional): Price for limit orders
            stop_price (float, optional): Stop price for stop orders
            take_profit (float, optional): Take profit price
            stop_loss (float, optional): Stop loss price
        """
        try:
            # Place main order
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity
            }
            
            if order_type == 'LIMIT':
                order_params['timeInForce'] = 'GTC'
                order_params['price'] = price
                
            if stop_price:
                order_params['stopPrice'] = stop_price
                
            order = self.client.futures_create_order(**order_params)
            logger.info(f"Order placed: {order}")
            
            # Place take profit if specified
            if take_profit:
                tp_order = self.client.futures_create_order(
                    symbol=symbol,
                    side='SELL' if side == 'BUY' else 'BUY',
                    type='TAKE_PROFIT_MARKET',
                    stopPrice=take_profit,
                    closePosition=True
                )
                logger.info(f"Take profit order placed: {tp_order}")
                
            # Place stop loss if specified
            if stop_loss:
                sl_order = self.client.futures_create_order(
                    symbol=symbol,
                    side='SELL' if side == 'BUY' else 'BUY',
                    type='STOP_MARKET',
                    stopPrice=stop_loss,
                    closePosition=True
                )
                logger.info(f"Stop loss order placed: {sl_order}")
                
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Error placing order: {e}")
            return None
            
    def close_position(self, symbol: str):
        """
        Close all positions for a symbol
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
        """
        try:
            position = self.client.futures_position_information(symbol=symbol)[0]
            if float(position['positionAmt']) != 0:
                side = 'SELL' if float(position['positionAmt']) > 0 else 'BUY'
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='MARKET',
                    quantity=abs(float(position['positionAmt']))
                )
                logger.info(f"Position closed: {order}")
                return order
        except BinanceAPIException as e:
            logger.error(f"Error closing position: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Replace with your API keys
    API_KEY = "your_api_key"
    API_SECRET = "your_api_secret"
    
    trader = BinanceFuturesTrader(API_KEY, API_SECRET)
    
    # Example: Place a long order with take profit and stop loss
    trader.set_leverage('BTCUSDT', 10)
    trader.place_order(
        symbol='BTCUSDT',
        side='BUY',
        quantity=0.001,
        order_type='MARKET',
        take_profit=50000,  # Take profit at $50,000
        stop_loss=45000     # Stop loss at $45,000
    )
