import streamlit as st
import pandas as pd
from components.upload_section import render_upload_section
from components.table_section import render_table_section_assignment

def create_assignment_data():
    return pd.DataFrame([{
        "ID": "MS0002",
        "First Name": "Nguyen",
        "Last Name": "Huu",
        "Middle Name": "Phuong",
        "Studen ID": "000012",
        "Course ID": "202022",
        "Score": 8.25,
        "Create Date": "01-04-2024 09:00:00.000",
        "Create Upload": "01-04-2024 09:00:00.000"
    }] * 30)

def show():
    st.markdown("### 📄 Assignment Management")
    st.markdown("---")

    render_upload_section("Assignment")

    df = create_assignment_data()
    render_table_section_assignment(df)
    # render_pagination()
