import streamlit as st
import pandas as pd
from components.upload_section import render_upload_assignment_section
from components.table_section import render_table_section_assignment
from database.assignment import get_all_assignments
def create_assignment_data():
    """
    Create a sample DataFrame containing assignment records.

    Returns:
        pd.DataFrame: A DataFrame with 30 identical records, each containing the following columns:
            - ID: A fixed identifier "MS0002".
            - First Name: Student's first name, fixed as "Nguyen".
            - Last Name: Student's last name, fixed as "Huu".
            - Middle Name: Student's middle name, fixed as "Phuong".
            - Studen ID: Student identifier, fixed as "000012".
            - Course ID: Course identifier, fixed as "202022".
            - Score: Student's score, fixed as 8.25.
            - Create Date: A fixed creation date "01-04-2024 09:00:00.000".
            - Create Upload: A fixed upload date "01-04-2024 09:00:00.000".
    """
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
    """
    Display the "Assignment Management" page using Streamlit.
    Behavior:
        - Displays the page title and a separator line.
        - Renders the upload section for assignments using `render_upload_section("Assignment")`.
        - Generates a sample dataset of assignments by calling `create_assignment_data()`.
        - Displays the dataset in a table using `render_table_section_assignment()`.
        - (Optional) Pagination can be added by enabling the commented-out `render_pagination()` call.
    Note:
        This function depends on Streamlit UI components and external helper functions 
        `render_upload_section` and `render_table_section_assignment`.
    """
    st.markdown("### 📄 Assignment Management")
    st.markdown("---")

    render_upload_assignment_section("Assignment")
    user_id = st.session_state["id"]
    df = get_all_assignments(user_id)
    render_table_section_assignment(df)
