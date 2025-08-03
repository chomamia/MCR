from typing import List, Tuple
import pandas as pd
from datetime import datetime

def convert_insert_assignment(data: List[List[str]]) -> Tuple[
    str, str, str, str, str, str, str, List[List[str]]
]:
    last_name = ""
    first_name = ""
    middle_name = ""
    test_form_code = ""
    student_id = ""
    course_id = ""
    source_file = ""
    assignment_list = []
    for i in range(len(data)):
        if data[i][0] == "Last Name":
            last_name = data[i][1]
        elif data[i][0] == "First Name":
            first_name = data[i][1]
        elif data[i][0] == "Middle Name":
            middle_name = data[i][1]
        elif data[i][0] == "Test Form Code":
            test_form_code = data[i][1]
        elif data[i][0] == "Student ID":
            student_id = data[i][1]
        elif data[i][0] == "Course ID":
            course_id = data[i][1]
        elif data[i][0] == "Source File":
            source_file = data[i][1]
        else:
            assignment_list.append(data[i])
    return last_name, first_name, middle_name, test_form_code, student_id, course_id, source_file, assignment_list

def convert_list_assignment(df: pd.DataFrame):
    column_mapping = {
        "id": "ID",
        "first_name": "First Name",
        "last_name": "Last Name",
        "middle_name": "Middle Name",
        "student_id": "Student ID",
        "course_id": "Course ID",
        "test_form_code": "Test Form Code",
        "score": "Score",
        "create_date": "Create Date",
        "update_date": "Create Upload"
    }
    df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
    return df

def convert_list_answer(df: pd.DataFrame):
    column_mapping = {
        "id": "ID",
        "name_file": "File Name",
        "course_id": "Course ID",
        "answer_list": "Number Of Answers",
        "test_form_code": "Test Form Code",
        "create_date": "Create Date",
        "update_date": "Create Upload"
    }

    df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
    return df

def process_anskeys(uploaded_file) -> Tuple[str, str, List[List[str]]]:
    df = pd.read_excel(uploaded_file)
    course_id = ""
    test_form_code = ""
    questions = []
    if "Key" in df.columns and "Value" in df.columns:
        for _, row in df.iterrows():
            key = str(row["Key"]).strip()
            value = str(row["Value"]).strip()

            if key.lower().startswith("course"):
                course_id = value if value != "nan" else ""
            elif key.lower().startswith("test"):
                test_form_code = value if value != "nan" else ""
            elif key.lower().startswith("q"):
                questions.append([key, value])
    else:
        raise ValueError("File must contain 'Key' and 'Value' columns.")

    return course_id, test_form_code, questions

def format_datetime(dt_str: str) -> str:
    """Convert ISO datetime string to 'dd-mm-yyyy HH:MM:SS.sss' format."""
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%d-%m-%Y %H:%M:%S.%f")[:-3]
    except Exception:
        return dt_str  # fallback if format fails