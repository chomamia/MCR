import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "mcr"))
import streamlit as st
from page_views import answer, assignment, answer_detail, assignment_detail
from components.sidebar import render_sidebar
from database.mydatabase import create_table

create_table()
st.set_page_config(page_title="Management App", layout="wide")

params = dict(st.query_params)
file_name = params.get("file")
page_param = params.get("page")
id = params.get("id")

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Answer"

if page_param == "answer_detail":
    if id is not None:
        answer_detail.show(id)
elif page_param == "assignment_detail":
    if id is not None:
        assignment_detail.show(id)
else:
    selected_page = render_sidebar()
    st.session_state["current_page"] = selected_page

    if selected_page == "Answer":
        answer.show()
    elif selected_page == "Assignment":
        assignment.show()