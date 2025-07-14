import streamlit as st
from PIL import Image

st.set_page_config(page_title="Antoria Bot Login", page_icon="🔐", layout="centered")

# -- Inject custom CSS --
st.markdown("""
    <style>
    .stApp {
        background-color: #0f1115;
        color: white;
        font-family: 'Helvetica Neue', sans-serif;
        padding: 2rem;
    }
    .logo-container {
        text-align: center;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .logo-img {
        width: 90px;
        border-radius: 100%;
    }
    .brand-title {
        font-size: 16px;
        color: #dddddd;
        text-align: center;
        margin-bottom: 2rem;
    }
    label {
        font-size: 14px !important;
        color: #cccccc !important;
    }
    input {
        background-color: #1e1e1e !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    .css-1cpxqw2 {
        color: white !important;
    }
    .login-btn {
        background-color: #fcd535;
        color: #000;
        font-weight: bold;
        width: 100%;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        margin-top: 1rem;
    }
    .social-btn {
        background-color: #1f1f1f;
        color: white;
        padding: 0.6rem;
        border-radius: 10px;
        border: 1px solid #333;
        width: 100%;
        margin-top: 0.5rem;
        text-align: center;
        font-size: 14px;
    }
    .alt-options {
        text-align: center;
        margin: 1.5rem 0 1rem;
        color: #888;
    }
    .footer-links {
        text-align: center;
        margin-top: 2rem;
        font-size: 13px;
        color: #fcd535;
    }
    </style>
""", unsafe_allow_html=True)

# -- Logo & Title --
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
logo = Image.open("A_digital_vector_logo_design_features_the_brand_\"A.png")
st.image(logo, use_column_width=False, width=90)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-title">Antoria Bot</div>', unsafe_allow_html=True)

# -- Login Form --
email = st.text_input("Email / Phone", placeholder="Enter your email or phone")
password = st.text_input("Password", type="password", placeholder="Enter your password")
remember_me = st.checkbox("Remember Me")

if st.button("Login", key="login", help="Secure Login", use_container_width=True):
    st.success("✅ Logged in successfully. (Simulation only)")

# -- Divider --
st.markdown('<div class="alt-options">or</div>', unsafe_allow_html=True)

# -- Social Buttons --
st.markdown('<div class="social-btn">🔒 Continue with Google</div>', unsafe_allow_html=True)
st.markdown('<div class="social-btn">🍎 Continue with Apple</div>', unsafe_allow_html=True)

# -- Footer Links --
st.markdown('<div class="footer-links">Forgot Password? | Create an Antoria Bot Account</div>', unsafe_allow_html=True)
