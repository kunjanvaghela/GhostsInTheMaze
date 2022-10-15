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
a1Survivability = dict()
a4Survivability = dict()
a5Survivability = dict()
getAwayFromGhostRunCheck = 0
agent2PathAndMetric = dict()
agent2For3 = dict()
a2Mazes = dict()        #Dictionary with key as NoOfMazes, value as List of all mazes generated for Agent2
a4PathTaken = []        # To check and compare path taken by Agent 4
a5PathTaken = []

# To create the grid
def create_grid(grid_size, blocked_cell=0.28):
    while True:
        my_grid = np.random.rand(grid_size,grid_size)
        # Populates grid with 1 (Blocked cell) and 0 (Unblocked cell) based on probability given by blocked_cell.        
        my_grid = np.where(my_grid<=blocked_cell, 1, 0)
        # Start position and goal must be unblocked
        my_grid[0][0]=0
        my_grid[grid_size-1, grid_size-1] = 0
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
        # invalid_indices = np.append(invalid_indices, [[row_ind, col_ind]], axis=0)
        # invalid_indices = invalid_indices.tolist()
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
    explored = [start]
    i=0     # can be deleted later, just a safety mechanism to analyze infinite loops
    try:
        while len(fringe) > 0:
            currCell = fringe.pop()
            if currCell not in explored:            # to solve the issue where code was revisiting already explored cells
                explored.append(currCell)
            if currCell == [goal_x, goal_y]:
                return True
            # Code to select nextCell as Left
            if currCell[1] != 0:
                if (my_grid[currCell[0], (currCell[1] - 1)] % 10) == 0:
                    nextCell = [currCell[0], (currCell[1] - 1)]
                    if nextCell not in explored:
                        fringe.append(nextCell)
            # Code to select nextCell as Up
            if currCell[0] != 0:
                if (my_grid[(currCell[0] - 1), currCell[1]] % 10) == 0:
                    nextCell = [(currCell[0] - 1), currCell[1]]
                    if nextCell not in explored:
                        fringe.append(nextCell)
            # Code to select nextCell as Down
            if currCell[0] != (grid_size - 1):
                if (my_grid[currCell[0] + 1, currCell[1]] % 10) == 0:
                    nextCell = [(currCell[0] + 1), currCell[1]]
                    if nextCell not in explored:
                        fringe.append(nextCell)
            # Code to select nextCell as Right
            if currCell[1] != (grid_size - 1):
                if (my_grid[currCell[0], currCell[1] + 1] % 10) == 0:
                    nextCell = [currCell[0], (currCell[1] + 1)]
                    if nextCell not in explored:
                        fringe.append(nextCell)
            if nextCell in explored:
                continue
            if nextCell is None:
                print('nextCell is not defined. Path probably does not exist')
                return False
            explored.append(nextCell)
        else:
            return False
    except Exception as errorDFS:
        print('No path present DFS')
        print(errorDFS)
        return False

# For retrieving Path found from BFS Algo
def print_bfs_path(childToParentMapping, goalCell, startCell):
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
    # ghostCheck attribute functionality if set to:
        # 0: Returns path to the goal node (goal_x, goal_y)
        # 1: Returns path till the nearest ghost
    print('In BFS')
    start = [start_x, start_y]
    fringe = [start]
    explored = [start]
    childToParentMap = {}
    i=0     # To restrict BFS condition to go on till long time.
    while len(fringe) > 0:
        currCell = fringe.pop(0)
        # Below If condition will exit if the ghost is encountered. This condition is being used to find the nearest ghost.
        if my_grid[currCell[0],currCell[1]] < 0 and ghostCheck == 1:
            return print_bfs_path(childToParentMap, (currCell[0], currCell[1]), (start_x, start_y))
        if currCell not in explored:            # to solve the issue where code was revisiting already explored cells
            explored.append(currCell)
        if currCell == [goal_x, goal_y]:
            path_xy = (goal_x, goal_y)
            return print_bfs_path(childToParentMap, (goal_x,goal_y), (start_x, start_y))
        # Code to select nextCell as Left
        if currCell[1] != 0:
            if (my_grid[currCell[0], (currCell[1] - 1)] % 10) == 0:
                nextCell = [currCell[0], (currCell[1] - 1)]
                if nextCell not in explored:
                    if (nextCell[0],nextCell[1]) in childToParentMap:
                        if childToParentMap[(nextCell[0],nextCell[1])] is not None:
                            childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                        else:
                            value = set()
                            value.add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = value
                    else:
                        value = set()
                        value.add((currCell[0],currCell[1]))
                        childToParentMap[(nextCell[0],nextCell[1])] = value
                    fringe.append(nextCell)
        # Code to select nextCell as Up
        if currCell[0] != 0:
            if (my_grid[(currCell[0] - 1), currCell[1]] % 10) == 0:
                nextCell = [(currCell[0] - 1), currCell[1]]
                if nextCell not in explored:
                    if (nextCell[0],nextCell[1]) in childToParentMap:
                        if childToParentMap[(nextCell[0],nextCell[1])] is not None:
                            childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                        else:
                            value = set()
                            value.add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = value
                    else:
                        value = set()
                        value.add((currCell[0],currCell[1]))
                        childToParentMap[(nextCell[0],nextCell[1])] = value
                    fringe.append(nextCell)
        # Code to select nextCell as Down
        if currCell[0] != (grid_size - 1):
            if (my_grid[currCell[0] + 1, currCell[1]] % 10) == 0:
                nextCell = [(currCell[0] + 1), currCell[1]]
                if nextCell not in explored:
                    if (nextCell[0],nextCell[1]) in childToParentMap:
                        if childToParentMap[(nextCell[0],nextCell[1])] is not None:
                            childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                        else:
                            value = set()
                            value.add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = value
                    else:
                        value = set()
                        value.add((currCell[0],currCell[1]))
                        childToParentMap[(nextCell[0],nextCell[1])] = value
                    fringe.append(nextCell)
        # Code to select nextCell as Right
        if currCell[1] != (grid_size - 1):
            if (my_grid[currCell[0], currCell[1] + 1] % 10) == 0:
                nextCell = [currCell[0], (currCell[1] + 1)]
                if nextCell not in explored:
                    if (nextCell[0],nextCell[1]) in childToParentMap:
                        if childToParentMap[(nextCell[0],nextCell[1])] is not None:
                            childToParentMap[(nextCell[0],nextCell[1])].add((currCell[0],currCell[1]))
                        else:
                            value = set()
                            value.add((currCell[0],currCell[1]))
                            childToParentMap[(nextCell[0],nextCell[1])] = value
                    else:
                        value = set()
                        value.add((currCell[0],currCell[1]))
                        childToParentMap[(nextCell[0],nextCell[1])] = value
                    fringe.append(nextCell)
        if nextCell in explored:
            print('if nextCell in explored Executed. nextCell : '+str(nextCell))
            continue
        if nextCell is None:
            print('nextCell is not defined. Path probably does not exist')
            return print_bfs_path(childToParentMap, (goal_x,goal_y), (start_x, start_y))
        explored.append(nextCell)
        i=i+1
        # print("VAL" + str(i))
        if i>2000:         # BFS loop will end in case if BFS is taking more than i steps to complete
            print('Value of i is more than threshold')
            return print_bfs_path(childToParentMap, (goal_x,goal_y), (start_x, start_y))
    else:
        print('Path does not exist!')
        return {}


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
    # Instantiating g_score and f_score with infinity initially, this will be updated later as new values are found while traversing
    g_score={cell: float('inf') for cell in gridPos}
    g_score[start]=0
    f_score={cell: float('inf') for cell in gridPos}
    f_score[start] = h(start, (goal_x, goal_y))     # Heuristic cost of start cell + g_score of the start cell. Since g_score of start cell is 0, only heuristic cost is assigned
    openQueue = PriorityQueue()             # Assigned Priority Queue
    openQueue.put(((h(start, (goal_x, goal_y)) + 0), h(start, (goal_x, goal_y)), start))      # Priority Queue contains tuple in order: 1) Heuristic Cost + g_score, 2) Heuristic cost, and 3) start cell
    aPath = {}
    while not openQueue.empty():
        currCell = openQueue.get()[2]           # Cell value in the Priority Queue is selected as the current cell for this loop
        if currCell == (goal_x,goal_y):         # If current cell reaches the goal, loop breaks as path found
            break
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
        # Code to select nextCell as Down
        if currCell[0] != (grid_size - 1):
            if ((my_grid[currCell[0] + 1, currCell[1]] % 10) == 0 and ghost_check==0) or ((my_grid[currCell[0] + 1, currCell[1]]) == 0 and ghost_check==1):
                nextCell = ((currCell[0] + 1), currCell[1])
                g1 = g_score[currCell] + 1
                f1 = g1 + h(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, h(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
        # Code to select nextCell as Right
        if currCell[1] != (grid_size - 1):
            if ((my_grid[currCell[0], currCell[1] + 1] % 10) == 0 and ghost_check==0) or ((my_grid[currCell[0], currCell[1] + 1]) == 0 and ghost_check==1):
                nextCell = (currCell[0], (currCell[1] + 1))
                g1 = g_score[currCell] + 1
                f1 = g1 + h(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, h(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
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
    my_grid = place_ghosts(nr_of_ghosts)

# Method for Random movements for ghosts, 
# It accounts for Ghosts position at call [spawn if Timestamp=0] considers the probability of moving to LUDR directions
# Or Stay at the same place.
def ghostmovement(my_grid):
    ghostPositionList=np.argwhere(my_grid < 0)      # Gets all the ghost coordinates in this list
    for index in ghostPositionList:
        no_of_ghosts=(math.ceil(abs(my_grid[index[0],index[1]]/10)))
        while no_of_ghosts>1:
            ghostPositionList=np.append(ghostPositionList,index)
            no_of_ghosts=no_of_ghosts-1
    ghostPositionList=ghostPositionList.reshape((ghostPositionList.size)//2,2)
    for list in ghostPositionList:              # Visits each ghost in the list
            #L=(1) U=(2) D=(3) R=(4)
            if(list[0]==0 and list[1]==0): #START :CANT GO UP AND LEFT
                    direction=np.random.choice([3,4])
            elif(list[0]==0 and list[1]==(grid_size - 1)): #RIGHT TOP :CANT GO UP AND RIGHT
                    direction=np.random.choice([1,3])
            elif(list[0]==(grid_size - 1) and list[1]==0): #BOTTOM LEFT :CANT GO DOWN AND LEFT
                    direction=np.random.choice([2,4])
            elif(list[1]==(grid_size - 1) and list[1]==(grid_size - 1)): #GOAL :CANT GO DOWN AND RIGHT
                    direction=np.random.choice([1,2])
            elif(list[1]==0):
                    direction=np.random.choice([2,3,4])     # If ghost is on the left most cell, can only go Up, Down and Right
            elif(list[0]==0):
                    direction=np.random.choice([1,3,4])     # If ghost is on the top most cell, can only go Left, Down and Right
            elif(list[0]==(grid_size - 1)):
                    direction=np.random.choice([1,2,4])     # If ghost is on the bottom most cell, can only go Left, Up and Right
            elif(list[1]==(grid_size - 1)):
                    direction=np.random.choice([1,2,3])     # If ghost is on the right most cell, can only go Left, Up and Down
            else:
                direction=np.random.randint(low=1, high=5)
            
            # Moves the ghost based on the direction determined above (L=(1) U=(2) D=(3) R=(4))
            if direction==1 : #GO-LEFT
                if (my_grid[list[0]][list[1]-1]==0 or my_grid[list[0]][list[1]-1]%10==0) and (list[1]>0) : #OPEN CELL
                    my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                    my_grid[list[0]][list[1]-1]=my_grid[list[0]][list[1]-1]-10
                    list[1]=list[1]-1
                elif (my_grid[list[0]][list[1]-1]==1 or my_grid[list[0]][list[1]-1]%10!=0) and (list[1]>0): #BLOCKED CELL
                    directionIfBlocked=np.random.randint(low=0, high=2) #0=Stay, 1 =Go inside the Block
                    if directionIfBlocked==1:
                        # print('MOVE TO BLOCKED')
                        my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                        my_grid[list[0]][list[1]-1]=my_grid[list[0]][list[1]-1]-10
                        list[1]=list[1]-1
                    # else: print('STAY @ CURRENT')#STAY -NO CHANGE IF WALL IS BLOCKED
                    
            elif direction==2 :#GO-UP
                if (my_grid[list[0]-1][list[1]]==0 or my_grid[list[0]-1][list[1]]%10==0) and (list[0]>0) : #OPEN CELL
                    my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                    my_grid[list[0]-1][list[1]]=my_grid[list[0]-1][list[1]]-10
                    list[0]=list[0]-1
                elif (my_grid[list[0]-1][list[1]]==1 or my_grid[list[0]-1][list[1]]%10!=0) and (list[0]>0): #BLOCKED CELL
                    directionIfBlocked=np.random.randint(low=0, high=2) #0=Stay, 1 =Go inside the Block
                    if directionIfBlocked==1:
                        # print('MOVE TO BLOCKED')
                        my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                        my_grid[list[0]-1][list[1]]=my_grid[list[0]-1][list[1]]-10
                        list[0]=list[0]-1
                    # else: print('STAY @ CURRENT')#STAY -NO CHANGE IF WALL IS BLOCKED

            elif direction==3 : #GO-DOWN
                if (my_grid[list[0]+1][list[1]]==0 or my_grid[list[0]+1][list[1]]%10==0) and (list[0]<grid_size) : #OPEN CELL
                    my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                    my_grid[list[0]+1][list[1]]=my_grid[list[0]+1][list[1]]-10
                    list[0]=list[0]+1
                elif (my_grid[list[0]+1][list[1]]==1 or my_grid[list[0]+1][list[1]]%10!=0) and (list[0]<grid_size): #BLOCKED CELL
                    directionIfBlocked=np.random.randint(low=0, high=2) #0=Stay, 1 =Go inside the Block
                    if directionIfBlocked==1:
                        # print('MOVE TO BLOCKED')
                        my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                        my_grid[list[0]+1][list[1]]=my_grid[list[0]+1][list[1]]-10
                        list[0]=list[0]+1
                    # else: print('STAY @ CURRENT')#STAY -NO CHANGE IF WALL IS BLOCKED
            else :#GO-RIGHT 
                if (my_grid[list[0]][list[1]+1]==0 or my_grid[list[0]][list[1]+1]%10==0) and (list[1]<grid_size) : #OPEN CELL
                    my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                    my_grid[list[0]][list[1]+1]=my_grid[list[0]][list[1]+1]-10
                    list[1]=list[1]+1
                elif (my_grid[list[0]][list[1]+1]==1 or my_grid[list[0]][list[1]+1]%10!=0) and (list[1]<grid_size): #BLOCKED CELL
                    directionIfBlocked=np.random.randint(low=0, high=2) #0=Stay, 1 =Go inside the Block
                    if directionIfBlocked==1:
                        # print('MOVE TO BLOCKED')
                        my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                        my_grid[list[0]][list[1]+1]=my_grid[list[0]][list[1]+1]-10
                        list[1]=list[1]+1
                    # else: print('STAY @ CURRENT')#STAY -NO CHANGE IF WALL IS BLOCKED

# Returns direction of the nextCell from current cell in integers: L:1 U:2 D:3 R:4:
def findDirection(currCell, nextCellPos):
    if nextCellPos[0] == (currCell[0] + 1):     # Next Cell lies in Down direction
        direction = 3
    elif nextCellPos[0] == (currCell[0] - 1):     # Next Cell lies in Up direction
        direction = 2
    elif nextCellPos[1] == (currCell[1] + 1):     # Next Cell lies in Right direction
        direction = 4
    elif nextCellPos[1] == (currCell[1] - 1):     # Next Cell lies in Left direction
        direction = 1
    return direction

# Agent one traversal logic     -> Returns True if Agent 1 reaches the goal cell, and False if Agent 1 dies
def agentOneTraversal():
    a1 = start_pos          # Agent 1 coordinates denoted by this variable
    # Agent One gets the shortest A Star path using Manhattan Distance heuristic, ignoring the ghosts.
    aStarPathDetermined = aStar(my_grid)
    # Agent One traverses in below while loop until either it reaches the ghost, or when Agent 1 gets in the same cell as ghost.
    while (a1 != final_pos):
        nextLocA1 = aStarPathDetermined[a1]
        ghostmovement(my_grid)
        # if my_grid[nextLocA1] == 1:
        #     print('Agent is in Blocked Cell. Some Serious Error !!!!!!!!!!!!!!')
        if my_grid[nextLocA1] != 0:
            print('Agent not in Open Cell. Ghost Encountered!')
            print(my_grid[nextLocA1])
            return False
        a1 = nextLocA1
    return True

def agentOneRun():
    # Agent 1 Traversing
    global my_grid
    nr_of_ghosts=1
    while True:                 # Loop to check till what number can the Agent survive
        for i in range(1,5):
            create_env()            # New Env everytime
            agentOneReached = agentOneTraversal()       # Agent 1 Traversal path with A* Algorithm
            print('Agent One Reached : ' + str(agentOneReached))
            if nr_of_ghosts in a1Survivability:         # Dictionary containing results of Agent 1's Traversal success
                a1Survivability[nr_of_ghosts].append(agentOneReached)
            else:
                a1Survivability[nr_of_ghosts] = [agentOneReached]
            print(my_grid)
        print(a1Survivability)
        if True not in a1Survivability[nr_of_ghosts]:       # Loop must break if Agent 1's survivability is no more.
            break
        if nr_of_ghosts>10:         # A check to limit how many times loop will go on, safety mechanism
            break
        nr_of_ghosts+=1

# Called when Agent needs to get away from the ghost. Receives current cell and coordinate which is nearest to the ghost cell
def getAwayFromGhost(currCell, nearestGhostPos):        # --> Returns tuple value of nextPosition to take
    validDirections = [1,2,3,4]     # Listed valid directions, this will be removed if the direction is invalid
    invalidDirections = getInvalidAdjacentDirectionsToGoTo(currCell)            # Get the direction which point to cell outside of environment
    for i in invalidDirections:
        validDirections.remove(i)       # Removes the invalid directions from the possible movement positions
    ghostInDirection = findDirection(currCell, nearestGhostPos)     # Gets the direction of the ghost cell
    validDirections.remove(ghostInDirection)        # Removes the direction from the list as Agent must not move towards ghost
    placeholderForRemovingValidDirections = validDirections[:]      # Placeholder to modify the validDirections list
    for i in placeholderForRemovingValidDirections:             # To remove blocked cells from the list of directions that can be taken
        nextCell = getNextCoordinatesToMoveTo(currCell, i)      # Fetches coordinate of the cell passed based on the direction from current cell
        if (not checkForOpenPosition(nextCell)):        # checkForOpenPosition(nextCell) will return False if the cell is blocked.
            validDirections.remove(i)                   # Direction pointing to the blocked cells will be removed
    if validDirections == []:
        # No valid direction available to run away from the ghost. Hence agent will stay at same cell
        return currCell
    else:
        # Agent chooses one of the remaining valid direction to move to
        direction = np.random.choice(validDirections)
        nextCell = getNextCoordinatesToMoveTo(currCell, direction)  # Gets the next coordinate to move to
        return nextCell


def agentTwoTraversal(start_pos = (0,0)):
    global agent2PathAndMetric
    a2 = start_pos          # Agent 2 coordinates denoted by this variable
    nearestGhostPosition = tuple()
    # Agent 2 travels until it reaches the goal position, or until it gets in same coordinate as ghost position
    while (a2 != final_pos):
        # Agent 2 gets a new A Star path based on current location in each step, and checks a path which is free of ghost
        aStarPathDetermined = aStar(my_grid, 1, a2[0], a2[1])
        if len(aStarPathDetermined) == 0:           # True if A Start path not present to goal node
            # Agent checks for the nearest ghost using BFS algorithm
            nearestGhostPath = breadth_first_search(my_grid, 1, a2[0], a2[1])       # Returns list of path to ghost
            # If the nearestGhostPath returned does not contain next cell, below 'if' will be triggered. Acts as safety mechanism
            if len(nearestGhostPath) == 1:
                return False
            nearestGhostPosition = nearestGhostPath[1]      # This will be the next cell from the agent's current cell
            nextLocA2 = getAwayFromGhost(a2, nearestGhostPosition)      # Passes current Agent 2 location and the next Path that Agent will have to take to get to the nearest ghost
            # if nextLocA2 == a2:   # Included to go towards ghost if there are no other paths present. Implemented this as Agent 2 cannot stay at same location
            #     nextLocA2=nearestGhostPosition
            if not nextLocA2 or my_grid[nextLocA2[0],nextLocA2[1]] < 0: # Returns False if there is no path or if index is out of bounds
                return False
        else:
            # If A Star path is present without ghost in path, agent will follow the A Star path
            nextLocA2 = aStarPathDetermined[a2]
        # Storing data of Agent 2 in path
        currCellToNextCellDirection = findDirection(a2, nextLocA2)
        agent2PathAndMetric[(a2[0], a2[1], currCellToNextCellDirection)] = False
        # Movement of ghost initiated
        ghostmovement(my_grid)
        # Returns False if agent steps in same cell as ghost
        if my_grid[nextLocA2] != 0:
            return False
        a2 = nextLocA2
    return True

# Stores Agent 2's data in file for heuristic
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

def agentTwoRun():
    global my_grid, agent2PathAndMetric, nr_of_ghosts
    # Metric: AgentNo, RunNo, No. of ghosts, MazeNo, Win/Loss, Time, Future-(No. of steps)    
    # Agent 2
    a2Survivability = {}
    a2Data = []
    a2RunNo = 1
    while True:                 # Loop to check till what number can the Agent survive
        for i in range(1,5):
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
                a2Data.append(["A2", a2RunNo, nr_of_ghosts, i, val, executionTime])
                a2RunNo+=1
                print(my_grid)
                print('agent2PathAndMetric : '+ str(agent2PathAndMetric))
                writeAg2MetricForAg3(i, nr_of_ghosts, agent2PathAndMetric, 'A2RunCheck')
                agent2PathAndMetric = {}
        print(a2Survivability)
        if True not in a2Survivability[nr_of_ghosts]:       # Loop must break if Agent 2's survivability is no more.
            break
        if nr_of_ghosts>3:         # A check to limit how many times loop will go on, safety mechanism
            break
        nr_of_ghosts+=1
    with open('a2Data1.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(a2Data)
    file.close()


def checkForOpenPosition(cellToCheck, onlyGhostChecks = 0):             # Returns True if the passed cell is unblocked
    # onlyGhostChecks values denote:
        # 0: Returns True only if the cellToCheck is not open (that is it must not have ghost, and also must not be blocked)
        # 1: Returns True only if the cellToCheck does not have ghosts (including ghosts in blocked cells)
        # 2: Returns True only if the cellToCheck does not have ghosts which are present in unblocked cells (ghosts in blocked cells will be ignored)
    if (cellToCheck[0] >=0 and cellToCheck[0] < grid_size) and (cellToCheck[1] >=0 and cellToCheck[1] <grid_size):
        if (my_grid[cellToCheck[0],cellToCheck[1]] != 0) and onlyGhostChecks == 0:  # Checks if the current cell is Unblocked
            return False
        elif (my_grid[cellToCheck[0],cellToCheck[1]] < 0) and onlyGhostChecks == 1:  # Checks if the current cell does have ghost
            return False
        elif (my_grid[cellToCheck[0],cellToCheck[1]] %10 != 0 and my_grid[cellToCheck[0],cellToCheck[1]] != 1) and onlyGhostChecks == 2:
            # Checks if the current cell has ghost in unblocked cells
            return False
    return True   # To return True if passed cell is invalid, like if it lies outside the boundary of matrix. This cell will not have ghost.

def checkOpenCellsForAgentFour(currPosition, determinedPath, visibility):
    # Checks if there are any ghosts in determinedPath till next visibility path (+1 more depth)
    for i in range(visibility):     # Iterates till visibility cell
        if currPosition in determinedPath:
            nextPosition = determinedPath[currPosition]     # Checks each adjacent cell from nextPosition for ghosts
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

def checkOpenCellsForAgentFive(currPosition, determinedPath, visibility):
    # Checks if there are any ghosts in determinedPath till next visibility path (+1 more depth)
    for i in range(visibility):     # Iterates till visibility cell
        if currPosition in determinedPath:
            nextPosition = determinedPath[currPosition]     # Checks each adjacent cell from nextPosition for ghosts
            if (not checkForOpenPosition(nextPosition, 2)):
                return True
            elif (not checkForOpenPosition((nextPosition[0]+1, nextPosition[1]), 2)):
                return True
            elif (not checkForOpenPosition((nextPosition[0]-1, nextPosition[1]), 2)):
                return True
            elif (not checkForOpenPosition((nextPosition[0], nextPosition[1]-1), 2)):
                return True
            elif (not checkForOpenPosition((nextPosition[0], nextPosition[1]+1), 2)):
                return True
            currPosition = nextPosition
    return False

def checkAdjacentCoordinatesForGhost(currCell):                 
    # Checks if adjacent cells to the current cell contains ghost (and also blocked cells), if yes, returns the blocked positions
    ghostPositionsNearby = []           # This list will contain positions of the nearby ghost, in adjacent cell
    if (not checkForOpenPosition((currCell[0]+1, currCell[1]), 1)):
        ghostPositionsNearby.append((currCell[0]+1, currCell[1]))
    if (not checkForOpenPosition((currCell[0]-1, currCell[1]), 1)):
        ghostPositionsNearby.append((currCell[0]-1, currCell[1]))
    if (not checkForOpenPosition((currCell[0], currCell[1]-1), 1)):
        ghostPositionsNearby.append((currCell[0], currCell[1]-1))
    if (not checkForOpenPosition((currCell[0], currCell[1]+1), 1)):
        ghostPositionsNearby.append((currCell[0], currCell[1]+1))
    return ghostPositionsNearby

# Returns the coordinates in which the agent must move to based on direction received
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

# Returns the list of directions (LUDR) towards which agent can't go to
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

def moveAsPerAgent2(nr_of_ghosts, currCell, allowedDirections):
    with open("a2DataFor3_" + str(nr_of_ghosts) + ".csv", newline='') as file:
        a2Reader = csv.reader(file, delimiter=' ', quotechar='|')
        directionValue = [0,0,0,0]
        for row in a2Reader:
            row = row[0].split(',')
            row = [int(i) for i in row]
            print(row)
            if row[1] == currCell[0] and row[2] == currCell[1]:
                if row[3] == 1:
                    directionValue[0] = row[4] / row[5]
                elif row[3] == 2:
                    directionValue[1] = row[4] / row[5]
                elif row[3] == 3:
                    directionValue[2] = row[4] / row[5]
                else:
                    directionValue[3] = row[4] / row[5]
        origDirections = [1,2,3,4]
        for x in allowedDirections:
            origDirections.remove(x)
        for i in origDirections:
            directionValue[i-1] = -100
        count=0
        for i in directionValue:
            if i == 0:
                count+=1
        if count == 4:
            return -100            
        directionToTake = directionValue.index(max(directionValue)) + 1
        print(directionToTake)
        return directionToTake

# Agent 3 Traversal function
def agent3Traversal(nr_of_ghosts):
    a3 = start_pos          # Agent 3 coordinates denoted by this variable.
    #Store each position taken by Agent3 in dict.
    #Read the right rows from CSV file.
    #Take one with the maximum survivability.
    #If again coming on this path, take the random move.
    #If no data for a given cell, run Agent 2's strategy only once.
    a3CellExplored = []
    while (a3 != final_pos):
        print(a3)
        if a3 in a3CellExplored:
            aStarPathDetermined = aStar(my_grid, 0, a3[0], a3[1])
            nextCell = aStarPathDetermined[(a3[0],a3[1])]
            if my_grid[nextCell[0]][nextCell[1]] != 0:
                a3 = a3
            else:
                a3 = nextCell
        else:
            a3AllowedDirections = [1,2,3,4]     # Initiated a direction list, invalid or blocked directions will be removed from this list.
            invalidDirections = getInvalidAdjacentDirectionsToGoTo(a3)      # Gets list of invalid adjacent directions, which will lead to agent going out of environment
            print('invalidDirections : '+str(invalidDirections))
            for i in invalidDirections:
                print('Removing value '+str(i)+' from a3AllowedDirections '+str(a3AllowedDirections))
                a3AllowedDirections.remove(i)       # Removes invalid directions from allowed directions for the agent from current position
            nearbyGhostPositions = checkAdjacentCoordinatesForGhost(a3)
            if len(nearbyGhostPositions) != 0:
                for pos in nearbyGhostPositions:
                    a3AllowedDirections.remove(findDirection(a3, pos))
            placeholderAllowedDirections = a3AllowedDirections[:]
            for dir in placeholderAllowedDirections:
                nextCell = getNextCoordinatesToMoveTo(a3, dir)
                if (not checkForOpenPosition(nextCell)):
                    a3AllowedDirections.remove(dir)

            print("Allowed Directions "+ str(a3AllowedDirections))
            directionToTake = moveAsPerAgent2(nr_of_ghosts, start_pos, a3AllowedDirections)
            if directionToTake == -100:
                print("no valid directions astar " + a3)
                aStarPathDetermined = aStar(my_grid, 0, a3[0], a3[1])
                nextCell = aStarPathDetermined[(a3[0],a3[1])]
                if my_grid[nextCell[0]][nextCell[1]] != 0:
                    a3 = a3
                else:
                    a3 = nextCell
            else:
                nextCell = getNextCoordinatesToMoveTo(a3, directionToTake)
                a3=nextCell

                # while my_grid[nextCell[0]][nextCell[1]] == 1 or my_grid[nextCell[0]][nextCell[1]] < 0:
                #     a3AllowedDirections.remove(directionToTake)
                #     if len(a3AllowedDirections) == 0:
                #         return False
                    # directionToTake = moveAsPerAgent2(nr_of_ghosts, start_pos, a3AllowedDirections)
                    # nextCell = getNextCoordinatesToMoveTo(a3, directionToTake)
                # Movement of ghost initiated
        ghostmovement(my_grid)
        print(a3)
        if a3 not in a3CellExplored:
            a3CellExplored.append(a3)
        if my_grid[a3[0]][a3[1]] == 1:
            print('Agent is in Blocked Cell. Some Serious Error !!!!!!!!!!!!!!')
        if my_grid[a3[0]][a3[1]] != 0:
            print('Agent not in Open Cell. Ghost Encountered ????????????')
            print(my_grid[a3[0]][a3[1]])
            return False

    return True

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

def agent3Traversal(nr_of_ghosts):
    a3 = start_pos          # Agent 3 coordinates denoted by this variable.
    a3CellExplored = []     # Storing each position taken by Agent3, so that we can decide if it is forming a loop in path or not?
    while (a3 != final_pos):
        print(a3)
        if a3 in a3CellExplored:      #If Agent3 is again visiting already visited cell, take the move as per A star, else stay in place.
            aStarPathDetermined = aStar(my_grid, 0, a3[0], a3[1])
            nextCell = aStarPathDetermined[(a3[0],a3[1])]
            if my_grid[nextCell[0]][nextCell[1]] != 0:
                a3 = a3              #Stay in place if the nextCell has ghosts.
            else:
                a3 = nextCell   
        else:
            a3AllowedDirections = [1,2,3,4]     # Initiated a direction list, invalid or blocked directions will be removed from this list.
            invalidDirections = getInvalidAdjacentDirectionsToGoTo(a3)      # Gets list of invalid adjacent directions, which will lead to agent going out of environment
            print('invalidDirections : '+str(invalidDirections))
            for i in invalidDirections:
                print('Removing value '+str(i)+' from a3AllowedDirections '+str(a3AllowedDirections))
                a3AllowedDirections.remove(i)       # Removes invalid directions from allowed directions for the agent from current position
            nearbyGhostPositions = checkAdjacentCoordinatesForGhost(a3)
            if len(nearbyGhostPositions) != 0:
                for pos in nearbyGhostPositions:
                    a3AllowedDirections.remove(findDirection(a3, pos))
            placeholderAllowedDirections = a3AllowedDirections[:]
            for dir in placeholderAllowedDirections:
                nextCell = getNextCoordinatesToMoveTo(a3, dir)
                if (not checkForOpenPosition(nextCell)):
                    a3AllowedDirections.remove(dir)

            print("Allowed Directions "+ str(a3AllowedDirections))
            directionToTake = moveAsPerAgent2(nr_of_ghosts, start_pos, a3AllowedDirections)       #Take one allowedDirection with the maximum survivability.
            if directionToTake == -100:     #If no data for a given cell, run Agent 2's strategy only once.
                print("no valid directions astar " + a3)
                aStarPathDetermined = aStar(my_grid, 0, a3[0], a3[1])
                nextCell = aStarPathDetermined[(a3[0],a3[1])]
                if my_grid[nextCell[0]][nextCell[1]] != 0:
                    a3 = a3
                else:
                    a3 = nextCell
            else:
                nextCell = getNextCoordinatesToMoveTo(a3, directionToTake)
                a3=nextCell
        
        ghostmovement(my_grid)          # Movement of ghost initiated
        print(a3)
        if a3 not in a3CellExplored:    # Adding to visitedCells.
            a3CellExplored.append(a3)
        if my_grid[a3[0]][a3[1]] == 1:
            print('Agent is in Blocked Cell. Some Serious Error !!!!!!!!!!!!!!')
        if my_grid[a3[0]][a3[1]] != 0:
            print('Agent not in Open Cell. Ghost Encountered ????????????')
            print(my_grid[a3[0]][a3[1]])
            return False

    return True

def agentThreeRun():
    #Metric:
    #AgentNo, No. of ghosts, Win/Loss, Time, Future-(No. of steps)
    a3Survivability = {}
    a3Data = []
    while True:                 # Loop to check till what number can the Agent survive
        for i in range(1,3):
            create_env()            # New Env everytime
            startTime = time.time()
            agentThreeReached = agent3Traversal(nr_of_ghosts)
            print('Agent Two Reached : ' + str(agentThreeReached))
            if agentThreeReached:
                val = True
            else:
                val = False
            if nr_of_ghosts in a3Survivability:         # Dictionary containing results of Agent 2's Traversal success
                a3Survivability[nr_of_ghosts].append(val)
            else:
                a3Survivability[nr_of_ghosts] = [val]
            executionTime = time.time() - startTime
            a3Data.append(["A3", nr_of_ghosts, val, executionTime])
            print(my_grid)
        print(a3Survivability)
        if True not in a3Survivability[nr_of_ghosts]:       # Loop must break if Agent 2's survivability is no more.
            break
        if nr_of_ghosts>3:         # A check to limit how many times loop will go on, safety mechanism
            break
        nr_of_ghosts+=1
        with open('a3DataTemp4.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(a3Data)
        file.close()
    with open('a3Data1.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(a3Data)
    file.close()
    agent3Reached = agent3Traversal(1)
    print(agent3Reached)

def agentFourTraversal():
    global a4PathTaken
    a4 = start_pos          # Agent 4 coordinates denoted by this variable
    aStarPathDetermined = aStar(my_grid, 0, a4[0], a4[1])
    # A Star path search without considering the ghost to get the shortest path possible to the end
    strike, visibility = 0, 3
    while (a4 != final_pos):
        if a4 in aStarPathDetermined:
            # If A Star path is present for the agent from the current cell, follow the path
            nextLocA4 = aStarPathDetermined[a4]
        else:
            # Find A Star path without considering the ghost, to get the shortest path possible to the end
            aStarPathDetermined = aStar(my_grid, 0, a4[0], a4[1])
            nextLocA4 = aStarPathDetermined[a4]
        # Check if any ghost is present in aStar's Visibility (+ 1 more depth) cells
        ghostPresentNearVisibility = checkOpenCellsForAgentFour(a4, aStarPathDetermined, visibility)
        if ghostPresentNearVisibility:
            # If ghost present in/near A Star path from the current cell, increments a counter to track consecutive ghost encounters
            strike += 1
            if strike==1:
                a4GhostPositionNearby = checkAdjacentCoordinatesForGhost(a4)    # List of ghost coordinates at adjacent cells
                if a4GhostPositionNearby != []:     # If there is a ghost in nearby cell
                    a4AllowedDirections = [1,2,3,4]
                    # Get list of invalid adjacent directions, which will lead to agent going out of environment
                    invalidDirections = getInvalidAdjacentDirectionsToGoTo(a4)
                    for i in invalidDirections:
                        a4AllowedDirections.remove(i)
                    placeholdera4GhostPositionNearby = a4GhostPositionNearby[:]
                    # Will remove cell coordinates/directions which will take the agent nearer to the ghost
                    for i in placeholdera4GhostPositionNearby:
                        restrictedDirection = findDirection(a4, i)
                        a4AllowedDirections.remove(restrictedDirection)
                    placeholderA4AllowedDirections = a4AllowedDirections[:]
                    # To remove blocked cells from the list of directions that can be taken
                    for i in placeholderA4AllowedDirections:
                        nextCell = getNextCoordinatesToMoveTo(a4, i)
                        if (not checkForOpenPosition(nextCell)):
                            # checkForOpenPosition(nextCell) will return False if the cell is blocked.
                            a4AllowedDirections.remove(i)       # If blocked, Agent cant move to this direction
                    if a4AllowedDirections == []:       # Stay at same location as Allowed Direction from checks is 0
                        nextLocA4 = a4
                    else:   # Choose random direction from allowed directions
                        directionToMove = np.random.choice(a4AllowedDirections)
                        nextLocA4 = getNextCoordinatesToMoveTo(a4, directionToMove)
                else:
                    nextLocA4 = a4    
                    # Stay at same position as ghost is not at immediate next step. Ghost can go away to another direction
            else:
                # Move away from the AStar path as ghost encountered nearby
                nextLocA4 = getAwayFromGhost(a4, nextLocA4)
        else:
            strike = 0
            nextLocA4 = aStarPathDetermined[a4]
            # Since no ghost in visibility. Agent will go on with AStar path.
        # Agent dies if agent is present with the ghost
        if my_grid[nextLocA4] != 0:
            return False
        a4 = nextLocA4
        ghostmovement(my_grid)  # Movement of each ghost present in my_grid
        a4PathTaken.append(a4)
    return True

def agentFourRun():
    global my_grid, nr_of_ghosts
    a4Data =[]
    while True:                 # Loop to check till what number can the Agent survive
        for i in range(1,5):
            create_env()            # New Env everytime
            startTime = time.time()
            agentFourReached = agentFourTraversal()       # Agent 1 Traversal path with A* Algorithm
            print('Agent Four Reached : ' + str(agentFourReached))
            if nr_of_ghosts in a4Survivability:         # Dictionary containing results of Agent 4's Traversal success
                a4Survivability[nr_of_ghosts].append(agentFourReached)
            else:
                a4Survivability[nr_of_ghosts] = [agentFourReached]
            print(my_grid)
            print(a4Survivability)
            a4DataLength = len(a4Survivability[nr_of_ghosts])
            executionTime = time.time() - startTime
            a4Data.append(["A4", i, nr_of_ghosts, agentFourReached, executionTime])
        if True not in a4Survivability[nr_of_ghosts]:       # Loop must break if Agent 1's survivability is no more.
            break
        if nr_of_ghosts>5:         # A check to limit how many times loop will go on, safety mechanism
            break
        nr_of_ghosts+=1

    with open('a4Data1.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(a4Data)

def agentFiveTraversal():
    global a5PathTaken, my_grid
    a5 = start_pos          # Agent 5 coordinates denoted by this variable, at the start in the beginning
    aStarPathDetermined = aStar(my_grid, 0, a5[0], a5[1])
    # A Star path search without considering the ghost to get the shortest path possible to the end
    strike, visibility = 0, 3
    while (a5 != final_pos):
        # Checks ghost if present in aStar's Visibility (+ 1 more depth) (based on length denoted by variable Visibility) cells
        if a5 in aStarPathDetermined:           # First need to check if AStar path lies from where Agent is currently positioned.
            nextLocA5 = aStarPathDetermined[a5] # If AStar path lies, will consider the next step as per AStar for traversal.
        else:               # If no AStar path found on current coordinate, A Star search is again done to get new coordinates.
            aStarPathDetermined = aStar(my_grid, 0, a5[0], a5[1])
            # A Star path search without considering the ghost to get the shortest path possible to the end
            nextLocA5 = aStarPathDetermined[a5]                 # Next coordinate taken from New AStar path
        ghostPresentNearVisibility = checkOpenCellsForAgentFive(a5, aStarPathDetermined, visibility)
        # Fetches if there are any ghost (only in unblocked cells) till Visibility length (+1 more depth) when AStar path is followed
        if ghostPresentNearVisibility:        # If ghost present in the AStar path (or in the next coordinate of the AStar path)
            strike += 1             # Increments to showcase that Ghost is still in path, even in next iteration
            if strike==1:           # If ghost came into the path in this iteration only, strike will be 1
                a5GhostPositionNearby = checkAdjacentCoordinatesForGhost(a5)
                # Since not moving is an option, agent needs list of ghost coordinates at adjacent cells to know the risk
                if a5GhostPositionNearby != []:
                    # If there is a ghost in adjacent cell, will enter this if condition to check where agent should move
                    a5AllowedDirections = [1,2,3,4]
                    # Initiated a direction list, invalid or blocked directions will be removed from this list.
                    invalidDirections = getInvalidAdjacentDirectionsToGoTo(a5)
                    # Gets list of invalid adjacent directions, which will lead to agent going out of environment
                    for i in invalidDirections:
                        a5AllowedDirections.remove(i)
                        # Removes invalid directions from allowed directions for the agent from current position
                    placeholdera5GhostPositionNearby = a5GhostPositionNearby[:]
                    # To remove cell coordinates/directions which will take the agent nearer to the ghost
                    for i in placeholdera5GhostPositionNearby:
                        restrictedDirection = findDirection(a5, i)
                        a5AllowedDirections.remove(restrictedDirection)
                        # Removed directions where ghost is present in the immediate cell
                    placeholderA5AllowedDirections = a5AllowedDirections[:]
                    for i in placeholderA5AllowedDirections:     # To remove blocked cells from the list of directions that can be taken
                        nextCell = getNextCoordinatesToMoveTo(a5, i)
                        if (not checkForOpenPosition(nextCell)): # checkForOpenPosition(nextCell) returns False if the cell is blocked
                            a5AllowedDirections.remove(i)
                            # This will remove the direction of blocked cells directions from allowed directions for the agent
                    if a5AllowedDirections == []:       # Stay at same location as Allowed Direction as all the other directions are blocked and possibly the only direction(s) open will lead to the ghost 
                        nextLocA5 = a5
                        # Ghost is present in adjacent cell. After choices, Agent decided to stay
                    else:
                        directionToMove = np.random.choice(a5AllowedDirections)
                        # If there is a direction that agent can move in, direction to move will be taken randomly among those
                        nextLocA5 = getNextCoordinatesToMoveTo(a5, directionToMove)
                else:
                    nextLocA5 = a5     # Stay at same position as ghost is not at immediate next step. Ghost can move away
            else:
                # Since ghost is in the path, and it is still travelling in/near the AStar path, Agent chooses to move away from the ghost
                nextLocA5 = getAwayFromGhost(a5, nextLocA5)      # Returns coordinates that Agent can move to get away from the ghost
        else:
            strike = 0
            nextLocA5 = aStarPathDetermined[a5]     # Since there are no ghost in vicinity, agent follows current AStar path
        print(nextLocA5)
        if my_grid[nextLocA5] != 0:         # Agent is not in Open cell, agent died!!
            print(my_grid[nextLocA5])
            return False
        a5 = nextLocA5
        ghostmovement(my_grid)          # Instantiates ghost movement
        a5PathTaken.append(a5)
    return True

def agentFiveRun():
    global my_grid, a5Survivability
    nr_of_ghosts=1
    a5Data =[]
    while True:                 # Loop to check till what number can the Agent survive
        for i in range(1,5):
            create_env()            # New Env everytime
            startTime = time.time()
            agentFiveReached = agentFiveTraversal()       # Agent 1 Traversal path with A* Algorithm
            print('Agent Five Reached : ' + str(agentFiveReached))
            if nr_of_ghosts in a5Survivability:         # Dictionary containing results of Agent 4's Traversal success
                a5Survivability[nr_of_ghosts].append(agentFiveReached)
            else:
                a5Survivability[nr_of_ghosts] = [agentFiveReached]
            print(my_grid)
            print(a5Survivability)
            a5DataLength = len(a5Survivability[nr_of_ghosts])
            executionTime = time.time() - startTime
            a5Data.append(["A5", i, nr_of_ghosts, agentFiveReached, executionTime])
        # if True not in a5Survivability[nr_of_ghosts]:       # Loop must break if Agent 1's survivability is no more.
        #     break
        nr_of_ghosts+=1
        if nr_of_ghosts>10:         # A check to limit how many times loop will go on, safety mechanism
            break

    with open('a5Data1.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(a5Data)

        file.close()

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


if __name__=='__main__':
    create_env()
    print('Original Grid generated : ')
    print(my_grid)
    my_grid_original = my_grid                  # To have a backup of original grid
    # print('Copied above grid to my_grid_original :')

    agentOneRun()

    agentTwoRun()

    agentThreeRun()

    agentFourRun()

    agentFiveRun()