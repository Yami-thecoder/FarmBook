import streamlit as st
import os
import base64
from api import register_user, login_user

st.set_page_config(page_title="Welcome to FarmBook", page_icon="🌾", layout="centered")

st.markdown(
    """
    <style>
        .stApp {background-color: #f0fff0;}
    </style>
    """,
    unsafe_allow_html=True
)

# Custom Styling to Hide Sidebar and Center Content
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {display: none;}
        .tagline {font-size: 1.2em; font-weight: bold; margin-bottom: 20px; color: #2E7D32; text-align: center;}
        .form-container {display: flex; flex-direction: column; align-items: flex-start; max-width: 300px; margin-left: auto; margin-right: auto;}
        .stButton>button {background-color: #2E7D32 !important; color: white !important; border-radius: 5px;}
        .left-align {text-align: left !important;}
    </style>
    """,
    unsafe_allow_html=True
)

# Apply the background color
# st.markdown(
#     f"""
#     <style>
#         .stApp {{
#             background-color: #f0fff0; /* Light green background */
#         }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Streamlit UI
st.markdown("<h1 style='text-align: center;'>Welcome to FarmBook 🌱</h1>", unsafe_allow_html=True)
st.markdown("<div class='tagline'>Your personal farming companion</div>", unsafe_allow_html=True)

# Toggle between Login and Register
menu = st.radio("New here? Register to start your FarmBook journey!", ["Login", "Register"], horizontal=True)

if menu == "Login":
    st.markdown("<div class='left-align'>", unsafe_allow_html=True)
    st.subheader("Login")
    with st.container():
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_btn"):
            response, status = login_user(email, password)
            if status == 200:
                st.session_state["jwt_token"] = response["access_token"]
                st.success("Login successful! Redirecting to dashboard...")
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Register":
    st.markdown("<div class='left-align'>", unsafe_allow_html=True)
    st.subheader("Register")
    with st.container():
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        username = st.text_input("Username", key="register_username")
        reg_email = st.text_input("Email", key="register_email")
        reg_password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        if st.button("Register", key="register_btn"):
            if reg_password == confirm_password:
                response, status = register_user(username, reg_email, reg_password)
                if status == 201:
                    st.success("Registration successful! Please log in.")
                else:
                    st.error(response.get("error", "Registration failed."))
            else:
                st.error("Passwords do not match.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Redirect if logged in
if "jwt_token" in st.session_state:
    st.switch_page("streamlit_home.py")
    st.rerun()
