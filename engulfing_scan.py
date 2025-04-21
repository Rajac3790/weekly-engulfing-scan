import yfinance as yf
import pandas as pd
import requests
import os

# List of NSE Stocks (sample – you can add more)
nse_stocks = [
    "3MINDIA.NS", "AARTIDRUGS.NS", "AARTIIND.NS", "AAVAS.NS", "ACCELYA.NS", "ACE.NS"
]

timeframe = "1wk"  # Weekly candles

def is_engulfing(df):
    """Check for engulfing pattern in last 2 candles, excluding candles with large wicks"""
    if len(df) < 2:
        return False, False

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    def valid_candle(candle):
        body = abs(candle.Close - candle.Open)
        upper_wick = candle.High - max(candle.Open, candle.Close)
        lower_wick = min(candle.Open, candle.Close) - candle.Low
        return upper_wick <= body and lower_wick <= body

    if not valid_candle(prev) or not valid_candle(curr):
        return False, False

    bullish = (
        (curr.Close > curr.Open) and
        (prev.Close < prev.Open) and
        (curr.Close > prev.Open) and
        (curr.Open < prev.Close)
    )

    bearish = (
        (curr.Close < curr.Open) and
        (prev.Close > prev.Open) and
        (curr.Close < prev.Open) and
        (curr.Open > prev.Close)
    )

    return bullish, bearish

def scan_stocks():
    print("Downloading weekly data...")
    data = yf.download(
        nse_stocks,
        period="21d",  # 3 weeks to ensure 2 full candles
        interval=timeframe,
        group_by='ticker',
        threads=True
    )

    engulfing_stocks = []

    for stock in nse_stocks:
        try:
            df = data[stock].copy() if len(nse_stocks) > 1 else data.copy()
            df.dropna(inplace=True)

            if df.shape[0] < 2:
                continue

            last_two_weeks = df.tail(2)
            bullish, bearish = is_engulfing(last_two_weeks)

            if bullish or bearish:
                pattern_date = last_two_weeks.index[-1].date()
                pattern = "Weekly Bullish Engulfing" if bullish else "Weekly Bearish Engulfing"
                engulfing_stocks.append((stock, pattern, pattern_date))

        except Exception as e:
            print(f"Error processing {stock}: {e}")

    return engulfing_stocks

def send_telegram_message(message):
    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if not bot_token or not chat_id:
        print("Telegram credentials not set in environment variables.")
        return

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    print(response.json())

# Main runner
if __name__ == "__main__":
    engulfing_stocks = scan_stocks()

    result_text = "\n".join([f"{stock}: {pattern} ({date})" for stock, pattern, date in engulfing_stocks])
    print("Final result_text:")
    print(result_text)

    if result_text:
        send_telegram_message(f"📈 Weekly Engulfing Scan Results:\n\n{result_text}")
    else:
        send_telegram_message("✅ No Weekly Engulfing patterns found in previous weeks.")
