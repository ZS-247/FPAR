# def addStudent(student_detail):
#     '''
#     Description: This function accepts students detail and writes to file
#     Args:
#         student_detail (dict): A dictionary containing the following key-value pairs:
#             - 'student_name': The name of the student.
#             - 'student_number': The student number.
#             - 'course_name': The name of the course.
#
#     Returns:
#         None. Prints a statement confirming that the file was written.
#
#     Conditions:
#         The use of error handling routine is compulsory.
#     '''
#     pass
import json


def addStudent(student_detail: dict) -> bool:
    try:
        with open("somefile.txt", "a") as f:
            f.write(json.dumps(student_detail))
    except Exception as e:
        print(f"Error {e} occured")
        return False
    return True


details = {"name": "zakarya", "student_num": "123456",
           "course": "software engineering"}

if addStudent(details):
    print("success")
