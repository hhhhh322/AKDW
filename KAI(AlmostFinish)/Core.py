'''
简单的语言控制工具，包含称呼，天气询问、问候语、指令：提醒
'''
from time import strftime
from snownlp import SnowNLP
from random import randint
from json import loads
from Weather import GetWeather
from tkinter import *
from sys import exit
from pyunit_time import Time as GetiTime
from datetime import datetime

call="博士"
calls="凯尔希"


Dict = {"1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "七", "8": "八", "9": "九", "0": "十"}
C_Dict = {"一": "1", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8", "九": "9", "零": "0"}
TC_Dict = {"1": "十", "2": "二十", "3": "三十", "4": "四十", "5": "五十"}

def GetTime(Input, OnlyTime=False, OnlyEvent=False):
    Call = "凯尔希"
    NTime = strftime("%Y-%m-%d %H:%M:%S")
    try:
        C_Time = Time = str(GetiTime(NTime).parse(Input)[0]["key"])
        Next_Time = str(GetiTime(NTime).parse(Input)[0]["keyDate"])
    except:
        return "Date ERROR"
    Lose_Time = ""

    # 将阿拉伯数字转换为汉字
    if ":" not in Input:
        for i in C_Time:
            try:
                int(i)
                if C_Time[C_Time.index(i) + 1].isdigit():
                    if i in TC_Dict.keys():
                        C_Time = C_Time.replace(i, TC_Dict[i], 1)
                    elif i == "0":
                        C_Time = C_Time.replace("0", "零")
            except:
                ...
            if i.isdigit():
                C_Time = C_Time.replace(str(i), Dict[i])
    if "零" in Input:
        for i in Input.replace(C_Time, "").replace("叫我", "").replace("提醒我", "").replace("分", ""):
            if i in C_Dict.keys():
                Lose_Time += i
                Lose_Time = Lose_Time.replace(i, C_Dict[i])
        if "分" not in Input:
            pass
        elif "分" in Input:
            Time = Time + Lose_Time + "分"
    Event = Input.replace(",", "").replace(Call, "").replace(C_Time, "").replace("叫我", "").replace("提醒我",
                                                                                                     "").replace("，",
                                                                                                                 "").replace(
        "。", "").replace("以后", "").replace("每天", "")

    Next_Time = Next_Time.split(" ")
    Fix_Time = Next_Time[1].split(":")
    New_Munit = ""
    # 将错误的分秒替换
    if "分" not in Time and "半" not in Time:
        New_Munit = "00"
        Fix_Time[1] = New_Munit
    elif "半" in Time:
        Fix_Time[1] = "30"
    else:
        for i in Time:
            if i == "点" and i != Time[-1]:
                i1 = Time[Time.index(i) + 1]
                New_Munit = New_Munit + i1 + Time[Time.index(i) + 2]
                break
        Fix_Time[1] = New_Munit
    Fix_Time[2] = "00"
    Fix_24H = ":".join(Fix_Time)
    Next_Time[1] = Fix_24H
    Next_Time = " ".join(Next_Time)

    DateCheck = Next_Time.split(" ")[0].split("-")
    DateCheck_Now = NTime.split(" ")[0].split("-")
    TimeCheck = Next_Time.split(" ")[1].split(":")
    TimeCheck_Now = NTime.split(" ")[1].split(":")

    Delta = datetime(int(DateCheck[0]), int(DateCheck[1]), int(DateCheck[2]), int(TimeCheck[0]),
                              int(TimeCheck[1]), int(TimeCheck[2])) - datetime(int(DateCheck_Now[0]),
                                                                                        int(DateCheck_Now[1]),
                                                                                        int(DateCheck_Now[2]),
                                                                                        int(TimeCheck_Now[0]),
                                                                                        int(TimeCheck_Now[1]),
                                                                                        int(TimeCheck_Now[2]))

    if not OnlyTime and not OnlyEvent:
        if Delta.days > 0 and Delta.days != 0 and Delta.days <= 6:
            return Next_Time, Event
        elif Delta.days == 0 and Delta.seconds != 0 and Delta.seconds >= 3600:
            return Next_Time, Event
        elif Delta.days == 0 and Delta.seconds != 0 and Delta.seconds < 3600:
            return "T_Short"
        else:
            return False
    elif OnlyTime and not OnlyEvent:
        if Delta.days > 0 and Delta.days != 0 and Delta.days <= 6:
            return Next_Time
        elif Delta.days == 0 and Delta.seconds != 0 and Delta.seconds >= 3600:
            return Next_Time
        elif Delta.days == 0 and Delta.seconds != 0 and Delta.seconds < 3600:
            return "T_Short"
        else:
            return False
    elif not OnlyTime and OnlyEvent:
        if Delta.days > 0 and Delta.days != 0 and Delta.days <= 6:
            return Event
        elif Delta.days == 0 and Delta.seconds != 0 and Delta.seconds >= 3600:
            return Event
        elif Delta.days == 0 and Delta.seconds != 0 and Delta.seconds < 3600:
            return "T_Short"
        else:
            return False


def GetTimeL(Input: str):
    global Year, Month, Day, Hour, Minute
    Back = GetTime(Input, True)
    if Back != "T_Short" or Back != False:
        BackL = Back.split(" ")
        BackDate = BackL[0].split("-")
        BackTime = BackL[1].split(":")
        Year = BackDate[0]
        Month = BackDate[1]
        Day = BackDate[2]
        Hour = BackTime[0]
        Minute = BackTime[1]
        return [Year, Month, Day, Hour, Minute]


# 句子成分或回答列表
WeatherIF=["天气","雨","雪","下雨","下雪","晴","晴天"]
Timing=["早","早上","午","中午","下午","晚","晚上"]
Greetings=["早安","早上好","午安","中午好","下午好","晚安","晚上好"]
Accepts=["好的。","明白了"]
Date=["周一","周二","周三","周四","周五","周六","周日","周天",]

# IF_Core必要变量
Weather=False
Change_Place=None


# 解析指令的函数，完全依赖判断句子成分运行，维护难度比较大，需要注意与其他类型句子的成分冲突。
def IF_Core(Input: str,Answer=None,Call="博士",CallS="凯尔希",NowEvent=None,Now_EventTime=None):
    global Time, Ask,Change_Place
    CallResot = ["怎么了," + Call+"?", "我在，有什么事？"]
    Input=Input.replace("?","").replace(",","").replace("。","")
    NLPed_Input=SnowNLP(Input)
    Tag=list(NLPed_Input.tags)
    Word=list(NLPed_Input.words)
    AcceptRand=randint(0,1)
    try:
        WordIndex = int(Word.index("".join(set(Word) & set(Timing))))
    except:
        pass
    Wordl=Input.split()
    Rewrite=0
    with open("MEMO.memory", "r",encoding='utf-8') as f:
        Memo = f.read()
        f.close()
    if Answer==None:
        # 称呼部分
        if CallS in Input and len(Input) == 3:
            print(CallResot[randint(0, 2)])
        # 天气询问
        elif len(list(set(WeatherIF) & set(Word)))!=0 or len(list(set(WeatherIF) & set(Wordl)))!=0:
            Weader_Data=loads(GetWeather("东莞"))
            for i in Tag:
                if i[1]=='t':
                    Time=i[0]
            if '明天' in Time:
                if "吗" in Word:
                    if "是" in Word:
                        Ask="是"
                    else:
                        for i in Tag:
                            if i[1]=='v' and i[0]!="看" and i[0]!="能" and i[0]!="帮":
                                Ask=i[0]
                                break
                    if len(list(set(list(Weader_Data["T_Weather"])) & set(list(Input))))!=0:
                        print(Ask)
                    else:
                        print("不"+Ask)
                elif "能" in Word:
                    if "天气" in Word:
                        print("明天的天气是" + Weader_Data["T_Weather"])
                    else:
                        for i in Tag:
                            if i[1]=='f'and "看" not in i[0] and "能" not in i[0] and "帮" not in i[0]:
                                Ask=i[0]
                                break
                            elif i[1]=='v'and "看" not in i[0] and "能" not in i[0] and "帮" not in i[0]:
                                Ask=i[0]
                                break
                    if len(list(set(list(Weader_Data["T_Weather"])) & set(list(Input))))!=0:
                        print(Ask)
                    else:
                        print("不"+Ask)
                elif "是否" in Word:
                    if len(list(set(list(Weader_Data["T_Weather"])) & set(list(Input)))) != 0 and "不会" not in Input:
                        print("是")
                    elif len(list(set(list(Weader_Data["T_Weather"])) & set(list(Input)))) != 0 and "不会" in Input:
                        print("不是")
                    else:
                        print("不是")
                else:
                    print("明天的天气是" + Weader_Data["T_Weather"])
            if "今天" in Time:
                if "吗" in Word:
                    if "是" in Word:
                        Ask = "是"
                    else:
                        for i in Tag:
                            if i[1] == 'v' and i[0] != "看" and i[0] != "能" and i[0] != "帮":
                                Ask = i[0]
                                break
                    if len(list(set(list(Weader_Data["T_Weather"])) & set(list(Input)))) != 0:
                        print(Ask)
                    else:
                        print("不" + Ask)
                elif "能" in Word:
                    if "天气" in Word:
                        print("今天的天气是" + Weader_Data["T_Weather"])
                    else:
                        for i in Tag:
                            if i[1] == 'f' and "看" not in i[0] and "能" not in i[0] and "帮" not in i[0]:
                                Ask = i[0]
                                break
                            elif i[1] == 'v' and "看" not in i[0] and "能" not in i[0] and "帮" not in i[0]:
                                Ask = i[0]
                                break
                    if len(list(set(list(Weader_Data["T_Weather"])) & set(list(Input)))) != 0:
                        print(Ask)
                    else:
                        print("不" + Ask)
                elif "是否" in Word:
                    if len(list(set(list(Weader_Data["T_Weather"])) & set(list(Input)))) != 0 and "不会" not in Input:
                        print("是")
                    elif len(list(set(list(Weader_Data["T_Weather"])) & set(list(Input)))) != 0 and "不会" in Input:
                        print("不是")
                    else:
                        print("不是")
                else:
                    print("今天的天气是"+Weader_Data["Weather"])
        # 备忘录部分
        elif "提醒我"in Input or"叫我"in Input:
            Fail=False
            Back = GetTime(Input)
            if "不用" in Input:
                # 删除逻辑
                Input=Input.replace("了",'').replace("明天","明天早上一点").replace("不用",'')
                f=open("MEMO.memory","r",encoding="utf-8")
                MEMOL=f.read().split("|")
                del MEMOL[-1]
                NowEvent=GetTime(Input,OnlyEvent=True)
                for i0 in MEMOL:
                    if eval(i0)[1]==NowEvent:
                        break
                    elif eval(i0)[1]!= NowEvent and i0==MEMOL[-1]:
                        print("你没有叫我提醒你做这件事，博士。")
                        Fail=True
                        return None
                if Fail!=True:
                    f.close()
                    f=open("MEMO.memory", "w+", encoding="utf-8")
                    for i in MEMOL:
                        i=eval(i)
                        if i[1] == NowEvent:
                            del MEMOL[MEMOL.index(str(i))]
                            print(Accepts[AcceptRand])
                            break
                    MEMOW="|".join(MEMOL)
                    f.write(MEMOW)
                    f.close()
                    return None
            else:
                pass
            if Back != False:
                if Back == "T_Short":
                    print("博士，这么短的时间内记住一件事不是什么困难吧。")
                MEMO=open("MEMO.memory","a+",encoding="utf-8")
                MEMO.seek(0)
                if MEMO.read()=="":
                    MEMO.write(str(Back)+"|")
                    print(Accepts[AcceptRand])
                else:
                    MEMO.seek(0)
                    for i in MEMO.read().split("|"):
                        if i!="":
                            Saved_Event_Time=eval(i)[0]
                            Now_EventTime=GetTime(Input,True)
                            if Saved_Event_Time==Now_EventTime:
                                Saved_Event=eval(i)[1]
                                Now_Event=GetTime(Input,OnlyEvent=True)
                                if Saved_Event==Now_Event:
                                    print("你已经说过了，我会记得的。")
                                    return None
                                if Saved_Event!=Now_Event:
                                    print("这个时候你要"+Saved_Event+",你想做哪个？")
                                    return "NeedAnswer",Now_Event,Now_EventTime
                    MEMO.write(str(Back)+"|")
                    print(Accepts[AcceptRand])
        # 问候语回复部分
        elif len(set(Word) & set(Timing))==1 and Word[WordIndex+1]=="好"or"安" and "你好" not in Word:
            a = Word[WordIndex + 1]
            del Word[WordIndex + 1]
            Word[WordIndex] = Word[WordIndex] + a
            if 0 < len(set(Greetings) & set(Word)) < 2:
                GreetingW = list(set(Greetings) & set(Word))
                NTime = int(strftime("%H"))
                if NTime > 5 and NTime < 11 and 0 <= Greetings.index(GreetingW[0]) <= 1:
                    print(GreetingW[0])
                elif 5 <= NTime <= 11 and 1 < Greetings.index(GreetingW[0]):
                    print(Call + "，你醒了吗，还是还在睡梦之中？")
                elif 12 == NTime and 2 <= Greetings.index(GreetingW[0]) <= 3:
                    print(GreetingW[0])
                elif 12 == NTime and 3 < Greetings.index(GreetingW[0]) and Greetings[0] != GreetingW[0] and \
                        Greetings[1] != GreetingW[0]:
                    print(Call + ",你醒了吗，还是还在睡梦之中？")
                elif 12 < NTime < 18 and Greetings.index(GreetingW[0]) == 4:
                    print(GreetingW[0])
                elif 12 < NTime < 18 and Greetings.index(GreetingW[0]) != 4:
                    print(Call + ",你醒了吗，还是还在睡梦之中？")
                elif 18 <= NTime < 5 and 4 < Greetings.index(GreetingW[0]) <= 6:
                    print(GreetingW[0])
                elif 18 <= NTime < 5 and Greetings.index(GreetingW[0]) <= 4:
                    print(print(Call + ",你醒了吗，还是还在睡梦之中？"))
        elif "你好"==Word[0] and len(Word)==1:
            print("你好,博士")
    elif Answer!=None:
        if Answer=="MEMO_SameTimeChos":
            MEMO=open("MEMO.memory","r",encoding="utf-8")
            for i in MEMO.read().split("|"):
                if i != "":
                    Saved_Event_Time = eval(i)[0]
                    if Saved_Event_Time==Now_EventTime:
                        Change_Place=list(eval(i))
                        break
            if  Change_Place[1] in Input:
                print(Accepts[AcceptRand])
            elif NowEvent in Input:
                MEMO.seek(0)
                MEMOF=MEMO.read().split("|")
                MEMO.close()
                MEMO=open("MEMO.memory","w+",encoding="utf-8")
                Index=MEMOF.index(str(tuple(Change_Place)))
                Change_Place[1]=NowEvent
                MEMOF[Index]=str(tuple(Change_Place))
                MEMOW="|".join(MEMOF)
                MEMO.write(MEMOW)
                print(Accepts[AcceptRand])
            else:
                print("是在这两个里面选一个，博士。")
                NowEvent = GetTime(Input, OnlyEvent=True)
                return "NeedAnswer",NowEvent,Now_EventTime

# 界面相关变量
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
            c=IF_Core(a)
        else:
            if c[0]=="NeedAnswer":
                c=IF_Core(a,"MEMO_SameTimeChos",NowEvent=c[1],Now_EventTime=c[2])

# 界面
tk=Tk()
tk.geometry("300x100")
tk.title("Chat")
Input=Entry(tk,width=190)
Input.place(x=0,y=0)
Buton=Button(tk,text="In",command=Inp)
Buton.place(x=20,y=30)
tk.mainloop()