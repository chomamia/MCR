import streamlit as st

def render_sidebar():
    with st.sidebar:
        # st.image("https://via.placeholder.com/100x40?text=LOGO")
        st.markdown("## Management")
        selected = st.radio("Choose option", ["Answer", "Assignment"])
        st.markdown("## Setting")
        st.markdown("- Information\n- Change Password\n- Support")
    return selected
