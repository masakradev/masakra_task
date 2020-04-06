#!/usr/bin/python3
from ctypes import *

__all__ = ["gotoxy", "cls"]

class COORD(Structure):
  _fields_ = [
      ("x", c_short),
      ("y", c_short)
  ]

class SMALL_RECT(Structure):
  _fields_ = [
      ("Left", c_short),
      ("Top", c_short),
      ("Right", c_short),
      ("Bottom", c_short),
  ]    

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
  _fields_ = [
      ("dwSize", COORD),
      ("dwCursorPosition", COORD),
      ("wAttributes", c_ushort),
      ("srWindow", SMALL_RECT),
      ("dwMaximumWindowSize", COORD)
  ]


# Active Console Screen Buffer
ACSB = None

STD_OUTPUT_HANDLE = -11
STD_INPUT_HANDLE = -10

k32 = windll.kernel32


def _acsb():
  global ACSB

  if ACSB is None:
    ACSB = k32.GetStdHandle(STD_OUTPUT_HANDLE)

  return ACSB

def gotoxy(x, y):
  c = COORD()
  c.x = x
  c.y = y
  
  k32.SetConsoleCursorPosition(_acsb(), c)
  
def cls():
  # Basically https://support.microsoft.com/en-us/kb/99261 translated to
  # Python.
  csbi = CONSOLE_SCREEN_BUFFER_INFO()
  k32.GetConsoleScreenBufferInfo(_acsb(), byref(csbi))
  con_size = csbi.dwSize.x * csbi.dwSize.y

  coord_screen = COORD()
  coord_screen.x = 0
  coord_screen.y = 0

  chars_written = c_uint()

  k32.FillConsoleOutputCharacterA(
      _acsb(), 0x20, con_size, coord_screen, byref(chars_written))
  k32.FillConsoleOutputAttribute(
      _acsb(), csbi.wAttributes, con_size, coord_screen, byref(chars_written))
  k32.SetConsoleCursorPosition(_acsb(), coord_screen)

if __name__ == "__main__":
  print("cls() test")
  cls()
  print("after cls")
  print("gotoxy(10, 10) test")
  gotoxy(10, 10)
  print("after goto")