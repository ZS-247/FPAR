import sqlite3
from contextlib import closing
from Tasks.addStudent import addStudent


def promptStudent() -> None:
    """
    Prompts a User to enter details and maps to the student_detail dictionary

    Parameters:s
            student_name : Name of the student.
            student_number : The student's unique identifier.
            course_name : The student's course name.

    Returns:
        dict: A dictionary containing details entered by the user, including:
            - 'student_name': Name of the student.
            - 'student_number': The student's unique identifier.
            - 'course_name': The student's course name.

    Note:
        This function requires the implementation of error handling.

    # This function is redundant in the complete implementation of the project.
    """
    while True:
        try:
            student_name = input("Enter student name: ")
            student_number = input("Enter student number: ")
            course_name = input("Enter course name: ")
            student_detail = {
                'student_name': student_name,
                'student_number': student_number,
                'course_name': course_name
            }
        except Exception as e:
            print(f"Error: {e}")
            print("Please enter valid details.")
            continue
        break
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
                    print(f"Student with {
                          student_number} does not exist in the database. Do you want to add this student to the database.")
                    while True:
                        add_to_db = input(
                            "Enter 'yes' to add student or 'no' to exit: ")
                        match add_to_db.lower():
                            case 'yes':
                                addStudent(student_detail)
                                break
                            case 'no':
                                print("Exiting...")
                                exit()
                            case _:
                                print("Invalid input. Please enter 'yes' or 'no'.")
                                continue
    except sqlite3.Error as e:
        print(f"A database error occurred: {e}")
