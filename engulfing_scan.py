import yfinance as yf
import pandas as pd
import requests
import os
from time import sleep

# List of NSE Stocks
nse_stocks = [
    "3MINDIA.NS", "AARTIDRUGS.NS", "AARTIIND.NS", "AAVAS.NS", "ACCELYA.NS", "ACE.NS"
]


# ========== ENGULFING CHECK ==========
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


# ========== WEEKLY SCAN ==========
def weekly_scan():
    print("📥 Downloading weekly data...")
    data = yf.download(
        nse_stocks,
        period="21d",
        interval="1wk",
        group_by='ticker',
        threads=True
    )

    results = []

    for stock in nse_stocks:
        try:
            df = data[stock].copy() if len(nse_stocks) > 1 else data.copy()
            df.dropna(inplace=True)
            if df.shape[0] < 2:
                continue

            bullish, bearish = is_engulfing(df.tail(2))

            if bullish or bearish:
                pattern = "Weekly Bullish Engulfing" if bullish else "Weekly Bearish Engulfing"
                date = df.index[-1].date()
                results.append(f"{stock}: {pattern} ({date})")
        except Exception as e:
            print(f"Error processing {stock}: {e}")

    return results


# ========== DAILY SCAN ==========
def daily_scan():
    print("📥 Downloading daily data...")
    results = []
    batch_size = 100

    for i in range(0, len(nse_stocks), batch_size):
        batch = nse_stocks[i:i + batch_size]
        try:
            data = yf.download(
                batch,
                period="5d",
                interval="1d",
                group_by="ticker",
                threads=True,
                progress=False
            )
        except Exception as e:
            print(f"Download error for batch: {e}")
            continue

        for stock in batch:
            try:
                df = data[stock].copy() if len(batch) > 1 else data.copy()
                df.dropna(inplace=True)
                if len(df) < 2:
                    continue

                bullish, bearish = is_engulfing(df.tail(2))

                if bullish or bearish:
                    pattern = "Daily Bullish Engulfing" if bullish else "Daily Bearish Engulfing"
                    date = df.index[-1].date()
                    results.append(f"{stock}: {pattern} ({date})")
            except Exception as e:
                print(f"Error processing {stock}: {e}")

        sleep(2)  # Be gentle with the API

    return results


# ========== TELEGRAM ALERT ==========
def send_telegram_message(message):
    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if not bot_token or not chat_id:
        print("Telegram credentials not set in environment variables.")
        return

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=payload)
    print(response.json())


# ========== MAIN RUNNER ==========
if __name__ == "__main__":
    weekly_results = weekly_scan()
    daily_results = daily_scan()

    full_message = "📊 Engulfing Pattern Scan Results\n\n"

    if weekly_results:
        full_message += "🗓️ *Weekly Patterns*\n" + "\n".join(weekly_results) + "\n\n"
    else:
        full_message += "🗓️ Weekly: No patterns found.\n\n"

    if daily_results:
        full_message += "📆 *Daily Patterns*\n" + "\n".join(daily_results)
    else:
        full_message += "📆 Daily: No patterns found."

    print(full_message)
    send_telegram_message(full_message)
