import sqlite3
from contextlib import closing
from components.config import DB_FILE


def addStudent(student_detail: dict[str, str]) -> None:
    '''
    Description: This function accepts students'
    details and writes to the database.
    Args:
        student_detail (dict):
        A dictionary containing the following key-value pairs:
            - 'student_name': The name of the student.
            - 'student_number': The student number
            (string, converted to integer)
            - 'course_name': The name of the course.

    Returns:
        None. Prints a statement confirming that the record was written.

    Conditions:
        The use of error handling routine is compulsory.
    '''
    try:
        # Ensure student_number is an integer
        student_number = int(student_detail['student_number'])
    except ValueError as e:
        print("Error: Student number must be a numeric value.")
        raise e
    try:
        with closing(sqlite3.connect(DB_FILE)) as conn:
            with closing(conn.cursor()) as cursor:
                _ = cursor.execute('''
                    INSERT INTO students (student_number, student_name, course_name)
                    VALUES (?, ?, ?)
                ''', (student_number, student_detail['student_name'],
                      student_detail['course_name']))
                conn.commit()
                print(
                    f"Student {student_detail['student_name']} added successfully.")
    except sqlite3.IntegrityError:
        print("Student number already exists!")
    except sqlite3.Error as e:
        print("An error occurred while adding the student:", e)
        raise e
