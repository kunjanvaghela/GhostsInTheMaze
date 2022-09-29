from genericpath import samestat
from importlib import invalidate_caches
import numpy as np
import sys
#print(sys.path)
#print(numpy.__version__)

my_grid=[]
invalid_indices=[]
grid_size=6

def create_grid(grid_size, blocked_cell=0.28):
    my_grid = np.random.rand(grid_size,grid_size)
    my_grid = np.where(my_grid<=blocked_cell, 1, 0)
    my_grid[0][0]=0
    my_grid[grid_size-1, grid_size-1] = 0
    print(my_grid)
    return my_grid

def get_ghost_cell_index():
    i=0
    #while i!=grid_size:
    row_index = np.random.randint(0, grid_size)
    column_index = np.random.randint(0, grid_size)
    return row_index, column_index

def set_invalid_indices():
    invalid_indices = np.argwhere(my_grid == 1)
    invalid_indices = np.append(invalid_indices, [[0,0]], axis=0)
    invalid_indices = np.append(invalid_indices, [[grid_size-1, grid_size-1]], axis=0)
    return invalid_indices

def place_ghosts(num_ghosts):
    for i in range(num_ghosts):
        row_ind, col_ind = get_ghost_cell_index()
        print('place ghost coordinates: ' + str(row_ind) + ',' + str(col_ind))
        print('invalid_indices[0][1] : ' + str(invalid_indices[1]))
        if (row_ind, col_ind) in invalid_indices:
            print('Executed if')
            i = i - 1
        else:
            print('Executed else')
            my_grid[row_ind][col_ind] = -1
    return my_grid


my_grid= create_grid(grid_size)
invalid_indices = set_invalid_indices()
print(invalid_indices)
my_grid = place_ghosts(2)
print(my_grid)