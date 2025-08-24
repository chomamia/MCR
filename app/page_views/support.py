import streamlit as st

def show():
    """
    Display the "Information" page in the sidebar Setting.

    Behavior:
        - Shows the application title and description.
        - Displays current logged-in user information (username, id).
    """
    st.markdown("### 👤 User Information")
    st.markdown("---")

    # Get user id from session
    user_id = st.session_state.get("id", "Unknown")
    # If you store the username in session or database, fetch it here
    user_name = st.session_state.get("username", f"User {user_id}")
    st.markdown("For any questions please contact the author:")
    st.write(f"**Author Name:** Trịnh Duy Nguyên")
    st.write(f"**Author Email:** trinhduynguyen123@gmail.com")
