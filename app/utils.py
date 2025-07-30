from typing import List, Tuple
import pandas as pd

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
        "score": "Score",
        "create_date": "Create Date",
        "update_date": "Create Upload"
    }

    df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
    return df
