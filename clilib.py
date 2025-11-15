import os
import platform
def print_with_box_no_endline(s : str):
    ml = 0
    sl = s.splitlines()
    for t in sl:
        ml = max(len(t),ml)
    for i in range(ml):
        print("=",end="")
    print("")
    for t in sl:
        print(f"|{t}|")
    for i in range(ml):
        print("=", end="")
def print_with_box(s : str):
    print_with_box_no_endline(s)
    print("")
def cleans():
    s = platform.system()
    if s == "Windows":
        os.system("cls")
    else:
        os.system("clear")
