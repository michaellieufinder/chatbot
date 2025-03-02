import streamlit as st
from google.oauth2 import id_token
from google.auth.transport import requests
import gspread
from google.auth import default, exceptions
import json

# Google OAuth Client ID (Replace with your actual Client ID from Google Cloud)
GOOGLE_CLIENT_ID = "985468613077-fe816bfledrbp976rr9dr1me82qc89g9.apps.googleusercontent.com"

st.title("Google One Tap Login with Streamlit")

# Session state for login
if "user" not in st.session_state:
    st.session_state.user = None

# Display One Tap Login Button
login_button = st.button("Login with Google")

if login_button:
    # Google One Tap Login
    auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri=http://localhost:8501&response_type=token&scope=email%20profile%20https://www.googleapis.com/auth/spreadsheets.readonly"
    st.markdown(f"[Click here to log in with Google]({auth_url})")

# If the user is logged in, fetch data from Google Sheets
if st.session_state.user:
    st.success(f"Welcome {st.session_state.user['name']}")

    # Authenticate with Google Sheets
    creds, _ = default()
    client = gspread.authorize(creds)

    SHEET_URL = "https://docs.google.com/spreadsheets/d/1fPCnFNmR89giapLRTy1NLMaQaBSGetNRmm13iEfRzcg/edit?gid=0"
    sheet = client.open_by_url(SHEET_URL).sheet1
    data = sheet.get_all_records()
    
    st.dataframe(data)
