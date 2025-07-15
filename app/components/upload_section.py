import streamlit as st

def render_upload_section(name_file):
    st.markdown("#### Upload or Drop {} file".format(name_file))
    uploaded_files = st.file_uploader(
        "", type="csv", accept_multiple_files=True, label_visibility="collapsed"
    )
    if uploaded_files:
        for file in uploaded_files:
            st.success(f"Uploaded: {file.name}")
    st.button("Delete", key="delete")
