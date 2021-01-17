import pygame, sys, random
from pygame.locals import *

WINDOWWIDTH = 480
WINDOWHEIGHT = 600

pygame.init()

FPS = 60
fpsClock = pygame.time.Clock()
BGSPEED = 1.5
BGIMG = pygame.image.load('image/background.png')
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

#Constant for Mouse

MOUSEWIDTH = 60
MOUSEHEIGHT = 60
MOUSESPEED = 3
MOUSEIMG = pygame.image.load('image/mouse_modeFour.png')

#Constant for Cat
LANEWIDTH = 60
CATWIDTH = 60
CATHEIGHT = 60
DISTANCE = 200
CATSPEED = 2
CHANGESPEED = 0.001
CATIMG = pygame.image.load('image/a.png')

class Cats():
    def __init__(self):
        self.width = CATWIDTH
        self.height = CATHEIGHT
        self.distance = DISTANCE
        self.speed = CATSPEED
        self.changeSpeed = CHANGESPEED
        self.ls = []
        for i in range(5):
            y = -CATHEIGHT-i*self.distance
            lane = random.randint(0, 7)
            self.ls.append([lane, y])
           
    def draw(self):
        for i in range(5):
            x = int(self.ls[i][0]*LANEWIDTH )
            y = int(self.ls[i][1])
            DISPLAYSURF.blit(CATIMG, (x, y))
    def update(self):
        for i in range(5):
            self.ls[i][1] += self.speed
        self.speed += self.changeSpeed
        if self.ls[0][1] > WINDOWHEIGHT:
            self.ls.pop(0)
            y = self.ls[3][1] - self.distance
            lane = random.randint(0, 7)
            self.ls.append([lane, y])


class Mouse():
    def __init__(self):
        self.width = MOUSEWIDTH
        self.height = MOUSEHEIGHT
        self.x = (WINDOWWIDTH-self.width)/2
        self.y = WINDOWHEIGHT
        self.speed = MOUSESPEED
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 255, 255))
    def draw(self):
        DISPLAYSURF.blit(MOUSEIMG, (int(self.x), int(self.y)))
    def update(self, moveLeft, moveRight, moveUp, moveDown):
        if moveLeft == True:
            self.x -= self.speed
        if moveRight == True:
            self.x += self.speed
        if moveUp == True:
            self.y -= self.speed
        if moveDown == True:
            self.y += self.speed
        
        if self.x < 0:
            self.x = 0
        if self.x + self.width > WINDOWWIDTH :
            self.x = WINDOWWIDTH  - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > WINDOWHEIGHT :
            self.y = WINDOWHEIGHT - self.height

class Score():
    def __init__(self):
        self.score = 0
    def draw(self):
        font = pygame.font.SysFont('consolas', 30)
        scoreSuface = font.render('Score: '+str(int(self.score)), True, (255, 255, 0))
        DISPLAYSURF.blit(scoreSuface, (10, 10))
    def update(self):
        self.score += 0.02

class Background():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = BGSPEED
        self.img = BGIMG
        self.width = self.img.get_width()
        self.height = self.img.get_height()
    def draw(self):
        DISPLAYSURF.blit(self.img, (int(self.x), int(self.y)))
        DISPLAYSURF.blit(self.img, (int(self.x), int(self.y-self.height)))
    def update(self):
        self.y += self.speed
        if self.y > self.height:
            self.y -= self.height

def gameStart(bg):
    bg.__init__()
    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('START', True, (255, 0, 0))
    headingSize = headingSuface.get_size()

    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Press "SPACE" to play, "ESC" to back', True, (255, 255, 255))
    commentSize = commentSuface.get_size()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == K_SPACE:
                    return False
                elif event.key == pygame.K_ESCAPE:
                    return True
            
        bg.draw()
        DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
        DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 400))
        pygame.display.update()
        fpsClock.tick(FPS)

def gamePlay(bg, mouse, cats,score):
    bg.__init__()
    mouse.__init__()
    cats.__init__()
    score.__init__()
    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    moveLeft = True
                if event.key == K_RIGHT:
                    moveRight = True
                if event.key == K_UP:
                    moveUp = True
                if event.key == K_DOWN:
                    moveDown = True
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False
                elif event.key == pygame.K_ESCAPE:
                    return True
        if isGameover(mouse, cats):
            return False
        bg.draw()
        bg.update()
        mouse.draw()
        mouse.update(moveLeft, moveRight, moveUp, moveDown)
        cats.draw()
        cats.update()
        score.draw()
        score.update()
        pygame.display.update()
        fpsClock.tick(FPS)
#Xử lý va chạm
def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] -15  and rect2[0] <= rect1[0]+rect1[2] -15 and rect1[1] <= rect2[1]+rect2[3]  and rect2[1]  <= rect1[1]+rect1[3] :
        return True
    return False
    
def isGameover(mouse, cats):
    mouseRect = [mouse.x, mouse.y, mouse.width, mouse.height]
    for i in range(5):
        x = int(cats.ls[i][0]*LANEWIDTH )
        y = int(cats.ls[i][1])
        catsRect = [x, y, cats.width, cats.height]
        if rectCollision(mouseRect, catsRect) == True:
            return True
    return False
def gameOver(bg, mouse, cats, score):
    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('GAMEOVER', True, (255, 0, 0))
    headingSize = headingSuface.get_size()
    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Press "space" to replay', True, (255, 255, 0))
    commentSize = commentSuface.get_size()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == K_SPACE:
                    return False
                if event.key == pygame.K_ESCAPE:
                    return True
            
        bg.draw()
        mouse.draw()
        cats.draw()
        score.draw()
        DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
        DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 400))
        pygame.display.update()
        fpsClock.tick(FPS)

def runModeThree():
    isBack=False
    pygame.display.set_mode((480, 600))
    bg = Background()
    isBackGameStart = gameStart(bg)
    mouse = Mouse()
    cats = Cats()
    score = Score()
    if(isBackGameStart==False):
        while True:
            isBackGamePlay = gamePlay(bg, mouse,cats,score)  
            if(isBackGamePlay==False):
                isBackGameOver = gameOver(bg,mouse,cats,score)
                if(isBackGameOver==True):
                    pygame.display.set_mode((850, 550))
                    return isBackGameOver
            else:
                pygame.display.set_mode((850, 550))
                return isBackGamePlay
    else:
        pygame.display.set_mode((850, 550))
        return isBackGameStart

