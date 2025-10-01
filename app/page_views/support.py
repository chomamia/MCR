import streamlit as st
from utils import get_localized_string

def show():
    """
    Display the "Information" page in the sidebar Setting.

    Behavior:
        - Shows the application title and description.
        - Displays current logged-in user information (username, id).
    """
    lang = st.session_state.get("lang", "en")
    st.markdown(f"### 👤 {get_localized_string('user_information', lang)}")
    st.markdown("---")
    user_id = st.session_state.get("id", "Unknown")
    user_name = st.session_state.get("username", f"User {user_id}")
    st.markdown(get_localized_string("contact_author", lang))
    st.write(f"**{get_localized_string('author_name', lang)}** Trịnh Duy Nguyên")
    st.write(f"**{get_localized_string('author_email', lang)}** trinhduynguyen123@gmail.com")
