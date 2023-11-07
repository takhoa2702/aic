from enum import Enum
class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    NO_MOVE = 5

def cell_to_coord(path, nrow):
    return [(cell % nrow, cell // nrow) for cell in path]

def coord_to_direction(path, start_x, start_y):
    cur_x = start_x
    cur_y = start_y

    output = []
    for t in path:
        i, j = t
        if (i, j) == (cur_y, cur_x):
            continue
        if i > cur_x:
            output.append(Direction.DOWN.value)
        elif i < cur_x:
            output.append(Direction.UP.value)
        else:
            if j > cur_y:
                output.append(Direction.RIGHT.value)
            elif j < cur_y:
                output.append(Direction.LEFT.value)


        cur_x = i
        cur_y = j

    return output


if __name__ == "__main__":
    
    path = [(2, 8), (2, 9), (2, 10), (2, 11), (3, 11), \
            (4, 11), (5, 11), (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (6, 16)]
    start_x = 2
    start_y = 8
 
    print(coord_to_direction(path, start_x, start_y))