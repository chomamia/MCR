import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def render_table_section(df):
    selected_rows = st.multiselect("Select rows to delete:", df.index, label_visibility="collapsed")
    st.dataframe(df, use_container_width=True, height=800)
    return selected_rows

def render_table_section_answer(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_selection("single")
    clickable_style = {
        "color": "#6aa9ff",
        "textDecoration": "underline",
        "cursor": "pointer"
    }
    gb.configure_columns(["ID", "Name File"], cellStyle=clickable_style)
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

    selected = grid_response["selected_rows"]
    if selected is not None and len(selected) > 0:
        id = selected.iloc[0]["ID"]
        st.query_params["page"] = "answer_detail"
        st.query_params["id"] = id
        st.rerun()


def render_table_section_assignment(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_selection("single")
    clickable_style = {
        "color": "#6aa9ff",
        "textDecoration": "underline",
        "cursor": "pointer"
    }
    gb.configure_columns(["ID", "First Name", "Last Name"], cellStyle=clickable_style)
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

    selected = grid_response["selected_rows"]
    if selected is not None and len(selected) > 0:
        id = selected.iloc[0]["ID"]
        st.query_params["page"] = "assignment_detail"
        st.query_params["id"] = id
        st.rerun()