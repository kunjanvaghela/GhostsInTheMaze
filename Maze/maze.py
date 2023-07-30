from utils import algorithms
from utils import variables
import numpy as np

class Maze(object):
    """docstring for Maze."""

    def __init__(self):
        super(Maze, self).__init__()
        self.my_grid=[]              # To store grid, changes when ghost traverses will happen in this directly.
        self.invalid_indices=[]      # To store indices which are blocked, and where ghost cannot pop up
        self.a2Mazes = dict()        #Dictionary with key as NoOfMazes, value as List of all mazes generated for Agent2          # What is the use????
        # self.search_alg = SearchAlgorithms()
        self.create_env()

    # To create the grid
    def create_grid(self, blocked_cell=0.28):
        while True:
            self.my_grid = np.random.rand(variables.GRID_SIZE, variables.GRID_SIZE)
            self.my_grid = np.where(self.my_grid <= blocked_cell, 1, 0)        # Populates grid with 1 (Blocked cell) and 0 (Unblocked cell) based on probability given by blocked_cell.
            self.my_grid[0][0]=0        # Start position and goal must be unblocked
            self.my_grid[variables.GRID_SIZE - 1, variables.GRID_SIZE - 1] = 0
            if (algorithms.depth_first_search(self.my_grid, variables.GRID_SIZE - 1, variables.GRID_SIZE - 1)):     # To check using Depth First Search if grid has a path to reach from the start to the goal
                break
        # return my_grid

    def create_env(self):
        # if nr_of_ghosts in self.a2Mazes:
        #     self.a2Mazes[nr_of_ghosts].append(self.my_grid)
        # else:
        #     self.a2Mazes[nr_of_ghosts] = [self.my_grid]
        self.create_grid()
        self.set_invalid_indices()
        self.invalid_indices = self.invalid_indices.tolist()


    def set_invalid_indices(self):
        self.invalid_indices = np.argwhere(self.my_grid == 1)
        self.invalid_indices = np.append(self.invalid_indices, [[0,0]], axis=0)
        self.invalid_indices = np.append(self.invalid_indices, [[variables.GRID_SIZE - 1, variables.GRID_SIZE - 1]], axis=0)
    
    def get_my_grid(self):
        return self.my_grid
    
    def get_invalid_indices(self):
        return self.invalid_indices
    
    def set_my_grid_value(self, i, j, val):
        self.my_grid[i][j] = val