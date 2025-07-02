import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import requests
from textblob import TextBlob
from investment_projection import project_investment
from ai_predictor import train_predict_model
import plotly.express as px


# Asset type and ticker options
asset_options = {
    "Stocks": {
        "Apple (AAPL)": "AAPL",
        "Tesla (TSLA)": "TSLA",
        "Microsoft (MSFT)": "MSFT",
        "Amazon (AMZN)": "AMZN",
        "NVIDIA (NVDA)": "NVDA",
        "Meta (META)": "META",
        "Google (GOOGL)": "GOOGL",
        "Netflix (NFLX)": "NFLX",
        "PepsiCo (PEP)": "PEP",
        "Walmart (WMT)": "WMT",
    },
    "Crypto": {
        "Bitcoin (BTC-USD)": "BTC-USD",
        "Ethereum (ETH-USD)": "ETH-USD",
        "Solana (SOL-USD)": "SOL-USD",
        "Cardano (ADA-USD)": "ADA-USD",
        "Dogecoin (DOGE-USD)": "DOGE-USD",
        "Ripple (XRP-USD)": "XRP-USD",
        "Polkadot (DOT-USD)": "DOT-USD",
        "Binance Coin (BNB-USD)": "BNB-USD",
        "Litecoin (LTC-USD)": "LTC-USD",
        "Shiba Inu (SHIB-USD)": "SHIB-USD",
    },
    "Commodities": {
        "Gold (GC=F)": "GC=F",
        "Silver (SI=F)": "SI=F",
        "Crude Oil (CL=F)": "CL=F",
        "Natural Gas (NG=F)": "NG=F",
        "Corn (ZC=F)": "ZC=F",
        "Soybeans (ZS=F)": "ZS=F",
        "Coffee (KC=F)": "KC=F",
        "Cotton (CT=F)": "CT=F",
        "Wheat (ZW=F)": "ZW=F",
        "Cocoa (CC=F)": "CC=F",
    },
    "ETFs": {
        "S&P 500 ETF (SPY)": "SPY",
        "NASDAQ 100 ETF (QQQ)": "QQQ",
        "ARK Innovation ETF (ARKK)": "ARKK",
        "Vanguard Total Market (VTI)": "VTI",
        "iShares Russell 2000 (IWM)": "IWM",
        "Vanguard Growth ETF (VUG)": "VUG",
        "Vanguard Value ETF (VTV)": "VTV",
        "Energy Select Sector ETF (XLE)": "XLE",
        "Healthcare ETF (XLV)": "XLV",
        "Financials ETF (XLF)": "XLF",
    },
    "Indexes": {
        "S&P 500 (^GSPC)": "^GSPC",
        "Dow Jones (^DJI)": "^DJI",
        "NASDAQ (^IXIC)": "^IXIC",
        "VIX Volatility (^VIX)": "^VIX",
        "FTSE 100 (^FTSE)": "^FTSE",
        "Nikkei 225 (^N225)": "^N225",
        "Hang Seng (^HSI)": "^HSI",
        "CAC 40 (^FCHI)": "^FCHI",
        "DAX (^GDAXI)": "^GDAXI",
        "S&P/TSX (^GSPTSE)": "^GSPTSE",
    }
}


# Page config
st.set_page_config(page_title="IntelliStock Tracker", layout="wide")

st.markdown("## 📈 IntelliStock Tracker")

# Step 1: Select Asset Category
asset_type = st.selectbox("Select Asset Type", list(asset_options.keys()) + ["Other (Manual Input)"])

# Step 2: Select Ticker or Enter Manually
if asset_type != "Other (Manual Input)":
    selected_label = st.selectbox(f"Select {asset_type}", list(asset_options[asset_type].keys()))
    ticker = asset_options[asset_type][selected_label]
else:
    ticker = st.text_input("Enter a ticker manually (e.g., TSLA, BTC-USD)", "").upper()
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

        # --- Historical Chart using Plotly ---
        st.markdown(f"### {ticker} Historical Price (1 Year)")
        # Flatten multi-index columns if needed
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.map(lambda x: x[0])

        fig = px.line(
            df,
            x=df.index,
            y="Close",
            title=f"{ticker} Stock Price",
            labels={"Close": "Price ($)", "index": "Date"}
        )
        st.plotly_chart(fig, use_container_width=True)


        # --- Top Weekly Gainers & Losers ---
    st.markdown("### 🔥 Top Weekly Gainers & Losers")

    # List of popular tickers to compare
    gainer_loser_tickers = [
        "AAPL", "TSLA", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "NFLX",
        "SPY", "QQQ", "ARKK", "XLF", "BTC-USD", "ETH-USD", "SOL-USD", "DOGE-USD",
        "GC=F", "CL=F", "SI=F", "ADA-USD", "XRP-USD", "DIA", "VTI", "IWM", "BND"
    ]

    weekly_changes = []

    for t in gainer_loser_tickers:
        try:
            hist = yf.download(t, period="7d", interval="1d", progress=False)
            if isinstance(hist.columns, pd.MultiIndex):
                hist.columns = hist.columns.map(lambda x: x[0])  # Flatten
            if len(hist) >= 2:
                pct_change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                weekly_changes.append((t, pct_change))
        except:
            pass

    # Sort and separate top gainers/losers
    weekly_changes.sort(key=lambda x: x[1], reverse=True)
    top_gainers = weekly_changes[:5]
    top_losers = weekly_changes[-5:]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Gainers")
        for ticker, change in top_gainers:
            st.markdown(f"<span style='color:green'><strong>{ticker}</strong>: {change:+.2f}%</span>", unsafe_allow_html=True)

    with col2:
        st.markdown("#### 📉 Losers")
        for ticker, change in top_losers:
            st.markdown(f"<span style='color:red'><strong>{ticker}</strong>: {change:+.2f}%</span>", unsafe_allow_html=True)

    
    # Get prediction
    prediction, probability, accuracy = train_predict_model(df)


    # --- AI Prediction (Real) ---
    prediction, probability, accuracy = train_predict_model(df)

    st.markdown("### 🤖 AI Price Movement Prediction")
    icon = "⬆️" if prediction == 1 else "⬇️"
    direction = "Up" if prediction == 1 else "Down"
    color = "green" if prediction == 1 else "red"

    st.markdown(f"**Tomorrow's Prediction:** <span style='color:{color}'>{icon} {direction}</span>", unsafe_allow_html=True)
    st.markdown(f"Model confidence: {probability * 100:.2f}% | Accuracy: {accuracy * 100:.2f}%")

    # --- Investment Projection ---
    st.markdown("### 💰 Investment Projection Based on AI")

    investment_amount = st.number_input("Enter amount to invest (€)", min_value=10, max_value=10000, step=10, value=100)
    forecast_period = st.selectbox("Forecast Horizon", ["6 Months", "1 Year"])

    future_value, diff = project_investment(investment_amount, forecast_period, prediction)
    color = "green" if diff > 0 else "red"

    st.markdown(
        f"**Projected Value in {forecast_period}:** <span style='color:{color}'>€{future_value:,.2f} ({diff:+.2f})</span>",
        unsafe_allow_html=True
    )

    # --- News Sentiment Analysis ---
    st.subheader("🗞️ News Sentiment Analysis")
    try:
        api_key = "f3bc50b5708744aca5cd6c4e8e7ae382"  # Replace with your real key
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





