import sqlite3
from contextlib import closing
from components.config import DB_FILE


def getStudent(student_num: str) -> dict[str, str]:
    '''
    Description: This function searches the database for a student
    using the student_number argument.

    Args:
        student_number (str): The number of the student
        (string, converted to integer).

    Returns:
        student_detail (dict): A dictionary containing
        the following key-value pairs:
            - 'student_name': The name of the student.
            - 'student_number': The student number.
            - 'course_name': The name of the course.

    Conditions:
        The use of error handling routine is compulsory.
    '''
    try:
        # Ensure student_number is an integer
        student_number = int(student_num)
    except ValueError as e:
        print("Error: Student number must be a numeric value.")
        raise e
    try:
        with closing(sqlite3.connect(DB_FILE)) as conn:
            with closing(conn.cursor()) as cursor:
                _ = cursor.execute(
                    'SELECT * FROM students WHERE student_number = ?', (student_number,))
                row = cursor.fetchone()
                if row:
                    student_detail = {
                        'student_number': row[0],
                        'student_name': row[1],
                        'course_name': row[2]
                    }
                    return student_detail
                else:
                    raise Exception(
                        f"No student found with number {student_number}")
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving the student: {e}")
        raise e
