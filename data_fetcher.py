import yfinance as yf
import pandas as pd

def get_live_price(ticker):
    stock = yf.Ticker(ticker)
    todays_data = stock.history(period='1d', interval='1m')
    
    if not todays_data.empty:
        latest_price = todays_data['Close'].iloc[-1]
        previous_price = todays_data['Close'].iloc[-2]
        return latest_price, latest_price - previous_price
    else:
        return None, None

def get_historical_data(ticker, period='3mo'):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist
