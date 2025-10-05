
# 📈 Stock Intraday Data Viewer (India)

This Streamlit app allows you to fetch and analyze **1-minute intraday stock data** for Indian stocks (from Yahoo Finance via `yfinance`).  
It includes tools to view the **price at a specific time**, **full intraday chart**, and **summary statistics** for the selected day.

---

## 🚀 Features

- 🔎 Get stock price at a specific time (within the last 7 days)
- 📊 Interactive intraday line chart and volume chart
- 📋 Summary statistics (Open, Close, Change %, etc.)
- ⚡ Powered by Yahoo Finance (`yfinance`)

---


# 🔍 Example Usage

Symbol: RELIANCE.NS, TCS.NS, INFY.NS

Valid Date Range: Only the last 7 calendar days

Valid Time: Between 09:15 and 15:30 IST (Indian market hours)

# ⚠️ Limitations

Intraday (1-minute) data is only available for last 7 days from Yahoo Finance

Market holidays and weekends will return no data

App is focused on Indian stock symbols (use .NS suffix)

# 📦 Dependencies

streamlit

yfinance

pandas

datetime
