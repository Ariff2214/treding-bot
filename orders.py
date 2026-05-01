import os
from .client import BinanceFuturesClient
from .logging_config import logger

def get_client() -> BinanceFuturesClient:
    api_key = os.environ.get("BINANCE_API_KEY")
    api_secret = os.environ.get("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        raise ValueError("BINANCE_API_KEY and BINANCE_API_SECRET must be set in environment variables.")
        
    return BinanceFuturesClient(api_key, api_secret)

def place_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    client = get_client()
    try:
        response = client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        return response
    except Exception as e:
        logger.error(f"Failed to place order: {e}")
        raise
