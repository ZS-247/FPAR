'''
Import and test your functions here
Example:
    - from Tasks.addStudent import addStudent

Use this section to test your functions and verify if the output is as expected.
Using assert or unittest would fetch you more marks.
'''


import shutil
import sys
import builtins
import sqlite3
from contextlib import closing
from os import path
try:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from Tasks.addStudent import addStudent
    from Tasks.deleteStudent import deleteStudent
    from Tasks.getStudent import getStudent
    from components import startup as mm
    from components import config
except ImportError:
    print("An error occurred while importing the functions:")

DB_PATH = config.DB_PATH
DB_NAME = config.DB_NAME
DB_FILE = config.DB_FILE


def test_addStudent():
    student_detail = {
        'student_name': 'John Doe',
        'student_number': '123456',
        'course_name': 'Computer Science'
    }
    student_detail2 = {
        'student_name': 'Jane Doe',
        'student_number': '654321',
        'course_name': 'Computer Science'
    }
    print("Adding students to the database...")
    try:
        addStudent(student_detail)
        addStudent(student_detail2)
    except Exception as e:
        print("An error occurred while adding students:", e)
        return False
    return True


def test_deleteStudent():
    student_number = '123456'
    fake_student_number = '696969'
    invalid_student_number = 'lemon'
    try:
        print("Deleting valid student from the database...")
        deleted_student = deleteStudent(student_number)
        print(
            f"Student {deleted_student['student_name']} deleted successfully.")
    except Exception as e:
        print("An error occurred while deleting student:", e)
        raise e
    try:
        print("Deleting fake student from the database...")
        print(deleteStudent(fake_student_number))
    except Exception as e:
        print("An error occurred while deleting student:", e)
    try:
        print("Deleting invalid student from the database...")
        print(deleteStudent(invalid_student_number))
    except Exception as e:
        print("An error occurred while deleting student:", e)


def test_getStudent():
    student_number = '123456'
    invalid_student_number = "lemon"
    fake_student_number = '696969'
    try:
        print("Retrieving student from the database...")
        student_detail = getStudent(student_number)
        print(f"Student found: {student_detail}")
    except Exception as e:
        print("An error occurred while retrieving student:", e)
        raise e
    try:
        print("Retrieving fake student from the database...")
        print(getStudent(fake_student_number))
    except Exception as e:
        print("An error occurred while retrieving student:", e)
    try:
        print("Retrieving invalid student from the database...")
        print(getStudent(invalid_student_number))
    except Exception as e:
        print("An error occurred while retrieving student:", e)


def test_startup_no_dir():
    # first test the startup function when no Student_Records directory exists
    # remove the Student_Records directory if it exists
    try:
        shutil.rmtree(DB_PATH)
    except FileNotFoundError:
        pass
    status = mm.startup()
    try:
        shutil.rmtree(DB_PATH)
    except FileNotFoundError:
        pass
    return status


def test_startup_no_db():
    # test the startup function when Student_Records directory exists but no database file
    try:
        shutil.rmtree(DB_PATH)
    except FileNotFoundError:
        pass
    # create the Student_Records directory only
    try:
        # make the Student_Records folder
        shutil.os.mkdir(DB_PATH)
    except Exception as e:
        print("An error occurred while creating the Student_Records directory:", e)
        raise e
    status = mm.startup()
    try:
        shutil.rmtree(DB_PATH)
    except FileNotFoundError:
        pass
    return status


def test_startup_db_exists():
    # test the startup function when Student_Records directory exists and database file exists
    try:
        shutil.rmtree(DB_PATH)
    except FileNotFoundError:
        pass
    # create the Student_Records directory and the database file
    try:
        shutil.os.mkdir(DB_PATH)
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

    except Exception as e:
        print("An error occurred while creating the Student_Records directory and the database file:", e)
        raise e
    status = mm.startup()
    # clean up the broken database file
    try:
        shutil.rmtree(DB_PATH)
    except FileNotFoundError:
        pass
    return status


def test_startup_corrupted_db():
    # test the startup function when Student_Records directory exists but the database file is corrupted
    try:
        shutil.rmtree(DB_PATH)
    except FileNotFoundError:
        pass
    # create the Student_Records directory and the database file
    try:
        # make the Student_Records folder
        shutil.os.mkdir(DB_PATH)
        # make the database file
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

        with open(DB_FILE, 'w') as f:
            _ = f.write("corrupted file >:3")
    except Exception as e:
        print("An error occurred while creating corupted db:", e)
        raise e
    status = mm.startup()
    try:
        shutil.rmtree(DB_PATH)
    except FileNotFoundError:
        pass
    return not status


if __name__ == "__main__":
    assert test_startup_no_dir()
    assert test_startup_no_db()
    assert test_startup_db_exists()
    assert test_startup_corrupted_db()
    assert mm.startup()
    print("All db tests passed successfully!")
    assert test_addStudent() is True
    print("Add student test passed successfully!")
    test_getStudent()
    print("Get student test passed successfully!")
    test_deleteStudent()
    print("Delete student test passed successfully!")
