from binance.client import Client
from binance.enums import *
import config

# Khởi tạo client với API key và secret key
client = Client(config.API_KEY, config.API_SECRET)

def place_buy_order(symbol, quantity, price=None):
    """
    Đặt lệnh mua
    
    Args:
        symbol (str): Cặp giao dịch (ví dụ: 'BTCUSDT')
        quantity (float): Số lượng muốn mua
        price (float, optional): Giá mua. Nếu None sẽ là lệnh thị trường
    
    Returns:
        dict: Thông tin về lệnh đã đặt
    """
    try:
        if price:
            # Lệnh giới hạn
            order = client.create_order(
                symbol=symbol,
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price
            )
        else:
            # Lệnh thị trường
            order = client.create_order(
                symbol=symbol,
                side=SIDE_BUY,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
        return order
    except Exception as e:
        print(f"Lỗi khi đặt lệnh mua: {e}")
        return None

def place_sell_order(symbol, quantity, price=None):
    """
    Đặt lệnh bán
    
    Args:
        symbol (str): Cặp giao dịch (ví dụ: 'BTCUSDT')
        quantity (float): Số lượng muốn bán
        price (float, optional): Giá bán. Nếu None sẽ là lệnh thị trường
    
    Returns:
        dict: Thông tin về lệnh đã đặt
    """
    try:
        if price:
            # Lệnh giới hạn
            order = client.create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price
            )
        else:
            # Lệnh thị trường
            order = client.create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
        return order
    except Exception as e:
        print(f"Lỗi khi đặt lệnh bán: {e}")
        return None

def get_order_status(symbol, order_id):
    """
    Kiểm tra trạng thái lệnh
    
    Args:
        symbol (str): Cặp giao dịch
        order_id (str): ID của lệnh cần kiểm tra
    
    Returns:
        dict: Thông tin về trạng thái lệnh
    """
    try:
        order = client.get_order(symbol=symbol, orderId=order_id)
        return order
    except Exception as e:
        print(f"Lỗi khi kiểm tra trạng thái lệnh: {e}")
        return None

# Ví dụ sử dụng
if __name__ == "__main__":
    # Đặt lệnh mua BTC với giá thị trường
    buy_order = place_buy_order('BTCUSDT', 0.001)
    if buy_order:
        print("Đặt lệnh mua thành công:", buy_order)
    
    # Đặt lệnh bán BTC với giá giới hạn
    sell_order = place_sell_order('BTCUSDT', 0.001, 50000)
    if sell_order:
        print("Đặt lệnh bán thành công:", sell_order)
