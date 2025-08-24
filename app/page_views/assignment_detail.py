import streamlit as st
import pandas as pd
from components.table_section import render_table_section
from database.assignment import get_assignments_by_id

def create_answer_detail_data():
    """
    Create a sample DataFrame containing detailed question and answer records.

    Returns:
        pd.DataFrame: A DataFrame with 29 records, each containing the following columns:
            - ID: A fixed identifier "MS0002".
            - Question: Question titles in the format "Question 01" to "Question 29".
            - Answer: Corresponding answers in the format "Answer 01" to "Answer 29".
            - Correct Answer: The correct answer, fixed as "Hi".
            - Correct: Indicates if the answer is correct, fixed as "True".
            - Score: Indicates if the score is given, fixed as "True".
            - Create Date: A fixed creation date "01-04-2024 09:00:00.000".
            - Create Upload: A fixed upload date "01-04-2024 09:00:00.000".
    """
    return pd.DataFrame([{
        "ID": "MS0002",
        "Question": f"Question {i:02}",
        "Answer": f"Answer {i:02}",
        "Correct Answer": "Hi",
        "Correct": "True",
        "Score": "True",
        "Create Date": "01-04-2024 09:00:00.000",
        "Create Upload": "01-04-2024 09:00:00.000"
    } for i in range(1, 30)])

def show(id:str):
    """
    Display a detailed view of a specific assignment's answers using Streamlit.

    Args:
        id (str): The identifier of the assignment for which details are displayed.

    Behavior:
        - Displays a header with the assignment ID and a separator line.
        - Provides a "Back" button that resets query parameters and navigates back to the "Assignment" page.
        - Generates a sample dataset of detailed answers by calling `create_answer_detail_data()`.
        - Displays the dataset in a table using `render_table_section()`.

    Note:
        This function depends on Streamlit UI components and an external helper function `render_table_section`.
    """
    st.markdown(f"### 📝 Assignment > {id}")
    st.markdown("---")
    if st.button("⬅️ Back"):
        st.query_params.clear()
        st.query_params["page"] = "Assignment"
        st.session_state["current_page"] = "Assignment"
        st.rerun()
    user_id = st.session_state["id"]
    df = get_assignments_by_id(user_id, id)
    render_table_section(df)

