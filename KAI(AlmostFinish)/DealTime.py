from pyunit_time import Time as GetiTime
from time import strftime
import datetime

Dict={"1":"一","2":"二","3":"三","4":"四","5":"五","6":"六","7":"七","8":"八","9":"九","0":"十"}
C_Dict={"一":"1","二":"2","三":"3","四":"4","五":"5","六":"6","七":"7","八":"8","九":"9","零":"0"}
TC_Dict={"1":"十","2":"二十","3":"三十","4":"四十","5":"五十"}

def GetTime(Input,OnlyTime=False,OnlyEvent=False):
    Call="凯尔希"
    NTime=strftime("%Y-%m-%d %H:%M:%S")
    try:
        C_Time=Time=str(GetiTime(NTime).parse(Input)[0]["key"])
        Next_Time=str(GetiTime(NTime).parse(Input)[0]["keyDate"])
    except:
        return "Date ERROR"
    Lose_Time=""

    #将阿拉伯数字转换为汉字
    if ":"not in Input:
        for i in C_Time:
            try:
                int(i)
                if C_Time[C_Time.index(i)+1].isdigit():
                    if i in TC_Dict.keys():
                        C_Time=C_Time.replace(i,TC_Dict[i],1)
                    elif i=="0":
                        C_Time=C_Time.replace("0","零")
            except:
                ...
            if i.isdigit():
                C_Time=C_Time.replace(str(i), Dict[i])
    if "零"in Input:
        for i in Input.replace(C_Time, "").replace("叫我", "").replace("提醒我", "").replace("分", ""):
            if i in C_Dict.keys():
                Lose_Time+=i
                Lose_Time=Lose_Time.replace(i,C_Dict[i])
        if "分"not in Input:
            pass
        elif "分" in Input:
            Time=Time+Lose_Time+"分"
    Event = Input.replace(",", "").replace(Call, "").replace(C_Time, "").replace("叫我", "").replace("提醒我","").replace("，","").replace("。", "").replace("以后", "").replace("每天", "")

    Next_Time = Next_Time.split(" ")
    Fix_Time = Next_Time[1].split(":")
    New_Munit = ""
    # 将错误的分秒替换
    if "分"not in Time and "半" not in Time:
        New_Munit = "00"
        Fix_Time[1] = New_Munit
    elif "半" in Time:
        Fix_Time[1]="30"
    else:
        for i in Time:
            if i == "点" and i != Time[-1]:
                i1 = Time[Time.index(i) + 1]
                New_Munit=New_Munit+i1+Time[Time.index(i) + 2]
                break
        Fix_Time[1] = New_Munit
    Fix_Time[2] = "00"
    Fix_24H = ":".join(Fix_Time)
    Next_Time[1] = Fix_24H
    Next_Time = " ".join(Next_Time)

    DateCheck=Next_Time.split(" ")[0].split("-")
    DateCheck_Now=NTime.split(" ")[0].split("-")
    TimeCheck=Next_Time.split(" ")[1].split(":")
    TimeCheck_Now=NTime.split(" ")[1].split(":")

    Delta=datetime.datetime(int(DateCheck[0]), int(DateCheck[1]), int(DateCheck[2]), int(TimeCheck[0]), int(TimeCheck[1]), int(TimeCheck[2]))-datetime.datetime(int(DateCheck_Now[0]), int(DateCheck_Now[1]), int(DateCheck_Now[2]), int(TimeCheck_Now[0]), int(TimeCheck_Now[1]), int(TimeCheck_Now[2]))
    
    if not OnlyTime and not OnlyEvent:
        if Delta.days > 0 and Delta.days!=0 and Delta.days<=6:
            return Next_Time,Event
        elif Delta.days==0 and Delta.seconds!=0 and Delta.seconds>=3600:
            return Next_Time,Event
        elif Delta.days==0 and Delta.seconds!=0 and Delta.seconds<3600:
            return "T_Short"
        else:
            return False
    elif OnlyTime and not OnlyEvent:
        if Delta.days > 0 and Delta.days!=0 and Delta.days<=6:
            return Next_Time
        elif Delta.days==0 and Delta.seconds!=0 and Delta.seconds>=3600:
            return Next_Time
        elif Delta.days==0 and Delta.seconds!=0 and Delta.seconds<3600:
            return "T_Short"
        else:
            return False
    elif not OnlyTime and OnlyEvent:
        if Delta.days > 0 and Delta.days!=0 and Delta.days<=6:
            return Event
        elif Delta.days==0 and Delta.seconds!=0 and Delta.seconds>=3600:
            return Event
        elif Delta.days==0 and Delta.seconds!=0 and Delta.seconds<3600:
            return "T_Short"
        else:
            return False

def GetTimeL(Input:str):
    global Year,Month,Day,Hour,Minute
    Back=GetTime(Input,True)
    if Back!="T_Short" or Back!=False:
        BackL=Back.split(" ")
        BackDate=BackL[0].split("-")
        BackTime=BackL[1].split(":")
        Year=BackDate[0]
        Month=BackDate[1]
        Day=BackDate[2]
        Hour=BackTime[0]
        Minute=BackTime[1]
        return [Year,Month,Day,Hour,Minute]