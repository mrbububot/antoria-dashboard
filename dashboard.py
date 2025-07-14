import streamlit as st
from supabase import create_client
import os

# === Streamlit Config ===
st.set_page_config(page_title="Antoria Bot", layout="centered")

# === Supabase Setup (replace these with .env later) ===
SUPABASE_URL = "https://flxvuyeisrcqvhontjij.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZseHZ1eWVpc3JjcXZob250amlqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjQ5MzcyMCwiZXhwIjoyMDY4MDY5NzIwfQ.0KnxgLse29zDzNaRDLqHvl16vB3kX2hjVmTRujPOLvo"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Binance-Style CSS ===
st.markdown("""
    <style>
    .block-container {
        padding-top: 4rem;
        max-width: 350px;
        margin: auto;
    }
    h1 {
        text-align: center;
        font-size: 20px;
        color: #fcd535;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    input {
        font-size: 14px !important;
    }
    .stTextInput > div > input {
        padding: 10px;
        border-radius: 8px;
    }
    .stButton > button {
        background-color: #fcd535 !important;
        color: black !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        width: 100%;
    }
    .custom-links {
        text-align: center;
        margin-top: 1rem;
        font-size: 13px;
    }
    .custom-links a {
        color: #fcd535;
        text-decoration: none;
    }
    .custom-checkbox {
        font-size: 13px;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# === Login Interface ===
if "user" not in st.session_state:
    st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://your-image-url.com/antoria_logo.png' width='150'>
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown("<h1>Antoria Bot</h1>", unsafe_allow_html=True)
    login_as = st.radio("Sign in with:", ["Email", "Phone Number"], horizontal=True, label_visibility="collapsed")
    contact = st.text_input("Email or Phone", placeholder="Enter your email or phone number")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    show_2fa = st.checkbox("2FA Enabled", value=False)
    remember_me = st.checkbox("Remember Me", key="remember")

    if show_2fa:
        twofa = st.text_input("2FA Code", max_chars=6)

    if st.button("Login"):
        auth_data = {"email": contact, "password": password}
        user = supabase.auth.sign_in_with_password(auth_data)
        if not user.get("user"):
            signup = supabase.auth.sign_up(auth_data)
            if signup.get("user"):
                st.success("✅ Account created. You're now logged in!")
                st.session_state["user"] = signup["user"]
                st.rerun()
            else:
                st.error("❌ Failed to log in or sign up.")
        else:
            st.success("✅ Logged in successfully!")
            st.session_state["user"] = user["user"]
            st.rerun()

    st.markdown("""
        <div class="custom-links">
            <a href="#">Forgot Password?</a><br>
            <a href="#">Create Antoria Bot Account</a>
        </div>
    """, unsafe_allow_html=True)

# === Post-login Tabs ===
if "user" in st.session_state:
    st.success(f"Welcome, {st.session_state['user']['email']} 👋")

    tabs = st.tabs(["🏠 Home", "📈 Markets", "🤖 Bot", "👤 Profile"])

    # Home Tab
    with tabs[0]:
        st.subheader("📊 Portfolio Summary")
        st.metric("Balance", "£50.00", "+2.5%")
        st.metric("Active Trades", "3 positions")
        st.metric("Today’s P&L", "£3.25")

    # Markets Tab
    with tabs[1]:
        st.subheader("📈 Live Market Prices")
        st.info("Live price feed coming soon...")

    # Bot Tab
    with tabs[2]:
        st.subheader("🤖 Antoria Bot Settings")
        st.toggle("Enable Auto-Trading", value=True)
        st.selectbox("Risk Level", ["Low", "Medium", "High"])
        st.button("📍 Start Bot")

    # Profile Tab
    with tabs[3]:
        st.subheader("👤 Account Settings")
        st.write(f"Email: `{st.session_state['user']['email']}`")
        if st.button("Sign Out"):
            del st.session_state["user"]
            st.rerun()
