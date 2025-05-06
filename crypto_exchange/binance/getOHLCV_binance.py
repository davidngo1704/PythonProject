import requests
from datetime import datetime

def get_klines(symbol, interval='1d', limit=30):
    """
    Get OHLCV data for a cryptocurrency from Binance
    
    Args:
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
        interval (str): Kline interval (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
        limit (int): Number of klines to return (max 1000)
    
    Returns:
        list: List of klines data where each kline is [Open time, Open, High, Low, Close, Volume, ...]
    """
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Convert timestamp to readable date and format the data
    formatted_data = []
    for kline in data:
        timestamp = datetime.fromtimestamp(kline[0] / 1000)
        formatted_kline = {
            'timestamp': timestamp,
            'open': float(kline[1]),
            'high': float(kline[2]),
            'low': float(kline[3]),
            'close': float(kline[4]),
            'volume': float(kline[5])
        }
        formatted_data.append(formatted_kline)
    
    return formatted_data

if __name__ == "__main__":
    # Example usage
    klines = get_klines("ETHUSDT", interval='1d', limit=10)
    for kline in klines:
        print(f"Time: {kline['timestamp']}")
        print(f"Open: {kline['open']}")
        print(f"High: {kline['high']}")
        print(f"Low: {kline['low']}")
        print(f"Close: {kline['close']}")
        print(f"Volume: {kline['volume']}")
        print("-" * 50)