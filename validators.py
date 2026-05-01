class ValidationError(Exception):
    pass

def validate_symbol(symbol: str) -> str:
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol must be a non-empty string.")
    return symbol.upper()

def validate_side(side: str) -> str:
    side = str(side).upper()
    if side not in ["BUY", "SELL"]:
        raise ValidationError("Side must be 'BUY' or 'SELL'.")
    return side

def validate_order_type(order_type: str) -> str:
    order_type = str(order_type).upper()
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValidationError("Order type must be 'MARKET' or 'LIMIT'.")
    return order_type

def validate_quantity(quantity: str) -> float:
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError
        return qty
    except ValueError:
        raise ValidationError("Quantity must be a positive number.")

def validate_price(price: str, order_type: str) -> float:
    if order_type.upper() == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        try:
            p = float(price)
            if p <= 0:
                raise ValueError
            return p
        except ValueError:
            raise ValidationError("Price must be a positive number for LIMIT orders.")
    return None

def validate_order_input(symbol, side, order_type, quantity, price=None):
    return {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "order_type": validate_order_type(order_type),
        "quantity": validate_quantity(quantity),
        "price": validate_price(price, order_type)
    }
