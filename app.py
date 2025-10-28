# Mini-trader-ai-2
from fastapi import FastAPI
import yfinance as yf
import pandas as pd
import numpy as np
import ta
import joblib

app = FastAPI()

def fetch_data(symbol="RELIANCE.NS", period="60d", interval="15m"):
    df = yf.download(symbol, period=period, interval=interval, progress=False)
    df = df.dropna()
    return df

def add_indicators(df):
    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    df['EMA20'] = ta.trend.EMAIndicator(df['Close'], window=20).ema_indicator()
    df['EMA50'] = ta.trend.EMAIndicator(df['Close'], window=50).ema_indicator()
    return df

def generate_signal(df):
    latest = df.iloc[-1]
    if latest['EMA20'] > latest['EMA50'] and latest['RSI'] < 70:
        return "BUY"
    elif latest['EMA20'] < latest['EMA50'] and latest['RSI'] > 30:
        return "SELL"
    else:
        return "HOLD"

@app.get("/")
def home():
    return {"message": "AI Trading Bot Active ✅"}

@app.get("/signal/{symbol}")
def get_signal(symbol: str):
    df = fetch_data(symbol)
    df = add_indicators(df)
    signal = generate_signal(df)
    return {"symbol": symbol, "signal": signal}
