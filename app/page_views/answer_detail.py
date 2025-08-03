import streamlit as st
import pandas as pd
from components.table_section import render_table_section
from database.answer import get_answer_by_id
def create_answer_detail_data():
    """
    Create a sample DataFrame containing a list of questions and answers.
    Returns:
        pd.DataFrame: A DataFrame with 29 records, each containing the following columns:
            - ID: A fixed identifier "MS0002".
            - Question: Question titles in the format "Question 01" to "Question 29".
            - Answer: Corresponding answers in the format "Answer 01" to "Answer 29".
            - Description: A sample description, fixed as "Hi".
            - Create Date: A fixed creation date "01-04-2024 09:00:00.000".
            - Create Upload: A fixed upload date "01-04-2024 09:00:00.000".
    """
    return pd.DataFrame([{
        "ID": "MS0002",
        "Question": f"Question {i:02}",
        "Answer": f"Answer {i:02}",
        "Description": "Hi",
        "Create Date": "01-04-2024 09:00:00.000",
        "Create Upload": "01-04-2024 09:00:00.000"
    } for i in range(1, 30)])

def show(id: str):
    """
    Display a detailed view of a given file using Streamlit.

    Args:
        file_name (str): The name of the file to display details for.

    Behavior:
        - Renders a header and a separator line for the detail view.
        - Provides a "Back" button to return to the "Answer" page by clearing and resetting query parameters.
        - Generates sample answer detail data by calling `create_answer_detail_data()`.
        - Displays the data using `render_table_section()`.

    Note:
        This function depends on Streamlit's session state and UI components.
    """
    st.markdown(f"### 📄 Answer > `{id}`")
    st.markdown("---")
    if st.button("🔙 Back"):
        st.query_params.clear()
        st.query_params["page"] = "Answer"
        st.rerun()
    user_id = st.session_state["id"]
    df = get_answer_by_id(id, user_id)
    render_table_section(df)
