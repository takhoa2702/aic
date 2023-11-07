import tkinter
import pygame
import numpy as np
import random
from enum import Enum
from direction import *

class Color(Enum):
    BLACK = (0, 0, 0)
    BLUE = (25, 118, 210)
    GREEN = (56, 142, 60)
    PURPLE = (123, 31, 162)
    RED = (211, 47, 47)
    WHITE = (255, 255, 255)

COLOR_LIST = [e.value for e in Color]
COLOR_LIST.remove(Color.WHITE.value)

WINDOW_TITLE = "PACMAN"
FONT = "res/font.ttf"
SCREEN_HEIGHT, SCREEN_WIDTH = (600, 800)
DYNAMIC_SCREEN_SIZE = True  # Tự động thay đổi kích thước phù hợp với map
BLOCK_SIZE = 30             # Giá trị BLOCK_SIZE có thể bị thay đổi khi DYNAMIC_SCREEN_SIZE = True
DOT_SIZE = BLOCK_SIZE // 6
GAME_FPS = 60

FOOD_COLOR = Color.BLACK.value
WALL_COLOR = Color.PURPLE.value
ROAD_COLOR = Color.WHITE.value
TEXT_COLOR = Color.BLUE.value

GHOST_IMG = "res/slime" + random.choice(["1", "2", "3", "4"]) + ".png"
PACMAN_IMG = "res/pacman.png"
PACMAN_ANIMATION = ["res/walk1.png", "res/walk2.png", "res/walk3.png"]
PACMAN_STEP_COST = 1
PACMAN_ANIMATION_SPEED = 5
SCORE_PER_FOOD = 20
STEP_LEN = 1

ROAD = 0
WALL = 1
FOOD = 2
GHOST = 3
PACMAN = 4

def set_screen_size(grid_2d):

    global BLOCK_SIZE
    global DOT_SIZE

    if DYNAMIC_SCREEN_SIZE:
        nrow, ncol = grid_2d.shape

        if nrow <= 20:
            BLOCK_SIZE = 30
        elif nrow <= 40:
            BLOCK_SIZE = 20
        else:
            BLOCK_SIZE = 10

        screen_width, screen_height = map_graphic.total_screen_size(grid_2d, BLOCK_SIZE)
        DOT_SIZE = BLOCK_SIZE // 6
    else:
        screen_width, screen_height = (SCREEN_WIDTH, SCREEN_HEIGHT)

    return screen_width, screen_height


class map_graphic():
    def __init__(self, screen, grid_2d: np.ndarray, start_y: int, pacman_i: int, pacman_j: int):

        self.screen = screen
        self.game_over = False, -1

        self.grid_2d = grid_2d.copy()

        # tách riêng ghost_map vì GHOST có thể trùng với FOOD
        self.ghost_map = self.grid_2d.copy()
        # thay FOOD trong ghost_map thành ROAD
        self.ghost_map[self.ghost_map == FOOD] = ROAD

        # cập nhật vị trí PACMAN
        self.grid_2d[pacman_i, pacman_j] = PACMAN
        # thay GHOST trong map thành ROAD
        self.grid_2d[self.grid_2d == GHOST] = ROAD


        self.start_y = start_y
        self.pacman_x, self.pacman_y = self.to_screen_coord(pacman_i, pacman_j)

        self.font = pygame.font.Font(FONT, BLOCK_SIZE//2)

        self.pacman_block = None
        self.wall_blocks = pygame.sprite.Group()
        self.food_blocks = pygame.sprite.Group()
        self.ghost_blocks = pygame.sprite.Group()
        self.ghost_objs = []

        for i, row in enumerate(grid_2d): # không phải self.grid_2d
            for j, item in enumerate(row):
                x, y = self.to_screen_coord(i, j)
                if (x, y) == (self.pacman_x, self.pacman_y):
                    pacman_obj = pacman_graphic(self.pacman_x, self.pacman_y, height=BLOCK_SIZE, width=BLOCK_SIZE)
                    self.pacman_block = pacman_obj
                elif item == WALL:
                    wall_obj = wall_graphic(x, y, height=BLOCK_SIZE, width=BLOCK_SIZE)
                    self.wall_blocks.add(wall_obj)
                elif item == FOOD:
                    food_obj = food_graphic(x, y, height=BLOCK_SIZE, width=BLOCK_SIZE)
                    self.food_blocks.add(food_obj)
                elif item == GHOST:
                    ghost_obj = ghost_graphic(x, y, height=BLOCK_SIZE, width=BLOCK_SIZE)
                    self.ghost_objs.append(ghost_obj)
                    self.ghost_blocks.add(ghost_obj)


    def to_screen_coord(self, i: int, j: int) -> tuple:
        x = j * BLOCK_SIZE
        y = self.start_y + i * BLOCK_SIZE
        return x, y

    def to_cell_coord(self, x, y)->tuple:
        j = x // BLOCK_SIZE
        i = abs(y - self.start_y) // BLOCK_SIZE
        return i, j

    @staticmethod
    def total_screen_size(grid_2d, start_y=0) -> tuple:
        n_rows = len(grid_2d)
        n_cols = len(grid_2d[0])
        height = BLOCK_SIZE * (n_rows) + start_y
        width = BLOCK_SIZE * (n_cols)
        return width, height

    def get_total_screen_size(self)->tuple:
        return map_graphic.total_screen_size(self.grid_2d, self.start_y)

    def draw_map(self):
        self.screen.fill(ROAD_COLOR)

        # --- Draw the game here ---
        self.wall_blocks.draw(self.screen)
        self.food_blocks.draw(self.screen)
        self.ghost_blocks.draw(self.screen)

        self.screen.blit(self.pacman_block.image, self.pacman_block.rect)

        # Render the text for the score
        score = self.pacman_block.score
        time = self.pacman_block.path_length
        text = self.font.render(f"Score: {score} Time: {time}", True, Color.BLUE.value)

        # Put the text on the screen
        self.screen.blit(text, (0,0))

        pygame.display.flip()

class character_animation():
    def __init__(self, animation_imgs, height, width):

        # một list object các hình khi chạy sẽ cho ra animation
        self.animations = [pygame.transform.scale(img, (width, height)) for img in animation_imgs]

        # Index đến tấm hình hiện tại trong self.animations
        self.clock = 0
        self.index = 0

    def get_current_image(self):
        return self.animations[self.index]

    def get_animation_list(self):
        return self.animations.copy()

    def get_animation_len(self):
        return len(self.animations)

    @DeprecationWarning
    @staticmethod
    def to_animation_list(animation_img, height, width, colorkey=ROAD_COLOR)->str:
        animations = []
        if animation_img.get_height() >= animation_img.get_width():
            n_img = animation_img.get_height() // animation_img.get_width()
            full_height = height * n_img
            full_width = width
        else:
            n_img = animation_img.get_width() // animation_img.get_height()
            full_height = height
            full_width = width * n_img

        resize_animation_img = pygame.transform.scale(animation_img, (full_width, full_height))
        resize_animation_img.set_colorkey(colorkey)

        for y in range(0, full_height, height):
            for x in range(0, full_width, width):
                # blank image
                image = pygame.Surface((width, height)).convert_alpha()
                image.set_colorkey(colorkey)

                # Vẽ đè animation_img vào image
                image.blit(resize_animation_img, (0,0), (x, y, width, height))
                animations.append(image)
        return animations

    def update(self, fps):
        step = 30 // fps
        l = range(1, 30, step)

        if self.clock == 30:
            self.clock = 1
        else:
            self.clock += 1

        if self.clock in l:
            # Increase index
            self.index += 1
            if self.index == len(self.animations):
                self.index = 0


class pacman_graphic(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y, width, height,
                img_path=PACMAN_IMG, animation_paths=PACMAN_ANIMATION, color_key=ROAD_COLOR):

        super().__init__()

        # Ảnh hiện tại
        img = pygame.image.load(img_path).convert_alpha()
        img.set_colorkey(color_key)
        self.image = pygame.transform.scale(img, (width, height))

        self.moving_direction = None
        self.moving_steps = 0

        self.original_image = self.image
        self.rect = self.image.get_rect()

        # position
        self.rect.topleft = (init_x, init_y)
        self.start_x, self.start_y = init_x, init_y
        self.prev_i = -1
        self.prev_j = -1

        self.score = 0
        self.path_length = 0

        # walk animations objects
        animation_imgs = [pygame.image.load(path).convert_alpha() for path in animation_paths]
        for i in animation_imgs:
            i.set_colorkey(color_key)

        left_flipped = list(map(lambda img: pygame.transform.flip(img, True, False), animation_imgs))

        up_flipped = list(map(lambda img: pygame.transform.rotate(img, 90), animation_imgs))

        down_flipped = [pygame.transform.rotate(img, 180) for img in up_flipped]

        self.right_animation = character_animation(animation_imgs, height=BLOCK_SIZE, width=BLOCK_SIZE)
        self.left_animation = character_animation(left_flipped, height=BLOCK_SIZE, width=BLOCK_SIZE)
        self.up_animation = character_animation(up_flipped, height=BLOCK_SIZE, width=BLOCK_SIZE)
        self.down_animation = character_animation(down_flipped, height=BLOCK_SIZE, width=BLOCK_SIZE)

    def current_pos(self, map_obj: map_graphic):
        x, y = self.rect.topleft
        return map_obj.to_cell_coord(x, y)

    def is_moving(self)->bool:
        return self.moving_direction is not None
    
    def turn(self, direction: Direction):
        self.moving_direction = direction
        self.moving_steps = 0


    def update(self, map_obj:map_graphic, step_cost=PACMAN_STEP_COST,
                step_len=STEP_LEN, update_fps=PACMAN_ANIMATION_SPEED):
        if self.moving_direction is None:
            return

        cur_x, cur_y = self.rect.x, self.rect.y

        # Pacman đang di chuyển
        if self.moving_direction is not None and self.moving_steps < BLOCK_SIZE:
            # Update lại tọa độ tùy thuộc vào hướng di chuyển
            if self.moving_direction == Direction.LEFT.value:
                self.left_animation.update(update_fps)
                self.image = self.left_animation.get_current_image()
                cur_x -= step_len

            elif self.moving_direction == Direction.RIGHT.value:
                self.right_animation.update(update_fps)
                self.image = self.right_animation.get_current_image()
                cur_x += step_len

            elif self.moving_direction == Direction.UP.value:
                self.up_animation.update(update_fps)
                self.image = self.up_animation.get_current_image()
                cur_y -= step_len

            elif self.moving_direction == Direction.DOWN.value:
                self.down_animation.update(update_fps)
                self.image = self.down_animation.get_current_image()
                cur_y += step_len
            else:
                raise Exception("UNKNOWN DIRECTION VALUE")
            self.moving_steps += step_len
        else:
            hit_food_blocks = pygame.sprite.spritecollide(self, map_obj.food_blocks, True)

            if len(hit_food_blocks) > 0:
                self.score += SCORE_PER_FOOD
                food_x, food_y = hit_food_blocks[0].rect.topleft

                food_i, food_j = map_obj.to_cell_coord(food_x, food_y)
                map_obj.grid_2d[food_i, food_j] = WALL
        
            # Nếu đã di chuyển đến ô đích
            if self.moving_direction is not None:
                self.score -= step_cost
                self.path_length += PACMAN_STEP_COST

                # Cập nhật vị trí pacman trên grid_2d
                i, j = map_obj.to_cell_coord(cur_x, cur_y)
                map_obj.grid_2d[i, j] = PACMAN
                if self.prev_i != -1 and self.prev_j != -1:
                    map_obj.grid_2d[self.prev_i, self.prev_j] = ROAD
                else:
                    start_i, start_j = map_obj.to_cell_coord(self.start_x, self.start_y)
                    map_obj.grid_2d[start_i, start_j] = ROAD
                    self.prev_i, self.prev_j = i, j

                nrow = map_obj.grid_2d.shape[0]

            self.moving_steps = 0
            self.moving_direction = None
            return

        # Dừng di chuyển khi đụng tường
        for block in pygame.sprite.spritecollide(self, map_obj.wall_blocks, False):
            block_x, block_y = block.rect.x, block.rect.y
            new_x, new_y = self.rect.x, self.rect.y

            if block_x != self.rect.x:
                if block_x < self.rect.x:
                    new_x = block_x + BLOCK_SIZE
                else:
                    new_x = block_x - BLOCK_SIZE
            elif block_y != self.rect.y:
                if block_y < self.rect.y:
                    new_y = block_y + BLOCK_SIZE
                else:
                    new_y = block_y - BLOCK_SIZE

            self.rect.topleft = new_x, new_y
            self.moving_direction = None
            self.moving_steps = 0
            return

        # tránh object lọt ra khỏi map
        max_width, max_height = map_obj.get_total_screen_size()
        if cur_x >= 0 and cur_x <= max_width - BLOCK_SIZE:
            self.rect.x = cur_x

        if cur_y >= 0 and cur_y <= max_height - BLOCK_SIZE:
            self.rect.y = cur_y

    def random_moves(self, map_obj: map_graphic)->Direction:
        if self.is_moving():
            return None

        x, y = self.rect.topleft
        i, j = map_obj.to_cell_coord(x, y)
        candidates = []

        if j > 0 and map_obj.grid_2d[i, j - 1] != WALL:
            candidates.append(Direction.LEFT.value)

        if j < len(map_obj.grid_2d[0]) - 1 and map_obj.grid_2d[i, j + 1] != WALL:
            candidates.append(Direction.RIGHT.value)

        if i > 0 and map_obj.grid_2d[i - 1, j] != WALL:
            candidates.append(Direction.UP.value)

        if i < len(map_obj.grid_2d[0]) - 1 and map_obj.grid_2d[i + 1, j] != WALL:
            candidates.append(Direction.DOWN.value)

        if len(candidates) == 0:
            return None

        move = random.choice(candidates)
        return move


class ghost_graphic(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img_path=GHOST_IMG, color_key=ROAD_COLOR):
        super().__init__()
        img = pygame.image.load(img_path).convert_alpha()
        img.set_colorkey(color_key)

        self.image = pygame.transform.scale(img, (width, height))

        self.moving_direction = None
        self.moving_steps = 0

        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        self.prev_i = -1
        self.prev_j = -1

        self.root_x, self.root_y = x, y

    def is_moving(self)->bool:
        return self.moving_direction is not None

    def turn(self, direction: Direction):
        self.moving_direction = direction
        self.moving_steps = 0


    def update(self, map_obj:map_graphic, step_len=STEP_LEN):

        if self.moving_direction is None:
            return

        cur_x, cur_y = self.rect.x, self.rect.y

        if self.moving_direction is not None and self.moving_steps < BLOCK_SIZE:
            if self.moving_direction == Direction.LEFT.value:
                cur_x -= step_len
            elif self.moving_direction == Direction.RIGHT.value:
                cur_x += step_len
            elif self.moving_direction == Direction.UP.value:
                cur_y -= step_len
            elif self.moving_direction == Direction.DOWN.value:
                cur_y += step_len
            if (cur_x, cur_y) != (self.rect.x, self.rect.y):
                self.moving_steps += step_len
        else:
            if self.moving_direction is not None:
                # Cập nhật vị trí pacman trên grid_2d
                i, j = map_obj.to_cell_coord(cur_x, cur_y)
                map_obj.ghost_map[i, j] = GHOST
                if self.prev_i != -1 and self.prev_j != -1:
                    map_obj.ghost_map[self.prev_i, self.prev_j]
                else:
                    self.prev_i, self.prev_j = i, j
                    start_i, start_j = map_obj.to_cell_coord(self.root_x, self.root_y)
                    map_obj.ghost_map[start_i, start_j] = ROAD


            self.moving_steps = 0
            self.moving_direction = None
            return


        for block in pygame.sprite.spritecollide(self, map_obj.wall_blocks, False):
            block_x, block_y = block.rect.x, block.rect.y
            new_x, new_y = self.rect.x, self.rect.y

            if block_x != self.rect.x:
                if block_x < self.rect.x:
                    new_x = block_x + BLOCK_SIZE
                else:
                    new_x = block_x - BLOCK_SIZE
            elif block_y != self.rect.y:
                if block_y < self.rect.y:
                    new_y = block_y + BLOCK_SIZE
                else:
                    new_y = block_y - BLOCK_SIZE

            self.rect.topleft = new_x, new_y

            self.moving_direction = None
            self.moving_steps = 0

            return

        max_width, max_height = map_obj.get_total_screen_size()
        if cur_x >= 0 and cur_x <= max_width - BLOCK_SIZE:
            self.rect.x = cur_x

        if cur_y >= 0 and cur_y <= max_height - BLOCK_SIZE:
            self.rect.y = cur_y

    def get_current_pos(self)->tuple:
        return self.rect.x, self.rect.y

    def random_moves(self, map_obj: map_graphic)->Direction:
        if self.is_moving():
            return None
        x, y = self.rect.topleft
        i, j = map_obj.to_cell_coord(x, y)
        candidates = []
        if j > 0 and map_obj.ghost_map[i, j - 1] != WALL:
            candidates.append(Direction.LEFT.value)

        if j < len(map_obj.ghost_map[0]) - 1 and map_obj.ghost_map[i, j + 1] != WALL:
            candidates.append(Direction.RIGHT.value)

        if i > 0 and map_obj.ghost_map[i - 1, j] != WALL:
            candidates.append(Direction.UP.value)

        if i < len(map_obj.ghost_map[0]) - 1 and map_obj.ghost_map[i + 1, j] != WALL:
            candidates.append(Direction.DOWN.value)

        if len(candidates) == 0:
            return None

        move = random.choice(candidates)

        return move

    def random_moves_around_root(self,  map_obj: map_graphic)->Direction:
        x, y = self.rect.topleft
        i, j = map_obj.to_cell_coord(x, y)

        if (x, y) == (self.root_x, self.root_y):
            move = self.random_moves(map_obj)
        else:
            root_i, root_j = map_obj.to_cell_coord(self.root_x, self.root_y)
            path = [(i, j), (root_i, root_j)]
            move = coord_to_direction(path, i, j)[0]

        return move

import math
class food_graphic(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width, colorkey=FOOD_COLOR):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.color = colorkey

        self.image.fill(ROAD_COLOR)

        center = int(math.sqrt(2) / 2 * BLOCK_SIZE)
        pygame.draw.ellipse(self.image, colorkey,(int(center/2), int(center/2), DOT_SIZE, DOT_SIZE))

        self.rect = self.image.get_rect()
        self.rect.topleft = x, y


class wall_graphic(pygame.sprite.Sprite):

    def __init__(self, x, y, height, width, colorkey=WALL_COLOR):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width,height))
        self.image.fill(colorkey)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

if __name__ == "__main__":
    
    from readfile import *

    pygame.init()

    size, grid_2d, start = readfile("input/3/input5.txt")
    size = np.array(size)
    grid_2d = np.array(grid_2d)
    start = np.array(start)
    grid_2d, size, start = check_fence(grid_2d, size, start)

    screen_width, screen_height = set_screen_size(grid_2d)
    screen = pygame.display.set_mode((screen_width, screen_height + BLOCK_SIZE))

    pygame.display.set_caption(WINDOW_TITLE)
    
    clock = pygame.time.Clock()

    closed_window = False
    start_y = BLOCK_SIZE

    pacman_i = start[0]
    pacman_j = start[1]

    map_obj = map_graphic(screen, grid_2d, start_y, pacman_i=pacman_i, pacman_j=pacman_j)

    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        map_obj.draw_map()

        clock.tick(GAME_FPS)
    pygame.quit()
