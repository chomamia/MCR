import streamlit as st
from database.user import update_password
from utils import get_localized_string
def show():
    """
    Display the "Change Password" page.

    Behavior:
        - Provides input fields for old password, new password, and confirmation.
        - Validates that new password and confirmation match.
        - Shows a success or error message.
    """
    lang = st.session_state.get("lang", "en")
    st.markdown(f"### 🔒 {get_localized_string('change_password', lang)}")
    st.markdown("---")

    # Password input fields
    old_password = st.text_input(get_localized_string("old_password", lang), type="password")
    new_password = st.text_input(get_localized_string("new_password", lang), type="password")
    confirm_password = st.text_input(get_localized_string("confirm_new_password", lang), type="password")

    if st.button(get_localized_string("update_password", lang)):
        if not old_password or not new_password or not confirm_password:
            st.error(get_localized_string("fill_all_fields", lang))
        elif new_password != confirm_password:
            st.error(get_localized_string("password_not_match", lang))
        elif new_password == old_password:
            st.error(get_localized_string("password_same_as_old", lang))
        else:
            user_id = st.session_state.get("id")
            if update_password(user_id, old_password, new_password):
                st.success(get_localized_string("password_updated_success", lang))
                from auth.streamlit_javascript import delete_jwt
                delete_jwt()
            else:
                st.error(get_localized_string("password_update_failed", lang))
