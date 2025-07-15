import streamlit as st

def render_pagination(current_page=1, total_pages=20):
    page = st.selectbox("Page:", list(range(1, 6)), index=current_page-1)
    st.caption(f"Page in {page}/{total_pages}")
    return page
