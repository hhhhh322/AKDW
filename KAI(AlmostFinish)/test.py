from snownlp import SnowNLP,seg
from sys import argv
#from jieba import lcut,load_userdict
from time import strftime
#from pyunit_time import Time
#from DealTime import Time

#print(Time(argv[1]))

with open("MEMO.memory","r") as f:
    a=f.read()
    print(a)
    f.close()


'''
s=SnowNLP(argv[1])

print(list(s.tags))
print(list(s.words))


print(s.keywords(5,True))
Date=["周一","周二","周三","周四","周五","周六","周日","周天",]
Re_Time=""
for i in s.keywords(5, True):
    for i1 in list(SnowNLP(i).tags):
        print(list(SnowNLP(i).tags))
        if i1[1] == 't':
            Re_Time = Re_Time.join(i)
            break
        elif i1[1] == 'e':
            for i2 in Date:
                if i2 in i:
                    Re_Time = Re_Time.join(i)
Mounth=strftime("%m")
Day=strftime("%d")
Hour=strftime("%H")
Munin=strftime("%M")
Sec=strftime("%S")
Week=strftime("%a")
# 需要补全时间转换
#Call="凯尔希"
#UnEvent=argv[1].replace(",","").replace(Call,"").replace(Re_Time,"").replace("叫我","").replace("提醒我","").replace("，","").replace("。","")
#print(UnEvent)
print(Re_Time)
'''
'''
T=""
for i in s.keywords(5,True):
    for i1 in list(SnowNLP(i).tags):
        print(list(SnowNLP(i).tags))
        if i1[1]=='v':
            T=T.join(i)
            break
        elif i1[1]=='nr':
            T=T.join(i)
            break
        elif i1[1]=='e':
            T=T.join(i)
            break
'''


#print(T)
'''
load_userdict("./Jieba.txt")
for i in lcut(argv[1]):
    print(list(SnowNLP(i).keywords(5,True)))

for i in lcut(argv[1]):
    print(list(SnowNLP(i).tags))
'''


