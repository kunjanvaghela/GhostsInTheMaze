from utils import variables

class Agent(object):
    """docstring for Agent."""

    def __init__(self, type):
        super(Agent, self).__init__()
        self.type = type


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

    # Agent one traversal logic     -> Returns True if Agent 1 reaches the goal cell, and False if Agent 1 dies
    def agentOneTraversal():
        a1 = start_pos          # Agent 1 coordinates denoted by this variable
        # Agent One gets the shortest A Star path using Manhattan Distance heuristic, ignoring the ghosts.
        aStarPathDetermined = a_star(my_grid)
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
