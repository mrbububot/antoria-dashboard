import streamlit as st
from supabase import create_client
import os
import base64

# === Streamlit Config ===
st.set_page_config(page_title="Antoria Bot", layout="centered")

# === Supabase Setup ===
SUPABASE_URL = "https://flxvuyeisrcqvhontjij.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZseHZ1eWVpc3JjcXZob250amlqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjQ5MzcyMCwiZXhwIjoyMDY4MDY5NzIwfQ.0KnxgLse29zDzNaRDLqHvl16vB3kX2hjVmTRujPOLvo"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Local image loader ===
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64_image("antoria_logo.png")
st.markdown(f"""
    <div style='text-align: center; padding-top: -16rem; margin-bottom: -80px;'>
        <img src='data:image/png;base64,{logo_base64}' width='300'>
    </div>
""", unsafe_allow_html=True)

# === Custom CSS ===
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

# === Handle password reset from email link ===
query_params = st.query_params
if "access_token" in query_params:
    access_token = query_params["access_token"]
    st.markdown("### 🔐 Reset Your Password")
    new_pw = st.text_input("New password", type="password")
    confirm_pw = st.text_input("Confirm password", type="password")

    if new_pw and confirm_pw:
        if new_pw == confirm_pw:
            try:
                supabase.auth.session().access_token = access_token
                supabase.auth.update_user({"password": new_pw})
                st.success("✅ Password reset successful. Please login.")
            except Exception:
                st.error("❌ Failed to reset password.")
        else:
            st.warning("⚠️ Passwords do not match.")
    st.stop()

# === Login UI ===
if "user" not in st.session_state:
    st.markdown("<h1 style='margin-bottom: -4rem;'>Master & Titanic</h1>", unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="Enter your email")
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
            except Exception as e:
                st.error("❌ Login failed. Please check your credentials.")

    elif login_mode == "Sign Up":
        if not contact or not password:
            st.warning("⚠️ Please enter email and password.")
        else:
            try:
                res = supabase.auth.sign_up({"email": contact, "password": password})
                st.success("✅ Sign-up successful! Please check your email for confirmation.")
                st.rerun()
            except Exception as e:
                st.error("❌ Sign-up failed. Ensure your email is valid and not already used.")


if st.button(login_mode):
    if login_mode == "Forgot Password":
        if not contact:
            st.warning("⚠️ Please enter your email.")
        else:
            try:
                supabase.auth.reset_password_email(contact)
                st.info("📨 Password reset email sent. Check your inbox.")
            except Exception:
                st.error("❌ Failed to send reset email. Please try again.")
    else:
        if not contact or not password:
            st.warning("⚠️ Please enter email and password.")
        else:
            try:
                if login_mode == "Login":
                    res = supabase.auth.sign_in_with_password({"email": contact, "password": password})
                    st.session_state["user"] = res.user
                    st.success("✅ Logged in successfully!")
                    st.rerun()
                elif login_mode == "Sign Up":
                    res = supabase.auth.sign_up({"email": contact, "password": password})
                    st.success("✅ Sign-up successful. Please check your email to verify.")
                    st.rerun()
            except Exception as e:
                st.error("❌ Could not complete request. Make sure your email is valid.")

        if login_mode == "Forgot Password":
            if not email:
                st.warning("⚠️ Please enter your email.")
            else:
                try:
                    supabase.auth.reset_password_email(email)
                    st.info("📨 Password reset email sent. Check your inbox.")
                except Exception:
                    st.error("❌ Failed to send reset email. Please try again.")
        else:
            if not email or not password:
                st.warning("⚠️ Please enter email and password.")
            else:
                try:
                    if login_mode == "Login":
                        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state["user"] = res.user
                        st.success("✅ Logged in successfully!")
                        st.rerun()
                    elif login_mode == "Sign Up":
                        res = supabase.auth.sign_up({"email": email, "password": password})
                        st.success("✅ Sign-up successful. Please check your email to verify.")
                        st.rerun()
                except Exception:
                    st.error("❌ Could not complete request. Make sure your email is valid.")

                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state["user"] = res.user
                    st.success("✅ Logged in successfully!")
                    st.rerun()

                elif login_mode == "Sign Up":
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    st.success("✅ Sign-up successful. Please check your email to verify.")
                    st.rerun()

                elif login_mode == "Forgot Password":
                    supabase.auth.reset_password_email(email)
                    st.info("📨 Password reset email sent. Check your inbox.")
            except Exception:
                st.error("❌ Could not complete request. Make sure your email is valid.")

    st.markdown("""
        <div class="custom-links">
            <a href="#">Forgot Password?</a><br>
            <a href="#">Create Antoria Bot Account</a>
        </div>
    """, unsafe_allow_html=True)

# === Post-login UI ===
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
