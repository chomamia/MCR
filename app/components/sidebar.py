import streamlit as st
from auth.streamlit_javascript import delete_jwt, get_token_from_local_storage

def render_sidebar():
    with st.sidebar:
        # st.image("https://via.placeholder.com/100x40?text=LOGO")
        st.markdown("## Management")
        selected = st.radio("Choose option", ["Answer", "Assignment"])
        st.markdown("## Setting")
        st.markdown("- Information\n- Change Password\n- Support")
        logout = st.button("Logout", use_container_width=True)
    if logout:
        delete_jwt()
    return selected
