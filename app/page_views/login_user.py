import streamlit as st
from database.user import verify_user, add_user, get_user
from auth.jwt_utils import create_token
from auth.streamlit_javascript import save_token_to_local_storage

def login_page():
    st.set_page_config(layout="wide")
    if "show_register" not in st.session_state:
        st.session_state["show_register"] = False

    show_register = st.query_params.get("page") == "register"

    if show_register:
        register_page()
        return
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
            <div style='background-color: #f5f5f5; display: flex; justify-content: center; align-items: center; height: 100vh;'>
                <h1 style='color: #2c3e50;'>LOGO and Name</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if not st.session_state["show_register"]:
            st.markdown(
            """
            <div style='background-color: #0000000; height: 30vh; padding-top: 25vh; padding-left: 30px; padding-right: 30px;'>
                <h3 style='text-align: center;'>Login to your Account</h3>
            """,
            unsafe_allow_html=True
             )
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            remember = st.checkbox("Remember Me")
            col1, col2, col3, col4, col5 = st.columns([2, 1, 0.5, 1, 2])
            with col2:
                login = st.button("Login", key="login_button", use_container_width=True)

            with col4:
                register = st.button("Register", key="register_button", use_container_width=True)

            st.markdown("""
                 <style>
                div.stButton > button {
                    background-color: #407AB4;
                    color: white;
                    width: 100px;
                    height: 40px;
                    margin-right: 10px;
                }
                .btn-container {
                    display: flex;
                    justify-content: space-between;
                    gap: 20px;
                }
            </style>
            """, unsafe_allow_html=True)
            if login:
                if verify_user(email, password):
                    user = get_user(email)
                    token = create_token({"email": email, "id": user[0], "full_name": user[2]})
                    save_token_to_local_storage(token)
                    st.rerun()
                else:
                    st.error("Invalid email or password")

            if register:
                st.session_state["show_register"] = True
                st.rerun()
        else:
            register_page()

def register_page():
    st.markdown(
        """
        <div style='background-color: #0000000; height: 30vh; padding-top: 25vh; padding-left: 30px; padding-right: 30px;'>
            <h3 style='text-align: center;'>Create new Account</h3>
        """,
        unsafe_allow_html=True
    )

    full_name = st.text_input("Full Name")
    email_reg = st.text_input("Email", key="reg_email")
    pw1 = st.text_input("Password", type="password", key="reg_pw1")
    pw2 = st.text_input("Confirm Password", type="password", key="reg_pw2")

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col2:
        register_clicked = st.button("Register", key="register_button", use_container_width=True)

    with col4:
        back_clicked = st.button("Back to Login", key="back_button", use_container_width=True)

    st.markdown("""
        <style>
            div.stButton > button {
                background-color: #407AB4;
                color: white;
                width: 150px;
                height: 40px;
                margin-right: 30px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Handle logic
    if register_clicked:
        if pw1 != pw2:
            st.error("Passwords do not match")
        else:
            success = add_user(email_reg, pw1, full_name)
            if success:
                st.success("Registration successful! You can now login.")
                st.session_state["show_register"] = False
                st.rerun()
            else:
                st.error("User already exists.")

    if back_clicked:
        st.session_state["show_register"] = False
        st.rerun()