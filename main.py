import tkinter as tk
from sys import platform,exit
from tkinter import ttk,simpledialog
import os.path
from tkinter.messagebox import showerror,showinfo

import pymupdf
from PIL import ImageTk

now_page = 0
all_page = 0
doc = None
page_bar = None
image_doc = None
dpi = 83


def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def upd_title():
    app.title(f"{doc.metadata["title"]}-{now_page+1}/{all_page} 按[Control+G]跳转")
def upd_bar():
    page_bar["value"] = now_page+1
def go_button(event : tk.Event):
    i = simpledialog.askinteger("请输入",f"页数(1-{all_page})")
    if (i-1)>=all_page or (i-1)<0 :
        showinfo("提示","输入不合法")
        return
    global now_page
    now_page = i-1
    upd_image()
    upd_title()
    upd_bar()
def upd_image():
    try:
        pag_ = doc.load_page(now_page)
        pix = pag_.get_pixmap(dpi=dpi)
        pili = pix.pil_image()
        tki = ImageTk.PhotoImage(pili)
        image_doc.config(image=tki)
        image_doc.image = tki
    except Exception as e:
        showerror(title="错误",message=f"渲染错误：\n{e}")
def on_up():
    global now_page
    if now_page <= 0:
        return
    now_page = now_page -1
    upd_title()
    upd_bar()
    upd_image()
def on_next():
    global now_page
    if now_page + 1 >= all_page:
        return
    now_page = now_page +1
    upd_title()
    upd_bar()
    upd_image()
def s_ch(event : tk.Event):
    global dpi
    if dpi - event.delta <= 0:
        return
    dpi = dpi - event.delta
    upd_image()
def s_ch_up(event : tk.Event):
    global dpi
    dpi = dpi + 2
    upd_image()
def s_ch_down(event : tk.Event):
    global dpi
    if dpi - 2 <= 0:
        return
    dpi = dpi - 2
    upd_image()
if __name__ == "__main__":
    #init
    try:
        doc = pymupdf.open(get_resource_path("file"))
    except Exception as e:
        showerror("错误",f"文件加载错误:{e}")
        exit(1)
    app = tk.Tk()
    try:
        app.iconphoto(False, tk.PhotoImage(file=get_resource_path("icon.png")))
    except Exception as e:
        showerror("错误",f"图标加载错误{e}")
    app.geometry("1024x720")
    all_page = doc.page_count
    upd_title()
    #工具栏定义，初始化
    top_frame = tk.Frame(app,height=30)
    top_frame.pack(fill="x")
    page_bar = ttk.Progressbar(top_frame,orient="horizontal")
    up_page = tk.Button(top_frame,text="上一页",command=on_up)
    next_page = tk.Button(top_frame,text="下一页",command=on_next)
    up_page.place(relwidth=0.1,relheight=1,relx=0)
    next_page.place(relwidth=0.1,relheight=1,relx=0.9)
    page_bar.place(relheight=1,relwidth=0.8,relx=0.1)
    page_bar["maximum"] = all_page
    upd_bar()
    #文章初始化
    image_doc = tk.Label(app,background="black")
    image_doc.pack(fill="both")
    #滚轮-win man and linux
    if platform == "linux":
        app.bind("<Button-5>",s_ch_down)
        app.bind("<Button-4>",s_ch_up)
    else:
        app.bind("<MouseWheel>",s_ch)
    app.bind("<Control-g>",go_button)
    upd_image()
    #run
    app.mainloop()
