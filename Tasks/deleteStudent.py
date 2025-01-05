import sqlite3
from contextlib import closing
from components.config import DB_FILE


def deleteStudent(student_number: str) -> dict[str, str]:
    """
    Deletes a student record

    Parameters:
        student_number (str): The unique identifier for the student.

    Returns:
        dict: A dictionary containing details of the deleted student,
        including:
            - 'student_name': Name of the student.
            - 'student_number': The student's unique identifier.
            - 'course_name': The student's course name.

    Note:
        This function requires the implementation of error handling.
    """
    # Ensure student_number is an integer
    try:
        student_id = int(student_number)
    except ValueError as e:
        print("Error: Student number must be a numeric value.")
        raise e
    try:
        with closing(sqlite3.connect(DB_FILE)) as conn:
            with closing(conn.cursor()) as cursor:
                _ = cursor.execute(
                    'SELECT * FROM students WHERE student_number = ?',
                    (student_id,))
                row = cursor.fetchone()
                if not row:
                    raise Exception(f"No student found with number {
                                    student_number}")
                student_detail = {
                    'student_number': row[0],
                    'student_name': row[1],
                    'course_name': row[2]
                }
                _ = cursor.execute(
                    'DELETE FROM students WHERE student_number = ?', (student_id,))
                conn.commit()
                return student_detail
    except sqlite3.Error as e:
        print("An error occurred while deleting the student:", e)
        raise e
