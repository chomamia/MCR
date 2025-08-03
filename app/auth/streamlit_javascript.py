import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager


cookies = EncryptedCookieManager(
    prefix="app_",  # optional
    password="Pass1234!"
)

if not cookies.ready():
    st.stop()

def save_token_to_local_storage(token: str):
    cookies["jwt_token"] = token
    cookies.save()

def get_token_from_local_storage():
    if "jwt_token" in cookies:
        return cookies["jwt_token"]
    else:
        return ""
    
def delete_jwt():
    cookies["jwt_token"] = ""
    cookies.save()
    st.rerun()

