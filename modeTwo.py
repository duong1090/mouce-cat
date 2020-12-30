# import
import sys
from object.animal import Animal
from object.wallK import WallK
from object.holeK import HoleK
from object.Light import Light
import time
import pygame
import copy
import threading
import random
from random import seed
from random import choice
from const import *

pygame.init()

# declare object
imgCat = pygame.transform.scale(pygame.image.load(
    'image/cat.png'), (WIDTH_CAT, HEIGHT_CAT))
imgMice = pygame.transform.scale(pygame.image.load(
    'image/mouse.png'), (WIDTH_MICE, HEIGHT_MICE))
imgHoldTop = pygame.transform.scale(pygame.image.load(
    'image/hold_top.png'), (HOLD_TOP_WIDTH, HOLD_TOP_HEIGHT))
imgHoldBot = pygame.transform.scale(pygame.image.load(
    'image/hold_bot.png'), (HOLD_BOT_WIDTH, HOLD_BOT_HEIGHT))

imgLightTop = pygame.transform.scale(pygame.image.load(
    'image/light_top.png'), (HOLD_TOP_WIDTH+75, HOLD_TOP_HEIGHT))
imgLightBot = pygame.transform.scale(pygame.image.load(
    'image/light_bot.png'), (HOLD_BOT_WIDTH+60, HOLD_BOT_HEIGHT + 40))


cat = Animal(X_CAT, Y_CAT, WIDTH_CAT, HEIGHT_CAT,
             SPEED_CAT, imgCat, False, 'RIGHT')
mice = Animal(X_MICE, Y_MICE, WIDTH_MICE,
              HEIGHT_MICE, SPEED_MICE, imgMice, False, 'RIGHT')

font = pygame.font.Font('freesansbold.ttf', 32)
textGameOver = font.render('Game Over', True, WHITE)
textRect = textGameOver.get_rect()
textRect.center = (WIDTH_WIN // 2, HEIGHT_WIN // 2)
textFinish = font.render('Mice Win', True, WHITE)
textFinishRect = textFinish.get_rect()
textFinishRect.center = (WIDTH_WIN // 2, HEIGHT_WIN // 2)

# declare walls
walls = []
wall_num = random.randrange(3, 10)
for x in range(0, wall_num):
    ran_x = random.randrange(100, 650)
    ran_y = random.randrange(100, 450)
    ran_w = random.randrange(5, 100)
    ran_h = random.randrange(5, 100)
    image = pygame.transform.scale(pygame.image.load(
        'image/wall.png'), (ran_w, ran_h))

    ran_wall = WallK(ran_x, ran_y, ran_w, ran_h, image)
    walls.append(ran_wall)

# declare holes

# holeOne = HoleK(20, 470, 60, 60)
lightBot = Light(20, 500, HOLD_BOT_WIDTH, HOLD_BOT_HEIGHT, imgLightBot)
lightTop = Light(680, 40, HOLD_TOP_WIDTH, HOLD_TOP_HEIGHT, imgLightTop)

holeTop = HoleK(720, 0, HOLD_TOP_WIDTH, HOLD_TOP_HEIGHT, imgHoldTop)
holeBot = HoleK(50, 540, HOLD_BOT_WIDTH, HOLD_BOT_HEIGHT, imgHoldBot)

holes = [holeBot, holeTop]
lights = [lightBot, lightTop]


# function


def draw(gameScreen):
    for wall in walls:
        gameScreen.blit(wall.image, pygame.Rect(
            wall.x, wall.y, wall.width, wall.height))
        # pygame.draw.rect(gameScreen, BROWN,
        #                  (wall.x, wall.y, wall.width, wall.height))
    for light in lights:
        gameScreen.blit(light.image, pygame.Rect(
            light.x, light.y, light.width, light.height))

    for hole in holes:
        gameScreen.blit(hole.image, pygame.Rect(
            hole.x, hole.y, hole.width, hole.height))

    gameScreen.blit(cat.image, pygame.Rect(
        cat.x, cat.y, cat.width, cat.height))
    gameScreen.blit(mice.image, pygame.Rect(
        mice.x, mice.y, mice.width, mice.height))

    if (checkAnimalTouch(cat, mice)):
        gameScreen.blit(textGameOver, textRect)


def checkWallTouching(animal):
    tempAnimal = copy.copy(animal)
    tempAnimal.move()

    for wall in walls:
        if (wall.checkTouching(tempAnimal)):
            return False
    return True


def checkOutOfRangeM(animal):
    tempAnimal = copy.copy(animal)
    tempAnimal.move()

    checkLeft = tempAnimal.x < 0
    checkRight = tempAnimal.x + animal.width > WIDTH_WIN
    checkTop = tempAnimal.y < 0 and (
        mice.x < holes[1].x or mice.x > holes[1].x+holes[1].width-mice.width)
    checkBottom = (tempAnimal.y + animal.height > HEIGHT_WIN) and (tempAnimal.x <
                                                                   holes[0].x or mice.x > holes[0].x+holes[0].width-mice.width)
    if (checkLeft or checkRight or checkBottom or checkTop):
        return False
    return True


def checkOutOfRangeC(animal):
    tempAnimal = copy.copy(animal)
    tempAnimal.move()

    checkLeft = tempAnimal.x < 0
    checkRight = tempAnimal.x + animal.width > WIDTH_WIN
    checkTop = tempAnimal.y < 0
    checkBottom = tempAnimal.y + animal.height > HEIGHT_WIN
    if (checkLeft or checkRight or checkBottom or checkTop):
        return False
    return True


def checkAnimalTouch(animal1, animal2):
    checkLeft = animal1.x < (animal2.x + animal2.width)
    checkRight = (animal1.x + animal1.width) > animal2.x
    checkTop = animal1.y < (animal2.y + animal2.height)
    checkBottom = (animal1.y + animal1.height) > animal2.y
    if (checkLeft and checkRight and checkTop and checkBottom):
        return True
    return False


def checkMiceJumpHole():
    if (mice.y > holes[0].y - mice.height+10) and mice.x > holes[0].x and mice.x < holes[0].x+holes[0].width-mice.width:
        mice.moveToXY(holes[1].x+20, holes[1].y)
    elif mice.y < holes[1].y and mice.x > holes[1].x and mice.x < holes[1].x+holes[1].width-mice.width:
        mice.moveToXY(holes[0].x+20, holes[0].y-mice.height)
# def checkMiceJumpHole():
#     if mice.y > holes[0].y and mice.x > holes[0].x and mice.x < holes[0].x+holes[0].width-mice.width:
#         mice.moveToXY(holes[1].x+holes[1].width/4, holes[1].y-mice.height)
#     elif mice.y < holes[1].y-mice.height and mice.x > holes[1].x and mice.x < holes[1].x+holes[1].width-mice.width:
#         mice.moveToXY(holes[0].x+holes[0].width/4, holes[0].y)


def reset():
    cat.x = X_CAT
    cat.y = Y_CAT
    mice.x = X_MICE
    mice.y = Y_MICE


def event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cat.direction = 'LEFT'
                cat.isMoving = True

            elif event.key == pygame.K_RIGHT:
                cat.direction = 'RIGHT'
                cat.isMoving = True

            elif event.key == pygame.K_UP:
                cat.direction = 'UP'
                cat.isMoving = True

            elif event.key == pygame.K_DOWN:
                cat.direction = 'DOWN'
                cat.isMoving = True

            if event.key == pygame.K_a:
                mice.direction = 'LEFT'
                mice.isMoving = True

            elif event.key == pygame.K_d:
                mice.direction = 'RIGHT'
                mice.isMoving = True

            elif event.key == pygame.K_w:
                mice.direction = 'UP'
                mice.isMoving = True

            elif event.key == pygame.K_s:
                mice.direction = 'DOWN'
                mice.isMoving = True

            elif event.key == pygame.K_SPACE:
                reset()

        elif event.type == pygame.KEYUP:
            cat.isMoving = False
            mice.isMoving = False


# run mode
def runModeTwo(gameScreen):
    pygame.time.delay(1)
    event()
    for x in range(80000):
        x = x+1-1
    if (checkAnimalTouch(cat, mice) == False):
        if (checkWallTouching(cat) and checkOutOfRangeC(cat)):
            cat.move()

        if (checkWallTouching(mice) and checkOutOfRangeM(mice)):
            mice.move()

        checkMiceJumpHole()
    gameScreen.fill((0, 0, 0))
    draw(gameScreen)
    pygame.display.flip()
