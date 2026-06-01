# Trading Bot — Binance Futures Testnet

A clean Python CLI application to place **Market** and **Limit** orders on Binance Futures Testnet (USDT-M).

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API wrapper (signing, HTTP)
│   ├── orders.py          # Order placement logic + response formatting
│   ├── validators.py      # CLI input validation
│   └── logging_config.py  # Structured file + console logging
├── cli.py                 # CLI entry point (argparse)
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Register on Binance Futures Testnet

- Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
- Sign up and log in
- Navigate to **API Management** → Generate API Key and Secret
- Copy both values

### 2. Clone the repo and install dependencies

```bash
git clone https://github.com/YOUR_USERNAME/trading-bot.git
cd trading-bot
pip install -r requirements.txt
```

### 3. Set API credentials as environment variables

**Linux / macOS:**
```bash
export BINANCE_TESTNET_API_KEY=your_api_key_here
export BINANCE_TESTNET_API_SECRET=your_api_secret_here
```

**Windows (Command Prompt):**
```cmd
set BINANCE_TESTNET_API_KEY=your_api_key_here
set BINANCE_TESTNET_API_SECRET=your_api_secret_here
```

---

## How to Run

### Place a MARKET BUY order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a LIMIT SELL order
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3200
```

### View all options
```bash
python cli.py --help
```

---

## Example Output

```
==================================================
  ORDER REQUEST SUMMARY
==================================================
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.001
==================================================

  ORDER RESPONSE
==================================================
  Order ID     : 3927461823
  Status       : FILLED
  Symbol       : BTCUSDT
  Side         : BUY
  Type         : MARKET
  Executed Qty : 0.001
  Avg Price    : 43215.60
==================================================

  ✅  Order placed successfully!
```

---

## Logging

All requests, responses, and errors are logged to:
```
logs/trading_YYYYMMDD.log
```

Log entries include timestamp, log level, module, and message. Console output shows INFO and above only; the log file captures full DEBUG detail including raw API responses.

---

## Validation & Error Handling

| Scenario | Behaviour |
|---|---|
| Invalid side (not BUY/SELL) | Validation error, prints help |
| Missing price for LIMIT order | Validation error with clear message |
| Non-numeric quantity | Validation error |
| API error (e.g. insufficient margin) | Error code + message from Binance |
| Network timeout or connection failure | Friendly error, logged to file |

---

## Assumptions

- Uses **USDT-M Futures Testnet** only (`https://testnet.binancefuture.com`)
- API credentials are loaded from environment variables (not hardcoded)
- LIMIT orders use `timeInForce=GTC` (Good Till Cancelled) by default
- No position management or balance checks — pure order placement
