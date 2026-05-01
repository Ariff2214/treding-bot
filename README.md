# Binance Futures Testnet Trading Bot

A simplified Python trading bot to place Market and Limit orders on the Binance Futures Testnet (USDT-M). This project uses raw `requests` to interact with the Binance API, clearly demonstrating proper HTTP client usage, HMAC SHA256 request signing, and separated concerns.

## Features
- Places MARKET and LIMIT orders on the Binance Futures Testnet.
- Supports both BUY and SELL sides.
- Validates user input via a Command Line Interface (CLI).
- Separates client layer (`bot/client.py`) and CLI layer (`cli.py`).
- Comprehensive error handling and input validation.
- Extensive logging of all API requests, responses, and errors to `trading_bot.log`.

## Setup Steps

1. **Clone the repository or extract the zip folder.**

2. **Ensure you have Python 3.x installed.**

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables:**
   - Copy `.env.example` to a new file named `.env`:
     ```bash
     cp .env.example .env
     ```
   - Register and activate a [Binance Futures Testnet](https://testnet.binancefuture.com/) account.
   - Generate API credentials and place them inside your `.env` file:
     ```env
     BINANCE_API_KEY=your_testnet_api_key
     BINANCE_API_SECRET=your_testnet_api_secret
     ```

## How to Run Examples

Run the bot using the `cli.py` entry point.

### MARKET Order Example
Places a BUY market order for 0.001 BTCUSDT:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### LIMIT Order Example
Places a SELL limit order for 0.001 BTCUSDT at the price of 90000:
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 90000
```

### CLI Help
To see all available options:
```bash
python cli.py --help
```

## Logs
All API interactions and errors are logged to `trading_bot.log` in the root directory.

## Assumptions
- The bot exclusively targets the Binance Futures Testnet (`https://testnet.binancefuture.com`).
- Assumes the trading pair (symbol) exists and the user has sufficient testnet USDT balance.
- LIMIT orders are submitted with `timeInForce="GTC"` (Good Till Cancel).
