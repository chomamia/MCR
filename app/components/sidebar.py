from streamlit_option_menu import option_menu
import streamlit as st

def render_sidebar():
    with st.sidebar:
        # st.markdown("<div class='mcr-logo'>Multiple Choice Reader</div>", unsafe_allow_html=True)

        selected = option_menu(
            menu_title="MCR Menu",  
            options=["Answer", "Assignment", "Information", "Change Password", "Support"],  
            icons=["file-earmark-text", "pencil", "info-circle", "lock", "question-circle"],  
            menu_icon="cast",  
            default_index=0,
        )

        if st.button("Logout", use_container_width=True):
            from auth.streamlit_javascript import delete_jwt
            delete_jwt()

    return selected
