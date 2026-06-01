#!/usr/bin/env python3
"""
trading_bot CLI — Place orders on Binance Futures Testnet

Usage examples:
  # Market BUY
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  # Limit SELL
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3200
"""

import argparse
import os
import sys

from bot.client import BinanceClient
from bot.logging_config import setup_logger
from bot.orders import place_order
from bot.validators import ValidationError, validate_all

logger = setup_logger()


def get_credentials():
    api_key = os.environ.get("BINANCE_TESTNET_API_KEY", "").strip()
    api_secret = os.environ.get("BINANCE_TESTNET_API_SECRET", "").strip()

    if not api_key or not api_secret:
        print("\n❌  API credentials not found.")
        print("    Set environment variables before running:")
        print("    export BINANCE_TESTNET_API_KEY=your_key")
        print("    export BINANCE_TESTNET_API_SECRET=your_secret\n")
        sys.exit(1)

    return api_key, api_secret


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place orders on Binance Futures Testnet (USDT-M)",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3200
        """,
    )
    parser.add_argument("--symbol",   required=True,  help="Trading pair symbol (e.g. BTCUSDT)")
    parser.add_argument("--side",     required=True,  help="Order side: BUY or SELL")
    parser.add_argument("--type",     required=True,  dest="order_type", help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", required=True,  help="Order quantity (e.g. 0.001)")
    parser.add_argument("--price",    required=False, default=None, help="Limit price (required for LIMIT orders)")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Validate inputs
    try:
        symbol, side, order_type, quantity, price = validate_all(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValidationError as e:
        print(f"\n❌  Validation error: {e}\n")
        logger.warning(f"Validation failed: {e}")
        parser.print_help()
        sys.exit(1)

    # Load credentials
    api_key, api_secret = get_credentials()

    # Create client and place order
    client = BinanceClient(api_key=api_key, api_secret=api_secret)
    success = place_order(
        client=client,
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
