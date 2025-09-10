import streamlit as st 
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

# Load data
df = pd.read_csv("/Users/jordynpolk/Desktop/Bitcoin/bitcoin_price_Training - Training.csv") 
df['Date'] = pd.to_datetime(df['Date'])  
df = df.sort_values(by="Date")

data = df.sort_index(ascending=False).reset_index(drop=True)
data.set_index('Date', inplace=True)

# Create percentage change column
data["Close_pct_change"] = data["Close"].pct_change() * 100

# Sample for candlestick
bitcoin_sample = data.head(100)

# Streamlit setup
st.set_page_config(page_title="Bitcoin Dashboard", layout="wide")
st.title("Comprehensive Bitcoin Price Analysis Dashboard")

# 1st Plot - Candlestick chart
st.subheader("Bitcoin Candlestick Chart")
trace = go.Candlestick(
    x = bitcoin_sample.index,
    high = bitcoin_sample['High'],
    open = bitcoin_sample['Open'],
    close = bitcoin_sample['Close'],
    low = bitcoin_sample['Low']
)

fig_candle = go.Figure(data=[trace], layout={'title':'Bitcoin Historical Price','xaxis':{'title':'Date'}})
fig_candle.update_layout(xaxis_rangeslider_visible=False)

st.plotly_chart(fig_candle, use_container_width=True)

# 2nd Plot - Percentage Change
st.subheader("Daily Percentage Change in Closing Price")

fig_pct = go.Figure([
    go.Scatter(
        x = data.index,
        y = data["Close_pct_change"],
        mode = "lines"
    )
])
fig_pct.update_layout(
    xaxis_title = "Date",
    yaxis_title = "Percentage Change (%)",
    template = "plotly_white"
)

st.plotly_chart(fig_pct, use_container_width=True)

# 3rd Plot - Bitcoin Price Trends
st.subheader("Bitcoin Price Trends Over Time")
price_type = st.selectbox("Select Price Type:", options=['Open', 'High', 'Low', 'Close'])

fig_trend = go.Figure([
    go.Scatter(
        x = data.index,
        y = data[price_type],
        mode = "lines"
    )
])

fig_trend.update_layout(
    title = f"{price_type} Price Over Time",
    xaxis_title = "Date",
    yaxis_title = "Price (USD)",
    template = "plotly_white"
)

st.plotly_chart(fig_trend, use_container_width=True)


# 4th Plot - Average Plots

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Yearly Average Close Price")
    yearly_avg = data['Close'].resample('YE').mean()
    fig_year = px.bar(
        x = yearly_avg.index.strftime("%Y") ,
        y = yearly_avg.values ,
        labels = {'x': "year", "y" : "Average value"} ,
        title= "Yearly avg trend"
    )

    st.plotly_chart(fig_year, use_container_width = True)

with col2:
    st.subheader("Quarterly Average Close Price")
    quarterly_avg = data['Close'].resample('QE').mean()
    fig_quarter = px.bar(
        x = quarterly_avg.index.strftime("%Y") ,
        y = quarterly_avg.values ,
        labels = {'x': "Quarter", "y" : "Average value"} ,
        title= "Quarterly avg trend"
    )

    st.plotly_chart(fig_quarter, use_container_width = True)


with col3:
    st.subheader("Monthly Average Close Price")
    monthly_avg = data['Close'].resample('ME').mean()
    fig_month = px.bar(
        x = monthly_avg.index.strftime("%Y-%m") ,
        y = monthly_avg.values ,
        labels = {'x': "Month", "y" : "Average value"} ,
        title= "Monthly avg trend"
    )

    st.plotly_chart(fig_month, use_container_width = True)

# 5th Plot - Closing Plots

col4, col5 = st.columns(2)

with col4:
    st.subheader("Closing Price [Normal Scale]")

    fig_normal = px.line(
        data_frame = data ,
        x = data.index,
        y = 'Close' ,
        labels = {'x': "Date", "Close" : "Closing Price"} ,
        title= "Bitcoin Closing Price (Normal Scale)"
    )

    st.plotly_chart(fig_normal, use_container_width = True)


with col5:
    st.subheader("Closing Price [Log Scale]")

    fig_log = px.line(
        data_frame = data ,
        x = data.index,
        y = np.log1p(data['Close']) ,
        labels = {'x': "Date", "Close" : "Log(Closing Price + 1)"} ,
        title= "Bitcoin Closing Price (Log Scale)"
    )

    st.plotly_chart(fig_log, use_container_width = True)

    