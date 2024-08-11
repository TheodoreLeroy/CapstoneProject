import psycopg2
import pickle
from config import Config

def connect():
    return psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )

def get_students_by_id(student_ids: list):
    conn = connect()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT student_id, name, embedding FROM students WHERE student_id IN [{student_ids[1:-1]}]"""
    )
    rows = cur.fetchall()
    conn.close()
    return {row[0]: pickle.loads(row[2]) for row in rows}


def import_student(student_id, name, embedding):
    conn = connect()
    cur = conn.cursor()
    # Check if the student already exists
    cur.execute("SELECT COUNT(1) FROM students WHERE student_id = %s", (student_id,))
    exists = cur.fetchone()[0]

    if exists:
        # Update the existing student's data
        cur.execute(
            "UPDATE students SET name = %s, embedding = %s WHERE student_id = %s",
            (name, pickle.dumps(embedding), student_id)
        )
    else:
        # Insert a new student record
        cur.execute(
            "INSERT INTO students (student_id, name, embedding) VALUES (%s, %s, %s)",
            (student_id, name, pickle.dumps(embedding))
        )

    conn.commit()
    cur.close()
    conn.close()