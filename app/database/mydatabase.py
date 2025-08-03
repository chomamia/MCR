import sqlite3
import json
from typing import List
from utils import convert_insert_assignment, convert_list_assignment, convert_list_answer
import uuid
import pandas as pd
from datetime import datetime
from ast import literal_eval


def create_connection():
    conn = sqlite3.connect("mydata.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id TEXT PRIMARY KEY,
            last_name TEXT,
            first_name TEXT,
            middle_name TEXT,
            test_form_code TEXT,
            student_id TEXT,
            course_id TEXT,
            score TEXT,
            create_date TEXT,
            update_date TEXT,
            source_file TEXT,
            assignment_list TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id TEXT PRIMARY KEY,
            name_file TEXT,
            course_id TEXT,
            test_form_code TEXT,
            answer_list TEXT, 
            create_date TEXT,
            update_date TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_assignment(data: List[List[str]]):
    """
    assignment_list: Python list (we'll JSON-serialize)
    """
    # Get answer key.
    conn = sqlite3.connect("mydata.db")
    cursor = conn.cursor()
    
    last_name, first_name, middle_name, test_form_code, student_id, course_id, source_file, assignment_list = convert_insert_assignment(data)
    
    cursor.execute("""SELECT
        answer_list
        FROM answers WHERE course_id = ? AND test_form_code = ?
    """, (course_id, test_form_code))
    answer_key = literal_eval(cursor.fetchone()[0])

    print(answer_key, type(answer_key))
    print(assignment_list, type(assignment_list))
    score = sum(answer_key[i][1] == assignment_list[i][1] for i in range(len(answer_key)))
    assignment_id = str(uuid.uuid4())
    assignment_json = json.dumps(assignment_list, ensure_ascii=False)
    now = datetime.utcnow().isoformat()
    
    cursor.execute("""
        INSERT INTO assignments (
            id, last_name, first_name, middle_name,
            test_form_code, student_id, course_id,
            score, create_date, update_date,
            source_file, assignment_list
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        assignment_id,
        last_name, first_name, middle_name,
        test_form_code, student_id, course_id,
        score, now, now,
        source_file, assignment_json
    ))
    conn.commit()
    conn.close()

def insert_answer(name_file: str, course_id:str, test_form_code:str, answer_list:List[List[str]]):
    """
    answer_list: Python list (we'll JSON-serialize)
    """
    conn = create_connection()
    answer_id = str(uuid.uuid4())
    answer_json = json.dumps(answer_list, ensure_ascii=False)
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO answers (
            id, name_file, course_id, test_form_code, answer_list, create_date, update_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        answer_id, name_file, course_id, test_form_code, answer_json, now, now
    ))
    conn.commit()
    conn.close()

def get_assignments_by_id(assignment_id:str) -> pd.DataFrame:
    conn = sqlite3.connect("mydata.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT 
            assignment_list,
            create_date,
            update_date FROM assignments WHERE id = ?''', (assignment_id,))
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
    # Get data from answer key.
    
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

def get_all_assignments() -> pd.DataFrame:
    conn = sqlite3.connect("mydata.db")
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
            update_date FROM assignments''')
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # get column names
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

def get_answer_by_id(answer_id:str) -> pd.DataFrame:
    conn = sqlite3.connect("mydata.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT 
            answer_list,
            create_date,
            update_date FROM answers WHERE id = ?''', (answer_id,))
    row = cursor.fetchone()
    if not row:
        return pd.DataFrame(columns=["question", "answer", "create_date", "update_date"])
    conn.close()
    data = []
    row = list(row)
    try:
        answer_list = json.loads(row[0])
    except:
        answer_list = []
    create_date = format_datetime(row[1])
    update_date = format_datetime(row[2])
    data = []
    for answer in answer_list:
        question = answer[0]
        answer = answer[1]
        data.append({
            "Question": question,
            "Answer": answer,
            "Description": "",
            "Create Date": create_date,
            "Update Date": update_date
        })
    return pd.DataFrame(data)

def get_all_answers() -> pd.DataFrame:
    conn = sqlite3.connect("mydata.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT 
            id,
            name_file,
            course_id,
            test_form_code,
            answer_list,
            create_date,
            update_date FROM answers''')
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # get column names
    conn.close()
    data = []
    for row in rows:
        row = list(row)
        try:
            answer_list = json.loads(row[4])
            number_answer = len(answer_list)
            row[4] = number_answer
        except:
            number_answer = 0
        row[5] = format_datetime(row[5])  # create_date
        row[6] = format_datetime(row[6])  # update_date
        data.append(row)

    df = pd.DataFrame(data, columns=columns)
    df = convert_list_answer(df)
    return df



def format_datetime(dt_str: str) -> str:
    """Convert ISO datetime string to 'dd-mm-yyyy HH:MM:SS.sss' format."""
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%d-%m-%Y %H:%M:%S.%f")[:-3]
    except Exception:
        return dt_str  # fallback if format fails