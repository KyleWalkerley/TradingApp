import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
from textblob import TextBlob

# Page config
st.set_page_config(page_title="IntelliStock Tracker", layout="wide")

# Title and input
st.markdown("## 📈 IntelliStock Tracker")
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, MSFT)", "AAPL").upper()

# Fetch data
try:
    data = yf.download(ticker, period="1y", progress=False)
    if data.empty:
        st.error("No data found for this ticker.")
    else:
        df = data.copy()

        # --- Latest price ---
        latest_price = df['Close'].iloc[-1].item()
        prev_price = df['Close'].iloc[-2].item()
        price_change = latest_price - prev_price
        color = "green" if price_change > 0 else "red"

        st.markdown(f"### {ticker} Price: <span style='color:{color}'>${latest_price:.2f} ({price_change:+.2f})</span>", unsafe_allow_html=True)

        # --- Historical Chart ---
        st.markdown(f"### {ticker} Historical Price (1 Year)")
        fig, ax = plt.subplots()
        ax.plot(df.index, df['Close'], label='Close Price')
        ax.set_ylabel('Price ($)')
        ax.grid(True)
        st.pyplot(fig)

        # --- AI Prediction (Mock) ---
        st.markdown("### 🤖 AI Price Movement Prediction")
        # Simulated prediction logic
        mock_pred = np.random.choice(["Up", "Down"])
        mock_conf = np.random.uniform(55, 80)
        mock_acc = np.random.uniform(50, 70)
        icon = "⬆️" if mock_pred == "Up" else "⬇️"
        color = "green" if mock_pred == "Up" else "red"
        st.markdown(f"**Tomorrow's Prediction:** <span style='color:{color}'>{icon} {mock_pred}</span>", unsafe_allow_html=True)
        st.markdown(f"Model confidence: {mock_conf:.2f}% | Accuracy: {mock_acc:.2f}%")

        # --- News Sentiment Analysis ---
    st.subheader("🗞️ News Sentiment Analysis")
    try:
        api_key = "XXXXX"  # Replace with your real key
        url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&apiKey={api_key}&language=en&pageSize=5"
        response = requests.get(url)
        news_data = response.json()

        if news_data["status"] != "ok":
            st.warning("Error fetching news.")
        elif news_data["totalResults"] == 0:
            st.warning("No recent news found for this ticker.")
        else:
            for article in news_data["articles"]:
                st.write(f"**{article['title']}**")
                st.caption(f"Source: {article['source']['name']} | {article['publishedAt']}")
                st.write(article['description'] or "")
                st.markdown("---")

    except Exception as e:
        st.warning(f"Could not fetch news: {e}")


except Exception as e:
    st.error(f"Error loading stock data: {e}")




