import pygame, sys

from pygame.locals import *

#Initialize pygame
pygame.init()
mainClock = pygame.time.Clock()
#create the screen 
pygame.display.set_caption('PACMAN WINNING STAGE')

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FONT_MENU_COLOR = (255, 255, 255)
FONT_MENU_COLOR_2 = (153, 153, 153)
FONT_MAP_COLOR = (115, 115, 115)

BACKGROUND_COLOR = (38, 44, 58)

font = pygame.font.Font(r'res/font.ttf', 25)
font2 = pygame.font.Font(r'res/font.ttf', 18)
font3 = pygame.font.Font(r'res/font.ttf', 20)

trophy = pygame.image.load(r'res/award.png')

def draw_Text(text, font, color, surface, x, y):
    textobj  = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    return textrect

def text_to_button(text, font, color, surface, buttonx, buttony, buttonwidth, buttonheight):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = ((buttonx+(buttonwidth//2)), buttony+(buttonheight//2))
    surface.blit(textobj, textrect)

def hover(text, font, rect_text, inactive_color, active_color):
    cur = pygame.mouse.get_pos()
    x, y = rect_text.center
    if rect_text.collidepoint(cur):
        draw_Text(text, font, active_color, screen, x, y)
    else:
        draw_Text(text, font, inactive_color, screen, x, y)

def button(text, x, y, width, height, inactive_color, active_color):
    cur = pygame.mouse.get_pos()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        text_to_button(text, font3, FONT_MENU_COLOR, screen, x, y, width, height)
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
        text_to_button(text, font3, FONT_MENU_COLOR, screen, x, y, width, height)


def winning_screen(flag, score, time):
    i = 0
    while True:
        screen.fill((0, 0, 0))    
                
        mx, my = pygame.mouse.get_pos()
        
        if flag == -1:
            draw_Text("Game was crashed by user", font, FONT_MENU_COLOR, screen, SCREEN_WIDTH//2, 290)
        
        elif flag == 0:
            stripe1 = pygame.Rect((SCREEN_WIDTH - 160)//2, 140, 3, 160)
            pygame.draw.rect(screen, FONT_MENU_COLOR, stripe1)
            stripe2 = pygame.Rect((SCREEN_WIDTH + 160)//2, 140, 3, 160)
            pygame.draw.rect(screen, FONT_MENU_COLOR, stripe2)

            draw_Text("SCORE", font, FONT_MENU_COLOR, screen, SCREEN_WIDTH//2, 150)

            draw_Text(str(i), pygame.font.Font(r'res/font.ttf', 40), FONT_MENU_COLOR, screen, SCREEN_WIDTH//2, 230)
            if i != score:
                if int(score) > 0:
                    i += 1
                else: i -= 1
            else: 
                draw_Text("Time: "+ str(time) +" s", font2, FONT_MENU_COLOR, screen, SCREEN_WIDTH//2, 290)

            outline = pygame.Rect((SCREEN_WIDTH - 602 )//2, 349, 602, 52)
            pygame.draw.rect(screen, FONT_MENU_COLOR, outline)
            button("It’s better not to move", (SCREEN_WIDTH - 600 )//2, 350, 600, 50, BACKGROUND_COLOR, BACKGROUND_COLOR)

        else:

            stripe1 = pygame.Rect(100, 140, 3, 160)
            pygame.draw.rect(screen, FONT_MENU_COLOR, stripe1)
            stripe2 = pygame.Rect(260, 140, 3, 160)
            pygame.draw.rect(screen, FONT_MENU_COLOR, stripe2)    

            draw_Text("SCORE", font, FONT_MENU_COLOR, screen, 180, 150)
            draw_Text(str(i), pygame.font.Font(r'res/font.ttf', 40), FONT_MENU_COLOR, screen, 180, 230)
            if i != score:
                if int(score) > 0:
                    i += 1
                else: i -= 1
            else: 
                draw_Text("Time: "+ str(time) +"s", font2, FONT_MENU_COLOR, screen, 180, 290)

                if flag == 1:
                    draw_Text("GAME OVER", font, FONT_MENU_COLOR, screen, 600, 220)
                    outline = pygame.Rect((SCREEN_WIDTH - 552 )//2, 370, 552, 52)
                    pygame.draw.rect(screen, FONT_MENU_COLOR, outline)
                    button("Monster catched the pacman", (SCREEN_WIDTH - 550 )//2, 371, 550, 50, BACKGROUND_COLOR, BACKGROUND_COLOR)
                elif flag == 2:

                    screen.blit(trophy, (575, 230))

                    draw_Text("VICTORY", font, FONT_MENU_COLOR, screen, 600, 180)

                    outline = pygame.Rect((SCREEN_WIDTH - 482 )//2, 370, 482, 52)
                    pygame.draw.rect(screen, FONT_MENU_COLOR, outline)
                    button("Pacman eats all the food!", (SCREEN_WIDTH - 480 )//2, 371, 480, 50, BACKGROUND_COLOR, BACKGROUND_COLOR)


        draw_Text("Do you want to continue?", font2, FONT_MENU_COLOR, screen, SCREEN_WIDTH//2, 470)
        rect1 = draw_Text("MAIN MENU", font2, FONT_MENU_COLOR_2, screen, 390, 515)
        underline1 = pygame.Rect(355, 530, 70, 3)
        pygame.draw.rect(screen, FONT_MENU_COLOR_2, underline1)

        if rect1.collidepoint((mx, my)):
            hover("MAIN MENU", font2, rect1, FONT_MENU_COLOR_2, FONT_MENU_COLOR)
            if rect1.collidepoint((mx, my)):
                pygame.draw.rect(screen, FONT_MENU_COLOR, underline1)
            else: 
                pygame.draw.rect(screen, FONT_MENU_COLOR_2, underline1)
           
            if click:
                pass

            if click:
                pygame.quit()
                sys.exit()    

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
        mainClock.tick(40)
        
if __name__ == "__main__":
    winning_screen(2, 40, 125)