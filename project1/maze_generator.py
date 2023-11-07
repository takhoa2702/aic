import random

WALL = 1
ROAD = 0

def generate_maze(width, height):
    maze = [["#" for _ in range(width)] for _ in range(height)]
    
    def create_maze(x, y):
        maze[y][x] = "."
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == "#":
                maze[y+dy][x+dx] = "."
                create_maze(nx, ny)
    
    create_maze(0, 0)
    s = ""
    for row in maze:
        s += ''.join(row + ['\n'])

    maze_blocks = []
    for row in maze:
        tmp = []
        for r in row:
            if r == '#':
                tmp.append(WALL)
            elif r == '.':
                tmp.append(ROAD)
        if len(tmp) != 0:
            maze_blocks.append(tmp)

    maze_blocks_str = "\n".join(" ".join(str(col) for col in row) for row in maze_blocks)
    
    rows = len(maze_blocks)
    cols = len(maze_blocks[0])

    return s, f"{rows} {cols}\n{maze_blocks_str}"

if __name__ == '__main__':
    s, blocks = generate_maze(width=10, height=5)
    print(s)
    print(blocks)