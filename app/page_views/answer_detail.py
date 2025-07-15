import streamlit as st
import pandas as pd
from components.table_section import render_table_section

def create_answer_detail_data():
    return pd.DataFrame([{
        "ID": "MS0002",
        "Question": f"Question {i:02}",
        "Answer": f"Answer {i:02}",
        "Description": "Hi",
        "Create Date": "01-04-2024 09:00:00.000",
        "Create Upload": "01-04-2024 09:00:00.000"
    } for i in range(1, 30)])

def show(file_name: str):
    st.markdown(f"### 📄 Detail View for `{file_name}`")
    st.markdown("---")
    
    if st.button("🔙 Back"):
        st.query_params.clear()
        st.query_params["page"] = "Answer"
        st.rerun()

    df = create_answer_detail_data()
    render_table_section(df)
