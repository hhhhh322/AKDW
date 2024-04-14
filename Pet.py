import jpype.imports
import pygame
from jpype import JImplements, JOverride
from random import randint
from os import getcwd,listdir,system
from sys import argv,exit
from win32gui import FindWindow,SetWindowPos,GetWindowRect,SetForegroundWindow,GetDC
from win32print import GetDeviceCaps
from win32con import HWND_TOPMOST,SWP_SHOWWINDOW,WS_EX_LAYERED,WS_EX_TRANSPARENT,GWL_EXSTYLE,LWA_ALPHA,DESKTOPHORZRES,DESKTOPVERTRES
from threading import Timer,Thread
from time import strftime
from zipimport import zipimporter
from pygame import mixer
from pygame import *
from win32api import SetWindowLong,GetWindowLong

ExtraFunc=zipimporter("ExtraFunc.zip")
Soap=ExtraFunc.load_module("SoapSystem")
PopWindow=ExtraFunc.load_module("PopWindow")
ModleName=argv[1]+"/"
Modle_Atlas="Modle/"+ModleName+argv[2]
Modle_Json="Modle/"+ModleName+argv[3]

# 定义Jar文件列表，不同平台需要不同的natives文件，待添加Winodws、MacOS
Windows=['./Jars/gdx-backend-lwjgl3-1.11.0.jar','./Jars/gdx-1.11.0.jar','./Jars/lwjgl-glfw-3.3.1.jar','./Jars/lwjgl-3.3.1.jar','./Jars/gdx-jnigen-loader-2.3.1.jar','./Jars/gdx-platform-1.11.0-natives-desktop.jar',
           './Jars/lwjgl-3.3.1-natives-windows.jar','./Jars/lwjgl-glfw-3.3.1-natives-windows.jar','./Jars/lwjgl-opengl-3.3.1.jar','./Jars/lwjgl-opengl-3.3.1-natives-windows.jar','./Jars/lwjgl-openal-3.3.1.jar',
           './Jars/lwjgl-openal-3.3.1-natives-windows.jar','./Jars/Spine-GDX.jar','./Jars/gdx-freetype-1.11.0.jar','./Jars/gdx-freetype-platform-1.11.0-natives-desktop.jar']
PLATFORM=Windows
jpype.startJVM(classpath=PLATFORM)  # 启动JVM

pygame.init()
mixer.init()# 初始化音频播放，由于结构设计或是jpype的问题，GDX的音频无法使用

# 引入相关Jar包 下面那些注释不能删，删了报错。
# noinspection PyUnresolvedReferences
from com.badlogic.gdx.backends.lwjgl3 import Lwjgl3Application,Lwjgl3ApplicationConfiguration
# noinspection PyUnresolvedReferences
from com.badlogic.gdx.graphics.g2d import TextureAtlas,SpriteBatch
# noinspection PyUnresolvedReferences
from com.badlogic.gdx.utils import TimeUtils, Array,ScreenUtils
# noinspection PyUnresolvedReferences
from com.badlogic.gdx.math import MathUtils, Rectangle, Vector3
# noinspection PyUnresolvedReferences
from com.badlogic.gdx import ApplicationListener, Gdx, Input,InputProcessor,InputAdapter
# noinspection PyUnresolvedReferences
from com.badlogic.gdx import *
# noinspection PyUnresolvedReferences
from com.esotericsoftware.spine.utils import TwoColorPolygonBatch
# noinspection PyUnresolvedReferences
from com.esotericsoftware.spine import SkeletonRenderer,Skeleton,AnimationState,SkeletonJson,SkeletonData,AnimationStateData
# noinspection PyUnresolvedReferences
from com.badlogic.gdx.graphics.g2d.freetype import FreeTypeFontGenerator
# noinspection PyUnresolvedReferences
from com.badlogic.gdx.graphics import Color,Texture
# noinspection PyUnresolvedReferences
from com.badlogic.gdx.scenes.scene2d.ui import Image
# noinspection PyUnresolvedReferences
from com.badlogic.gdx.scenes.scene2d.ui import Button
# noinspection PyUnresolvedReferences
from com.badlogic.gdx.scenes.scene2d.utils import ClickListener,TextureRegionDrawable

@JImplements(ApplicationListener)# Jpype的包装器，实现libgdx的接口
class Pet:
    def PygameLoop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.PygameRunning=False
        
        self.PygameScreen.fill((255,255,255))
        pygame.display.update()

    def Buttons(self):
        if self.RightClik:
            self.SkinTexture.draw(self.Textbatch,1)
            self.ChatTexture.draw(self.Textbatch,1)
            self.SetingTexture.draw(self.Textbatch,1)
            self.ExitTexture.draw(self.Textbatch,1)
            if Gdx.input.isTouched() and 260<Gdx.input.getX()<285 and 118<Gdx.input.getY()<143:
                self.PygameRunning=True
                self.RightClik=False
            if Gdx.input.isTouched() and 260<Gdx.input.getX()<285 and 149<Gdx.input.getY()<173:
                print("Chat")
                self.RightClik=False
            if Gdx.input.isTouched() and 260 < Gdx.input.getX() < 285 and 189<Gdx.input.getY()<213:
                print("settings")
                self.RightClik=False
            if Gdx.input.isTouched() and 260 < Gdx.input.getX() < 285 and 219<Gdx.input.getY()<243:
                self.batch.dispose()
                jpype.shutdownJVM()
                exit()

            else:
                if Gdx.input.isButtonPressed(Input.Buttons.LEFT):
                    self.RightClik=False

    def cut(self,obj, sec):
        return [obj[i:i + sec] for i in range(0, len(obj), sec)]
    def DelSoap(self):
        self.TouchState=False
    def SoapSpawn(self,text,time,audio):
        self.TouchState=True
        self.text=text
        self.TextY=85
        if len(self.cut(text,25))>=3:
            self.text="\n".join(self.cut(text))
            self.TouchBak=self.SoapBak_Large
            self.TextY+=15
        Timer(time,self.DelSoap).start()
        Audio=mixer.Sound(audio)
        Audio.set_volume(0.5)
        Audio.play()

    def ExtraLoop(self):# 放置一些需要时间且需要循环检测的操作，CheckMail会严重拖慢主循环
        while True:
            if PopWindow.Check_Mail() and not self.WindowPoped:
                self.WindowPoped=False
                system("python PopWindow.pyw")
                Timer(60,self.WinPop).start()
    def WinPop(self):
        self.WindowPoped=False
    def ChangeNState(self,NewState,Time,Animation=None,AnimationLoop=False):
        def _SetTimer():
            self.NState=NewState
            if Animation!=None:
                self.state.setAnimation(0,Animation,AnimationLoop)
        t1 = Timer(Time, _SetTimer)
        t1.start()

    def Check_State(self,state):
        # 窗口拖动逻辑
        if Gdx.input.isTouched() and Gdx.input.isButtonPressed(Input.Buttons.MIDDLE) and self.WinMove==0 and self.Soapon==0:
            if self.NState=="RELAX" or self.NState=="SIT":
                if self.NState=="SIT":
                    self.NState="RELAX"
                    self.state.setAnimation(0,"Relax",True)
                self.Startx=Gdx.input.getX()
                self.Starty=Gdx.input.getY()
                self.WinMoving=True
                self.WinMove=1
        if Gdx.input.isTouched() and Gdx.input.isButtonPressed(Input.Buttons.MIDDLE) and self.WinMove==1 and self.Soapon==0:
            self.WinRect=GetWindowRect(self.WinPID)
            Winx=Gdx.input.getX()-self.Startx
            Winy=Gdx.input.getY()-self.Starty
            #print(Winx)
            SetWindowPos(self.WinPID,HWND_TOPMOST,int(self.WinRect[0]+Winx),int(self.WinRect[1]+Winy),380,300,SWP_SHOWWINDOW)

        # 窗口落体逻辑
        if not Gdx.input.isTouched() and self.WinRect[1] < self.screenh-340 and not self.WinMoving:  # 之后要加屏幕适应,1366,768
            self.WinRect = GetWindowRect(self.WinPID)
            if self.WinRect[1] + 20 > self.screenh-340:
                SetWindowPos(self.WinPID, HWND_TOPMOST, self.WinRect[0], self.screenh-340, 380, 300, SWP_SHOWWINDOW)
            else:
                SetWindowPos(self.WinPID, HWND_TOPMOST, self.WinRect[0], self.WinRect[1] + 20, 380, 300, SWP_SHOWWINDOW)
        # 窗口拖动相关变量恢复
        if not Gdx.input.isTouched() and self.WinMove==1:
            self.WinMoving=False
            self.WinMove=0

        # 点击互动逻辑
        if self.NState=="RELAX" and Gdx.input.isTouched() and Gdx.input.isButtonPressed(Input.Buttons.LEFT) and 142<Gdx.input.getX()<236 and 93<=Gdx.input.getY()<300:
            self.NState="INTERACT"
            RandAudio=randint(0,4)
            if RandAudio==0:
                self.SoapSpawn("我会定期为你进行理学检查，记录你的生命征象与意识状态，其他人没有这个权限。任何人想对你进行进一步的检查，你都有权拒绝，明白吗？",14,getcwd()+"\Modle\\"+ModleName.replace("/","")+"\Touch1.mp3")
            elif RandAudio==1:
                self.SoapSpawn("你会质疑自己存在的意义吗，博士？我会。大地上的生命十分顽强，它们在演化有着自己的位置，后天的驯化与对抗往往只是徒劳。我们的归宿会在何方，博士？你会有自己的答案，我只能这样坚持。",25,getcwd()+"\Modle\\"+ModleName.replace("/","")+"\Touch2.wav")
            elif RandAudio ==2:
                self.SoapSpawn("你在做什么？",1,getcwd() + "\Modle\\" + ModleName.replace("/", "") + "\Touch3.wav")
            elif RandAudio ==3:
                self.SoapSpawn("越是强大越是脆弱，这就是万物的道理。",3,getcwd() + "\Modle\\" + ModleName.replace("/", "") + "\Touch4.wav")
            elif RandAudio ==4:
                self.SoapSpawn("你似乎更加适应自己的工作和职责了，更像一个领导者了。",4,getcwd() + "\Modle\\" + ModleName.replace("/", "") + "\Touch5.wav")
            self.state.setAnimation(0,"Interact",False)
            self.ChangeNState("RELAX",2.5,"Relax",True)

        # 坐逻辑
        if self.NState == "RELAX" and self.Rand in self.Sit and self.Soapon==0:
            self.NState="SIT"
            self.state.setAnimation(0,"Sit",True)
            self.ChangeNState("RELAX",self.RandSit[randint(0,4)],"Relax",True)

        # 移动逻辑
        if self.NState == "RELAX" and self.Rand in self.Move and not Gdx.input.isTouched() and self.Soapon==0:
            self.Speed=1
            self.WinRect=GetWindowRect(self.WinPID)
            self.BeforMove=self.WinRect[0]
            self.NState="MOVING"
            while self.MoveTarget==self.WinRect[0]:
                    self.MoveTarget = self.MoveNode[randint(0, len(self.MoveNode)-1)]
            if self.MoveTarget<self.BeforMove:
                self.Speed=-1
            self.skeleton.setScaleX(self.Speed)
            self.state.setAnimation(0,"Move",True)
        if self.NState == "MOVING":
            self.WinRect=GetWindowRect(self.WinPID)
            if self.WinRect[0] <= self.MoveTarget and self.BeforMove > self.MoveTarget:
                self.NState = "RELAX"
                self.state.setAnimation(0, "Relax", True)
                SetWindowPos(self.WinPID, HWND_TOPMOST, self.MoveTarget, self.WinRect[1], 380, 300,SWP_SHOWWINDOW)
            if self.WinRect[0] >= self.MoveTarget and self.BeforMove < self.MoveTarget:
                self.NState = "RELAX"
                self.state.setAnimation(0, "Relax", True)
                SetWindowPos(self.WinPID, HWND_TOPMOST, self.MoveTarget, self.WinRect[1], 380, 300, SWP_SHOWWINDOW)
            elif self.WinRect[0]<self.MoveTarget and self.MoveTarget>self.BeforMove:
                SetWindowPos(self.WinPID,HWND_TOPMOST,self.WinRect[0]+self.Speed,self.WinRect[1],380,300,SWP_SHOWWINDOW)
            elif self.WinRect[0]>self.MoveTarget and self.MoveTarget<self.BeforMove:
                SetWindowPos(self.WinPID,HWND_TOPMOST,self.WinRect[0]+self.Speed,self.WinRect[1],380,300,SWP_SHOWWINDOW)

        # 睡眠逻辑
        if self.NState=="RELAX" and 230000<= self.Time <= 235959:
            self.NState="SLEEP"
            self.state.setAnimation(0,"Sleep",True)
        if self.NState!="SLEEP" and 0<=self.Time<60000:
            self.NState="SLEEP"
            self.state.setAnimation(0,"Sleep",True)
        if self.NState=="SLEEP" and self.Time==232000:
            self.NState="RELAX"
            self.state.setAnimation(0,"Relax",True)

        # 右键菜单
        if Gdx.input.isTouched() and Gdx.input.isButtonPressed(Input.Buttons.RIGHT) and 102<Gdx.input.getX()<140 and 201<Gdx.input.getY()<289 and self.NState=="RELAX":
            self.RightClik=True

    @JOverride
    def resize(self, width, height):
        pass
        '''
        通过以下代码可以在窗口大小改变后保持小人大小，但是不能100%一致，同时小人的位置会改变，目前弃用
        if self.resize1<=1:
            self.resize1+=1
            pass
        else:
            self.batch = TwoColorPolygonBatch()
            self.renderer = SkeletonRenderer()
            self.renderer.setPremultipliedAlpha(True)
            self.atlas = TextureAtlas(Gdx.files.internal(Modle_Atlas))
            self.loader = SkeletonJson(self.atlas)

            self.loader.setScale(0.25)#修改大小

            self.skeletonData = self.loader.readSkeletonData(Gdx.files.internal(Modle_Json))
            self.skeleton = Skeleton(self.skeletonData)
            self.stateData = AnimationStateData(self.skeletonData)
            self.state = AnimationState(self.stateData)
            self.state.setTimeScale(0.8)
            self.entry=self.state.setAnimation(0, "Relax", True)
            self.skeleton.setPosition(200, 0)
            self.skeleton.setScaleX(self.Speed)
          '''

    @JOverride
    def pause(self):
        pass

    @JOverride
    def resume(self):
        pass

    @JOverride
    def dispose(self):
        self.batch.dispose()
        self.Textbatch.dispose()
        self.ExitTexture.dispose()
        self.SetingTexture.dispose()
        self.ChatTexture.dispose()
        exit()
        
    @JOverride
    def create(self):
        self.resize1=0
        # 骨骼动画相关
        self.batch = TwoColorPolygonBatch()
        self.renderer = SkeletonRenderer()
        self.renderer.setPremultipliedAlpha(True)
        self.atlas = TextureAtlas(Gdx.files.internal(Modle_Atlas))
        self.loader = SkeletonJson(self.atlas)
        self.loader.setScale(0.25)
        self.skeletonData = self.loader.readSkeletonData(Gdx.files.internal(Modle_Json))
        self.skeleton = Skeleton(self.skeletonData)
        self.stateData = AnimationStateData(self.skeletonData)
        self.state = AnimationState(self.stateData)
        self.state.setTimeScale(0.8)

        # 屏幕分辨率
        hdc=GetDC(0)
        self.screenw=GetDeviceCaps(hdc,DESKTOPHORZRES)
        self.screenh=GetDeviceCaps(hdc,DESKTOPVERTRES)

        # 运行变量
        self.Textbatch=SpriteBatch()# 由于文字和骨骼动画冲突，需要两个batch
        self.NState="RELAX"
        self.Rand=randint(0,10000)
        self.Speed=1
        self.WinMove=0
        self.WinPID=FindWindow("GLFW30","AKDWCORE")# 之后需要为多开做点修改，格式可以为AKDWCORE+WinIndex
        self.WinRect=GetWindowRect(self.WinPID)
        self.WinMoving=False
        self.RandSit=[60,90,120,150,180]
        self.Sit=[2325]
        self.Move=[524,124,1014,111]
        self.MoveTarget=10
        self.Time=int(strftime("%H%M%S"))
        self.BeforMove=0
        self.TouchState=False
        self.text=""
        self.TextX=25
        self.TextY=85
        self.RightClik=False
        self.MenuThread=Thread(target=system)
        self.Soapon=self.ThreadStart=0
        self.WindowPoped=False
        self.ClickTime=0

        # 加载气泡背景
        self.SoapBak=Image(Texture("./assets/VOICE.png"))
        self.SoapBak_Large=Image(Texture("./assets/VOICE_LARGE.png"))
        self.SoapBak_Large.setPosition(21,45)
        self.SoapBak.setPosition(21,45)
        self.TouchBak=self.SoapBak

        # 加载右键菜单按钮
        self.SkinTexture=Image(Texture(Gdx.files.internal("./assets/skin.png")))
        self.SkinTexture.setPosition(260,160)
        self.ChatTexture=Image(Texture(Gdx.files.internal("./assets/chat.png")))
        self.ChatTexture.setPosition(260,128)
        self.SetingTexture=Image(Texture(Gdx.files.internal("./assets/settings.png")))
        self.SetingTexture.setPosition(260,96)
        self.ExitTexture=Image(Texture(Gdx.files.internal("./assets/exit.png")))
        self.ExitTexture.setPosition(260,58)

        self.PygameRunning=False
        self.PygameScreen=None


        # 绘制文字设置
        self.Font=FreeTypeFontGenerator(Gdx.files.internal("./Font/simhei.ttf"))
        self.Font_paramer=self.Font.FreeTypeFontParameter()
        self.Font_paramer.size=13
        self.Font_paramer.color=Color.WHITE
        self.Font_paramer.characters="你似乎更加适应自己的工作和职责了，像一个领导者。越是强大脆弱这就万物道理在做什么？会定期为进行学检查记录生命征象与意识状态其他人没有权限任何想对步都拒绝明白吗质疑存义博士我地上十分顽它们演化着位置后天驯抗往只徒劳归宿方答案能样坚持好,"
        self.Font_Draw=self.Font.generateFont(self.Font_paramer)
        self.Font.dispose()

        # 设置骨骼动画过渡
        self.stateData.setMix("Relax", "Move", 0.3)
        self.stateData.setMix("Move", "Relax", 0.3)
        self.stateData.setMix("Relax", "Interact", 0.3)
        self.stateData.setMix("Interact", "Relax", 0.3)
        self.stateData.setMix("Relax", "Sit", 0.3)
        self.stateData.setMix("Sit", "Relax", 0.3)
        self.stateData.setMix("Relax", "Sleep", 0.3)
        self.stateData.setMix("Sleep", "Relax", 0.3)

        # 设置初始动画
        self.entry=self.state.setAnimation(0, "Relax", True)
        self.skeleton.setPosition(200, 0)
        self.skeleton.setScaleX(self.Speed)

        self.ChildLop=Thread(target=self.ExtraLoop)
        self.ChildLop.start()

        self.MoveNode=[10]
        NodeMax=self.screenw-310
        for i in range(110,NodeMax,100):
            self.MoveNode.append(i)

        SetWindowPos(self.WinPID,HWND_TOPMOST,10,self.WinRect[1],380,300,SWP_SHOWWINDOW)
        SetWindowLong(self.WinPID, GWL_EXSTYLE,GetWindowLong(self.WinPID, GWL_EXSTYLE) | WS_EX_LAYERED)


    @JOverride
    def render(self):
        self.Time=int(strftime("%H%M%S"))
        #Input_ProcessorF=Input_Processor()
        self.skeleton.setScaleX(self.Speed)
        self.Rand=randint(0,10000)
        self.Soapon=FindWindow(None,"Soap")

        if self.PygameRunning and self.PygameScreen==None:
            self.PygameScreen=pygame.display.set_mode((500,400))
            pygame.display.set_caption("Test Window")
        if not self.PygameRunning and self.PygameScreen!=None:
            self.PygameScreen=None
            pygame.quit()
        if self.PygameRunning and self.PygameScreen!=None:
            self.PygameLoop()
        
        ScreenUtils.clear(0, 0, 0, 0)

        self.Check_State(self.NState)
        self.state.update(Gdx.graphics.getDeltaTime())
        self.state.apply(self.skeleton)
        self.skeleton.updateWorldTransform()

        self.batch.begin()
        self.renderer.draw(self.batch, self.skeleton)
        self.batch.end()

        self.Textbatch.begin()
        self.Buttons()
        if self.TouchState:
            self.TouchBak.draw(self.Textbatch,1)
            self.Font_Draw.draw(self.Textbatch,self.text,self.TextX,self.TextY)
        self.Textbatch.end()

def Main():
    cfg = Lwjgl3ApplicationConfiguration()
    cfg.setForegroundFPS(60)
    cfg.setWindowedMode(380, 300)
    cfg.setResizable(False)
    cfg.setDecorated(False)
    cfg.setTitle("AKDWCORE")
    cfg.setTransparentFramebuffer(True)
    Lwjgl3Application(Pet(), cfg)
Main()
