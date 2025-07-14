import streamlit as st
from supabase import create_client
import base64

# === Streamlit Config ===
st.set_page_config(page_title="Antoria Bot", layout="centered")

# === Supabase Setup ===
SUPABASE_URL = "https://flxvuyeisrcqvhontjij.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZseHZ1eWVpc3JjcXZob250amlqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjQ5MzcyMCwiZXhwIjoyMDY4MDY5NzIwfQ.0KnxgLse29zDzNaRDLqHvl16vB3kX2hjVmTRujPOLvo"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Logo Loader ===
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_image("antoria_logo.png")
st.markdown(
    f"""
    <div style='text-align: center; padding-top: -16rem; margin-bottom: -80px;'>
        <img src='data:image/png;base64,{logo_base64}' width='300'>
    </div>
    """,
    unsafe_allow_html=True
)

# === CSS Styling ===
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

# === LOGIN ===
if "user" not in st.session_state:
    st.markdown("<h1 style='margin-bottom: -4rem;'>Master & Titanic</h1>", unsafe_allow_html=True)

    login_as = st.radio("Sign in with:", ["Email", "Phone Number"], horizontal=True, label_visibility="collapsed")
    contact = st.text_input("Email or Phone", placeholder="Enter your email or phone number")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    show_2fa = st.checkbox("2FA Enabled", value=False)
    remember_me = st.checkbox("Remember Me", key="remember")

    if show_2fa:
        twofa = st.text_input("2FA Code", max_chars=6)

    login_mode = st.radio("Action:", ["Login", "Sign Up", "Forgot Password"], horizontal=True)

    if login_mode == "Login":
        if st.button("Login"):
            auth_data = {"password": password}
            if "@" in contact and "." in contact:
                auth_data["email"] = contact
            else:
                auth_data["phone"] = contact

            try:
                user = supabase.auth.sign_in_with_password(auth_data)
                if user.get("user"):
                    st.success("✅ Logged in successfully!")
                    st.session_state["user"] = user["user"]
                    st.rerun()
                else:
                    st.error("❌ Login failed. Check your credentials.")
            except Exception as e:
                st.error("❌ An error occurred during authentication.")

    elif login_mode == "Sign Up":
        if st.button("Sign Up"):
            auth_data = {"password": password}
            if "@" in contact and "." in contact:
                auth_data["email"] = contact
            else:
                auth_data["phone"] = contact

            try:
                signup = supabase.auth.sign_up(auth_data)
                if signup.get("user"):
                    st.success("✅ Account created. You're now logged in!")
                    st.session_state["user"] = signup["user"]
                    st.rerun()
                else:
                    st.error("❌ Sign-up failed. Please try again.")
            except Exception as e:
                st.error("❌ Could not sign up. Ensure email/phone is valid.")

    elif login_mode == "Forgot Password":
        if st.button("Reset Password"):
            try:
                supabase.auth.reset_password_email(contact)
                st.success("📧 A reset link has been sent to your email.")
            except Exception as e:
                st.error("❌ Could not send reset email. Try again.")

# === DASHBOARD ===
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
