from ctypes import c_int, c_uint, WinDLL, Structure, pointer, byref, c_wchar
from ctypes import WINFUNCTYPE, sizeof, windll
from ctypes.wintypes import HANDLE, LPCWSTR, LPARAM, WPARAM, HWND, MSG

from components.config import *

user32 = WinDLL('user32', use_last_error=True)
gdi32 = WinDLL('gdi32', use_last_error=True)
kernel32 = WinDLL('kernel32', use_last_error=True)

WNDPROCTYPE = WINFUNCTYPE(c_int, HWND, c_uint, WPARAM, LPARAM)
user32.DefWindowProcW.argtypes = [HWND, c_uint, WPARAM, LPARAM]


class WNDCLASSEX(Structure):
    _fields_ = [
        ("cbSize", c_uint),
        ("style", c_uint),
        ("lpfnWndProc", WNDPROCTYPE),
        ("cbClsExtra", c_int),
        ("cbWndExtra", c_int),
        ("hInstance", HANDLE),
        ("hIcon", HANDLE),
        ("hCursor", HANDLE),
        ("hBrush", HANDLE),
        ("lpszMenuName", LPCWSTR),
        ("lpszClassName", LPCWSTR),
        ("hIconSm", HANDLE)
    ]


def create_textbox(parent, x, y, width, height, text):
    return user32.CreateWindowExW(
        0, "Static", text,
        WS_VISIBLE | WS_CHILD | SS_SUNKEN,
        x, y, width, height, parent, None, None, None
    )


def create_edit_control(parent, x, y, width, height,
                        id):
    return user32.CreateWindowExW(
        0, "Edit", None,
        WS_VISIBLE | WS_CHILD | ES_LEFT,
        x, y, width, height, parent, id, None, None)


def create_button(parent, text, x, y, width, height, id_):
    return user32.CreateWindowExW(
        0, "Button", text,
        WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
        x, y, width, height, parent, id_, None, None
    )


def messagebox(text: str, title: str) -> int:
    return user32.MessageBoxW(None, text, title, 0)


class PythonWindow:
    def __init__(self, wndClass, classname, callback_f, inst: LPARAM):
        self.wndClass = wndClass
        self.classname = classname
        self.callback_f = callback_f
        self.inst = inst
        self.hWnd = None

    def setupWindow(self):
        self.wndClass.cbSize = sizeof(WNDCLASSEX)
        self.wndClass.style = CS_HREDRAW | CS_VREDRAW
        self.wndClass.lpfnWndProc = self.callback_f
        self.wndClass.cbClsExtra = 0
        self.wndClass.cbWndExtra = 0
        self.wndClass.hInstance = self.inst
        self.wndClass.hIcon = 0
        self.wndClass.hCursor = 0
        self.wndClass.hBrush = gdi32.GetStockObject(GRAY_BRUSH)
        self.wndClass.lpszMenuName = 0
        self.wndClass.lpszClassName = self.classname
        self.wndClass.hIconSm = 0
        user32.RegisterClassExW(byref(self.wndClass))

    def createWindow(self, window_name: str, x: int, y: int, width: int, height: int):
        self.hWnd = windll.user32.CreateWindowExW(
            0, self.classname, window_name,
            WS_OVERLAPPEDWINDOW | WS_CAPTION,
            x, y, width, height, 0, 0, self.inst, 0)
        if not self.hWnd:
            print('Failed to create window')
            exit(0)
        return self.hWnd

    def showWindow(self):
        user32.ShowWindow(self.hWnd, SW_SHOWNORMAL)
        user32.UpdateWindow(self.hWnd)
        return self.hWnd

    def run(self, msg: MSG):
        while user32.GetMessageW(byref(msg), 0, 0, 0) != 0:
            user32.TranslateMessage(byref(msg))
            user32.DispatchMessageW(byref(msg))
        return
