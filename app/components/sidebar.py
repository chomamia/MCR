import streamlit as st
from auth.streamlit_javascript import delete_jwt, get_token_from_local_storage

def render_sidebar():
    # Inject CSS for custom styling
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #F4F4F4;
            color: #333333;
            padding-top: 1rem;
            border-right: 1px solid #E0E0E0;
        }
        /* Logo */
        .mcr-logo {
            font-size: 1.8rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 1.5rem;
            letter-spacing: 2px;
            color: #1E88E5;
        }
        /* Section title */
        .sidebar-section {
            font-size: 1.1rem;
            font-weight: 600;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
            color: #555555;
        }
        /* Radio buttons */
        div[role='radiogroup'] label {
            padding: 0.5rem 0.6rem;
            border-radius: 8px;
            transition: background-color 0.2s;
            color: #333333 !important;
        }
        div[role='radiogroup'] label:hover {
            background-color: #E3F2FD;
        }
        .stButton button {
            background-color: #90CAF9;
            color: #ffffff;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 0;
            font-weight: bold;
        }
        .stButton button:hover {
            background-color: #64B5F6;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        # Logo
        st.markdown("<div class='mcr-logo'>Multiple Choice Reader</div>", unsafe_allow_html=True)
        # Management section
        st.markdown("<div class='sidebar-section'>Management</div>", unsafe_allow_html=True)
        selected = st.radio(
            "     ",
            ["Answer", "Assignment"],
            index=["Answer", "Assignment"].index(st.session_state["current_page"])
        )
        # Setting section
        st.markdown("<div class='sidebar-section'>Setting</div>", unsafe_allow_html=True)
        st.markdown("- Information\n- Change Password\n- Support")
        # Logout button
        logout = st.button("Logout", use_container_width=True)

    if logout:
        delete_jwt()
    return selected