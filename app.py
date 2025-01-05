"""
I will only use stdlib modules for this project
No external libraries will be used so there is no need to install dependencies
As long as you have a standard python installation on windows,
everything should run smoothly.
"""
import sqlite3
import os

import components.startup as mm
from components.config import *
from components.gui import *
from components import gui as gui
from Tasks.addStudent import addStudent
from Tasks.deleteStudent import deleteStudent
from Tasks.getStudent import getStudent


def win_callback(hWnd: HWND, Msg: MSG, wParam: WPARAM, lParam: LPARAM):
    if Msg == WM_COMMAND:
        control_id = wParam & 0xFFFF
        match control_id:
            case gui.ID_BUTTON1:
                # get the id from the edit control
                edit_control = user32.GetDlgItem(hWnd, ID_EDIT1)
                text_length = user32.GetWindowTextLengthW(edit_control)
                buffer = (c_wchar * (text_length + 1))()
                user32.GetWindowTextW(edit_control, buffer, text_length + 1)
                current_id = buffer.value
                messagebox(f"Looking for student with ID: {
                           current_id}", "Notification")
                try:
                    messagebox(str(getStudent(current_id)), "Student Found")
                except Exception as e:
                    messagebox(str(e), "Error")
                finally:
                    user32.SetWindowTextW(edit_control, "")
            case gui.ID_BUTTON2:
                # delete student from ID
                edit_control = user32.GetDlgItem(hWnd, ID_EDIT1)
                text_length = user32.GetWindowTextLengthW(edit_control)
                buffer = (c_wchar * (text_length + 1))()
                user32.GetWindowTextW(edit_control, buffer, text_length + 1)
                current_id = buffer.value
                messagebox(f"Deleting student with ID: {
                           current_id}", "Notification")
                try:
                    deleteStudent(current_id)
                    messagebox("Student deleted successfully", "Notification")
                except Exception as e:
                    messagebox(str(e), "Error")
                finally:
                    user32.SetWindowTextW(edit_control, "")
            case gui.ID_BUTTON3:
                # add student
                edit_control1 = user32.GetDlgItem(hWnd, ID_EDIT1)
                edit_control2 = user32.GetDlgItem(hWnd, ID_EDIT2)
                edit_control3 = user32.GetDlgItem(hWnd, ID_EDIT3)
                text_length1 = user32.GetWindowTextLengthW(edit_control1)
                text_length2 = user32.GetWindowTextLengthW(edit_control2)
                text_length3 = user32.GetWindowTextLengthW(edit_control3)
                buffer1 = (c_wchar * (text_length1 + 1))()
                buffer2 = (c_wchar * (text_length2 + 1))()
                buffer3 = (c_wchar * (text_length3 + 1))()
                user32.GetWindowTextW(edit_control1, buffer1, text_length1 + 1)
                user32.GetWindowTextW(edit_control2, buffer2, text_length2 + 1)
                user32.GetWindowTextW(edit_control3, buffer3, text_length3 + 1)
                current_id = buffer1.value
                current_name = buffer2.value
                current_course = buffer3.value
                student = {
                    "student_name": current_name,
                    "student_number": current_id,
                    "course_name": current_course
                }
                messagebox(f"Adding student: {student}", "Notification")
                try:
                    addStudent(student)
                    messagebox("Student added successfully", "Notification")
                except Exception as e:
                    messagebox(str(e), "Error")
                finally:
                    user32.SetWindowTextW(edit_control1, "")
                    user32.SetWindowTextW(edit_control2, "")
                    user32.SetWindowTextW(edit_control3, "")
    elif Msg == WM_DESTROY:
        user32.PostQuitMessage(0)
        return 0
    return user32.DefWindowProcW(hWnd, Msg, wParam, lParam)


def main():
    WndProc = WNDPROCTYPE(win_callback)
    hInst = kernel32.GetModuleHandleW(0)
    wndClass = WNDCLASSEX()
    wndclassname = "my windowclass"

    window = PythonWindow(wndClass, wndclassname, WndProc, hInst)
    window.setupWindow()
    hwnd = window.createWindow(
        "Student Records App", 100, 100, 600, 400)

    create_textbox(hwnd, 50, 50, 200, 20, "Enter ID:")
    create_edit_control(hwnd, 50, 70, 200, 20, ID_EDIT1)
    create_textbox(hwnd, 50, 120, 200, 20, "Enter Name:")
    create_edit_control(hwnd, 50, 140, 200, 20, ID_EDIT2)
    create_textbox(hwnd, 50, 165, 200, 20, "Enter course:")
    create_edit_control(hwnd, 50, 180, 200, 20, ID_EDIT3)

    create_button(hwnd, "Get Student From ID", 270, 50, 200, 30, ID_BUTTON1)
    create_button(hwnd, "Delete Student From DB by ID",
                  270, 80, 200, 30, ID_BUTTON2)
    create_button(hwnd, "Add Student", 270, 110, 200, 30, ID_BUTTON3)

    window.showWindow()
    msg = MSG()
    window.run(msg)


if __name__ == '__main__':
    mm.startup()
    main()
