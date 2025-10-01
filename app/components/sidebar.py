from streamlit_option_menu import option_menu
import streamlit as st

from utils import get_localized_string

def render_sidebar():
    with st.sidebar:
        lang = st.selectbox(
            get_localized_string("select_language", st.session_state.get("lang", "en")),
            ["en", "vi"],
            format_func=lambda x: get_localized_string("english", "en") if x == "en" else get_localized_string("vietnamese", "vi"),
            index=0 if st.session_state.get("lang", "en") == "en" else 1
        )
        st.session_state["lang"] = lang
        options = [
            {"key": "Answer", "label": get_localized_string("answer", lang)},
            {"key": "Assignment", "label": get_localized_string("assignment", lang)},
            {"key": "Information", "label": get_localized_string("information", lang)},
            {"key": "Change Password", "label": get_localized_string("change_password", lang)},
            {"key": "Support", "label": get_localized_string("support", lang)}
        ]
        selected_label = option_menu(
            menu_title=get_localized_string("title", lang),
            options=[opt["label"] for opt in options],
            icons=["file-earmark-text", "pencil", "info-circle", "lock", "question-circle"],
            menu_icon="cast",
            default_index=0,
        )
        selected = next((opt["key"] for opt in options if opt["label"] == selected_label), "Answer")

        if st.button(get_localized_string("logout", lang), use_container_width=True):
            from auth.streamlit_javascript import delete_jwt
            delete_jwt()

    return selected
