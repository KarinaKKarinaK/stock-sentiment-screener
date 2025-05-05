import requests
from bs4 import BeautifulSoup
import datetime

def get_ahoo_finance_headlines(stock_ticker, limit: int = 10) -> list[str]:
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
