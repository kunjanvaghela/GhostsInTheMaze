import math
import numpy as np
import time
import csv

# Variable Declare
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
a4PathTaken = []        # To check and compare path taken by Agent 4
a5PathTaken = []






def agentTwoTraversal(start_pos = (0,0)):
    global agent2PathAndMetric
    a2 = start_pos          # Agent 2 coordinates denoted by this variable
    nearestGhostPosition = tuple()
    # Agent 2 travels until it reaches the goal position, or until it gets in same coordinate as ghost position
    while (a2 != final_pos):
        # Agent 2 gets a new A Star path based on current location in each step, and checks a path which is free of ghost
        aStarPathDetermined = a_star(my_grid, 1, a2[0], a2[1])
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
            aStarPathDetermined = a_star(my_grid, 0, a3[0], a3[1])
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
                aStarPathDetermined = a_star(my_grid, 0, a3[0], a3[1])
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

def agent3Traversal(nr_of_ghosts):
    a3 = start_pos          # Agent 3 coordinates denoted by this variable.
    a3CellExplored = []     # Storing each position taken by Agent3, so that we can decide if it is forming a loop in path or not?
    while (a3 != final_pos):
        print(a3)
        if a3 in a3CellExplored:      #If Agent3 is again visiting already visited cell, take the move as per A star, else stay in place.
            aStarPathDetermined = a_star(my_grid, 0, a3[0], a3[1])
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
                aStarPathDetermined = a_star(my_grid, 0, a3[0], a3[1])
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
    aStarPathDetermined = a_star(my_grid, 0, a4[0], a4[1])
    # A Star path search without considering the ghost to get the shortest path possible to the end
    strike, visibility = 0, 3
    while (a4 != final_pos):
        if a4 in aStarPathDetermined:
            # If A Star path is present for the agent from the current cell, follow the path
            nextLocA4 = aStarPathDetermined[a4]
        else:
            # Find A Star path without considering the ghost, to get the shortest path possible to the end
            aStarPathDetermined = a_star(my_grid, 0, a4[0], a4[1])
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
    aStarPathDetermined = a_star(my_grid, 0, a5[0], a5[1])
    # A Star path search without considering the ghost to get the shortest path possible to the end
    strike, visibility = 0, 3
    while (a5 != final_pos):
        # Checks ghost if present in aStar's Visibility (+ 1 more depth) (based on length denoted by variable Visibility) cells
        if a5 in aStarPathDetermined:           # First need to check if AStar path lies from where Agent is currently positioned.
            nextLocA5 = aStarPathDetermined[a5] # If AStar path lies, will consider the next step as per AStar for traversal.
        else:               # If no AStar path found on current coordinate, A Star search is again done to get new coordinates.
            aStarPathDetermined = a_star(my_grid, 0, a5[0], a5[1])
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


# if __name__=='__main__':
#     create_env()
#     print('Original Grid generated : ')
#     print(my_grid)
#
#     agentOneRun()
