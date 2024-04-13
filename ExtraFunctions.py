from hashlib import md5
from os import listdir
from time import strftime
from zhdate import ZhDate as L_Date

def CheckIntegrity():
    ...

def Check_Festival():
    DBF=str(L_Date(int(strftime("%Y")),5,5).to_datetime()).replace(" 00:00:00","").replace("-","")#端午节时间
    SF=str(L_Date(int(strftime("%Y")),1,1).to_datetime()).replace(" 00:00:00","").replace("-","")# 春节时间
    ChristmasDay=strftime("%Y")+"1215"
    Labor=strftime("%Y")+"0501"
    National=strftime("%Y")+"1001"
    Festival_L=[DBF,SF,ChristmasDay,Labor,National]
    Festival_D={0: "端午节",1: "新年",2:"圣诞节",3:"劳动节",4:"国庆节"}
    if strftime("%Y%m%d") in Festival_L:
        print(Festival_D[Festival_L.index(strftime("%Y%m%d"))])


