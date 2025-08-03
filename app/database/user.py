import sqlite3
import uuid
from database.create_table import create_connection
from passlib.hash import bcrypt

def add_user(email:str, password:str, full_name:str):
    conn = create_connection()
    cursor = conn.cursor()
    hashed_pw = bcrypt.hash(password)
    user_id = str(uuid.uuid4())
    try:
        cursor.execute("INSERT INTO users (id, email, password, full_name) VALUES (?, ?, ?, ?)",
                       (user_id, email, hashed_pw, full_name))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    conn.close()
    return True

def verify_user(email:str, password:str):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    if result and bcrypt.verify(password, result[0]):
        return True
    return False

def get_user(email:str):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, full_name FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user