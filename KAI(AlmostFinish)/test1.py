from time import strftime
from snownlp import SnowNLP
from sys import argv
Greetings=["早安","早上好","午安","中午好","下午好","晚安","晚上好","你好"]
Timing=["早","早上","午","中午","下午","晚","晚上"]
Call="博士"
Input=argv[1]
Input=Input.replace("?","").replace(",","").replace("。","")
NLPed_Input=SnowNLP(Input)
Word=list(NLPed_Input.words)

WordIndex=int(Word.index("".join(set(Word) & set(Timing))))

if len(set(Word) & set(Timing))==1 and Word[WordIndex+1]=="好"or"安" and "你好" not in Word:
    a=Word[WordIndex+1]
    del Word[WordIndex+1]
    Word[WordIndex]=Word[WordIndex]+a
    if 0 < len(set(Greetings) & set(Word)) < 2:
        GreetingW=list(set(Greetings) & set(Word))
        NTime=int(strftime("%H"))
        if GreetingW[0]!=Greetings[-1]:
            if NTime>5 and NTime < 11 and 0<=Greetings.index(GreetingW[0])<=1:
                print(GreetingW[0])
            elif 5 <= NTime <= 11 and 1<Greetings.index(GreetingW[0]):
                print(Call+"，你醒了吗，还是还在睡梦之中？")
            elif 12==NTime and 2<=Greetings.index(GreetingW[0])<=3:
                print(GreetingW[0])
            elif 12==NTime and 3<Greetings.index(GreetingW[0]) and Greetings[0]!= GreetingW[0] and Greetings[1] != GreetingW[0]:
                print(Call+",你醒了吗，还是还在睡梦之中？")
            elif 12<NTime<18 and Greetings.index(GreetingW[0])==4:
                print(GreetingW[0])
            elif 12<NTime<18 and Greetings.index(GreetingW[0])!=4:
                print(Call + ",你醒了吗，还是还在睡梦之中？")
            elif 18<=NTime<5 and 4<Greetings.index(GreetingW[0])<=6:
                print(GreetingW[0])
            elif 18<=NTime<5 and Greetings.index(GreetingW[0])<=4:
                print(print(Call + ",你醒了吗，还是还在睡梦之中？"))
        else:
            print(GreetingW[0])