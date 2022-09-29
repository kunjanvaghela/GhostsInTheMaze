from calendar import c
from queue import Empty
import numpy as np
import time

# Variable Declare
my_grid=[]
invalid_indices=[]
grid_size=11
nr_of_ghosts=0

# To create the grid
def create_grid(grid_size, blocked_cell=0.28):
    #while :
    my_grid = np.random.rand(grid_size,grid_size)
    my_grid = np.where(my_grid<=blocked_cell, 1, 0)
    my_grid[0][0]=0
    my_grid[grid_size-1, grid_size-1] = 0
    print(my_grid)
    print(depth_first_search(my_grid))
    #if depth_first_search(my_grid):
    #    break
    #time.sleep(200)
    return my_grid


# To get Ghost Cell, on which ghost can be spawned.
def get_ghost_cell_index():
    while True:
        row_index = np.random.randint(0, grid_size)
        column_index = np.random.randint(0, grid_size)
        if (row_index, column_index) not in invalid_indices:
            return row_index, column_index
    

def set_invalid_indices():
    invalid_indices = np.argwhere(my_grid == 1)
    invalid_indices = np.append(invalid_indices, [[0,0]], axis=0)
    invalid_indices = np.append(invalid_indices, [[grid_size-1, grid_size-1]], axis=0)
    return invalid_indices

def place_ghosts(num_ghosts):
    for i in range(num_ghosts):
        row_ind, col_ind = get_ghost_cell_index()
        my_grid[row_ind][col_ind] = -1
    return my_grid

def depth_first_search(my_grid):
    start=[0,0]
    fringe=[start]
    print('Fringe : '+str(fringe) + str(type(fringe)))
    print('Start : '+ str(start) + str(type(start)))
    explored=[start]
    i=0
    try:
        while len(fringe) > 0:
            currCell = fringe.pop()
            print('Fringe : '+str(fringe))
            print('currcell : ' + str(currCell) + str(type(currCell)))
            if currCell not in explored:            # to solve the issue where code was revisiting already explored cells
                explored.append(currCell)
            #explored.append(nextCell)      # when was this appended? Unsure
            if currCell == [grid_size-1,grid_size-1]:
                print('Path exists')
                print('Fringe : '+str(fringe))
                print('Explored Path : '+str(explored))
                return True
            # write code to check each side : LUDR and check if not going array out of bounds
            # Code to select nextCell as Left
            if currCell[1] != 0:
                if my_grid[currCell[0], (currCell[1] - 1)] == 0:
                    nextCell = [currCell[0], (currCell[1] - 1)]
                    if nextCell not in explored:
                        fringe.append(nextCell)
                    print('In first loop')
            # Code to select nextCell as Up
            if currCell[0] != 0:
                if my_grid[(currCell[0] - 1), currCell[1]] == 0:
                    nextCell = [(currCell[0] - 1), currCell[1]]
                    if nextCell not in explored:
                        fringe.append(nextCell)
                    print('In sec loop')
            # Code to select nextCell as Down
            if currCell[0] != (grid_size - 1):
                if my_grid[currCell[0] + 1, currCell[1]] == 0:
                    nextCell = [(currCell[0] + 1), currCell[1]]
                    if nextCell not in explored:
                        fringe.append(nextCell)
                    print('In third loop')
            # Code to select nextCell as Right
            if currCell[1] != (grid_size - 1):
                if my_grid[currCell[0], currCell[1] + 1] == 0:
                    nextCell = [currCell[0], (currCell[1] + 1)]
                    if nextCell not in explored:
                        fringe.append(nextCell)
                    print('In fourth loop')
            if nextCell in explored:
                continue
            if nextCell is None:
                print('nextCell is not defined. Path probably does not exist')
                return False
            explored.append(nextCell)
            #fringe.append(nextCell)
            print('Fringe : '+str(fringe))
            print('Explored : '+str(explored))
            i=i+1
            if i>50:
                print('Value of i is more than threshold')
                return False
        else:
            print('Path does not exist!')
            return False
    except Exception as error111:
        print('No path present')
        print(error111)
        return False
        
        

my_grid= create_grid(grid_size)
invalid_indices = set_invalid_indices()
invalid_indices = invalid_indices.tolist()
my_grid = place_ghosts(nr_of_ghosts)
print(my_grid)
#depth_first_search(my_grid)
