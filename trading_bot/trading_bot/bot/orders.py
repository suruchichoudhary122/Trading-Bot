from typing import Optional

from bot.client import BinanceClient, BinanceClientError
from bot.logging_config import setup_logger

logger = setup_logger()


def print_order_summary(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float]):
    print("\n" + "=" * 50)
    print("  ORDER REQUEST SUMMARY")
    print("=" * 50)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        print(f"  Price      : {price}")
    print("=" * 50)


def print_order_response(response: dict):
    print("\n  ORDER RESPONSE")
    print("=" * 50)
    print(f"  Order ID     : {response.get('orderId', 'N/A')}")
    print(f"  Status       : {response.get('status', 'N/A')}")
    print(f"  Symbol       : {response.get('symbol', 'N/A')}")
    print(f"  Side         : {response.get('side', 'N/A')}")
    print(f"  Type         : {response.get('type', 'N/A')}")
    print(f"  Executed Qty : {response.get('executedQty', 'N/A')}")
    avg_price = response.get('avgPrice') or response.get('price', 'N/A')
    print(f"  Avg Price    : {avg_price}")
    print("=" * 50)


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
) -> bool:
    print_order_summary(symbol, side, order_type, quantity, price)

    logger.info(f"Placing {order_type} {side} order | Symbol: {symbol} | Qty: {quantity}" +
                (f" | Price: {price}" if price else ""))

    try:
        response = client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )
        print_order_response(response)
        logger.info(f"Order placed successfully | OrderId: {response.get('orderId')} | Status: {response.get('status')}")
        print("\n  ✅  Order placed successfully!\n")
        return True

    except BinanceClientError as e:
        print(f"\n  ❌  Order failed: {e}\n")
        logger.error(f"Order placement failed: {e}")
        return False
