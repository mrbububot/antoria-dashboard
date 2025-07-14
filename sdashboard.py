import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import pandas as pd

# Load env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Antoria Bot", layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #0b0e11;
            color: white;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stTabs [role="tablist"] {
            background-color: #1e2329;
            border-radius: 8px;
        }
        .stTabs [role="tab"] {
            color: #999;
            font-weight: bold;
        }
        .stTabs [aria-selected="true"] {
            color: #f0b90b !important;
            border-bottom: 3px solid #f0b90b !important;
        }
        .stButton>button {
            background-color: #f0b90b;
            color: black;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Auth logic
def login(email, password):
    try:
        result = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if result.user:
            st.session_state.authenticated = True
            st.session_state.user_email = email
            return True
    except Exception as e:
        st.error(f"Login failed: {e}")
    return False

def signup(email, password):
    try:
        supabase.auth.sign_up({"email": email, "password": password})
        st.success("✅ Account created. You can now log in.")
    except Exception as e:
        st.error(f"Signup failed: {e}")

# Login UI
if not st.session_state.authenticated:
    st.title("🔐 Antoria Bot Login")
    login_email = st.text_input("Email")
    login_password = st.text_input("Password", type="password")
    col1, col2 = st.columns(2)
    if col1.button("Log In"):
        login(login_email, login_password)
    if col2.button("Sign Up"):
        signup(login_email, login_password)
    st.stop()

# Sidebar + Main UI
st.sidebar.markdown(f"👤 Logged in as `{st.session_state.user_email}`")
tabs = st.tabs(["🏠 Home", "📈 Markets", "💱 Trade", "💼 Assets"])

with tabs[0]:
    st.title("🏠 Antoria Bot - Home")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Account Balance", "$50.00")
        st.button("🔄 Enable Profit Reinvestment")
    with col2:
        st.metric("Trailing Stop-Loss", "Enabled ✅")
        st.button("⚙️ Disable Trailing Stop")
    st.info("📊 Antoria Bot is running in Paper Mode using Binance Testnet.")

with tabs[1]:
    st.title("📈 Markets")
    st.markdown("🔍 Live price feeds coming soon...")
    st.markdown("""
    | Symbol | Price | Change | Trend |
    |--------|-------|--------|-------|
    | BTC/USDT | $30,100 | +1.2% | 🟢 Bullish |
    | ETH/USDT | $1,950 | -0.3% | 🔴 Bearish |
    | AAPL     | $188.90 | +0.4% | 🟢 Bullish |
    | TSLA     | $225.10 | -1.1% | 🔴 Bearish |
    """)

with tabs[2]:
    st.title("💱 Trade")
    st.write("📍 Manual trade triggers coming soon...")
    st.button("📉 Force SELL Now")
    st.button("📈 Force BUY Now")
    st.warning("This will be replaced with live strategy toggles and override controls.")

with tabs[3]:
    st.title("💼 Assets")
    st.metric("Total Profit", "$43.25")
    st.metric("Win Rate", "68%")
    st.metric("Trade Count", "29")
    st.markdown("📑 **Trade Log:** (sample)")
    st.dataframe(pd.DataFrame([
        {"Time": "2025-07-14 13:00", "Pair": "BTC/USDT", "Side": "Buy", "Profit": "+$3.50"},
        {"Time": "2025-07-14 12:00", "Pair": "ETH/USDT", "Side": "Sell", "Profit": "-$0.90"},
        {"Time": "2025-07-14 11:45", "Pair": "AAPL", "Side": "Buy", "Profit": "+$5.00"}
    ]))
