from tkinter import *
import tkinter
from PIL import Image, ImageTk
#from sys import argv
from time import sleep
from webbrowser import open_new as openurl
from imaplib import IMAP4_SSL,Commands
from sys import exit
from threading import Timer

frame=1
x=332
f=open("./EmailSetting","r")
tk=None

def create_images():
    img1 = Image.open("./assets/INBOX.png")
    mask = Image.open("./assets/Mask.png")
    photo = ImageTk.PhotoImage(mask)
    photo1 = ImageTk.PhotoImage(img1)
    return photo,photo1

def GoEmail(event):
    global frame
    frame=62
    url=""
    f.seek(0)
    Adress=f.read().split(",")[0]
    f.seek(0)
    if "@qq.com" in Adress:
        url="https://mail.qq.com/"
    elif "@aliyun.com" in Adress:
        url="https://mail.aliyun.com/"
    elif "@163.com" in Adress:
        url="https://mail.163.com/"
    elif "@126.com" in Adress:
        url="https://www.126.com/"
    elif "@yeah.net" in Adress:
        url="https://www.yeah.net/"
    elif "@outlook.com" in Adress:
        url="https://www.microsoft.com/zh-cn/microsoft-365/outlook/email-and-calendar-software-microsoft-outlook/"
    elif len(f.read().split(","))==3:
        f.seek(0)
        url=f.read().split(",")[2]
    openurl(url)

def _update():
    global frame,x,tk
    if frame<30:
        x-=11.5
        label_img.place(x=x, y=-2)
    elif frame==30:
        l.place(x=-2, y=-2)
        label_img.place(x=x,y=-2)
    elif frame>30 and frame<61:
        x-=11.5
        l.place(x=-2,y=-2)
        label_img.place(x=x, y=-2)
    elif frame == 61:
        x=332
        l.place(x=-2, y=-2)
        label_img.place(x=x, y=-2)
        sleep(2)
    elif frame>61 and frame<91:
        x -= 11.5
        l.place(x=-2, y=-2)
        label_img.place(x=x, y=-2)
    elif frame==91:
        l.place(x=-2,y=-100)
    elif frame>91 and frame<121:
        x-=11.5
        label_img.place(x=x,y=-2)
    if frame!=121:
        frame += 1
        tk.after(13, _update)
    else:
        tk.destroy()

def OutWindow():
    global label_img,l,tk
    tk = Tk()
    photo,photo1=create_images()
    tk.attributes('-topmost', 'true')
    width=tk.winfo_screenwidth()
    hight=tk.winfo_screenwidth()
    Wx=width-330
    Wy=int(hight/7)-51
    wp='330x51'+'+'+str(Wx)+'+'+str(Wy)
    TRANSCOLOUR = 'gray'
    tk.bind("<Button-1>",GoEmail)
    tk.geometry(wp)
    tk.overrideredirect(True)
    TRANSCOLOUR = 'gray'
    tk.wm_attributes('-transparentcolor', TRANSCOLOUR)
    tk.config(bg=TRANSCOLOUR)
    l=tkinter.Label(tk, image=photo1)
    label_img = tkinter.Label(tk, image=photo)
    if frame==1:
        label_img.place(x=x,y=0)
    _update()
    create_images()
    tk.mainloop()
def Get_server():
    f.seek(0)
    adress=f.read().split(",")[0]
    if "@qq.com" in adress:
        return 'imap.qq.com','993'
    elif "@163.com" in adress:
        return 'imap.163.com','993'
    elif "@aliyun.com" in adress:
        return 'imap.aliyun.com','993'
    elif "@126.com" in adress:
        return 'imap.126.com','993'
    elif "@yeah.net" in adress:
        return 'imap.yeah.net','993'
    elif "@outlook.com" in adress:
        return 'imap-mail.outlook.com','993'
def Check_Mail():
    f.seek(0)
    user=f.read().split(",")[0]
    f.seek(0)
    password=f.read().split(",")[1]
    if "@163.com" in user:
        from imapclient import IMAPClient
        server=IMAPClient(Get_server()[0],ssl=True,port=Get_server()[1])
        server.login(user,password)
        server.id_({"name": "sbwangyirnm", "version": "1.0.0"})
        server.select_folder('INBOX')
        unRead=server.search("UNSEEN")
        if unRead != []:
            return True
        else:
            return False
    else:
        M = IMAP4_SSL(Get_server()[0],Get_server()[1])
        M.login(user,password)
        args = ("name","AKDW","support-email",user,"version","1.0.0","vendor","myclient")
        unRead = M.search(None, 'UnSeen')
        M.logout()
        if unRead[1][0]!=b'':
            return True
        else:
            return False
OutWindow()
