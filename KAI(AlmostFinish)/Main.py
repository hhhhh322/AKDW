import Core
import tkinter
from tkinter import *
from sys import exit
call="博士"
calls="凯尔希"

a=None
c=None
def Inp():
    global a,c
    a=Input.get()
    Input.delete(0,"end")
    if a=="再见":
        print("再见")
        tk.destroy()
        exit(0)
    else:
        if c is None:
            c=Core.IF_Core(a)
        else:
            if c[0]=="NeedAnswer":
                c=Core.IF_Core(a,"MEMO_SameTimeChos",NowEvent=c[1],Now_EventTime=c[2])
tk=Tk()
tk.geometry("300x100")
tk.title("Chat")
Input=tkinter.Entry(tk,width=190)
Input.place(x=0,y=0)
Buton=tkinter.Button(tk,text="In",command=Inp)
Buton.place(x=20,y=30)
tk.mainloop()

'''
Memory=Core.Read_Memory()
for i in Memory:
    i=i.replace("\n","")
    i=i.split(",")
    if "#" in i:
        pass
    else:
        if "call" in i:
            call = i[1]
        elif "calls" in i:
            calls = i[1]


while True:
    Input=input(">")
    if Input!="再见":
        Core.IF_Core(Input,call,calls)
    else:
        print("再见")
        break
'''