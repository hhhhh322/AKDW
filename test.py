import pygame
from pygame.locals import *
import os

pygame.init()
os.environ["SDL_IME_SHOW_UI"] = "1"
win = pygame.display.set_mode((590, 64))

font = pygame.font.Font('Font/simhei.ttf', 18)

textx=""
run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
        if event.type==pygame.TEXTINPUT:
            textx+=event.text
        if event.type==pygame.KEYDOWN and event.key==pygame.K_BACKSPACE:
            a=list(textx)
            del a[-1]
            textx="".join(a)
        if event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN:
            print(textx)
            textx=""
    text = font.render(textx, True, (0, 0, 0))
    win.fill((255, 255, 255))
    win.blit(text,(0,20))
    pygame.display.update()