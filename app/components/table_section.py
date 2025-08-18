import streamlit as st
import pandas as pd 
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from database.answer import *
from database.assignment import *
import io

def render_table_section(df: pd.DataFrame):
    selected_rows = st.multiselect("Select rows to delete:", df.index, label_visibility="collapsed")
    st.dataframe(df, use_container_width=True, height=800)
    return selected_rows

def render_table_section_answer(df:  pd.DataFrame):
    if "delete_mode" not in st.session_state:
        st.session_state.delete_mode = False
    
    if st.button("Delete"):
        if st.session_state.delete_mode:
            selected_rows = st.session_state.get("selected_rows", [])
            if selected_rows is not None and not selected_rows.empty:
                ids_to_delete = [row["ID"] for _, row in selected_rows.iterrows()]
                delete_answers(ids_to_delete)
                st.success(f"{len(ids_to_delete)} record deleted")
                st.session_state.delete_mode = False
                st.rerun()
            else:
                st.warning("You have not selected any records to delete.")
            st.session_state.delete_mode = False
        else:
            st.session_state.delete_mode = True
            st.session_state.upload_key += 1
            st.rerun()
    gb = GridOptionsBuilder.from_dataframe(df)
    if st.session_state.delete_mode:
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    else:
        gb.configure_selection(selection_mode="single")
        clickable_style = {
            "color": "#6aa9ff",
            "textDecoration": "underline",
            "cursor": "pointer"
        }
        gb.configure_columns(["ID"], cellStyle=clickable_style)
    gb.configure_pagination(paginationAutoPageSize=True)

    grid_options = gb.build()
    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        height=600,
        width='100%',
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True
    )
    if st.session_state.delete_mode:
        st.session_state.selected_rows = grid_response.get("selected_rows", [])
    else:
        selected = grid_response["selected_rows"]
        if selected is not None and not selected.empty:
            id = selected.iloc[0]["ID"]
            st.query_params["page"] = "answer_detail"
            st.query_params["id"] = id
            st.rerun()


def render_table_section_assignment(df: pd.DataFrame):
    if "delete_mode" not in st.session_state:
        st.session_state.delete_mode = False
    col1, col_spacer, col2 = st.columns([1, 10, 1])
    with col1:
        if st.button("Delete"):
            if st.session_state.delete_mode:
                selected_rows = st.session_state.get("selected_rows", [])
                if selected_rows is not None and not selected_rows.empty:
                    ids_to_delete = [row["ID"] for _, row in selected_rows.iterrows()]
                    delete_assignments(ids_to_delete)
                    st.success(f"{len(ids_to_delete)} record deleted")
                    st.session_state.delete_mode = False
                    st.rerun()
                else:
                    st.warning("You have not selected any records to delete.")
                st.session_state.delete_mode = False
            else:
                st.session_state.delete_mode = True
                st.session_state.upload_assignment_key += 1
                st.rerun()
    with col2:
        if not df.empty:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Assignments")
            excel_data = output.getvalue()
            st.markdown(
                    """
                    <style>
                    div.stDownloadButton > button {
                        background-color: #25C37A;
                        color: white;
                        font-weight: bold;
                        border-radius: 8px;
                    }
                    div.stDownloadButton > button:hover {
                        background-color: #1e9e63;
                        color: white;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
            st.download_button(
                label="Export Excel",
                data=excel_data,
                file_name="assignments.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.session_state.upload_assignment_key += 1
    gb = GridOptionsBuilder.from_dataframe(df)
    if st.session_state.delete_mode:
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    else:
        gb.configure_selection(selection_mode="single")
        clickable_style = {
            "color": "#6aa9ff",
            "textDecoration": "underline",
            "cursor": "pointer"
        }
        gb.configure_columns(["ID", "First Name", "Last Name"], cellStyle=clickable_style)
    gb.configure_pagination(paginationAutoPageSize=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        height=600,
        width='100%',
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True
    )

    if st.session_state.delete_mode:
        st.session_state.selected_rows = grid_response.get("selected_rows", [])
    else:
        selected = grid_response["selected_rows"]
        if selected is not None and not selected.empty:
            id = selected.iloc[0]["ID"]
            st.query_params["page"] = "assignment_detail"
            st.query_params["id"] = id
            st.rerun()