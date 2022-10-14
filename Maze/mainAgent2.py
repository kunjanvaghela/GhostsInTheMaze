import math
from queue import Empty, PriorityQueue
import numpy as np
import time
import csv

# Variable Declare
my_grid=[]              # To store grid, changes when ghost traverses will happen in this directly.
my_grid_original=[]     # To store original grid, with original position of ghosts
invalid_indices=[]      # To store indices which are blocked, and where ghost cannot pop up
grid_size=51            # Size of the grid
nr_of_ghosts=1          # Number of the ghosts to conjure
start_pos = (0,0)
final_pos = (grid_size-1, grid_size-1)
a1Survivability=dict()
getAwayFromGhostRunCheck = 0
agent2PathAndMetric = dict()
agent2For3 = dict()
a2Mazes = dict()        #Dictionary with key as NoOfMazes, value as List of all mazes generated for Agent2

# To create the grid
def create_grid(grid_size, blocked_cell=0.28):
    while True:
        my_grid = np.random.rand(grid_size,grid_size)
        # Populates grid with 1 (Blocked cell) and 0 (Unblocked cell) based on probability given by blocked_cell.        
        my_grid = np.where(my_grid<=blocked_cell, 1, 0)
        # Start position and goal must be unblocked
        my_grid[0][0]=0
        my_grid[grid_size-1, grid_size-1] = 0
        # print(my_grid)
        # To check using Depth First Search if grid has a path to reach from the start to the goal
        if (depth_first_search(my_grid, grid_size-1, grid_size-1)):
            break
    return my_grid


# To get randomly generated coordinates to spawn ghosts.
def get_ghost_cell_index():
    while True:
        row_index = np.random.randint(0, grid_size)
        column_index = np.random.randint(0, grid_size)
        # print('Random coordinate of Ghost populated : '+str(row_index)+','+str(column_index))
        # Checks if the randomly generated coordinates is not within invalid_indices, and then returns the coordinates. 
        if [row_index,column_index] not in invalid_indices:
            #print('Indices are valid.')
            if row_index==0 and column_index==0:
                print('row_index==0 and column_index==0; invalid_indices : '+ str(invalid_indices))
                continue
            if my_grid[row_index,column_index]==1:
                print('Generated ghost on Blocked wall : '+str(row_index)+','+str(column_index))
            if (depth_first_search(my_grid, row_index, column_index)):
                # print('Ghost populated')
                return row_index, column_index
        else:
            # print('Invalid Indices found')
            continue    # Can remove this in final code

# This function will call get_ghost_cell_index() to create ghosts based on number of ghosts received.
def place_ghosts(num_ghosts):
    global invalid_indices
    for i in range(num_ghosts):
        row_ind, col_ind = get_ghost_cell_index()
        my_grid[row_ind][col_ind] = my_grid[row_ind][col_ind] - 10
        # print(my_grid)
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
                # print('Path exists')
                # print('Fringe : '+str(fringe))
                # print('Explored Path : '+str(explored))
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
            # i=i+1
            # if i>5000:
            #     print('Value of i is more than threshold')
            #     return False
        else:
            # print('Path does not exist!')
            return False
    except Exception as errorDFS:
        print('No path present DFS')
        print(errorDFS)
        return False

# For retrieving Path found from BFS Algo
def print_bfs_path(childToParentMapping, goalCell, startCell):
    # childToParentMapping = {(1, 0): {(0, 0)}, (0, 1): {(0, 0)}, (2, 0): {(1, 0)}, (2, 1): {(2, 0)}, (3, 1): {(2, 1)}, (2, 2): {(2, 1)}, (2, 3): {(2, 2)}, (3, 3): {(2, 3)}}
    # goalCell = (3,3)
    curr = goalCell
    path = []
    path.append(goalCell)
    while curr != startCell:
        val = childToParentMapping[curr]
        curr = list(val)[0]
        path.append(curr)
    path.reverse()
    return path

# Breadth First Search algorithm        --> Returns dictionary of path
def breadth_first_search(my_grid, ghostCheck=0, start_x=0, start_y=0, goal_x=grid_size-1, goal_y=grid_size-1):
    print('In BFS')
    start = [start_x, start_y]
    fringe = [start]
    # print('Fringe : '+ str(fringe) + str(type(fringe)))
    # print('Start : '+ str(start) + str(type(start)))
    explored = [start]
    childToParentMap = {}
    # bfs_path = {}
    # pathFwd = {}
    # startTuple = (start_x,start_y)        # KV: commented as not in use
    i=0     # can be deleted later, just a safety mechanism to analyze infinite loops
    # try:
    while len(fringe) > 0:
        currCell = fringe.pop(0)
        # print('Fringe : '+str(fringe))
        # print('currcell : ' + str(currCell) + str(type(currCell)))
        # KV: Introduced below If condition to check for nearest ghost
        if my_grid[currCell[0],currCell[1]] < 0 and ghostCheck == 1:
            return print_bfs_path(childToParentMap, (currCell[0], currCell[1]), (start_x, start_y))
        if currCell not in explored:            # to solve the issue where code was revisiting already explored cells
            explored.append(currCell)
        #explored.append(nextCell)      # when was this appended? Unsure
        if currCell == [goal_x, goal_y]:
            # print('Path exists')
            # print('Final Fringe : '+str(fringe))
            # print('Explored Path : '+str(explored))
            # print('BFS_Path : '+str(bfs_path))
            path_xy = (goal_x, goal_y)
            # while path_xy != startTuple:
                # pathFwd[bfs_path[path_xy]] = path_xy
                # path_xy = bfs_path[path_xy]
            #     print('PathFwd : '+str(pathFwd))
            # return pathFwd
            return print_bfs_path(childToParentMap, (goal_x,goal_y), (start_x, start_y))
        # write code to check each side : LUDR and check if not going array out of bounds
        # Code to select nextCell as Left
        if currCell[1] != 0:
            if (my_grid[currCell[0], (currCell[1] - 1)] % 10) == 0:
                nextCell = [currCell[0], (currCell[1] - 1)]
                if nextCell not in explored:
                    if (nextCell[0],nextCell[1]) in childToParentMap:
                        if childToParentMap[(nextCell[0],nextCell[1])] is not None:
                            childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                            # val = childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                            # childToParentMap[(nextCell[0],nextCell[1])] = val
                        else:
                            value = set()
                            value.add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = value
                    else:
                        value = set()
                        value.add((currCell[0],currCell[1]))
                        childToParentMap[(nextCell[0],nextCell[1])] = value
                    fringe.append(nextCell)
                print('In Left loop')
        # Code to select nextCell as Up
        if currCell[0] != 0:
            if (my_grid[(currCell[0] - 1), currCell[1]] % 10) == 0:
                nextCell = [(currCell[0] - 1), currCell[1]]
                if nextCell not in explored:
                    if (nextCell[0],nextCell[1]) in childToParentMap:
                        if childToParentMap[(nextCell[0],nextCell[1])] is not None:
                            childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                            # val = childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                            # childToParentMap[(nextCell[0],nextCell[1])] = val
                        else:
                            value = set()
                            value.add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = value
                    else:
                        value = set()
                        value.add((currCell[0],currCell[1]))
                        childToParentMap[(nextCell[0],nextCell[1])] = value
                    fringe.append(nextCell)
                print('In Up loop')
        # Code to select nextCell as Down
        if currCell[0] != (grid_size - 1):
            if (my_grid[currCell[0] + 1, currCell[1]] % 10) == 0:
                nextCell = [(currCell[0] + 1), currCell[1]]
                if nextCell not in explored:
                    if (nextCell[0],nextCell[1]) in childToParentMap:
                        if childToParentMap[(nextCell[0],nextCell[1])] is not None:
                            childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                            # val = childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                            # childToParentMap[(nextCell[0],nextCell[1])] = val
                        else:
                            value = set()
                            value.add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = value
                    else:
                        value = set()
                        value.add((currCell[0],currCell[1]))
                        childToParentMap[(nextCell[0],nextCell[1])] = value
                    fringe.append(nextCell)
                print('In Down loop')
        # Code to select nextCell as Right
        if currCell[1] != (grid_size - 1):
            if (my_grid[currCell[0], currCell[1] + 1] % 10) == 0:
                nextCell = [currCell[0], (currCell[1] + 1)]
                if nextCell not in explored:
                    if (nextCell[0],nextCell[1]) in childToParentMap:
                        if childToParentMap[(nextCell[0],nextCell[1])] is not None:
                            childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                            # val = childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                            # childToParentMap[(nextCell[0],nextCell[1])] = val
                        else:
                            value = set()
                            value.add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = value
                    else:
                        value = set()
                        value.add((currCell[0],currCell[1]))
                        childToParentMap[(nextCell[0],nextCell[1])] = value
                    fringe.append(nextCell)
                print('In Right loop')
        # print('Fringe : '+str(fringe))
        # print('Explored : '+str(explored))
        # print('BFS Path : '+str(bfs_path))
        if nextCell in explored:
            print('if nextCell in explored Executed. nextCell : '+str(nextCell))
            continue
        if nextCell is None:
            print('nextCell is not defined. Path probably does not exist')
            return print_bfs_path(childToParentMap, (goal_x,goal_y), (start_x, start_y))
            # return pathFwd
        explored.append(nextCell)
        # bfs_path[tuple(nextCell)] = tuple(currCell)
        #fringe.append(nextCell)        # Dont remember, useful?
        # print('Fringe : '+str(fringe))
        # print('Explored : '+str(explored))
        # print('BFS Path : '+str(bfs_path))
        # can be deleted later, just a safety mechanism to analyze infinite loops
        i=i+1
        print("VAL" + str(i))
        if i>5000:
            print('Value of i is more than threshold')
            # return pathFwd
            return print_bfs_path(childToParentMap, (goal_x,goal_y), (start_x, start_y))
    else:
        print('Path does not exist!')
        return {}
    # except Exception as error111:
    #     print('No path present')
    #     print(error111)
    #     return pathFwd


# Heuristic of Manhattan Distance
def h(cell1, cell2):
    x1,y1 = cell1       # Represents cell1 coordinates
    x2,y2 = cell2       # Represents cell2 coordinates
    return abs(x1-x2) + abs(y1-y2)      # Maanhattan distance between cell1 and cell2

# A Star Algorithm with Heuristic of Manhattan Distance     -- Returns Forward Path determined as part of the Algo in the grid
def aStar(gridd, ghost_check=0, start_x=0, start_y=0, goal_x=grid_size-1, goal_y=grid_size-1):
    start=(start_x,start_y)
    gridPos=[]
    a=0
    for i in gridd:         # To get grid vertices in a list
        for j in range(len(i)):
            gridPos.append((a,j))
        a=a+1
    # print('gridPos = '+str(gridPos))
    g_score={cell: float('inf') for cell in gridPos}
    g_score[start]=0
    f_score={cell: float('inf') for cell in gridPos}
    f_score[start] = h(start, (goal_x, goal_y))     # Heuristic cost of start cell + g_score of the start cell. Since g_score of start cell is 0, only heuristic cost is assigned
    # print('g_score : ' + str(g_score))
    # print('f_score : ' + str(f_score))
    openQueue = PriorityQueue()             # Assigned Priority Queue
    openQueue.put(((h(start, (goal_x, goal_y)) + 0), h(start, (goal_x, goal_y)), start))      # Priority Queue contains tuple in order: 1) Heuristic Cost + g_score, 2) Heuristic cost, and 3) start cell
    aPath = {}
    #print('openQueue : '+str(openQueue.get()))
    while not openQueue.empty():
        currCell = openQueue.get()[2]           # Cell value in the Priority Queue is selected as the current cell for this loop
        # print('currCell : '+ str(currCell))
        if currCell == (goal_x,goal_y):
            # print('currCell reached to goalCell : '+str(currCell))
            break
        # write code to check each side : LUDR and check if not going array out of bounds
        # Code to select nextCell as Left
        if currCell[1] != 0:
            # ghost_check=0 denotes A Star algo will bypass ghosts into its check, and ghost_check=1 denotes that A Star will consider only open cells, that is will not consider ghost cells in its run
            if ((my_grid[currCell[0], (currCell[1] - 1)] % 10) == 0 and ghost_check==0) or ((my_grid[currCell[0], (currCell[1])]) == 0 and ghost_check==1):
                nextCell = (currCell[0], (currCell[1] - 1))
                g1 = g_score[currCell] + 1
                f1 = g1 + h(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, h(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
                # print('In Left loop')
        # Code to select nextCell as Up
        if currCell[0] != 0:
            if ((my_grid[(currCell[0] - 1), currCell[1]] % 10) == 0 and ghost_check==0) or ((my_grid[(currCell[0] - 1), currCell[1]]) == 0 and ghost_check==1):
                nextCell = ((currCell[0] - 1), currCell[1])
                g1 = g_score[currCell] + 1
                f1 = g1 + h(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, h(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
                # print('In Up loop')
        # Code to select nextCell as Down
        if currCell[0] != (grid_size - 1):
            if ((my_grid[currCell[0] + 1, currCell[1]] % 10) == 0 and ghost_check==0) or ((my_grid[currCell[0] + 1, currCell[1]]) == 0 and ghost_check==1):
                nextCell = ((currCell[0] + 1), currCell[1])
                g1 = g_score[currCell] + 1
                f1 = g1 + h(nextCell , (goal_x, goal_y))
                # print('f1 : '+str(f1)+'; type:'+ str(type(f1)))
                # print('f_score : '+str(f_score)+'; type:'+ str(type(f_score)))
                # print(f_score[nextCell])
                # print('f_score[nextCell] : '+str(f_score[nextCell])+'; type:'+ str(type(f_score[nextCell])))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, h(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
                # print('In Down loop')
        # Code to select nextCell as Right
        if currCell[1] != (grid_size - 1):
            if ((my_grid[currCell[0], currCell[1] + 1] % 10) == 0 and ghost_check==0) or ((my_grid[currCell[0], currCell[1] + 1]) == 0 and ghost_check==1):
                nextCell = (currCell[0], (currCell[1] + 1))
                # print(nextCell)
                g1 = g_score[currCell] + 1
                f1 = g1 + h(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, h(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
                # print('In Right loop')
    print('aPath : '+str(aPath))
    fwdPath={}
    goal_xy=(goal_x,goal_y)
    try:
        while goal_xy!=start:
            fwdPath[aPath[goal_xy]] = goal_xy
            goal_xy = aPath[goal_xy]
        print('fwdPath : '+ str(fwdPath))
        return fwdPath
    except Exception as errorAStar:
        print('No AStar path present')
        print(errorAStar)
        return {}


def create_env():
    global my_grid, invalid_indices, a2Mazes
    my_grid = create_grid(grid_size)
    if nr_of_ghosts in a2Mazes:
        a2Mazes[nr_of_ghosts].append(my_grid)
    else:
        a2Mazes[nr_of_ghosts] = [my_grid]
    invalid_indices = set_invalid_indices()
    invalid_indices = invalid_indices.tolist()
    # print('Invalid Indices: ' + str(invalid_indices))
    my_grid = place_ghosts(nr_of_ghosts)
    # print(my_grid)

#MANAN-START
# Method for Random movements for ghosts, 
# It accounts for Ghosts position at call [spawn if Timestamp=0] considers the probability of moving to LUDR
# Or Stay at the same place.

# Kunjan Edits:
#   1) Changing argument - removing my_grid as argument and implementing global my_grid to avoid copying my_grid after ghost movement.
#   2) Changed hardcoded 3 to 'gridsize-1'
#   3) Possible if-else error. Changing to if-elif-else:
# def ghostmovement(my_grid):
#MANAN-START
# Method for Random movements for ghosts, 
# It accounts for Ghosts position at call [spawn if Timestamp=0] considers the probability of moving to LUDR
# Or Stay at the same place.

def ghostmovement(my_grid):
    ghostPositionList=np.argwhere(my_grid < 0)
    print('ghostPositionList:12312123123::::',(ghostPositionList))

    for index in ghostPositionList:
        no_of_ghosts=(math.ceil(abs(my_grid[index[0],index[1]]/10)))
        while no_of_ghosts>1:
            ghostPositionList=np.append(ghostPositionList,index)
            no_of_ghosts=no_of_ghosts-1
    print('ghostPositionList:345345345345::::',(ghostPositionList))
    ghostPositionList=ghostPositionList.reshape((ghostPositionList.size)//2,2)

    for list in ghostPositionList:              #for element in list:
            #L=(1) U=(2) D=(3) R=(4)
            print('GHOST POSITION',list) 
            if(list[0]==0 and list[1]==0): #START :CANT GO UP AND LEFT
                    direction=np.random.choice([3,4])
                    #print('5')
            elif(list[0]==0 and list[1]==(grid_size - 1)): #RIGHT TOP :CANT GO UP AND RIGHT
                    direction=np.random.choice([1,3])
                    #print('6')
            elif(list[0]==(grid_size - 1) and list[1]==0): #BOTTOM LEFT :CANT GO DOWN AND LEFT
                    direction=np.random.choice([2,4])
                    #print('7')
            elif(list[1]==(grid_size - 1) and list[1]==(grid_size - 1)): #GOAL :CANT GO DOWN AND RIGHT
                    direction=np.random.choice([1,2])
                    #print('8')
            elif(list[1]==0):
                    direction=np.random.choice([2,3,4])     # If ghost is on the left most cell, can only go Up, Down and Right
                    #print('1')
            elif(list[0]==0):
                    direction=np.random.choice([1,3,4])     # If ghost is on the top most cell, can only go Left, Down and Right
                    #print('2')
            elif(list[0]==(grid_size - 1)):
                    direction=np.random.choice([1,2,4])     # If ghost is on the bottom most cell, can only go Left, Up and Right
                    #print('3')
            elif(list[1]==(grid_size - 1)):
                    direction=np.random.choice([1,2,3])     # If ghost is on the right most cell, can only go Left, Up and Down
                    #print('4')
            else:
                direction=np.random.randint(low=1, high=5)
                #print('9')
            
            print('Random Direction:L=(1) U=(2) D=(3) R=(4)::',direction)
            
            
            #L=(1) U=(2) D=(3) R=(4)
            if direction==1 : #GO-LEFT
                           
                if (my_grid[list[0]][list[1]-1]==0 or my_grid[list[0]][list[1]-1]%10==0) and (list[1]>0) : #OPEN CELL
                    #print('LEFT',my_grid[list[0]][list[1]-1]) 
                    my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                    my_grid[list[0]][list[1]-1]=my_grid[list[0]][list[1]-1]-10
                    list[1]=list[1]-1
                elif (my_grid[list[0]][list[1]-1]==1 or my_grid[list[0]][list[1]-1]%10!=0) and (list[1]>0): #BLOCKED CELL
                    #print('LEFT',my_grid[list[0]][list[1]-1])
                    directionIfBlocked=np.random.randint(low=0, high=2) #0=Stay, 1 =Go inside the Block
                    if directionIfBlocked==1:
                        print('MOVE TO BLOCKED')
                        my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                        my_grid[list[0]][list[1]-1]=my_grid[list[0]][list[1]-1]-10
                        list[1]=list[1]-1
                    else: print('STAY @ CURRENT')#STAY -NO CHANGE IF WALL IS BLOCKED
                    
            elif direction==2 :#GO-UP
                if (my_grid[list[0]-1][list[1]]==0 or my_grid[list[0]-1][list[1]]%10==0) and (list[0]>0) : #OPEN CELL
                    #print('UP',my_grid[list[0]-1][list[1]])
                    my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                    my_grid[list[0]-1][list[1]]=my_grid[list[0]-1][list[1]]-10
                    list[0]=list[0]-1
                elif (my_grid[list[0]-1][list[1]]==1 or my_grid[list[0]-1][list[1]]%10!=0) and (list[0]>0): #BLOCKED CELL
                    #print('UP',my_grid[list[0]-1][list[1]])
                    directionIfBlocked=np.random.randint(low=0, high=2) #0=Stay, 1 =Go inside the Block
                    if directionIfBlocked==1:
                        print('MOVE TO BLOCKED')
                        my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                        my_grid[list[0]-1][list[1]]=my_grid[list[0]-1][list[1]]-10
                        list[0]=list[0]-1
                    else: print('STAY @ CURRENT')#STAY -NO CHANGE IF WALL IS BLOCKED

            # KV: Check for possible bugs as written in comment below - Ref:Bug01
            elif direction==3 : #GO-DOWN
                if (my_grid[list[0]+1][list[1]]==0 or my_grid[list[0]+1][list[1]]%10==0) and (list[0]<grid_size) : #OPEN CELL   #KV: Changed from 'my_grid[list[0]][list[1]+1]==0' to 'my_grid[list[0]+1][list[1]]==0'  - Ref:Bug01
                    #print('DOWN',my_grid[list[0]+1][list[1]])
                    my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                    my_grid[list[0]+1][list[1]]=my_grid[list[0]+1][list[1]]-10
                    list[0]=list[0]+1
                elif (my_grid[list[0]+1][list[1]]==1 or my_grid[list[0]+1][list[1]]%10!=0) and (list[0]<grid_size): #BLOCKED CELL   #KV: Changed from 'my_grid[list[0]][list[1]+1]==0' to 'my_grid[list[0]+1][list[1]]==0' - Ref:Bug01
                    #print('DOWN',my_grid[list[0]+1][list[1]])
                    directionIfBlocked=np.random.randint(low=0, high=2) #0=Stay, 1 =Go inside the Block
                    if directionIfBlocked==1:
                        print('MOVE TO BLOCKED')
                        my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                        my_grid[list[0]+1][list[1]]=my_grid[list[0]+1][list[1]]-10
                        list[0]=list[0]+1
                    else: print('STAY @ CURRENT')#STAY -NO CHANGE IF WALL IS BLOCKED


            else :#GO-RIGHT 
                if (my_grid[list[0]][list[1]+1]==0 or my_grid[list[0]][list[1]+1]%10==0) and (list[1]<grid_size) : #OPEN CELL
                    #print('RIGHT',my_grid[list[0]][list[1]+1])
                    my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                    my_grid[list[0]][list[1]+1]=my_grid[list[0]][list[1]+1]-10
                    list[1]=list[1]+1
                elif (my_grid[list[0]][list[1]+1]==1 or my_grid[list[0]][list[1]+1]%10!=0) and (list[1]<grid_size): #BLOCKED CELL
                    directionIfBlocked=np.random.randint(low=0, high=2) #0=Stay, 1 =Go inside the Block
                    if directionIfBlocked==1:
                        print('MOVE TO BLOCKED')
                        my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                        my_grid[list[0]][list[1]+1]=my_grid[list[0]][list[1]+1]-10
                        list[1]=list[1]+1
                    else: print('STAY @ CURRENT')#STAY -NO CHANGE IF WALL IS BLOCKED
    print('--------------------')        

    print('GRID MOVEMENT',my_grid)

    #MANAN-END

def findDirection(currCell, nextCellPos):        # --> Returns direction of the nextCell from current cell in integers: L:1 U:2 D:3 R:4:
    if nextCellPos[0] == (currCell[0] + 1):     # Next Cell lies in Down direction
        direction = 3
    elif nextCellPos[0] == (currCell[0] - 1):     # Next Cell lies in Up direction
        direction = 2
    elif nextCellPos[1] == (currCell[1] + 1):     # Next Cell lies in Right direction
        direction = 4
    elif nextCellPos[1] == (currCell[1] - 1):     # Next Cell lies in Left direction
        direction = 1
    return direction

def agentOneTraversal():
    a1 = start_pos          # Agent 1 coordinates denoted by this variable
    aStarPathDetermined = aStar(my_grid)
    print('aStarPathDetermined for Agent 1 : '+str(aStarPathDetermined))
    while (a1 != final_pos):
        nextLocA1 = aStarPathDetermined[a1]
        ghostmovement(my_grid)
        print('Agent 1 Location : ' + str(nextLocA1))
        if my_grid[nextLocA1] == 1:
            print('Agent is in Blocked Cell. Some Serious Error !!!!!!!!!!!!!!')
        if my_grid[nextLocA1] != 0:
            print('Agent not in Open Cell. Ghost Encountered ????????????')
            print(my_grid[nextLocA1])
            return False
        a1 = nextLocA1
        # break
    return True

def getAwayFromGhost(currCell, nearestGhostPos):        # --> Returns tuple value of nextPosition to take
    validDirections = [1,2,3,4]
    invalidDirections = getInvalidAdjacentDirectionsToGoTo(currCell)            # Get the cells which are invalid as they lie outside of environment
    for i in invalidDirections:
        validDirections.remove(i)       # Removing the invalid directions from the possible movement positions
    ghostInDirection = findDirection(currCell, nearestGhostPos)
    validDirections.remove(ghostInDirection)
    print('validDirections after removing invalid indices '+str(validDirections))
    placeholderForRemovingValidDirections = validDirections[:]
    for i in placeholderForRemovingValidDirections:
        nextCell = getNextCoordinatesToMoveTo(currCell, i)
        print('Checking direction '+str(i)+', checking nextCell '+str(nextCell)+ ' using checkForOpenPosition function')
        if (not checkForOpenPosition(nextCell)):        # checkForOpenPosition(nextCell) will return False if the cell is blocked.
            print('Removing direction '+str(i))
            validDirections.remove(i)
            print('After removing, validDirection list : '+str(validDirections))
    if validDirections == []:
        print('No valid direction available to run away from the ghost. Hence agent will stay at same cell.')
        return currCell
    else:
        direction = np.random.choice(validDirections)
        nextCell = getNextCoordinatesToMoveTo(currCell, direction)
        print('From valid Directions '+ str(direction) +' in getAwayFromGhost(), selected '+str(nextCell))
        return nextCell

    global getAwayFromGhostRunCheck
    if nearestGhostPos[0] == (currCell[0] + 1):     # Ghost is in down direction of Agent 2
        if currCell[0] == 0 and currCell[1] == (grid_size-1):   #Agent cant go to the right, only possible option: go left
            direction = 1
            # nextCell = (currCell[0], currCell[1]-1)
        elif currCell[0] == 0 and currCell[1] == 0:   # Agent cant go to the left, only possible option: go right
            direction = 4
            # nextCell = (currCell[0], currCell[1]+1)
        elif currCell[0] == 0:                      # Agent can go left or right
            direction = np.random.choice([1,4])
        elif currCell[1] == 0:  # Agent can go up and right
            direction = np.random.choice([2,4])
        elif currCell[1] == (grid_size-1): # Agent can go left and up
            direction = np.random.choice([1,2])
        else:                   # Agent can go Left, Up and Right
            direction = np.random.choice([1,2,4])
            # nextCell = (currCell[0], currCell[1]+direction)
    elif nearestGhostPos[0] == (currCell[0] - 1):     # Ghost is in up direction of Agent 2
        if currCell[0] == (grid_size-1) and currCell[1] == (grid_size-1):   #Agent cant go to the right, only possible option: go left
            direction = 1
        elif currCell[0] == (grid_size-1) and currCell[1] == 0:   #Agent cant go to the left, only possible option: go right
            direction = 4
        elif currCell[0] == (grid_size-1):                      # Agent can go left or right
            direction = np.random.choice([1,4])
        elif currCell[1] == 0:  # Agent can go left and down
            direction = np.random.choice([3,4])
        elif currCell[1] == (grid_size-1): # Agent can go right and down
            direction = np.random.choice([1,3])
        else:
            direction = np.random.choice([1,3,4])
    elif nearestGhostPos[1] == (currCell[1] + 1):     # Ghost is in right direction of Agent 2
        if currCell[0] == 0 and currCell[1] == 0:   #Agent cant go to the left, only possible option: go down
            direction = 3
            # nextCell = (currCell[0], currCell[1]-1)
        elif currCell[0] == (grid_size-1) and currCell[1] == 0:   #Agent cant go down/left, only possible option: go up
            direction = 2
            # nextCell = (currCell[0], currCell[1]+1)
        elif currCell[1] == 0:                      # Agent can go up and down
            direction = np.random.choice([2,3])
        elif currCell[0] == 0:  # Agent can go left and down
            direction = np.random.choice([1,3])
        elif currCell[0] == (grid_size-1): # Agent can go left and up
            direction = np.random.choice([1,2])
        else:                   # Agent can go Left, Up and Down
            direction = np.random.choice([1,2,3])
            # nextCell = (currCell[0], currCell[1]+direction)
    elif nearestGhostPos[1] == (currCell[1] - 1):     # Ghost is in left direction of Agent 2
        if currCell[0] == 0 and currCell[1] == (grid_size-1):   #Agent cant go to the right and up, only possible option: go down
            direction = 3
            # nextCell = (currCell[0], currCell[1]-1)
        elif currCell[0] == (grid_size-1) and currCell[1] == (grid_size-1):   #Agent cant go down/right, only possible option: go up
            direction = 2
            # nextCell = (currCell[0], currCell[1]+1)
        elif currCell[1] == (grid_size-1):                      # Agent can go up and down
            direction = np.random.choice([2,3])
        elif currCell[0] == 0:  # Agent can go right and down
            direction = np.random.choice([3,4])
        elif currCell[0] == (grid_size-1): # Agent can go right and up
            direction = np.random.choice([2,4])
        else:                   # Agent can go Up, Down and Right
            direction = np.random.choice([4,2,3])
    if direction==1:            # Go Left
        nextCell = (currCell[0], currCell[1]-1)
    elif direction==2:            # Go Up
        nextCell = (currCell[0]-1, currCell[1])
    elif direction==3:            # Go Down
        nextCell = (currCell[0]+1, currCell[1])
    else:            # Go Right
        nextCell = (currCell[0], currCell[1]+1)

    if my_grid[nextCell[0]][nextCell[1]] != 0:
        getAwayFromGhostRunCheck+=1
        if getAwayFromGhostRunCheck > 10:
            return []
        getAwayFromGhost(currCell, nearestGhostPos)
    else:
        getAwayFromGhostRunCheck=0

    return nextCell

    #L=(1) U=(2) D=(3) R=(4)


def agentTwoTraversal():
    global agent2PathAndMetric
    a2 = start_pos          # Agent 1 coordinates denoted by this variable
    nearestGhostPosition = tuple()
    while (a2 != final_pos):
        aStarPathDetermined = aStar(my_grid, 1, a2[0], a2[1])
        print('aStarPathDetermined for Agent 2 : '+str(aStarPathDetermined))
        # Can move Agent 2 movement after ghost movement?
        if len(aStarPathDetermined) == 0:
            print('A Star path not present. Need to check for nearest ghost')
            nearestGhostPath = breadth_first_search(my_grid, 1, a2[0], a2[1])       # Returns list of path to ghost
            print('nearestGhostPath : ' + str(nearestGhostPath))
            if len(nearestGhostPath) == 1:
                return False
            nearestGhostPosition = nearestGhostPath[1]      # Checking the second path element
            print('nearestGhostPosition : ')
            print(nearestGhostPosition)
            nextLocA2 = getAwayFromGhost(a2, nearestGhostPosition)      # Passes current Agent 2 location and the next Path that Agent will have to take to get to the nearest ghost
            if nextLocA2 == a2:                                 # Included to go towards ghost if there are no other paths present. Implemented this as Agent 2 cannot stay at same location
                nextLocA2=nearestGhostPosition
            if not nextLocA2 or my_grid[nextLocA2[0],nextLocA2[1]] < 0:
                print('Agent is in Blocked Cell. Some Serious Error !!!!!!!!!!!!!!')
                return False
        else:
            nextLocA2 = aStarPathDetermined[a2]
        # Storing data of Agent 2 in path
        currCellToNextCellDirection = findDirection(a2, nextLocA2)
        # if (a2[0], a2[1], currCellToNextCellDirection) in agent2PathAndMetric:
        agent2PathAndMetric[(a2[0], a2[1], currCellToNextCellDirection)] = False

        # Movement of ghost initiated
        ghostmovement(my_grid)
        print(nextLocA2)
        if my_grid[nextLocA2] == 1:
            print('Agent is in Blocked Cell. Some Serious Error !!!!!!!!!!!!!!')
        if my_grid[nextLocA2] != 0:
            print('Agent not in Open Cell. Ghost Encountered ????????????')
            print(my_grid[nextLocA2])
            return False
        a2 = nextLocA2
        print(my_grid)
        # break
    return True


def writeAg2MetricForAg3(mazeNo, nr_of_ghost, agent2Dict, outputFileName):
    #Metric: No. of ghosts, MazeNo, position[0], position[1], direction, wins, total
    global agent2For3
    masterKey = ()
    masterVal = [0,0]
    for key in agent2Dict.keys():
        masterKey = (nr_of_ghost, key[0], key[1],key[2])
        val = agent2Dict[key]
        if masterKey in agent2For3:
            currentMasterValue = agent2For3[masterKey]
            if val:
                currentMasterValue[0] += 1
            currentMasterValue[1] += 1
            agent2For3[masterKey] = currentMasterValue
        else:
            if val:
                masterVal[0] = 1
            masterVal[1] = 1
            agent2For3[masterKey] = masterVal
    
    masterKeys = agent2For3.keys()
    toWriteData = []
    for key in masterKeys:
        a1 = list(key)
        a1 += list(agent2For3[key])
        toWriteData.append(a1)  #No of ghosts, position[0], position[1], survivability, countOfTurns

    print(toWriteData)
    with open(outputFileName, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(toWriteData)


    file.close()

def checkForOpenPosition(cellToCheck, onlyGhostChecks = 0):             # Returns True if the passed cell is unblocked (that is does not contain ghosts or ghost in blocked cell)
    if (cellToCheck[0] >=0 and cellToCheck[0] < grid_size) and (cellToCheck[1] >=0 and cellToCheck[1] <grid_size):
        if (my_grid[cellToCheck[0],cellToCheck[1]] != 0) and onlyGhostChecks == 0:
            return False
        elif (my_grid[cellToCheck[0],cellToCheck[1]] < 0) and onlyGhostChecks == 1:
            return False
    return True         # To return True if passed cell is invalid, like if it lies outside the boundary of matrix. This cell will not have ghost.

def checkOpenCellsForAgentFour(currPosition, determinedPath, visibility):       # Checks if there are any ghosts in determinedPath till next visibility path (+1 more depth)
    for i in range(visibility):
        if currPosition in determinedPath:
            nextPosition = determinedPath[currPosition]
            if (not checkForOpenPosition(nextPosition, 1)):
                return True
            elif (not checkForOpenPosition((nextPosition[0]+1, nextPosition[1]), 1)):
                return True
            elif (not checkForOpenPosition((nextPosition[0]-1, nextPosition[1]), 1)):
                return True
            elif (not checkForOpenPosition((nextPosition[0], nextPosition[1]-1), 1)):
                return True
            elif (not checkForOpenPosition((nextPosition[0], nextPosition[1]+1), 1)):
                return True
            currPosition = nextPosition
    return False

def checkAdjacentCoordinatesForGhost(currCell):                 # Checks if adjacent cells to the current cell contains ghost (and also blocked cells), if yes, returns the blocked positions
    ghostPositionsNearby = []           # This list will contain positions of the nearby ghost, in adjacent cell
    if (not checkForOpenPosition((currCell[0]+1, currCell[1]), 1)):
        ghostPositionsNearby.append((currCell[0]+1, currCell[1]))
    elif (not checkForOpenPosition((currCell[0]-1, currCell[1]), 1)):
        ghostPositionsNearby.append((currCell[0]-1, currCell[1]))
    elif (not checkForOpenPosition((currCell[0], currCell[1]-1), 1)):
        ghostPositionsNearby.append((currCell[0], currCell[1]-1))
    elif (not checkForOpenPosition((currCell[0], currCell[1]+1), 1)):
        ghostPositionsNearby.append((currCell[0], currCell[1]+1))
    return ghostPositionsNearby

def getNextCoordinatesToMoveTo(currCell, direction):
    nextCell = currCell
    if direction==1:            # Go Left
        nextCell = (currCell[0], currCell[1]-1)
    elif direction==2:            # Go Up
        nextCell = (currCell[0]-1, currCell[1])
    elif direction==3:            # Go Down
        nextCell = (currCell[0]+1, currCell[1])
    elif direction == 4:            # Go Right
        nextCell = (currCell[0], currCell[1]+1)
    else:
        print('Weird condition encountered in getNextCoordinatesToMoveTo')
    return nextCell

def getInvalidAdjacentDirectionsToGoTo(currcell):
    directions=[]        # LUDR
    if currcell[0] == 0:           # Top line, so cant go Up
        directions.append(2)
    if currcell[0] == (grid_size-1):    # Bottom line, so cant go Down
        directions.append(3)
    if currcell[1] == 0:        # Left most line, so cant go left
        directions.append(1)
    if currcell[1] == (grid_size-1):    # Right most line, so cant go right
        directions.append(4)
    return directions
    

def agent3Traversal(nr_of_ghosts):
    a3 = start_pos          # Agent 3 coordinates denoted by this variable.
    #Store each position taken by Agent3 in dict.
    #Read the right rows from CSV file.
    #Take one with the maximum survivability.
    #If again coming on this path, take the random move.
    #If no data for a given cell, run Agent 2's strategy only once.
    a3CellExplored = [start_pos]
    # with open('eggs.csv', newline='') as csvfile:
    #     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    #     for row in spamreader:
    #         print(', '.join(row))

    # nearestGhostPosition = tuple()
    # while (a3 != final_pos):
    #     aStarPathDetermined = aStar(my_grid, 1, a2[0], a2[1])
    #     print('aStarPathDetermined for Agent 2 : '+str(aStarPathDetermined))
    #     # Can move Agent 2 movement after ghost movement?
    #     if len(aStarPathDetermined) == 0:
    #         print('A Star path not present. Need to check for nearest ghost')
    #         nearestGhostPath = breadth_first_search(my_grid, 1, a2[0], a2[1])       # Returns list of path to ghost
    #         print('nearestGhostPath : ' + str(nearestGhostPath))
    #         if len(nearestGhostPath) == 1:
    #             return False
    #         nearestGhostPosition = nearestGhostPath[1]      # Checking the second path element
    #         print('nearestGhostPosition : ')
    #         print(nearestGhostPosition)
    #         nextLocA2 = getAwayFromGhost(a2, nearestGhostPosition)      # Passes current Agent 2 location and the next Path that Agent will have to take to get to the nearest ghost
    #         if not nextLocA2 or my_grid[nextLocA2[0],nextLocA2[1]] < 0:
    #             print('Agent is in Blocked Cell. Some Serious Error !!!!!!!!!!!!!!')
    #             return False
    #     else:
    #         nextLocA2 = aStarPathDetermined[a2]
    #     # Storing data of Agent 2 in path
    #     currCellToNextCellDirection = findDirection(a2, nextLocA2)
    #     # if (a2[0], a2[1], currCellToNextCellDirection) in agent2PathAndMetric:
    #     agent2PathAndMetric[(a2[0], a2[1], currCellToNextCellDirection)] = False

    #     # Movement of ghost initiated
    #     ghostmovement(my_grid)
    #     print(nextLocA2)
    #     if my_grid[nextLocA2] == 1:
    #         print('Agent is in Blocked Cell. Some Serious Error !!!!!!!!!!!!!!')
    #     if my_grid[nextLocA2] != 0:
    #         print('Agent not in Open Cell. Ghost Encountered ????????????')
    #         print(my_grid[nextLocA2])
    #         return False
    #     a2 = nextLocA2
    #     print(my_grid)
    #     # break
    # return True


import sys

if __name__=='__main__':

    lenOfArgs = len(sys.argv)
    input_no_of_ghosts = int(sys.argv[1])
    outputFileName = "a2DataFor3_" + str(input_no_of_ghosts) + ".csv"

    create_env()
    print('Original Grid generated : ')
    print(my_grid)
    my_grid_original = my_grid                  # To have a backup of original grid
    print('Copied above grid to my_grid_original :')

    # Agent 1 Traversing
    # agentOneReached = agentOneTraversal()
    # print('Agent One Reached : ' + str(agentOneReached))
    # print(my_grid)

    # Agent 1 Traversing
    # nr_of_ghosts=1
    # while True:                 # Loop to check till what number can the Agent survive
    #     for i in range(1,5):
    #         create_env()            # New Env everytime
    #         agentOneReached = agentOneTraversal()       # Agent 1 Traversal path with A* Algorithm
    #         print('Agent One Reached : ' + str(agentOneReached))
    #         if nr_of_ghosts in a1Survivability:         # Dictionary containing results of Agent 1's Traversal success
    #             a1Survivability[nr_of_ghosts].append(agentOneReached)
    #         else:
    #             a1Survivability[nr_of_ghosts] = [agentOneReached]
    #         print(my_grid)
    #     print(a1Survivability)
    #     if True not in a1Survivability[nr_of_ghosts]:       # Loop must break if Agent 1's survivability is no more.
    #         break
    #     if nr_of_ghosts>30:         # A check to limit how many times loop will go on, safety mechanism
    #         break
    #     nr_of_ghosts+=1


    #Metric:
    #AgentNo, RunNo, No. of ghosts, MazeNo, Win/Loss, Time, Future-(No. of steps)
    a2Survivability = {}
    a2Data = []
    a2RunNo = 1
    nr_of_ghosts = input_no_of_ghosts
    while True:                 # Loop to check till what number can the Agent survive
        create_env()            # New Env everytime
        for t in range(1,25):   # For each nr_of_ghost, each grid configuration, running agent 25 times.
            startTime = time.time()
            agentTwoReached = agentTwoTraversal()
            print('Agent Two Reached : ' + str(agentTwoReached))
            if agentTwoReached:
                val = True
                for keys in agent2PathAndMetric:
                    agent2PathAndMetric[keys] = True
            else:
                val = False
            if nr_of_ghosts in a2Survivability:         # Dictionary containing results of Agent 2's Traversal success
                a2Survivability[nr_of_ghosts].append(val)
            else:
                a2Survivability[nr_of_ghosts] = [val]
            executionTime = time.time() - startTime
            a2Data.append(["A2", a2RunNo, nr_of_ghosts, val, executionTime])
            a2RunNo+=1
            print(my_grid)
            print('agent2PathAndMetric : '+ str(agent2PathAndMetric))
            writeAg2MetricForAg3(0, nr_of_ghosts, agent2PathAndMetric, outputFileName)
            agent2PathAndMetric = {}
        print(a2Survivability)

        output_file_agent2 = "a2Data_" + str(nr_of_ghosts) + ".csv"
        with open(output_file_agent2, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(a2Data)
        
        file.close()

        break

        # if True not in a2Survivability[nr_of_ghosts]:       # Loop must break if Agent 2's survivability is no more.
        #     break
        # if nr_of_ghosts>100:         # A check to limit how many times loop will go on, safety mechanism
        #     break
        # nr_of_ghosts+=1


    # print('----------------- BFS Output -----------------')
    # print(breadth_first_search(my_grid))
    # aStar(my_grid)