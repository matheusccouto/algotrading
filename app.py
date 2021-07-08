"""Visualize brazilian stock prices."""

import datetime

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st


@st.cache(show_spinner=False)
def get_all_stocks():
    """Get list with all stocks."""
    url = r"https://brapi.ga/api/quote/list"
    response = requests.get(url)
    return [stock["stock"] for stock in response.json()["stocks"]]


@st.cache(show_spinner=False)
def get_stock_time_history(name):
    """Get stock time history."""
    # Get stock data
    url = r"https://brapi.ga/api/quote/"
    response = requests.get(url + name, params=dict(interval="1d", range="1y"))
    results = response.json()["results"][0]

    time_history = results["historicalDataPrice"]

    for day in time_history:
        day["date"] = datetime.datetime.fromtimestamp(day["date"])

    return pd.DataFrame(time_history)


def plot_candlesticks(time_history, title):
    """Plot candlesticks."""
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=time_history["date"],
                open=time_history["open"],
                high=time_history["high"],
                low=time_history["low"],
                close=time_history["close"],
            )
        ]
    )
    fig.update_layout(title=title, xaxis_rangeslider_visible=False, template="simple_white", plot_bgcolor='rgba(0,0,0,0)')
    return st.plotly_chart(fig)


st.set_page_config(page_title="Stock Viz", page_icon=":chart_with_upwards_trend:")
st.title(":chart_with_upwards_trend:Stock Viz")

# Get all stocks available.
all_stocks_names = get_all_stocks()

# Selectbox for choosing which one to plot.
stock_name = st.selectbox("Stock", options=all_stocks_names)

# Get the selected stock time history.
data = get_stock_time_history(stock_name)

# Plot candlesticks.
plot_candlesticks(data, title=stock_name)
