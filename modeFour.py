import pygame
from pygame.locals import *
import math
import random
from const import *

def runModeFour():
    # Initit game
    pygame.init()
    width, height = WIDTH_WIN, HEIGHT_WIN
    screen = pygame.display.set_mode((width, height))
    keys = [False, False, False, False]
    mousepos = [100,100]
    acc = [0, 0]
    arrows = []
    cattimer = 120
    cattimer1 = 0
    cats = [[640, 100]]
    healthvalue = 194
    pygame.mixer.init()

    # Load image
    mouse = pygame.image.load("image/mouse_modeFour.png")
    grass = pygame.image.load("image/grass.png")
    rat_hole = pygame.image.load("image/rat_hole.png")
    arrow = pygame.image.load("image/bullet.png")
    catimg1 = pygame.image.load("image/cat_modeFour.png")
    catimg = catimg1
    healthbar = pygame.image.load("image/healthbar.png")
    health = pygame.image.load("image/health.png")
    gameover = pygame.image.load("image/gameover.png")
    youwin = pygame.image.load("image/youwin.png")

    running = 1
    exitcode = 0
    while running:
        cattimer -= 1
        # Clear the screen before drawing it again
        screen.fill(0)
        # Draw mouse on the screen at X:100, Y:100
        for x in range(width//grass.get_width() + 1):
            for y in range(height//grass.get_height() + 1):
                screen.blit(grass,(x*100, y*100))
        screen.blit(rat_hole, (0, 30))
        # Set mouse position and rotation
        position = pygame.mouse.get_pos()
        # angle = math.atan2(position[1]-(mousepos[1]+32),position[0]-(mousepos[0]+26))
        mouserot = pygame.transform.rotate(mouse, 0)
        mousepos1 = (mousepos[0] - mouserot.get_rect().width/2, mousepos[1] - mouserot.get_rect().height/2)
        screen.blit(mouserot, mousepos1) 
        # Draw arrows
        for bullet in arrows:
            index = 0
            velx = math.cos(bullet[0])*10
            vely = math.sin(bullet[0])*10
            bullet[1] += velx
            bullet[2] += vely
            if bullet[1] < -64 or bullet[1] > 640 or bullet[2] <- 64 or bullet[2] > 480:
                arrows.pop(index)
            index += 1
            for projectile in arrows:
                arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0]*57.29)
                screen.blit(arrow1, (projectile[1], projectile[2]))
        # Draw cats
        if cattimer == 0:
            cats.append([640, random.randint(40, 400)])
            cattimer = 120 - (cattimer1*2)
            if cattimer1 >= 35:
                cattimer1 = 35
            else:
                cattimer1 += 5
        index = 0
        for catguy in cats:
            if catguy[0] <- 64:
                cats.pop(index)
            catguy[0] -= 7
            # Attack rat_hole
            catrect = pygame.Rect(catimg.get_rect())
            catrect.top = catguy[1]
            catrect.left = catguy[0]
            if catrect.left < 64:
                healthvalue -= random.randint(5, 20)
                cats.pop(index)
            # Check for collisions
            index1 = 0
            for bullet in arrows:
                bullrect = pygame.Rect(arrow.get_rect())
                bullrect.left = bullet[1]
                bullrect.top = bullet[2]
                if catrect.colliderect(bullrect):
                    acc[0] += 1
                    cats.pop(index)
                    arrows.pop(index1)
                index1 += 1
            # Next cat
            index += 1
        for catguy in cats:
            screen.blit(catimg, catguy)

        # Draw clock
        font = pygame.font.Font(None, 24)
        survivedtext = font.render(str(round(((90000 - pygame.time.get_ticks())/60000), 2)).zfill(2), True, (0,0,0))
        textRect = survivedtext.get_rect()
        textRect.topright=[635, 5]
        screen.blit(survivedtext, textRect)

        # Draw health bar
        screen.blit(healthbar, (5, 5))
        for health1 in range(healthvalue):
            screen.blit(health, (health1 + 8,8))
        # Update the screen
        pygame.display.flip()
        # loop through the events
        for event in pygame.event.get():
            # check if the event is the X button 
            if event.type == pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    keys[0] = True
                elif event.key == K_a:
                    keys[1] = True
                elif event.key == K_s:
                    keys[2] = True
                elif event.key == K_d:
                    keys[3] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    keys[0] = False
                elif event.key == pygame.K_a:
                    keys[1] = False
                elif event.key == pygame.K_s:
                    keys[2] = False
                elif event.key == pygame.K_d:
                    keys[3] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                acc[1] += 1
                arrows.append([math.atan2(position[1] - (mousepos1[1] + 32), position[0] - (mousepos1[0] + 26)), mousepos1[0] + 32, mousepos1[1] + 32])
                    
        # Move mouse
        if keys[0]:
            mousepos[1] -= 5
        elif keys[2]:
            mousepos[1] += 5
        if keys[1]:
            mousepos[0] -= 5
        elif keys[3]:
            mousepos[0] += 5

        # Win/Lose check
        if pygame.time.get_ticks() >= 90000:
            running = 0
            exitcode = 1
        if healthvalue <= 0:
            running = 0
            exitcode = 0
    # Win/lose display        
    if exitcode==0:
        pygame.font.init()
        font = pygame.font.Font(None, 28)
        text = font.render("Ban thua roi, meo đa pha huy thanh cong o chuot, Ban se la bua toi cua bay meo", True, (0, 255, 0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery + 24
        screen.blit(gameover, (0, 0))
        screen.blit(text, textRect)
    else:
        pygame.font.init()
        font = pygame.font.Font(None, 28)
        text = font.render("Ban thang, Bon meo da phai roi di", True, (0, 0, 255))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery + 24
        screen.blit(youwin, (0, 0))
        screen.blit(text, textRect)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()