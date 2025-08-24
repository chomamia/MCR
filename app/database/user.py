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

def update_password(user_id: str, old_password: str, new_password: str) -> bool:
    """
    Update user password in the database.

    Args:
        user_id (str): The ID of the user who wants to change password.
        old_password (str): The current password entered by the user.
        new_password (str): The new password to update.

    Returns:
        bool: True if password updated successfully, False otherwise.
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False

    current_hashed_pw = row[0]

    if not bcrypt.verify(old_password, current_hashed_pw):
        conn.close()
        return False 

    new_hashed_pw = bcrypt.hash(new_password)
    try:
        cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_hashed_pw, user_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error:
        conn.rollback()
        conn.close()
        return False
    
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