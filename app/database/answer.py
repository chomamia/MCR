import sqlite3
import json
from typing import List
from utils import convert_list_answer
import uuid
import pandas as pd
from datetime import datetime
from database.create_table import create_connection
from utils import format_datetime

def insert_answer(user_id:str, name_file: str, course_id:str, test_form_code:str, answer_list:List[List[str]]):
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
            id, user_id, name_file, course_id, test_form_code, answer_list, create_date, update_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        answer_id, user_id, name_file, course_id, test_form_code, answer_json, now, now
    ))
    conn.commit()
    conn.close()

def get_answer_by_id(answer_id:str, user_id:str) -> pd.DataFrame:
    conn = sqlite3.connect("mydata.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT 
            answer_list,
            create_date,
            update_date FROM answers WHERE id = ? and user_id = ?''', (answer_id,user_id,))
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

def get_all_answers(user_id:str) -> pd.DataFrame:
    conn = sqlite3.connect("mydata.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT 
            id,
            name_file,
            course_id,
            test_form_code,
            answer_list,
            create_date,
            update_date FROM answers WHERE user_id = ?''', (user_id,))
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