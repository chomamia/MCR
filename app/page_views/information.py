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
    st.markdown(f"### 💻 {get_localized_string('application_info', lang)}")
    st.markdown("---")
    st.write(get_localized_string("application_info_desc", lang))
