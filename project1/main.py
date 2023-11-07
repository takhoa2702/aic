import pygame, sys

from pygame.locals import *
import multiprocessing as mp
from readfile import *

import pacman_game

#Initialize pygame
pygame.init()
mainClock = pygame.time.Clock()
#create the screen 
pygame.display.set_caption('PACMAN MAIN MENU')

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

COLOR_MENU = (0, 102, 37)
COLOR_MENU_2 = (26, 255, 110)
EXIT_COLOR = (153, 0, 0)
EXIT_COLOR_2 = (255, 0, 0)
FONT_MENU_COLOR = (255, 255, 255)
FONT_MENU_COLOR2 = (153, 153, 153)
FONT_MAP_COLOR = (115, 115, 115)
font = pygame.font.Font(r'res/font.ttf', 25)

def draw_Text(text, font, color, surface, x, y):
    textobj  = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    return textrect

def text_to_button(text, font, color, surface, buttonx, buttony, buttonwidth, buttonheight):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (int(buttonx+(buttonwidth/2)), int(buttony+(buttonheight/2)))
    surface.blit(textobj, textrect)

def button(text, x, y, width, height, inactive_color, active_color):
    cur = pygame.mouse.get_pos()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        text_to_button(text, font, FONT_MENU_COLOR, screen, x, y, width, height)
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
        text_to_button(text, font, FONT_MENU_COLOR2, screen, x, y, width, height)

def hover(text, rect_text, inactive_color, active_color):
    cur = pygame.mouse.get_pos()
    x, y = rect_text.center
    if rect_text.collidepoint(cur):
        draw_Text(text, font, active_color, screen, x, y)
    else:
        draw_Text(text, font, inactive_color, screen, x, y)

click = False


def Main_Menu():
    while True:
        screen.fill((0, 0, 0)) 
                
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(100, 100, 200, 50)
        button_2 = pygame.Rect(500, 100, 200, 50)
        button_3 = pygame.Rect(100, 300, 200, 50)
        button_4 = pygame.Rect(500, 300, 200, 50)
        button_5 = pygame.Rect((SCREEN_WIDTH - 200 )//2, 500, 200, 50)

        try:
            if button_1.collidepoint((mx, my)):
                if click:
                    choose_map('LEVEL1')
            
            if button_2.collidepoint((mx, my)):
                if click:
                    choose_map('LEVEL2')
            if button_3.collidepoint((mx, my)):
                if click:
                    choose_map('LEVEL3')
            if button_4.collidepoint((mx, my)):
                if click:
                    choose_map('LEVEL4')
            if button_5.collidepoint((mx, my)):
                if click:
                    pygame.quit()
                    sys.exit()  
        except NameError:
            pass

        pygame.draw.rect(screen, COLOR_MENU, button_1)
        button("LEVEL 1", 100, 100, 200, 50, COLOR_MENU, COLOR_MENU_2)
        pygame.draw.rect(screen, COLOR_MENU, button_2)
        button("LEVEL 2", 500, 100, 200, 50, COLOR_MENU, COLOR_MENU_2)
        pygame.draw.rect(screen, COLOR_MENU, button_3)
        button("LEVEL 3", 100, 300, 200, 50, COLOR_MENU, COLOR_MENU_2)
        pygame.draw.rect(screen, COLOR_MENU, button_4)
        button("LEVEL 4", 500, 300, 200, 50, COLOR_MENU, COLOR_MENU_2)
        pygame.draw.rect(screen, EXIT_COLOR, button_5)
        button("EXIT", (SCREEN_WIDTH - 200 )//2, 500, 200, 50, EXIT_COLOR, EXIT_COLOR_2)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

def choose_map(level):
    screen.fill((0, 0, 0))

    draw_Text(level, font, (255, 255, 255), screen, SCREEN_WIDTH//2, 110)

    running = True
    while running:
        mx, my = pygame.mouse.get_pos()

        button1 = pygame.Rect(540, 520, 175, 50)
        button2 = pygame.Rect(95, 520, 175, 50)        

        try:
            if button1.collidepoint((mx, my)):
                if click:
                    pygame.quit()
                    sys.exit()
            if button2.collidepoint((mx, my)):
                if click:
                    running = False    
        except ValueError:
            pass
        
        pygame.draw.rect(screen, EXIT_COLOR, button1)
        button("EXIT", 540, 520, 175, 50, EXIT_COLOR, EXIT_COLOR_2)
        pygame.draw.rect(screen, EXIT_COLOR, button2)
        button("BACK", 95, 520, 175, 50, EXIT_COLOR, EXIT_COLOR_2)
        
        rect_text = []
        index = 1
        posx = 300
        for i in range(1, 3):
            posy = 250 
            for j in range(1, 5):
                rect_text.append(draw_Text("Map " + str(index), font, FONT_MAP_COLOR, screen, posx, posy))
                posy += 75
                index += 1
            posx += 200 

        for i in range (8):
            if rect_text[i].collidepoint((mx, my)):
                hover("Map "+ str(i+1), rect_text[i], FONT_MAP_COLOR, FONT_MENU_COLOR)                
                if click:
                    load_game("input/" + str(level[-1]) + "/input" + str(i+1) + ".txt" ,level)
                    
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    pygame.mixer.music.stop()
                    click = True            

        pygame.display.update()
        mainClock.tick(60)

def load_game(path, level):
    ctx = mp.get_context('spawn')

    p = ctx.Process(target=pacman_game.main, args=(level, path))
    p.start()
    p.join()
  
    
if __name__ == "__main__":
    Main_Menu()
