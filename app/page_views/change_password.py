import streamlit as st
from database.user import update_password
def show():
    """
    Display the "Change Password" page.

    Behavior:
        - Provides input fields for old password, new password, and confirmation.
        - Validates that new password and confirmation match.
        - Shows a success or error message.
    """
    st.markdown("### 🔒 Change Password")
    st.markdown("---")

    # Password input fields
    old_password = st.text_input("Old Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Update Password"):
        if not old_password or not new_password or not confirm_password:
            st.error("⚠️ Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("❌ New password and confirmation do not match.")
        elif new_password == old_password:
            st.error("⚠️ New password cannot be the same as old password.")
        else:
            user_id = st.session_state.get("id")
            if update_password(user_id, old_password, new_password):
                st.success("✅ Password updated successfully!")
                from auth.streamlit_javascript import delete_jwt
                delete_jwt()
            else:
                st.error("❌ Failed to update password. Please check your old password.")
