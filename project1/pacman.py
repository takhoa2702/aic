import pygame, sys

from pygame.locals import *

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576
mainClock = pygame.time.Clock()

BLOCK_SIZE = 32

player = pygame.image.load(r'res/pacman.png')

def pacman(X, Y, lastx, lasty):
    if X > lastx and Y == lasty:
        screen.blit(player, (X, Y))
    elif X < lastx and  Y == lasty:
        screen.blit(pygame.transform.flip(player, True, False), (X, Y)) 
    elif X == lastx and Y > lasty:
        screen.blit(pygame.transform.rotate(player, 90*3), (X, Y))
    elif X == lastx and Y < lasty:
        screen.blit(pygame.transform.rotate(player, 90), (X, Y)) 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BLOCK_SIZE = 32

click = False

def Main_Menu():
    playerx = 5
    playery = 5
    state = 1
    while True:
        screen.fill((0, 0, 0))
        lastx = playerx
        lasty = playery
        #laststate = state
        #playerx -= 0.01
        playery -= 0.01
        pacman(playerx*BLOCK_SIZE, playery*BLOCK_SIZE, lastx*BLOCK_SIZE, lasty*BLOCK_SIZE)
        
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        mainClock.tick(60)

Main_Menu()