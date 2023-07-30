from queue import Empty, PriorityQueue
from utils import variables

# class SearchAlgorithms:
#     def __init__(self):
#         pass


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
            if currCell[0] != (variables.GRID_SIZE - 1):
                if (my_grid[currCell[0] + 1, currCell[1]] % 10) == 0:
                    nextCell = [(currCell[0] + 1), currCell[1]]
                    if nextCell not in explored:
                        fringe.append(nextCell)
            # Code to select nextCell as Right
            if currCell[1] != (variables.GRID_SIZE - 1):
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
def breadth_first_search(my_grid, ghostCheck=0, start_x=0, start_y=0, goal_x=variables.GRID_SIZE-1, goal_y=variables.GRID_SIZE-1):
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
        if currCell[0] != (variables.GRID_SIZE - 1):
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
        if currCell[1] != (variables.GRID_SIZE - 1):
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
def heuristic_manhattan(cell1, cell2):
    x1,y1 = cell1       # Represents cell1 coordinates
    x2,y2 = cell2       # Represents cell2 coordinates
    return abs(x1-x2) + abs(y1-y2)      # Maanhattan distance between cell1 and cell2

# A Star Algorithm with Heuristic of Manhattan Distance     -- Returns Forward Path determined as part of the Algo in the grid
def a_star(my_grid, ghost_check=0, start_x=0, start_y=0, goal_x=variables.GRID_SIZE-1, goal_y=variables.GRID_SIZE-1):
    start=(start_x,start_y)
    gridPos=[]
    # a=0
    for i in range(len(my_grid)):         # To get grid vertices in a list
        for j in range(len(my_grid[0])):
            gridPos.append((i,j))
            # gridPos.append((a,j))
        # a=a+1
    # Instantiating g_score and f_score with infinity initially, this will be updated later as new values are found while traversing
    g_score={cell: float('inf') for cell in gridPos}
    g_score[start]=0
    f_score={cell: float('inf') for cell in gridPos}
    f_score[start] = heuristic_manhattan(start, (goal_x, goal_y))     # Heuristic cost of start cell + g_score of the start cell. Since g_score of start cell is 0, only heuristic cost is assigned
    openQueue = PriorityQueue()             # Assigned Priority Queue
    openQueue.put(((heuristic_manhattan(start, (goal_x, goal_y)) + 0), heuristic_manhattan(start, (goal_x, goal_y)), start))      # Priority Queue contains tuple in order: 1) Heuristic Cost + g_score, 2) Heuristic cost, and 3) start cell
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
                f1 = g1 + heuristic_manhattan(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, heuristic_manhattan(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
        # Code to select nextCell as Up
        if currCell[0] != 0:
            if ((my_grid[(currCell[0] - 1), currCell[1]] % 10) == 0 and ghost_check==0) or ((my_grid[(currCell[0] - 1), currCell[1]]) == 0 and ghost_check==1):
                nextCell = ((currCell[0] - 1), currCell[1])
                g1 = g_score[currCell] + 1
                f1 = g1 + heuristic_manhattan(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, heuristic_manhattan(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
        # Code to select nextCell as Down
        if currCell[0] != (variables.GRID_SIZE - 1):
            if ((my_grid[currCell[0] + 1, currCell[1]] % 10) == 0 and ghost_check==0) or ((my_grid[currCell[0] + 1, currCell[1]]) == 0 and ghost_check==1):
                nextCell = ((currCell[0] + 1), currCell[1])
                g1 = g_score[currCell] + 1
                f1 = g1 + heuristic_manhattan(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, heuristic_manhattan(nextCell,(goal_x,goal_y)), nextCell))
                    aPath[nextCell] = currCell
        # Code to select nextCell as Right
        if currCell[1] != (variables.GRID_SIZE - 1):
            if ((my_grid[currCell[0], currCell[1] + 1] % 10) == 0 and ghost_check==0) or ((my_grid[currCell[0], currCell[1] + 1]) == 0 and ghost_check==1):
                nextCell = (currCell[0], (currCell[1] + 1))
                g1 = g_score[currCell] + 1
                f1 = g1 + heuristic_manhattan(nextCell , (goal_x, goal_y))
                if f1 < f_score[nextCell]:
                    g_score[nextCell] = g1
                    f_score[nextCell] = f1
                    openQueue.put((f1, heuristic_manhattan(nextCell,(goal_x,goal_y)), nextCell))
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
