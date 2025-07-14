import streamlit as st
from supabase import create_client
import os
import pyotp
import qrcode
from io import BytesIO
from PIL import Image

# === Supabase Setup ===
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Streamlit Config ===
st.set_page_config(page_title="Antoria Bot", layout="centered")

# === Custom Binance-style CSS ===
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
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
    a {
        color: #fcd535;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# === Antoria Logo ===
st.image("/mnt/data/A_digital_vector_logo_design_features_the_brand_A.png, width=80)
st.markdown("<h1>Antoria Bot</h1>", unsafe_allow_html=True)

# === Auth + 2FA ===
if "user" not in st.session_state:
    email = st.text_input("Email", placeholder="Enter your email")
    phone = st.text_input("Phone Number", placeholder="Enter your phone")
    identifier = st.text_input("Email or Phone", placeholder="Use either to log in")
    password = st.text_input("Password", type="password", placeholder="Enter password")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("[Forgot Password?](#)")
    with col2:
        st.markdown("[Create Antoria Bot Account](#)")

    if st.button("Log In / Create Account"):
        auth_user = supabase.auth.sign_in_with_password({"email": identifier, "password": password})
        if not auth_user.get("user"):
            new_user = supabase.auth.sign_up({"email": email, "password": password})
            if new_user.get("user"):
                st.session_state.user = new_user["user"]
                st.session_state.verified = False
        else:
            st.session_state.user = auth_user["user"]
            st.session_state.verified = False
        st.rerun()

# === 2FA Setup ===
if "user" in st.session_state and not st.session_state.get("verified"):
    user_id = st.session_state.user["id"]
    totp_secret = pyotp.random_base32()
    supabase.table("2fa_secrets").upsert({"user_id": user_id, "secret": totp_secret}).execute()
    
    otp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(name=st.session_state.user["email"], issuer_name="Antoria Bot")
    qr = qrcode.make(otp_uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    st.image(buffer.getvalue(), caption="Scan this QR code with Google Authenticator")
    
    code = st.text_input("Enter the 6-digit code from your app")
    if st.button("Verify 2FA"):
        record = supabase.table("2fa_secrets").select("secret").eq("user_id", user_id).execute()
        secret = record.data[0]['secret']
        if pyotp.TOTP(secret).verify(code):
            st.session_state.verified = True
            st.success("✅ 2FA Verified!")
            st.rerun()
        else:
            st.error("❌ Invalid code. Please try again.")

# === Dashboard Tabs ===
if "user" in st.session_state and st.session_state.get("verified"):
    tabs = st.tabs(["🏠 Home", "📈 Markets", "🤖 Bot", "👤 Profile"])

    with tabs[0]:
        st.subheader("📊 Antoria Portfolio Summary")
        st.metric("Balance", "£50.00", "+2.5%")
        st.metric("Active Trades", "3 positions")
        st.metric("Today’s P&L", "£3.25")
        st.write("💡 Your AI Bot is learning and adapting...")

    with tabs[1]:
        st.subheader("📈 Live Market Prices")
        st.write("🔄 Coming next: BTC/GBP, ETH/GBP, AAPL, EUR/USD...")
        st.info("Live price feed in progress...")

    with tabs[2]:
        st.subheader("🤖 Antoria Bot Settings")
        st.toggle("Enable Auto-Trading", value=True)
        st.selectbox("Risk Level", ["Low", "Medium", "High"])
        st.button("📍 Start Bot")

    with tabs[3]:
        st.subheader("👤 Account Settings")
        st.write(f"Email: `{st.session_state['user']['email']}`")
        if st.button("Sign Out"):
            del st.session_state.user
            st.rerun()
