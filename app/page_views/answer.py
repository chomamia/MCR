import streamlit as st
import pandas as pd
from components.upload_section import render_upload_section
from components.table_section import render_table_section_answer

def create_answer_data():
    return pd.DataFrame([{
        "ID": "MS0001",
        "Name File": f"Answer_{i:02}.csv",
        "Course ID": f"MS0000{i:02}",
        "Number Of Answers": 25,
        "Create Date": "28-03-2024 00:07:23.566",
        "Create Upload": "28-03-2024 00:07:23.566"
    } for i in range(1, 30)])

def show():
    st.markdown("### 📄 Answer Management")
    st.markdown("---")

    render_upload_section("Answer")

    df = create_answer_data()
    render_table_section_answer(df)
    
