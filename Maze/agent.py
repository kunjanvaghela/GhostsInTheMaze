from maze import Maze
from utils import algorithms
from utils import variables
from utils import helper_functions

class Agent(object):
    """docstring for Agent."""

    def __init__(self, type):
        super(Agent, self).__init__()
        self.type = type

    def get_agent_type(self):
        return self.type


    def agent_traversal(self, maze: Maze):
        if self.type == 1:
            return self.agent_one_traversal()

    def agent_one_traversal(self, maze: Maze):
        return algorithms.a_star(maze.my_grid)

    def agent_two_traversal(self, maze: Maze, agentPosition: (int, int)):
        nearestGhostPosition = tuple()
        my_grid = maze.get_my_grid()
        aStarPathDetermined = algorithms.a_star(my_grid, 1, agentPosition[0], agentPosition[1])       # Agent 2 gets a new A Star path based on current location in each step, and checks a path which is free of ghost
        if len(aStarPathDetermined) == 0:           # True if A Start path not present to goal node
            if agentPosition == (variables.GRID_SIZE - 1, variables.GRID_SIZE - 1): return {agentPosition: agentPosition}
            # Agent checks for the nearest ghost using BFS algorithm
            nearestGhostPath = algorithms.breadth_first_search(my_grid, 1, agentPosition[0], agentPosition[1])       # Returns list of path to ghost
            # If the nearestGhostPath returned does not contain next cell, below 'if' will be triggered. Acts as safety mechanism
            if len(nearestGhostPath) == 1:        # Commented for Visualization
                # return False
                return {agentPosition: agentPosition}
            nearestGhostPosition = nearestGhostPath[1]      # This will be the next cell from the agent's current cell
            nextLocA2 = helper_functions.getAwayFromGhost(agentPosition, nearestGhostPosition, my_grid)      # Passes current Agent 2 location and the next Path that Agent will have to take to get to the nearest ghost
            # if nextLocA2 == a2:   # Included to go towards ghost if there are no other paths present. Implemented this as Agent 2 cannot stay at same location
            #     nextLocA2=nearestGhostPosition
            path_to_take = {agentPosition: nextLocA2}
            if not nextLocA2 or my_grid[nextLocA2[0],nextLocA2[1]] < 0: # Returns False if there is no path or if index is out of bounds
                # return False
                path_to_take = {agentPosition: agentPosition}
        else:
            # If A Star path is present without ghost in path, agent will follow the A Star path
            # nextLocA2 = aStarPathDetermined[agentPosition]
            path_to_take = aStarPathDetermined
        return path_to_take
