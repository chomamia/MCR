import streamlit as st

def show():
    """
    Display the "Information" page in the sidebar Setting.

    Behavior:
        - Shows the application title and description.
        - Displays current logged-in user information (username, id).
    """
    st.markdown("### 💻 Application Info")
    st.markdown("---")
    st.write("""
    **Multiple Choice Reader** is an application designed to manage 
    and evaluate multiple-choice exam papers.

    **Key Features:**
    - Manage answers and assignments.
    - Upload files and display structured data.
    - Automation calculate assignment scores using AI technology
    - Secure authentication with JWT tokens.
    - Simple and intuitive user interface.
             
    **User manual application:**
    - Step 1: Users can log in with the registered user account at login (If you do not have an account, please create a new account)
    - Step 2: After the user logs in successfully. The default screen is the Answer management screen. Here, the user can upload the desired Answer file. In addition, the old answer files that have been added can be viewed in the table below, click to see details.
    - Step 3: After the user successfully uploads the answer file. The user needs to click on the Assignment screen to upload the corresponding files so that the AI ​​program can automatically extract and score.
    - Step 4: The user can view the results in the table below and can click to see details.
    - Step 5: After the results are available, the user can export to an excel file by clicking the export button.
    """)
