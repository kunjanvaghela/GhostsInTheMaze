
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




def checkForOpenPosition(cellToCheck, visibility_level = 0):             # Returns True if the passed cell is unblocked
    # visibility_level values denote:
        # 0: Returns True only if the cellToCheck is not open (that is it must not have ghost, and also must not be blocked)
        # 1: Returns True only if the cellToCheck does not have ghosts (including ghosts in blocked cells)
        # 2: Returns True only if the cellToCheck does not have ghosts which are present in unblocked cells (ghosts in blocked cells will be ignored)
    if (cellToCheck[0] >=0 and cellToCheck[0] < grid_size) and (cellToCheck[1] >=0 and cellToCheck[1] <grid_size):
        if (my_grid[cellToCheck[0],cellToCheck[1]] != 0) and visibility_level == 0:  # Checks if the current cell is Unblocked
            return False
        elif (my_grid[cellToCheck[0],cellToCheck[1]] < 0) and visibility_level == 1:  # Checks if the current cell does have ghost
            return False
        elif (my_grid[cellToCheck[0],cellToCheck[1]] %10 != 0 and my_grid[cellToCheck[0],cellToCheck[1]] != 1) and visibility_level == 2:
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
