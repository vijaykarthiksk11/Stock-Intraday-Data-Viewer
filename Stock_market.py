import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta, time as dtime

# 🔹 Helper function to get 1-minute intraday data (last 7 days only)
def get_intraday_data(symbol, selected_date):
    today = datetime.now().date()
    delta = (today - selected_date).days

    if delta > 6:
        return None, "⚠️ 1-minute data available only for the past 7 days."

    ticker = yf.Ticker(symbol)
    data = ticker.history(period="7d", interval="1m")

    if data.empty:
        return None, "❌ No data found for this stock."

    data.index = data.index.tz_localize(None)
    data = data[data.index.date == selected_date]

    if data.empty:
        return None, "⚠️ No trading data for this date (weekend or holiday)."

    return data, None

# 🔹 Function to get historical daily data (up to 5 years)
def get_daily_data(symbol):
    data = yf.download(symbol, period="5y", interval="1d")
    if data.empty:
        return None, "❌ No historical data found."
    return data, None

# 🔹 Function to get price at selected time from intraday data
def get_price_at_time(data, target_time):
    data["time"] = data.index.time
    for i in range(len(data) - 1, -1, -1):
        if data["time"].iloc[i] <= target_time:
            return data["Close"].iloc[i], data.index[i]
    return None, None

# 🔹 Streamlit Page Config
st.set_page_config(page_title="📊 Stock Price Viewer", layout="centered")
st.title("📈 Stock Price Viewer (Intraday + 5-Year History)")

# 🔹 User inputs
symbol = st.text_input("Enter Stock Symbol (e.g., RELIANCE.NS, TCS.NS)", "RELIANCE.NS")

today = datetime.now().date()
min_intraday_date = today - timedelta(days=6)
selected_date = st.date_input(
    "Select Date for Intraday View (Last 7 Days Only)",
    value=today,
    min_value=min_intraday_date,
    max_value=today
)
selected_time = st.time_input("Select Time (for Intraday)", value=dtime(15, 15))

# 🔹 Tabs
tabs = st.tabs([
    "🔍 Price at Specific Time",
    "📊 Intraday Chart",
    "📋 Summary Stats",
    "📅 5-Year Daily Chart"
])

# ─────────────────────────────────────────────────────────────────────
# 🔸 TAB 1: Price at Specific Time (1-minute data)
with tabs[0]:
    st.subheader("🔍 Price at Selected Time (Intraday - 1m)")
    with st.spinner("Fetching intraday data..."):
        intraday_data, error = get_intraday_data(symbol, selected_date)

    if error:
        st.error(error)
    elif intraday_data is not None:
        price, actual_time = get_price_at_time(intraday_data, selected_time)
        if price:
            st.success(f"💹 **{symbol}** at {actual_time.strftime('%Y-%m-%d %H:%M:%S')} was ₹{price:.2f}")
            st.line_chart(intraday_data["Close"])
        else:
            st.warning("⚠️ No data at or before that time.")

# ─────────────────────────────────────────────────────────────────────
# 🔸 TAB 2: Full Intraday Chart
with tabs[1]:
    st.subheader("📊 Full Intraday Chart (1-minute)")
    if intraday_data is not None:
        st.line_chart(intraday_data["Close"])
        st.subheader("🔄 Volume")
        st.area_chart(intraday_data["Volume"])
    else:
        st.info("ℹ️ Select a valid recent date for intraday view.")

# ─────────────────────────────────────────────────────────────────────
# 🔸 TAB 3: Summary Stats
with tabs[2]:
    st.subheader("📋 Summary Statistics (Intraday)")
    if intraday_data is not None:
        st.write(intraday_data.describe())

        open_price = intraday_data["Open"].iloc[0]
        close_price = intraday_data["Close"].iloc[-1]
        change = close_price - open_price
        percent = (change / open_price) * 100

        st.metric("Open", f"₹{open_price:.2f}")
        st.metric("Close", f"₹{close_price:.2f}")
        st.metric("Change", f"₹{change:.2f}", delta=f"{percent:.2f}%")
    else:
        st.info("ℹ️ Summary available only after intraday data is loaded.")

# ─────────────────────────────────────────────────────────────────────
# 🔸 TAB 4: 5-Year Daily Chart
with tabs[3]:
    st.subheader(f"📅 Daily Close Price for Last 5 Years: {symbol}")
    with st.spinner("Fetching historical data..."):
        daily_data, daily_error = get_daily_data(symbol)

    if daily_error:
        st.error(daily_error)
    elif daily_data is not None:
        st.line_chart(daily_data["Close"])

        # Download CSV
        st.subheader("📥 Download Historical Data")
        csv = daily_data.to_csv().encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{symbol}_5year_daily.csv",
            mime='text/csv'
        )
