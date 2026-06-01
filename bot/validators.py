from typing import Optional


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


class ValidationError(Exception):
    pass


def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not symbol or len(symbol) < 3:
        raise ValidationError(f"Invalid symbol: '{symbol}'. Example: BTCUSDT")
    return symbol


def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError(f"Invalid side: '{side}'. Must be one of: {', '.join(VALID_SIDES)}")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(f"Invalid order type: '{order_type}'. Must be one of: {', '.join(VALID_ORDER_TYPES)}")
    return order_type


def validate_quantity(quantity: str) -> float:
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValidationError(f"Quantity must be greater than 0. Got: {qty}")
        return qty
    except ValueError:
        raise ValidationError(f"Invalid quantity: '{quantity}'. Must be a positive number.")


def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        try:
            p = float(price)
            if p <= 0:
                raise ValidationError(f"Price must be greater than 0. Got: {p}")
            return p
        except ValueError:
            raise ValidationError(f"Invalid price: '{price}'. Must be a positive number.")
    return None


def validate_all(symbol: str, side: str, order_type: str, quantity: str, price: Optional[str] = None):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    price = validate_price(price, order_type)
    return symbol, side, order_type, quantity, price
