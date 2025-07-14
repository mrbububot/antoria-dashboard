import streamlit as st
from supabase import create_client
import os
import base64

# === Streamlit Config ===
st.set_page_config(page_title="Antoria Bot", layout="centered")

# === Supabase Setup (update with env later) ===
SUPABASE_URL = "https://flxvuyeisrcqvhontjij.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZseHZ1eWVpc3JjcXZob250amlqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjQ5MzcyMCwiZXhwIjoyMDY4MDY5NzIwfQ.0KnxgLse29zDzNaRDLqHvl16vB3kX2hjVmTRujPOLvo"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Load logo ===
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64_image("antoria_logo.png")  # Ensure logo file exists

# === Display centered logo ===
st.markdown(
    f"""
    <div style='text-align: center; padding-top: -16rem; margin-bottom: -80px;'>
        <img src='data:image/png;base64,{logo_base64}' width='300'>
    </div>
    """,
    unsafe_allow_html=True
)

# === Binance-style CSS ===
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        max-width: 350px;
        margin: auto;
    }
    h1 {
        text-align: center;
        font-size: 5px;
        color: #fcd535;
        font-weight: 500;
        margin-bottom: 1rem;
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
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# === Login Panel ===
if "user" not in st.session_state:
    st.markdown("<h1 style='margin-bottom: -4rem;'>Master & Titanic</h1>", unsafe_allow_html=True)

    contact = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    login_mode = st.radio("Action:", ["Login", "Sign Up", "Forgot Password"], horizontal=True)

    if st.button(login_mode):
        if login_mode == "Forgot Password":
            if not contact:
                st.warning("⚠️ Please enter your email.")
            else:
                try:
                    supabase.auth.reset_password_email(contact)
                    st.success("📨 Password reset email sent. Check your inbox.")
                except Exception:
                    st.error("❌ Failed to send reset email. Please try again.")

        elif login_mode == "Login":
            if not contact or not password:
                st.warning("⚠️ Please enter email and password.")
            else:
                try:
                    res = supabase.auth.sign_in_with_password({"email": contact, "password": password})
                    st.session_state["user"] = res.user
                    st.success("✅ Logged in successfully!")
                    st.rerun()
                except Exception:
                    st.error("❌ Login failed. Please check your credentials.")

        elif login_mode == "Sign Up":
            if not contact or not password:
                st.warning("⚠️ Please enter email and password.")
            else:
                try:
                    res = supabase.auth.sign_up({"email": contact, "password": password})
                    st.success("✅ Sign-up successful! Please check your email for confirmation.")
                    st.rerun()
                except Exception:
                    st.error("❌ Sign-up failed. Ensure your email is valid and not already used.")

# === Logged-In Dashboard ===
if "user" in st.session_state:
    st.success(f"Welcome, {st.session_state['user']['email']} 👋")

    tabs = st.tabs(["🏠 Home", "📈 Markets", "🤖 Bot", "👤 Profile"])

    with tabs[0]:
        st.subheader("📊 Portfolio Summary")
        st.metric("Balance", "£50.00", "+2.5%")
        st.metric("Active Trades", "3 positions")
        st.metric("Today’s P&L", "£3.25")

    with tabs[1]:
        st.subheader("📈 Live Market Prices")
        st.info("Live price feed coming soon...")

    with tabs[2]:
        st.subheader("🤖 Antoria Bot Settings")
        st.toggle("Enable Auto-Trading", value=True)
        st.selectbox("Risk Level", ["Low", "Medium", "High"])
        st.button("📍 Start Bot")

    with tabs[3]:
        st.subheader("👤 Account Settings")
        st.write(f"Email: `{st.session_state['user']['email']}`")
        if st.button("Sign Out"):
            del st.session_state["user"]
            st.rerun()
