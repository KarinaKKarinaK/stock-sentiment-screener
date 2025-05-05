import streamlit as st
from screener import get_yahoo_finance_headlines, get_final_signal
from sentiment import analyze_sentiment

st.title("Stock Screener wih Sentiment Analysis")

ticker = st.text_input("Enter stock ticker (e.g., AAPL, TSLA):", "AAPL")

if ticker:
    st.subheader("Latest News Headklines")
    headlines = get_yahoo_finance_headlines(ticker)
    for h in headlines:
        st.write("•", h)

    st.subheader("Sentiment Analysis")
    sentiments = analyze_sentiment(headlines)
    for h, s in zip(headlines, sentiments):
        st.write(f"{h} → **{s}**")

    st.subheader("Trading Signal")
    signal = get_final_signal(sentiments)
    st.write(f"### 🚨 {signal}")