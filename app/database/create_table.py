import sqlite3

def create_connection():
    conn = sqlite3.connect("mydata.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id TEXT PRIMARY KEY,
            user_id TEXT,
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
            user_id TEXT,
            name_file TEXT,
            course_id TEXT,
            test_form_code TEXT,
            answer_list TEXT, 
            create_date TEXT,
            update_date TEXT
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT,
        full_name TEXT
    )
    """)

    conn.commit()
    conn.close()
