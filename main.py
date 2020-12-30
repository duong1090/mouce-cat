import os
import pygame
from modeOne import runModeOne
from modeTwo import runModeTwo
from modeThree import runModeThree
from const import *

# define screen
pygame.init()
gameScreen = pygame.display.set_mode((WIDTH_WIN, HEIGHT_WIN))
pygame.display.set_caption('Cat & Mouse')



# define mode


class Mode:
    def __init__(self):
        self.state = 'intro'


stateMode = Mode()
# function


def checkCursor(x, y, width, height):
    mouseX, mouseY = pygame.mouse.get_pos()
    checkHorizontal = mouseX > x and mouseX < x + width
    checkVertical = mouseY > y and mouseY < y + height
    if (checkHorizontal and checkVertical):
        return True
    return False


def startScreen():
    widthMode = int(WIDTH_WIN / 2 - MARGIN_MODE - PADDING_MODE)
    heightMode = int(HEIGHT_WIN / 2 - MARGIN_MODE - PADDING_MODE)
    xMode = [PADDING_MODE, int(WIDTH_WIN / 2 + MARGIN_MODE)]
    yMode = [PADDING_MODE, int(HEIGHT_WIN / 2 + MARGIN_MODE)]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if checkCursor(xMode[0], yMode[0], widthMode, heightMode):
                stateMode.state = 'one'
            if checkCursor(xMode[1], yMode[0], widthMode, heightMode):
                stateMode.state = 'two'
            if checkCursor(xMode[0], yMode[1], widthMode, heightMode):
                stateMode.state = 'three'
            if checkCursor(xMode[1], yMode[1], widthMode, heightMode):
                stateMode.state = 'four'

    gameScreen.fill((0, 0, 0))
    pygame.draw.rect(gameScreen, BROWN,
                     (xMode[0], yMode[0], widthMode, heightMode))
    pygame.draw.rect(gameScreen, YELLOW,
                     (xMode[1], yMode[0], widthMode, heightMode))
    pygame.draw.rect(gameScreen, WHITE,
                     (xMode[0], yMode[1], widthMode, heightMode))
    pygame.draw.rect(gameScreen, BLUE,
                     (xMode[1], yMode[1], widthMode, heightMode))

    pygame.display.flip()
    pygame.time.delay(1)


# main loop
while True:
    if stateMode.state == 'intro':
        startScreen()
    elif stateMode.state == 'one':
        runModeOne(gameScreen)
    #khang
    elif stateMode.state == 'two':
        runModeTwo(gameScreen)
    #thinh
    elif stateMode.state == 'three':
        runModeThree()
    #dao
    # elif stateMode == 'four':
    #     # runModeFour()
