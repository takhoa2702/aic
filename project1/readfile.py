import numpy as np

def readfile(path):
    f = open(path, 'r')
    a = f.readline()
    size = a.split(' ')
    for i in range(len(size)):
        size[i] = int(size[i].rstrip('\n'))
    map=[]
    while True:
        s = f.readline()
        if not s:
            break

        row = s.split(' ')
        for i in range(len(row)):
            row[i] = row[i].rstrip('\n')
            try:
                row[i] = int(row[i])
            except ValueError:
                row.pop(i)
        map.append(row)
    start = map.pop(-1)
    f.close()
    return size, map, start


def check_fence(map, size, start):
    new_map = map
    flag = 0
    row_one = np.ones(size[1], dtype=int).reshape((1, size[1]))
    col_one = np.ones(size[0], dtype=int).reshape((size[0], 1))

    first_row = map[0,:]
    if np.array_equal(first_row, row_one):
        flag+=1
    

    last_row = map[-1, :]
    if np.array_equal(last_row,row_one):
        flag += 1
    

    first_col = map[:,0]
    if np.array_equal(first_col, col_one):
        flag += 1
    

    last_col = map[:, -1]
    if np.array_equal(last_col, col_one):
        flag += 1
    

    if flag < 4:
        row_one = np.ones(size[1], dtype=int).reshape((1, size[1]))
        col_one = np.ones(size[0] + 2, dtype=int).reshape((size[0] + 2, 1))
        
        new_map = np.r_[row_one, new_map]  #add row
        new_map = np.r_[new_map, row_one]  
        new_map = np.c_[new_map, col_one]   #add collumn
        new_map = np.c_[col_one, new_map]
        size += 2
        start += 1
        return new_map, size, start
    else:
        return map, size, start

if __name__ == "__main__":
    size, map, start = readfile('input/1/input1.txt')
    
    size = np.array(size)
    map = np.array(map)
    start = np.array(start)
    
    map, size, start = check_fence(map, size, start)
    print(map)
    print(size)
    print(start)