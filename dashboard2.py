import streamlit as st
from supabase import create_client
import os
from PIL import Image

# === Streamlit Config ===
st.set_page_config(page_title="Antoria Bot", layout="centered")

# === Supabase Setup ===
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Custom Binance-style CSS ===
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
        padding: 0.5rem 1.2rem;
        font-size: 14px !important;
    }
    h1 {
        font-size: 10px !important;
        color: #fcd535;
        text-align: center;
        margin-bottom: 1rem;
    }
    .logo-container {
        text-align: center;
        margin-bottom: 1rem;
    }
    .links {
        text-align: center;
        font-size: 12px;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# === Display Logo ===
logo_path = "A_digital_vector_logo_design_features_the_brand_\"A.png"
if os.path.exists(logo_path):
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(logo_path, width=100)
    st.markdown('</div>', unsafe_allow_html=True)

# === Login/Signup Form ===
if "user" not in st.session_state:
    st.markdown("<h1>Antoria Bot</h1>", unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    remember = st.checkbox("Remember me")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="links"><a href="#">Forgot Password?</a></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="links"><a href="#">Create Account</a></div>', unsafe_allow_html=True)

    if st.button("Login"):
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if not user.get("user"):
            signup = supabase.auth.sign_up({"email": email, "password": password})
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

# === Logged In Interface ===
if "user" in st.session_state:
    st.success(f"Welcome, {st.session_state['user']['email']} 👋")

    tabs = st.tabs(["🏠 Home", "📈 Markets", "🤖 Bot", "👤 Profile"])

    # === Home Tab ===
    with tabs[0]:
        st.subheader("📊 Antoria Portfolio Summary")
        st.metric("Balance", "£50.00", "+2.5%")
        st.metric("Active Trades", "3 positions")
        st.metric("Today’s P&L", "£3.25")
        st.write("💡 Your AI Bot is learning and adapting...")

    # === Markets Tab ===
    with tabs[1]:
        st.subheader("📈 Live Market Prices")
        st.write("🔄 Coming next: BTC/GBP, ETH/GBP, AAPL, EUR/USD...")
        st.info("Live price feed in progress...")

    # === Bot Tab ===
    with tabs[2]:
        st.subheader("🤖 Antoria Bot Settings")
        st.toggle("Enable Auto-Trading", value=True)
        st.selectbox("Risk Level", ["Low", "Medium", "High"])
        st.button("📍 Start Bot")

    # === Profile Tab ===
    with tabs[3]:
        st.subheader("👤 Account Settings")
        st.write(f"Email: `{st.session_state['user']['email']}`")
        if st.button("Sign Out"):
            del st.session_state["user"]
            st.rerun()
