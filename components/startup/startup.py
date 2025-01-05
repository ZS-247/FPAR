import sqlite3
import os
from contextlib import closing
from components.config import DB_PATH, DB_FILE


def startup() -> bool:
    """
    startup - check if the database exists
    if not create it and initialize the table
    This function will be called at the start of the program
"""
    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)
    if not initialize_db():
        print("Error initializing database.")
        return False
    return True


def initialize_db() -> bool:
    """
    Creates database, is called by startup()
    """
    try:
        with closing(sqlite3.connect(DB_FILE)) as conn:
            with closing(conn.cursor()) as cursor:
                _ = cursor.execute('''
                    CREATE TABLE IF NOT EXISTS students (
                        student_number INTEGER PRIMARY KEY,
                        student_name TEXT NOT NULL,
                        course_name TEXT NOT NULL
                    )
                ''')
                conn.commit()
                print("Database initialized successfully.")
    except sqlite3.Error as e:
        print("Encountered error initializing db: ", e)
        return False
    return True
