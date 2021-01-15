# import
import sys
from object.animal import Animal
from object.wallK import WallK
from object.hole import Hole
import time
import pygame
import copy
import threading
from random import seed
from random import choice
from const import *
import random


pygame.init()

# declare object
imgCat = pygame.transform.scale(pygame.image.load(
    'image/cat.png'), (WIDTH_CAT, HEIGHT_CAT))
imgMice = pygame.transform.scale(pygame.image.load(
    'image/mouse.png'), (WIDTH_MICE, HEIGHT_MICE))


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

holeOne = Hole(20, 470, 60, 60)
holeTwo = Hole(770, 20, 60, 60)
holes = [holeOne, holeTwo]


# function


def draw(gameScreen):
    for wall in walls:
        gameScreen.blit(wall.image, pygame.Rect(
        wall.x, wall.y, wall.width, wall.height))

    for hole in holes:
        pygame.draw.rect(gameScreen, BLUE,
                         (hole.x, hole.y, hole.width, hole.height))

    pygame.draw.rect(gameScreen, YELLOW, (X_FINISH,
                                          Y_FINISH, WIDTH_FINISH, HEIGHT_FINISH))

    gameScreen.blit(cat.image, pygame.Rect(
        cat.x, cat.y, cat.width, cat.height))
    gameScreen.blit(mice.image, pygame.Rect(
        mice.x, mice.y, mice.width, mice.height))

    if (checkAnimalTouch(cat, mice)):
        gameScreen.blit(textGameOver, textRect)

    if (checkFinish()):
        gameScreen.blit(textFinish, textFinishRect)


def checkWallKTouching(animal):
    tempAnimal = copy.copy(animal)
    tempAnimal.move()

    for wall in walls:
        if (wall.checkTouching(tempAnimal)):
            return False
    return True


def checkOutOfRange(animal):
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
    index = 0
    currHole = 0
    while index < len(holes):
        if (holes[index].checkIn(mice)):
            if (index == 0):
                mice.moveTo(holes[1])
            elif (index == 1):
                mice.moveTo(holes[0])
        index += 1


def checkFinish():
    checkTop = (mice.y + mice.height) > Y_FINISH
    checkLeft = (mice.x + mice.width) > X_FINISH
    if (checkTop and checkLeft):
        return True
    return False


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
def runModeOne(gameScreen):
    pygame.time.delay(1)
    event()
    if (checkFinish() == False and checkAnimalTouch(cat, mice) == False):
        if (cat.isMoving and checkWallKTouching(cat) and checkOutOfRange(cat)):
            cat.move()

        if (mice.isMoving and checkWallKTouching(mice) and checkOutOfRange(mice)):
            mice.move()

        checkMiceJumpHole()
    gameScreen.fill((0, 0, 0))
    draw(gameScreen)
    pygame.display.flip()
