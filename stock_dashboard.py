import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from datetime import date

# Title
st.title("📈 Interactive Stock Price Dashboard")

# Sidebar inputs
st.sidebar.header("Select Stock & Date Range")

# Stock selection
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, INFY.NS):", "AAPL")

# Date range
start_date = st.sidebar.date_input("Start Date", date(2024, 1, 1))
end_date = st.sidebar.date_input("End Date", date(2024, 6, 1))

# Fetch data
try:
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    if stock_data.empty:
        st.error("⚠️ No data found. Please check the ticker symbol or date range.")
    else:
        # Line chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'],
                                 mode='lines', name='Close Price'))

        fig.update_layout(title=f'{ticker} Stock Price',
                          xaxis_title='Date',
                          yaxis_title='Price (USD)',
                          xaxis_rangeslider_visible=True)

        st.plotly_chart(fig)

        # Moving average
        stock_data['MA20'] = stock_data['Close'].rolling(window=20).mean()
        st.subheader("20-Day Moving Average")
        st.line_chart(stock_data[['Close', 'MA20']])

        # Volume
        st.subheader("Volume Traded")
        st.bar_chart(stock_data['Volume'])
except Exception as e:
    st.error(f"❌ Error fetching data: {e}")