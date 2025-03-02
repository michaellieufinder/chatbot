import streamlit as st
import base64
import requests

# Streamlit App Title
st.title("Google Ads API Authentication")

# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Fake Login Button
if not st.session_state.logged_in:
    if st.button("Log In"):
        st.session_state.logged_in = True
        st.success("You are now logged in!")

# Only run authentication after login
if st.session_state.logged_in:
    st.subheader("Fetching Access Token...")

    # Retrieve secrets from Streamlit Secrets
    client_id = st.secrets["google_ads"]["client_id"]
    client_secret = st.secrets["google_ads"]["client_secret"]
    clientCustomerID = st.secrets["google_ads"]["clientCustomerID"]
    developer_token = st.secrets["google_ads"]["developer_token"]
    refresh_token = st.secrets["google_ads"]["refresh_token"]

    # Encode client credentials
    encoded = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8"))

    # Prepare request headers
    headers = {
        'Authorization': f'Basic {encoded.decode("utf-8")}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Prepare request data
    data = {
        'grant_type': 'refresh_token',
        'redirect_uri': "https://www.finder.com.au/",
        'refresh_token': refresh_token
    }

    # Request access token
    with st.spinner("Requesting access token..."):
        response = requests.post('https://www.googleapis.com/oauth2/v3/token', headers=headers, data=data)
        response_data = response.json()

    # Extract access token
    access_token = response_data.get('access_token')

    if access_token:
        st.success("Access Token Generated Successfully!")
        st.code(access_token, language="plaintext")
    else:
        st.error("Failed to generate access token. Check credentials.")

