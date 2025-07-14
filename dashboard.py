import streamlit as st
from supabase import create_client
import os
import base64

# === CONFIG ===
st.set_page_config(page_title="Antoria Bot", layout="centered")

# === SUPABASE ===
SUPABASE_URL = "https://flxvuyeisrcqvhontjij.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZseHZ1eWVpc3JjcXZob250amlqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjQ5MzcyMCwiZXhwIjoyMDY4MDY5NzIwfQ.0KnxgLse29zDzNaRDLqHvl16vB3kX2hjVmTRujPOLvo"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# === LOAD LOGO ===
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64_image("antoria_logo.png")
st.markdown(
    f"<div style='text-align:center;margin-bottom:-50px'><img src='data:image/png;base64,{logo_base64}' width='280'></div>",
    unsafe_allow_html=True
)

# === STYLE ===
st.markdown("""
<style>
.block-container { padding-top: 2rem; max-width: 350px; margin: auto; }
h1 { text-align: center; font-size: 14px; color: #fcd535; font-weight: 600; margin-bottom: 0.5rem; }
.stTextInput input { font-size: 14px; padding: 10px; border-radius: 8px; }
.stButton > button { background-color: #fcd535 !important; color: black !important; font-weight: bold; border-radius: 8px; padding: 0.6rem 1.5rem; width: 100%; }
.custom-links { text-align: center; margin-top: 1rem; font-size: 13px; }
.custom-links a { color: #fcd535; text-decoration: none; cursor: pointer; }
</style>
""", unsafe_allow_html=True)

# === LOGIN/REGISTER/FORGOT ===
if "user" not in st.session_state:
    st.markdown("<h1>Titanic & Master</h1>", unsafe_allow_html=True)

    auth_mode = st.radio("Choose", ["Login", "Create Account", "Forgot Password"], horizontal=True)

    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if auth_mode == "Login":
        if st.button("Log In"):
            try:
                result = supabase.auth.sign_in_with_password({"email": email, "password": password})
                if result.get("user"):
                    st.success("✅ Logged in!")
                    st.session_state["user"] = result["user"]
                    st.rerun()
                else:
                    st.error("❌ Incorrect email or password.")
            except Exception as e:
                st.error(f"Login failed: {e}")

    elif auth_mode == "Create Account":
        if st.button("Create Antoria Bot Account"):
            try:
                result = supabase.auth.sign_up({"email": email, "password": password})
                if result.get("user"):
                    st.success("✅ Account created! Confirm your email.")
                    st.session_state["user"] = result["user"]
                    st.rerun()
                else:
                    st.error("❌ Failed to create account.")
            except Exception as e:
                st.error(f"Sign-up failed: {e}")

    elif auth_mode == "Forgot Password":
        if st.button("Send Reset Link"):
            try:
                supabase.auth.reset_password_email(email)
                st.success("📧 Reset link sent to your email.")
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.success(f"Welcome, {st.session_state['user']['email']} 👋")
    if st.button("Sign Out"):
        del st.session_state["user"]
        st.rerun()
