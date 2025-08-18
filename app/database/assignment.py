import sqlite3
import json
from typing import List
from utils import convert_insert_assignment, convert_list_assignment
import uuid
import pandas as pd
from datetime import datetime
from utils import format_datetime
from database.create_table import create_connection
from ast import literal_eval
import streamlit as st



def insert_assignment(user_id:str, data: List[List[str]]):
    """
    assignment_list: Python list (we'll JSON-serialize)
    """
    last_name, first_name, middle_name, test_form_code, student_id, course_id, source_file, assignment_list = convert_insert_assignment(data)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT
        answer_list
        FROM answers WHERE course_id = ? AND test_form_code = ?
    """, (course_id, test_form_code))
    answer_key = cursor.fetchone()
    if answer_key is None:
        st.error(f"Upload Error: The answer must match the Course Id and Test Form Code uploaded in the answer.")
        return False
    else:
        answer_key = literal_eval(answer_key[0])
        score = sum(answer_key[i][1] == assignment_list[i][1] for i in range(len(answer_key)))
        assignment_id = str(uuid.uuid4())
        assignment_json = json.dumps(assignment_list, ensure_ascii=False)
        now = datetime.utcnow().isoformat()
        cursor.execute("""
            INSERT INTO assignments (
                id, user_id, last_name, first_name, middle_name,
                test_form_code, student_id, course_id,
                score, create_date, update_date,
                source_file, assignment_list
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            assignment_id,user_id,
            last_name, first_name, middle_name,
            test_form_code, student_id, course_id,
            score, now, now,
            source_file, assignment_json
        ))
        conn.commit()
        conn.close()
        return True

def check_assignment_exist(user_id:str, test_form_code : str, student_id: str, course_id : str) -> bool:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT 
            * FROM assignments WHERE user_id = ? and test_form_code = ? and student_id = ? and course_id = ?''', (user_id, test_form_code, student_id, course_id))
    row = cursor.fetchone()
    if row is not None:
        return True
    else:
        return False
    
def get_assignments_by_id(user_id:str, assignment_id:str) -> pd.DataFrame:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT 
            assignment_list,
            create_date,
            update_date FROM assignments WHERE id = ? and user_id = ?''', (assignment_id, user_id, ))
    row = cursor.fetchone()
    if not row:
        return pd.DataFrame(columns=["question", "answer", "create_date", "update_date"])
    conn.close()
    data = []
    row = list(row)
    try:
        assignment_list = json.loads(row[0])
    except:
        assignment_list = []
    create_date = format_datetime(row[1])
    update_date = format_datetime(row[2])
    data = []
    for assignment in assignment_list:
        question = assignment[0]
        answer = assignment[1]
        data.append({
            "Question": question,
            "Answer": answer,
            "Correct Answer": "",
            "Corect": "",
            "Score": "",
            "Create Date": create_date,
            "Update Date": update_date
        })
    return pd.DataFrame(data)

def get_all_assignments(user_id:str ) -> pd.DataFrame:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT 
            id,
            first_name,
            last_name,
            middle_name,
            student_id,
            course_id,
            test_form_code,
            score,
            create_date,
            update_date FROM assignments WHERE user_id = ?''', (user_id, ))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description] 
    conn.close()
    # convert assignment_list from JSON to readable string (optional)
    data = []
    for row in rows:
        row = list(row)
        if len(row) > 10:
            row[8] = format_datetime(row[8])  # create_date
            row[9] = format_datetime(row[9])  # update_date
        data.append(row) 

    df = pd.DataFrame(data, columns=columns)
    df = convert_list_assignment(df)
    return df

def delete_assignments(id_list: list[str]):
    """
    Delete assignment by list id

    Args:
        id_list (list[str]): list id.
    """
    if not id_list:
        return

    conn = create_connection()
    cursor = conn.cursor()

    placeholders = ",".join(["?"] * len(id_list))
    sql = f"DELETE FROM assignments WHERE id IN ({placeholders})"

    cursor.execute(sql, id_list)
    conn.commit()
    conn.close()