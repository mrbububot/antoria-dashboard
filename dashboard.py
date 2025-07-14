import streamlit as st
from supabase import create_client
import os

# === Config ===
st.set_page_config(page_title="Antoria Bot", layout="centered")

# === Supabase Setup ===
# === Supabase Setup ===
SUPABASE_URL = "https://flxvuyeisrcqvhontjij.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZseHZ1eWVpc3JjcXZob250amlqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjQ5MzcyMCwiZXhwIjoyMDY4MDY5NzIwfQ.0KnxgLse29zDzNaRDLqHvl16vB3kX2hjVmTRujPOLvo"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# === Binance-Style CSS ===
st.markdown("""
    <style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
    }
    .stTextInput > div > input {
        font-size: 14px !important;
        padding: 10px;
    }
    .stButton > button {
        background-color: #fcd535 !important;
        color: black !important;
        border-radius: 10px;
        font-weight: bold;
        font-size: 14px !important;
        padding: 0.5rem 1.2rem;
    }
    h1 {
        font-size: 12px !important;
        color: #fcd535;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# === Auth Logic ===
if "user" not in st.session_state:
    st.markdown("<h1>Antoria Bot</h1>", unsafe_allow_html=True)
    email = st.text_input("Email", placeholder="Enter email")
    password = st.text_input("Password", type="password", placeholder="Enter password")

    if st.button("Log In / Sign Up"):
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if not user.get("user"):
            # Sign up if login fails
            signup = supabase.auth.sign_up({"email": email, "password": password})
            if signup.get("user"):
                st.session_state["user"] = signup["user"]
                st.success("✅ Account created and logged in!")
                st.rerun()
            else:
                st.error("❌ Failed to log in or sign up.")
        else:
            st.session_state["user"] = user["user"]
            st.success("✅ Logged in successfully!")
            st.rerun()

# === Main App ===
elif "user" in st.session_state:
    st.success(f"Welcome, {st.session_state['user']['email']} 👋")

    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📈 Markets", "🤖 Bot", "👤 Profile"])

    with tab1:
        st.subheader("📊 Antoria Portfolio Summary")
        st.metric("Balance", "£50.00", "+2.5%")
        st.metric("Active Trades", "3")
        st.metric("Today’s P&L", "£3.25")
        st.caption("Bot is watching the markets intelligently.")

    with tab2:
        st.subheader("📈 Market Feed")
        st.write("Live data will appear here...")
        st.info("Coming soon: BTC, ETH, AAPL, EUR/USD")

    with tab3:
        st.subheader("🤖 Bot Settings")
        st.toggle("Enable Auto-Trading", value=True)
        st.selectbox("Risk Level", ["Low", "Medium", "High"])
        st.button("🚀 Start Bot")

    with tab4:
        st.subheader("👤 Profile")
        st.write(f"Email: `{st.session_state['user']['email']}`")
        if st.button("Sign Out"):
            del st.session_state["user"]
            st.rerun()
