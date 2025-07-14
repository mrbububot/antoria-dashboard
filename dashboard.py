import streamlit as st
from supabase import create_client
import os
import base64

# === Streamlit Config ===
st.set_page_config(page_title="Antoria Bot", layout="centered")

# === Supabase Setup (will move to .env later) ===
SUPABASE_URL = "https://flxvuyeisrcqvhontjij.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZseHZ1eWVpc3JjcXZob250amlqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjQ5MzcyMCwiZXhwIjoyMDY4MDY5NzIwfQ.0KnxgLse29zDzNaRDLqHvl16vB3kX2hjVmTRujPOLvo"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Local image loader for logo ===
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# === Display centered logo ===
logo_base64 = get_base64_image("antoria_logo.png")  # Make sure this file exists in same folder
st.markdown(
    f"""
    <div style='text-align: center; padding-top: -16rem; margin-bottom: -80px;'>
        <img src='data:image/png;base64,{logo_base64}' width='300'>
    </div>
    """,
    unsafe_allow_html=True
)

# === Binance-Style CSS ===
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

# === Login Interface ===
if "user" not in st.session_state:
    st.markdown(
        "<h1 style='margin-bottom: -4rem;'>Master & Titanic</h1>",
        unsafe_allow_html=True
    )

    login_as = st.radio("Sign in with:", ["Email", "Phone Number"], horizontal=True, label_visibility="collapsed")
    contact = st.text_input("Email or Phone", placeholder="Enter your email or phone number")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    show_2fa = st.checkbox("2FA Enabled", value=False)
    remember_me = st.checkbox("Remember Me", key="remember")

    if show_2fa:
        twofa = st.text_input("2FA Code", max_chars=6)

    login_mode = st.radio("Action:", ["Login", "Sign Up", "Forgot Password"], horizontal=True)

    if st.button("Login"):
        # Determine if input is email or phone
        auth_data = {"password": password}
        if "@" in contact:
            auth_data["email"] = contact
        else:
            # NOTE: Supabase requires phone auth to be enabled (see warning below)
            auth_data["phone"] = contact

        try:
            user = supabase.auth.sign_in_with_password(auth_data)
            if user and user.get("user"):
                st.success("✅ Logged in successfully!")
                st.session_state["user"] = user["user"]
                st.rerun()
            else:
                raise Exception("User not found")
        except Exception as login_error:
            try:
                signup = supabase.auth.sign_up(auth_data)
                if signup and signup.get("user"):
                    st.success("✅ Account created and logged in!")
                    st.session_state["user"] = signup["user"]
                    st.rerun()
                else:
                    st.error("❌ Sign-up failed.")
            except Exception as signup_error:
                st.error(f"❌ An error occurred during authentication.")

# === Post-login Tabs ===
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
