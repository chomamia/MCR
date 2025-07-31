import streamlit as st
import pandas as pd
from components.upload_section import render_upload_answer_section
from components.table_section import render_table_section_answer
from database.mydatabase import get_all_answers
def create_answer_data():
    """
    Create a sample DataFrame representing answer file metadata.
    Returns:
        pd.DataFrame: A DataFrame with 29 records, each containing the following columns:
            - ID: A fixed identifier "MS0001".
            - Name File: The file name, in the format "Answer_01.csv" to "Answer_29.csv".
            - Course ID: The associated course ID, in the format "MS000001" to "MS000029".
            - Number Of Answers: A fixed number of answers, 25.
            - Create Date: A fixed creation date "28-03-2024 00:07:23.566".
            - Create Upload: A fixed upload date "28-03-2024 00:07:23.566".
    """
    return pd.DataFrame([{
        "ID": "MS0001",
        "Name File": f"Answer_{i:02}.csv",
        "Course ID": f"MS0000{i:02}",
        "Number Of Answers": 25,
        "Create Date": "28-03-2024 00:07:23.566",
        "Create Upload": "28-03-2024 00:07:23.566"
    } for i in range(1, 30)])

def show():
    """
    Display the "Answer Management" page using Streamlit.

    Behavior:
        - Displays the page title and a separator line.
        - Renders the upload section for answer files using `render_upload_section("Answer")`.
        - Generates a sample dataset of answer file metadata by calling `create_answer_data()`.
        - Displays the dataset in a table using `render_table_section_answer()`.

    Note:
        This function depends on Streamlit UI components and external helper functions 
        `render_upload_section` and `render_table_section_answer`.
    """
    st.markdown("### 📄 Answer Management")
    st.markdown("---")

    render_upload_answer_section("Answer")

    df = get_all_answers()
    render_table_section_answer(df)
    
