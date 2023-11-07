import pygame, sys
from pygame.math import Vector2 as vec
import random
import numpy as np

from map import *
import map as m
from pygame.math import Vector2 as vec
import win
import multiprocessing as mp

FORCE_TO_MOVE = False

class Pacman:
    def __init__(self, map_obj, pos):
        self.map_obj = map_obj
        self.map_nrow = map_obj.grid_2d.shape[0]
        self.map_ncol = map_obj.grid_2d.shape[1]
        self.saveghost = []
        self.grid_pos = pos
        self.road = self.map_obj.grid_2d.copy()
        self.pac_location = pos                
        self.pix_pos = self.get_pix_pos()       
        self.list_data = self.get_neighbors() 
        self.save_shadow = self.create_save_shadow()

    def update_pos(self, pos):
        self.pac_location = pos
        self.grid_pos = pos

    def get_pix_pos(self):
        return (vec(((self.grid_pos.x + 1/2)*m.BLOCK_SIZE), \
                ((self.grid_pos.y + 1/2)*m.BLOCK_SIZE)))
    
    def check_map(self, road):
        self.road = road

    def heuristic(self, current, food):
        return abs(current % self.map_nrow - food % self.map_nrow) + abs(current//self.map_nrow - food//self.map_nrow)

    def isValid(self, row:int, col:int):
        return (row >= 0) and (row < self.map_nrow) and (col >= 0) and (col < self.map_ncol)

    def isValid3(self, row:int, col:int, height, width):
        return (row >= 0) and (row < height) and (col >= 0) and (col < width)

    def isUnblock(self, vision, row:int, col:int):
        return self.map_obj.ghost_map[row, col] != GHOST and (vision[row, col] != WALL)
    
    def isUnblock3(self, vision, row:int, col:int):
        return vision[row][col] == ROAD or vision[row][col] == FOOD


    def isDestination(self, row:int, col:int, food: vec):
        return (row == int(food.x) and col == int(food.y))
    
    def get_neighbors(self):
        neighbors = []
        for col in range(self.map_ncol):
            for row in range(self.map_nrow):

                neighbor = []
                if self.isValid(row, col) and self.isUnblock(self.road, row, col):
                        up = [row - 1,col]
                        down = [row + 1, col]
                        left = [row, col - 1]
                        right = [row, col + 1]

                        if self.isValid(up[0], up[1]) and self.isUnblock(self.road, up[0], up[1]):
                            neighbor.append(self.map_nrow * up[1] + up[0])

                        if self.isValid(down[0], down[1]) and self.isUnblock(self.road, down[0], down[1]):
                            neighbor.append(self.map_nrow * down[1] + down[0])

                        if self.isValid(left[0], left[1]) and self.isUnblock(self.road, left[0], left[1]):
                            neighbor.append(self.map_nrow * left[1] + left[0])

                        if self.isValid(right[0], right[1]) and self.isUnblock(self.road, right[0], right[1]):
                            neighbor.append(self.map_nrow * right[1] + right[0])
                        neighbors.append(neighbor)

                else:
                    neighbors.append([])
        return neighbors

    def get_neighbors3(self, map_2d, width, height):
        neighbors = []
        for col in range(width):
            for row in range(height):

                neighbor = []
                if self.isValid3(row, col, height, width) and self.isUnblock3(map_2d, row, col):
                        up = [row - 1,col]
                        down = [row + 1, col]
                        left = [row, col - 1]
                        right = [row, col + 1]

                        if self.isValid3(up[0], up[1], height, width) and self.isUnblock3(map_2d, up[0], up[1]):
                            neighbor.append(int(height) * up[1] + up[0])

                        if self.isValid3(down[0], down[1], height, width) and self.isUnblock3(map_2d, down[0], down[1]):
                            neighbor.append(int(height) * down[1] + down[0])

                        if self.isValid3(left[0], left[1], height, width) and self.isUnblock3(map_2d, left[0], left[1]):
                            neighbor.append(int(height) * left[1] + left[0])

                        if self.isValid3(right[0], right[1], height, width) and self.isUnblock3(map_2d, right[0], right[1]):
                            neighbor.append(int(height) * right[1] + right[0])
                        neighbors.append(neighbor)

                else:
                    neighbors.append([])
        return neighbors

    def f_heuristic(self, node):
        return node[1]

    def next_node(self, current_node):
        return current_node[0][-1]

    def Graph_Search_A_Star(self, goal_x, goal_y):
        queue = []
        
        goal = int(goal_y) + self.map_nrow * int(goal_x)
        start = int(self.pac_location.y) + self.map_nrow * int(self.pac_location.x)

        queue.append(([start], self.heuristic(start,goal), 0))
        explored = []
        visited = []
        timeEscape = 0

        for i in range(0, len(self.list_data)):
            visited.append(False)
        visited[start] = True

        while len(queue) > 0:
            queue = sorted(queue,key=self.next_node)
            queue = sorted(queue,key=self.f_heuristic)

            catch = queue.pop(0)
            g = catch[2]
            explored.append(catch[0][-1])

            timeEscape += 1
            visited[catch[0][-1]] = True

            if catch[0][-1] == goal:
                return catch[0]

            else:

                for x in self.list_data[catch[0][-1]]:
                    catch1 = catch[0].copy()
                    catch1.append(x)
                    if visited[x] == False:
                        visited[x] = True
                        queue.append((catch1, self.heuristic(x,goal) + g + 1, g + 1))
        return []

    # METHODS FOR LEVEL 3
    def create_save_shadow(self):
        return [[-1 for _ in range(self.map_ncol)]] * self.map_nrow
    
    def get_shadow(self):
        map_shadow = []
        flag = 0
        check = 0

        for row in range(int(self.pac_location.y) - 3, int(self.pac_location.y) + 4):
            temp = []
            for col in range(int(self.pac_location.x) -3, int(self.pac_location.x) + 4):

                if self.isValid3(row, col, self.map_nrow, self.map_ncol) and col >= (int(self.pac_location.x) - flag) and col <= (int(self.pac_location.x) + flag):
                    if(self.pac_location.y == row and self.pac_location.x == col and self.road[row][col] == FOOD): ### WHY?
                        self.road[row][col] = ROAD
                    temp.append(self.road[row][col])
                    # --------------
                    if self.map_obj.ghost_map[row][col] == GHOST:
                        temp[-1] = GHOST

                    if temp[-1] == PACMAN:
                        temp[-1] = ROAD
                else:
                    temp.append(-1)

            if flag <= 3 and check == 0:
                flag += 1
            if flag > 3:
                flag = flag - 1
                check = 1
            if check == 1:
                flag -= 1
            map_shadow.append(temp)

        return map_shadow

    def get_food(self, map_shadow):
        food = []
        for row in range(len(map_shadow)):
            for col in range(len(map_shadow[0])):
                if(map_shadow[row][col] == FOOD):
                    food.append([row,col])
        return food
    
    def check_monster(self, map_shadow):
        for row in range(len(map_shadow)):
            for col in range(len(map_shadow[0])):
                check = 0
                if(map_shadow[row][col] == GHOST):
                    if(row == 3 and col == 0):
                        if  map_shadow[row][col + 1] == 3:
                            map_shadow[row][col] = 1
                        else:
                            map_shadow[row][col] = 1
                            map_shadow[row][col + 1] = 1
                    elif(row == 3 and col == len(map_shadow[0]) - 1):
                        if map_shadow[row][col - 1] == 3:
                            map_shadow[row][col] = 1
                        else:
                            map_shadow[row][col] = 1
                            map_shadow[row][col - 1] = 1
                    elif(col == 3 and row == 0):
                        if map_shadow[row + 1][col] == 3:
                            map_shadow[row][col] = 1
                        else:
                            map_shadow[row+1][col] = 1
                            map_shadow[row][col] = 1
                    elif(col == 3 and row == len(map_shadow[0]) - 1):
                        if map_shadow[row - 1][col] == 3: 
                            map_shadow[row][col] = 1
                        else:
                            map_shadow[row][col] = 1
                            map_shadow[row - 1][col] == 1
                    else:
                        if row == 3 and col == 2:
                            check = 1
                        elif(row == 2 and col == 3):
                            check = 2
                        elif(row == 3 and col == 4):
                            check = 3
                        elif(row == 4 and col == 3):
                            check = 4
                        map_shadow[row][col] = 1
                        if(map_shadow[row][col+1] != -1 and map_shadow[row][col+1] != 3 and check != 1):
                            map_shadow[row][col+1] = 1
                        if(map_shadow[row][col-1] != -1 and map_shadow[row][col-1] != 3 and check != 3):
                            map_shadow[row][col-1] = 1
                        if(map_shadow[row+1][col] != -1 and map_shadow[row+1][col] != 3 and check != 2):
                            map_shadow[row+1][col] = 1
                        if(map_shadow[row-1][col] != -1 and map_shadow[row-1][col] != 3 and check != 4):
                            map_shadow[row-1][col] = 1
        return map_shadow   

    def Breadth_First_Search(self, list_data, start, food):
        queue = []
        queue.append([start])
        explored = []
        timeEscape = 0

        visited = [False] * len(list_data)

        visited[0] = True
        while len(queue) > 0:

            catch = queue.pop(0)
            explored.append(catch[-1])
            timeEscape += 1
            visited[catch[-1]] = True

            if catch[-1] == food:
                return catch, explored, timeEscape
            else:
                for x in list_data[catch[-1]]:
                    catch1 = catch.copy()
                    catch1.append(x)
                    if visited[x] == False:
                        visited[x] = True
                        queue.append(catch1)
                
        return [], explored, timeEscape


    def get_w_food(self, set_food):
        data_food = []
        for x in set_food:
            data_food.append(int(x[0]) + int((7)*int(x[1])))
        return data_food
    
    def check_around(self, map_shadow):
        X = []

        if(map_shadow[3][2] == ROAD):
            X.append([3, 2])
        if(map_shadow[3][4] == ROAD):
            X.append([3, 4])
        if(map_shadow[2][3] == ROAD):
            X.append([2, 3])
        if(map_shadow[4][3] == ROAD):
            X.append([4, 3])
        
        if len(X) != 0:
            i = random.randint(0,len(X) - 1)
            return X[i]
        return []
    
    def set_limit(self, map_shadow):
        limit = []
        flag = 0
        check = 0

        for row in range(7):
            for col in range(7):
                if(col == (3 - flag) or col == (3 + flag)):
                    if map_shadow[row][col] != WALL and map_shadow[row][col] != -1:
                        limit.append([row,col])

            if flag <= 3 and check == 0:
                flag += 1
            if flag > 3:
                flag = flag - 1
                check = 1
            if check == 1:
                flag -= 1

        return limit

    def path_level_3(self):

        map_shadow = self.check_monster(self.get_shadow()).copy()

        set_food = self.get_food(map_shadow).copy()
        data_level3 = self.get_neighbors3(map_shadow, 7, 7).copy()

        start = 3 + 7 * 3
        data_food = self.get_w_food(set_food).copy()

        Y = []
        check = 0
        set_path_limit = []

        if not data_food:
            check = 1
            s_limit = self.set_limit(map_shadow)
            d_limit = self.get_w_food(s_limit)

            for i in d_limit:
                path_return, explored, timeEscape = self.Breadth_First_Search(data_level3,start, i)
                set_path_limit.append(path_return)
            
            list2 = [e for e in set_path_limit if e]
            if len(list2) > 1:
                list_path = sorted(list2, key = len)
                return list_path[0]
            else:
                print('end game')
                return []
            return path_return
        else:
            for i in data_food:
                path_return,explored,timeEscape = self.Breadth_First_Search(data_level3, start, i)
                Y.append(path_return)

        queue1 = [e for e in Y if e]
        if len(queue1) > 1:
            queue = sorted(queue1, key = len)
            return queue[0]

        if len(Y[0]) > 0:
            return Y[0]
        elif check != 1: 
            return explored
    
    def level_3(self):
        path_temp = self.path_level_3().copy()
        if len(path_temp) > 1:
            path_temp.pop(0)
        else:
            return Direction.NO_MOVE.value

        for i in path_temp:
            S_x = int(i // 7) - 3
            S_y = int(i % 7) - 3
            X = self.level_return(int(S_x), int(S_y))
            return X
    
    def level_return(self, S_x, S_y):
        if S_x == -1 and S_y == 0:
            return Direction.LEFT.value # 1
        elif  S_x == 1 and S_y == 0: 
            return Direction.RIGHT.value # 2
        elif S_x == 0 and S_y == -1:
            return Direction.UP.value # 3
        elif S_x == 0 and S_y == 1:
            return Direction.DOWN.value # 4
        elif S_x == 0 and S_y == 0:
            return Direction.NO_MOVE.value # 5
    
def level1_2(map_obj: map_graphic, pacman_moves: list):

    if map_obj.game_over[0]:
        return
    
    if pacman_moves is not None or len(pacman_moves) > 0:
        if not map_obj.pacman_block.is_moving():
            if len(pacman_moves) > 0:
                has_moves = True
                direction = pacman_moves.pop(0)
                map_obj.pacman_block.turn(direction)

        map_obj.pacman_block.update(map_obj)

    hit_ghost_blocks = pygame.sprite.spritecollide(map_obj.pacman_block, map_obj.ghost_blocks,True)
    
    if len(hit_ghost_blocks) > 0:
        map_obj.game_over = True, 1

    if len(pacman_moves) == 0 and not map_obj.pacman_block.is_moving():
        map_obj.game_over = True, 2

def run_game_level_1_2(grid_2d: np.ndarray, pacman_i, pacman_j, init_yet=False):
    if not init_yet:
        pygame.init()

    screen_width, screen_height = set_screen_size(grid_2d)
    screen = pygame.display.set_mode((screen_width, screen_height + m.BLOCK_SIZE))

    pygame.display.set_caption(WINDOW_TITLE)
    
    clock = pygame.time.Clock()

    start_y = m.BLOCK_SIZE

    map_obj = map_graphic(screen, grid_2d, start_y, pacman_i=pacman_i, pacman_j=pacman_j)
    pacman = Pacman(map_obj, vec(pacman_j, pacman_i))    
    
    foods = np.where(map_obj.grid_2d == FOOD)
    should_go = True
    if not np.size(foods) == 0:
        food_x = foods[1][0]
        food_y = foods[0][0]

        nrow, ncol = map_obj.grid_2d.shape
        path = pacman.Graph_Search_A_Star(food_x, food_y)

        if not FORCE_TO_MOVE:  
            if len(path) - 1 <= SCORE_PER_FOOD:
                should_go = True
            if len(path) == 0:
                should_go = False        
        pacman_moves = coord_to_direction(cell_to_coord(path, nrow), pacman_i, pacman_j)
    else: 
        path = []
        pacman_moves = []
        should_go = False
    
    done = False
    game_over = False

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        if should_go:
            level1_2(map_obj, pacman_moves)

        map_obj.draw_map()

        if map_obj.game_over[0] or not should_go:
            if not should_go:
                map_obj.game_over = True, 0

            game_over = True
            ctx = mp.get_context('spawn')
            p = ctx.Process(target=win.winning_screen, args=(map_obj.game_over[1], 
                            map_obj.pacman_block.score, map_obj.pacman_block.path_length))
            p.start()
            p.join()
            break

        clock.tick(GAME_FPS)

    if not should_go:
        pygame.time.wait(2000)

    if not init_yet:
        pygame.quit()

def level3(map_obj: map_graphic, pacman: Pacman, store_direction):

    if map_obj.game_over[0]:
        return
    
    has_move = False
    if not map_obj.pacman_block.is_moving():
        pacman.road = map_obj.grid_2d.copy()
        cur_i, cur_j = map_obj.pacman_block.current_pos(map_obj)

        pacman.update_pos(vec(cur_j, cur_i))
        direction = pacman.level_3()
        store_direction.append(direction)
        if direction != Direction.NO_MOVE.value:
            map_obj.pacman_block.turn(direction)
            has_move = True
        else:
            map_obj.game_over = True, 2


    map_obj.pacman_block.update(map_obj)

    hit_ghost_blocks = pygame.sprite.spritecollide(map_obj.pacman_block, map_obj.ghost_blocks,True)
    
    if len(hit_ghost_blocks) > 0:
        map_obj.game_over = True, 1

    for ghost in map_obj.ghost_objs:
       if not ghost.is_moving() and has_move:
           ghost.turn(ghost.random_moves_around_root(map_obj))

    map_obj.ghost_blocks.update(map_obj)

def check_repeat(store):
    repeat = 0
    if len(store) > 8:
        for i in range(len(store)-4):
            if store[i] != store[i+1]:
                if (store[i], store[i+1]) == (store[i+2], store[i+3]):
                    repeat += 1
                else: repeat = 0
        if repeat == 6:
            return True
        else: 
            return False
    else: 
        return False


def run_game_level_3(grid_2d: np.ndarray, pacman_i, pacman_j, init_yet=False):
    if not init_yet:
        pygame.init()

    screen_width, screen_height = set_screen_size(grid_2d)
    screen = pygame.display.set_mode((screen_width, screen_height + m.BLOCK_SIZE))

    pygame.display.set_caption(WINDOW_TITLE)
    
    clock = pygame.time.Clock()

    closed_window = False
    start_y = m.BLOCK_SIZE

    map_obj = map_graphic(screen, grid_2d, start_y, pacman_i=pacman_i, pacman_j=pacman_j)
    pacman = Pacman(map_obj, vec(pacman_j, pacman_i))    

    done = False
    game_over = False 
    first_move = pacman.level_3()
    should_go = first_move != Direction.NO_MOVE.value

    store_direction = []

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        if should_go:
            level3(map_obj, pacman, store_direction)
        
        if check_repeat(store_direction):
            map_obj.game_over = True, 0

        map_obj.draw_map()
        
        if map_obj.game_over[0] or not should_go:
            if not should_go:
                map_obj.game_over = True, 0

            game_over = True
            ctx = mp.get_context('spawn')
            p = ctx.Process(target=win.winning_screen, args=(map_obj.game_over[1], 
                            map_obj.pacman_block.score, map_obj.pacman_block.path_length))
            p.start()
            p.join()
            break

        clock.tick(GAME_FPS)

    if not should_go:
        pygame.time.wait(2000)

    if not init_yet:
        pygame.quit()

    
from readfile import *

def test(level,path):
    main(level, path)
    size, grid_2d, start = readfile('input/3/input1.txt')
    size = np.array(size)
    grid_2d = np.array(grid_2d)
    start = np.array(start)

    grid_2d, size, start = check_fence(grid_2d, size, start)
    run_game_level_1_2(grid_2d, pacman_i=start[0], pacman_j=start[1])

def main(level, path):

    size, grid_2d, start = readfile(path)
    size = np.array(size)
    grid_2d = np.array(grid_2d)
    start = np.array(start)

    grid_2d, size, start = check_fence(grid_2d, size, start)
    level1_2_str = [1, 2, "1", "2", "LEVEL1", "LEVEL2"]
    level1_3_str = [3, "3", "LEVEL3"]

    if level in level1_2_str:
        run_game_level_1_2(grid_2d, pacman_i=start[0], pacman_j=start[1])
    elif level in level1_3_str:
        run_game_level_3(grid_2d, pacman_i=start[0], pacman_j=start[1])

    

import sys
if __name__ == '__main__':
    argv = sys.argv
    if len(argv) <= 1:
        test(level = 1, path = "input/1/input3.txt")
    else:
        main(argv[1], argv[2])
