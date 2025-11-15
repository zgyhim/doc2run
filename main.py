import os
import uuid
import shutil
from InquirerPy import inquirer as ip
from PyInstaller.compat import system
from colorama import init,Fore,Back,Style
import clilib
import sys
from tkinter.filedialog import askopenfilename,asksaveasfilename
toolbox = ip.select("选择功能",choices=["编译","检测依赖","退出"])

while True:
    os.system("conda deactivate")
    clilib.cleans()
    clilib.print_with_box("""    ____  ____  _________   ____  __  ___   __
   / __ \\/ __ \\/ ____/__ \\ / __ \\/ / / / | / /
  / / / / / / / /    __/ // /_/ / / / /  |/ / 
 / /_/ / /_/ / /___ / __// _, _/ /_/ / /|  /  
/_____/\\____/\\____//____/_/ |_|\\____/_/ |_/   
                                              """)

    c = toolbox.execute()
    if c == "退出":
        clilib.cleans()
        exit(0)
    if c == "检测依赖":
        clilib.cleans()
        clilib.print_with_box("依赖检测")
        print("开始测试")
        print("pyinstall-",end="")
        if os.system(f"pyinstaller -v") == 0:
            print(Fore.GREEN + "OK" + Style.RESET_ALL)
        else:
            print(Fore.RED + "ERROR" + Style.RESET_ALL)
        print("pymupdf---",end="")
        try: import pymupdf
        except Exception:
            print(Fore.RED + "ERROR" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "OK" + Style.RESET_ALL)
        print("pillow----",end="")
        try: import PIL
        except Exception:
            print(Fore.RED + "ERROR" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "OK" + Style.RESET_ALL)
        print("测试完成")
        input("按下回车键退出")
    if c == "编译":
        fp = askopenfilename(title="选择文档",filetypes=(("Text files", "*.txt"), ("All files", "*.*"),("PDF files","*.pdf"),("XPS files","*.xps"),("EPUB files","*.epub"),("MOBI files","*.mobi"),("FB2","*.fb2"),("CBZ files","*.cbz"),("SVG files","*.svg")))
        print(fp)
        if fp == "" or fp is None or fp == ():
            continue
        op = asksaveasfilename(title="文件保存",filetypes=(("Exe","*.exe"),("ELF","*")))
        print(op)
        if op == "" or op is None or op == ():
            continue
        clilib.cleans()
        clilib.print_with_box("编译")
        fid = uuid.uuid4()
        print(f"生成UUID:f{fid}")
        if not os.path.exists("view_envs"):
            os.mkdir("view_envs")
        if not os.path.exists("output"):
            os.mkdir("output")
        if os.path.exists(f"view_envs/{fid}"):
            shutil.rmtree(f"view_envs/{fid}")
        shutil.copytree("view_program",f"view_envs/{fid}")
        os.chdir(f"view_envs/{fid}")
        shutil.copy(fp,"file")
        os.system(f"pyinstaller main.spec")
        if not os.path.exists("./dist/main"):
            print(Fore.RED + "编译失败" + Style.RESET_ALL)
            input("按下回车键退出")
            os.chdir("../..")
            shutil.rmtree(f"view_envs/{fid}")
            continue
        if os.path.exists(op):
            os.remove(op)
        shutil.copy("./dist/main",op)
        os.chdir("../..")
        shutil.rmtree(f"view_envs/{fid}")
        print(Fore.GREEN + "完成" + Style.RESET_ALL)
        input("按下回车键退出")