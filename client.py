import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from .logging_config import logger

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://testnet.binancefuture.com"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _dispatch_request(self, method: str, endpoint: str, params: dict = None) -> dict:
        if params is None:
            params = {}

        # Binance requires a timestamp for signed endpoints
        params['timestamp'] = int(time.time() * 1000)

        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        
        # For POST requests, parameters are often sent in the body as form data
        # But Binance Futures API accepts them in the query string too, 
        # or as URL-encoded body. We'll use URL-encoded body for POST.
        
        url = f"{self.base_url}{endpoint}"
        body = f"{query_string}&signature={signature}"
        
        logger.debug(f"Dispatching {method} request to {url}")
        
        try:
            if method.upper() == "GET":
                response = self.session.request(method, f"{url}?{body}")
            else:
                response = self.session.request(method, url, data=body)
                
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Response from {endpoint}: {data}")
            return data
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                error_msg = f"Binance API Error {error_data.get('code')}: {error_data.get('msg')}"
            except ValueError:
                error_msg = f"HTTP Error {e.response.status_code} on {endpoint}: {e.response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Network Error on {endpoint}: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
        """
        Place a new order.
        For MARKETS: symbol, side, type, quantity
        For LIMIT: symbol, side, type, timeInForce, quantity, price
        """
        endpoint = "/fapi/v1/order"
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity
        }

        if order_type.upper() == "LIMIT":
            if price is None:
                raise ValueError("Price is required for LIMIT orders.")
            params["price"] = price
            params["timeInForce"] = "GTC" # Good Till Cancel

        logger.info(f"Placing {order_type} order for {quantity} {symbol} ({side})")
        return self._dispatch_request("POST", endpoint, params)
