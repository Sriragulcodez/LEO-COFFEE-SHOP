import streamlit as st
import requests

# -------------------------
# Backend URL
# -------------------------
BASE_URL = "http://127.0.0.1:8000"

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(page_title="Leo Coffee Shop ☕", page_icon="☕", layout="centered")

st.title("Leo Coffee Shop ☕")
st.markdown("Welcome! Manage your coffee membership and enjoy your favorite drinks!")

# -------------------------
# Initialize session state
# -------------------------
if "jwt_token" not in st.session_state:
    st.session_state["jwt_token"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None

# -------------------------
# Sidebar Navigation
# -------------------------
menu = ["Home", "Register", "Login", "Buy Pass", "Get Coffee"]
choice = st.sidebar.selectbox("Menu", menu)

# -------------------------
# Home Page
# -------------------------
if choice == "Home":
    st.subheader("Home")
    if st.session_state["username"]:
        st.info(f"Logged in as: {st.session_state['username']}")
    else:
        st.info("Please login to use the coffee shop services.")

# -------------------------
# Register Page
# -------------------------
elif choice == "Register":
    st.subheader("Register")
    with st.form("register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")
        if submitted:
            if username and password:
                try:
                    response = requests.post(f"{BASE_URL}/register", json={
                        "username": username,
                        "password": password
                    })
                    if response.status_code == 200:
                        st.success(response.json()["message"])
                    else:
                        st.error(response.json()["detail"])
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter both username and password.")

# -------------------------
# Login Page
# -------------------------
elif choice == "Login":
    st.subheader("Login")
    with st.form("login_form"):
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")
        login_submitted = st.form_submit_button("Login")
        if login_submitted:
            if login_username and login_password:
                try:
                    response = requests.post(f"{BASE_URL}/login", json={
                        "username": login_username,
                        "password": login_password
                    })
                    if response.status_code == 200:
                        st.success("Login successful!")
                        st.session_state["jwt_token"] = response.json()["access_token"]
                        st.session_state["username"] = login_username
                        st.info("You can now buy a pass or get coffee.")
                    else:
                        st.error(response.json()["detail"])
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter both username and password.")

# -------------------------
# Buy Monthly Pass Page
# -------------------------
elif choice == "Buy Pass":
    st.subheader("Buy / Renew Monthly Pass")
    if not st.session_state["jwt_token"]:
        st.warning("Please login first to buy a pass.")
    else:
        if st.button("Buy / Renew Pass"):
            token = st.session_state["jwt_token"]
            try:
                response = requests.post(f"{BASE_URL}/buy-pass", params={"token": token})
                if response.status_code == 200:
                    st.success(response.json()["message"])
                else:
                    st.error(response.json()["detail"])
            except Exception as e:
                st.error(f"Error: {e}")

# -------------------------
# Get Coffee Page
# -------------------------
elif choice == "Get Coffee":
    st.subheader("Get Coffee ☕")
    if not st.session_state["jwt_token"]:
        st.warning("Please login first to get coffee.")
    else:
        if st.button("Get Coffee"):
            token = st.session_state["jwt_token"]
            try:
                response = requests.get(f"{BASE_URL}/get-coffee", params={"token": token})
                if response.status_code == 200:
                    data = response.json()
                    st.success(data["message"])
                    st.info(f"Remaining coffees: {data['remaining_coffees']}")
                else:
                    st.error(response.json()["detail"])
            except Exception as e:
                st.error(f"Error: {e}")
