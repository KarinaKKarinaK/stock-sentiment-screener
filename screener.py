import requests
from bs4 import BeautifulSoup
import datetime
import yfinance as yf
import ta
import pandas as pd

def get_yahoo_finance_headlines(stock_ticker, limit: int = 10) -> list[str]:
    url = f"https://finance.yahoo.com/quote/{stock_ticker}?p={stock_ticker}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    headlines = []
    for tag in soup.find_all("h3")[:limit]:
        if tag.a:
            headlines.append(tag.a.text)
    
    return headlines

def make_signal(sentiments: list[str]) -> str:
    positive_count = sentiments.count("POSITIVE")
    negative_count = sentiments.count("NEGATIVE")
    
    if positive_count > negative_count + 2:
        return "BUY"
    elif negative_count > positive_count+ 2:
        return "SELL"
    else:
        return "HOLD"
    
def get_rsi_signal(stock_ticker: str) -> str:
    df = yf.download(stock_ticker, period="1mo", interval="1d")
    df.dropna(inplace=True)

    # Ensuring it is a series rather than a DataFrame
    close_series = df["Close"]
    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.squeeze()
    
    rsi_indicator = ta.momentum.RSIIndicator(close=close_series)
    df["rsi"] = rsi_indicator.rsi()

    last_rsi = df["rsi"].dropna().iloc[-1]
    
    if last_rsi < 30:
        return "BUY"
    elif last_rsi > 70:
        return "SELL"
    else:
        return "HOLD"
    
def get_final_signal(sentiment_signal: str, rsi_signal: str) -> str:
    if sentiment_signal == "BUY" and rsi_signal == "BUY":
        return "STRONG BUY"
    elif sentiment_signal == "SELL" and rsi_signal == "SELL":
        return "STRONG SELL"
    else:
        return "NEUTRAL / CAUTION"
