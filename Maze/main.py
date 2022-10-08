from calendar import c
from glob import glob
from queue import Empty, PriorityQueue
from types import CellType
import numpy as np
import time

# Variable Declare
my_grid=[]              # To store grid
invalid_indices=[]      # To store indices which are blocked, and where ghost cannot pop up
grid_size=6            # Size of the grid
nr_of_ghosts=8          # Number of the ghosts to conjure

# To create the grid
def create_grid(grid_size, blocked_cell=0.28):
    while True:
        my_grid = np.random.rand(grid_size,grid_size)
        # Populates grid with 1 (Blocked cell) and 0 (Unblocked cell) based on probability given by blocked_cell.        
        my_grid = np.where(my_grid<=blocked_cell, 1, 0)
        # Start position and goal must be unblocked
        my_grid[0][0]=0
        my_grid[grid_size-1, grid_size-1] = 0
        print(my_grid)
        # To check using Depth First Search if grid has a path to reach from the start to the goal
        if (depth_first_search(my_grid, grid_size-1, grid_size-1)):
            break
    return my_grid


# To get randomly generated coordinates to spawn ghosts.
def get_ghost_cell_index():
    while True:
        row_index = np.random.randint(0, grid_size)
        column_index = np.random.randint(0, grid_size)
        print('Random coordinate of Ghost populated : '+str(row_index)+','+str(column_index))
        # Checks if the randomly generated coordinates is not within invalid_indices, and then returns the coordinates. 
        if [row_index,column_index] not in invalid_indices:
            #print('Indices are valid.')
            if row_index==0 and column_index==0:
                print('row_index==0 and column_index==0; invalid_indices : '+ str(invalid_indices))
                continue
            if my_grid[row_index,column_index]==1:
                print('Generated ghost on Blocked wall : '+str(row_index)+','+str(column_index))
            if (depth_first_search(my_grid, row_index, column_index)):
                print('Ghost populated')
                return row_index, column_index
        else:
            print('Invalid Indices found')

# This function will call get_ghost_cell_index() to create ghosts based on number of ghosts received.
def place_ghosts(num_ghosts):
    global invalid_indices
    for i in range(num_ghosts):
        row_ind, col_ind = get_ghost_cell_index()
        my_grid[row_ind][col_ind] = my_grid[row_ind][col_ind] - 10
        print(my_grid)
        # invalid_indices = np.append(invalid_indices, [[row_ind, col_ind]], axis=0)
        # invalid_indices = invalid_indices.tolist()
    #print('Invalid Indices : ' + str(invalid_indices))
    return my_grid   

def set_invalid_indices():
    invalid_indices = np.argwhere(my_grid == 1)
    invalid_indices = np.append(invalid_indices, [[0,0]], axis=0)
    invalid_indices = np.append(invalid_indices, [[grid_size-1, grid_size-1]], axis=0)
    return invalid_indices

# Depth First Search algorithm
def depth_first_search(my_grid, goal_x, goal_y):
    start = [0,0]
    fringe = [start]
    #print('Fringe : '+ str(fringe) + str(type(fringe)))
    #print('Start : '+ str(start) + str(type(start)))
    explored = [start]
    i=0     # can be deleted later, just a safety mechanism to analyze infinite loops
    try:
        while len(fringe) > 0:
            currCell = fringe.pop()
            #print('Fringe : '+str(fringe))
            #print('currcell : ' + str(currCell) + str(type(currCell)))
            if currCell not in explored:            # to solve the issue where code was revisiting already explored cells
                explored.append(currCell)
            #explored.append(nextCell)      # when was this appended? Unsure
            if currCell == [goal_x, goal_y]:
                print('Path exists')
                print('Fringe : '+str(fringe))
                print('Explored Path : '+str(explored))
                return True
            # write code to check each side : LUDR and check if not going array out of bounds
            # Code to select nextCell as Left
            if currCell[1] != 0:
                if (my_grid[currCell[0], (currCell[1] - 1)] % 10) == 0:
                    nextCell = [currCell[0], (currCell[1] - 1)]
                    if nextCell not in explored:
                        fringe.append(nextCell)
                    #print('In first loop')
            # Code to select nextCell as Up
            if currCell[0] != 0:
                if (my_grid[(currCell[0] - 1), currCell[1]] % 10) == 0:
                    nextCell = [(currCell[0] - 1), currCell[1]]
                    if nextCell not in explored:
                        fringe.append(nextCell)
                    #print('In sec loop')
            # Code to select nextCell as Down
            if currCell[0] != (grid_size - 1):
                if (my_grid[currCell[0] + 1, currCell[1]] % 10) == 0:
                    nextCell = [(currCell[0] + 1), currCell[1]]
                    if nextCell not in explored:
                        fringe.append(nextCell)
                    #print('In third loop')
            # Code to select nextCell as Right
            if currCell[1] != (grid_size - 1):
                if (my_grid[currCell[0], currCell[1] + 1] % 10) == 0:
                    nextCell = [currCell[0], (currCell[1] + 1)]
                    if nextCell not in explored:
                        fringe.append(nextCell)
                    #print('In fourth loop')
            if nextCell in explored:
                continue
            if nextCell is None:
                print('nextCell is not defined. Path probably does not exist')
                return False
            explored.append(nextCell)
            #fringe.append(nextCell)        # Dont remember, useful?
            #print('Fringe : '+str(fringe))
            #print('Explored : '+str(explored))
             # can be deleted later, just a safety mechanism to analyze infinite loops
            i=i+1
            if i>200:
                print('Value of i is more than threshold')
                return False
        else:
            print('Path does not exist!')
            return False
    except Exception as error111:
        print('No path present')
        print(error111)
        return False

def h(cell1, cell2):
    x1,y1 = cell1       # Represents cell1 coordinates
    x2,y2 = cell2       # Represents cell2 coordinates
    return abs(x1-x2) + abs(y1-y2)      # Maanhattan distance between cell1 and cell2

def aStar(gridd, start_x=0, start_y=0, goal_x=grid_size-1, goal_y=grid_size-1):
    start=(start_x,start_y)
    gridPos=[]
    a=0
    for i in gridd:
        for j in range(len(i)):
            gridPos.append((a,j))
        a=a+1
    print('gridPos = '+str(gridPos))
    g_score={cell: float('inf') for cell in gridPos}
    g_score[start]=0
    f_score={cell: float('inf') for cell in gridPos}
    f_score[start] = h(start, (goal_x, goal_y))     # Heuristic cost of start cell + g_score of the start cell. Since g_score of start cell is 0, only heuristic cost is assigned
    print('g_score : ' + str(g_score))
    print('f_score : ' + str(f_score))
    openQueue = PriorityQueue()             # Assigned Priority Queue
    openQueue.put(((h(start, (goal_x, goal_y)) + 0), h(start, (goal_x, goal_y)), start))      # Priority Queue contains tuple in order: 1) Heuristic Cost + g_score, 2) Heuristic cost, and 3) start cell
    aPath = {}
    #print('openQueue : '+str(openQueue.get()))
    while not openQueue.empty():
        currCell = openQueue.get()[2]           # Cell value in the Priority Queue is selected as the current cell for this loop
        print('currCell : '+ str(currCell))
        if currCell == (goal_x,goal_y):
            print('currCell reached to goalCell : '+str(currCell))
            break
        # write code to check each side : LUDR and check if not going array out of bounds
        # Code to select nextCell as Left
        if currCell[1] != 0:
            if (my_grid[currCell[0], (currCell[1] - 1)] % 10) == 0:
                nextCell = (currCell[0], (currCell[1] - 1))
                g1 = g_score[currCell] + 1
                f1 = g1 + h(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, h(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
                print('In Left loop')
        # Code to select nextCell as Up
        if currCell[0] != 0:
            if (my_grid[(currCell[0] - 1), currCell[1]] % 10) == 0:
                nextCell = ((currCell[0] - 1), currCell[1])
                g1 = g_score[currCell] + 1
                f1 = g1 + h(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, h(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
                print('In Up loop')
        # Code to select nextCell as Down
        if currCell[0] != (grid_size - 1):
            if (my_grid[currCell[0] + 1, currCell[1]] % 10) == 0:
                nextCell = ((currCell[0] + 1), currCell[1])
                g1 = g_score[currCell] + 1
                f1 = g1 + h(nextCell , (goal_x, goal_y))
                print('f1 : '+str(f1)+'; type:'+ str(type(f1)))
                print('f_score : '+str(f_score)+'; type:'+ str(type(f_score)))
                print(f_score[nextCell])
                print('f_score[nextCell] : '+str(f_score[nextCell])+'; type:'+ str(type(f_score[nextCell])))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, h(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
                print('In Down loop')
        # Code to select nextCell as Right
        if currCell[1] != (grid_size - 1):
            if (my_grid[currCell[0], currCell[1] + 1] % 10) == 0:
                nextCell = (currCell[0], (currCell[1] + 1))
                print(nextCell)
                g1 = g_score[currCell] + 1
                f1 = g1 + h(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, h(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
                print('In Right loop')
    print(openQueue)
    print('aPath : '+str(aPath))
    fwdPath={}
    goal_xy=(goal_x,goal_y)
    while goal_xy!=start:
        fwdPath[aPath[goal_xy]] = goal_xy
        goal_xy = aPath[goal_xy]
    print('fwdPath : '+ str(fwdPath))


def create_env():
    global my_grid, invalid_indices
    my_grid = create_grid(grid_size)
    invalid_indices = set_invalid_indices()
    invalid_indices = invalid_indices.tolist()
    print('Invalid Indices: ' + str(invalid_indices))
    my_grid = place_ghosts(nr_of_ghosts)
    # print(my_grid)

create_env()
aStar(my_grid)