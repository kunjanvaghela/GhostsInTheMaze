import numpy as np
from maze import Maze
from utils import variables, algorithms
import math

class Ghosts(object):
    """docstring for Ghosts."""

    def __init__(self, maze, num_ghosts):
        super(Ghosts, self).__init__()
        self.num_ghosts = num_ghosts
        self.place_ghosts(maze)

    # my_grid = place_ghosts(nr_of_ghosts) # -- Previously was called from create_env

    # This function will call get_ghost_cell_index() to create ghosts based on number of ghosts received.
    def place_ghosts(self, maze: Maze):
        invalid_indices = maze.get_invalid_indices()
        for i in range(self.num_ghosts):
            row_ind, col_ind = self.get_ghost_cell_index(maze, invalid_indices)
            # maze.set_my_grid_value(row_ind, col_ind, )
            maze.my_grid[row_ind][col_ind] -= 10
            # my_grid[row_ind][col_ind] = my_grid[row_ind][col_ind] - 10
        # return my_grid




    # Method for Random movements for ghosts,
    # It accounts for Ghosts position at call [spawn if Timestamp=0] considers the probability of moving to LUDR directions
    # Or Stay at the same place.
    def ghostmovement(self, my_grid):
        ghostPositionList = np.argwhere(my_grid < 0)      # Gets all the ghost coordinates in this list
        for index in ghostPositionList:
            no_of_ghosts = (math.ceil(abs(my_grid[index[0],index[1]]/10)))
            while no_of_ghosts > 1:
                ghostPositionList = np.append(ghostPositionList,index)
                no_of_ghosts = no_of_ghosts - 1
        ghostPositionList = ghostPositionList.reshape((ghostPositionList.size)//2,2)
        for list in ghostPositionList:              # Visits each ghost in the list
            #L=(1) U=(2) D=(3) R=(4)
            if(list[0]==0 and list[1]==0): #START :CANT GO UP AND LEFT
                    direction=np.random.choice([3,4])
            elif(list[0]==0 and list[1]==(variables.GRID_SIZE - 1)): #RIGHT TOP :CANT GO UP AND RIGHT
                    direction=np.random.choice([1,3])
            elif(list[0]==(variables.GRID_SIZE - 1) and list[1]==0): #BOTTOM LEFT :CANT GO DOWN AND LEFT
                    direction=np.random.choice([2,4])
            elif(list[1]==(variables.GRID_SIZE - 1) and list[1]==(variables.GRID_SIZE - 1)): #GOAL :CANT GO DOWN AND RIGHT
                    direction=np.random.choice([1,2])
            elif(list[1]==0):
                    direction=np.random.choice([2,3,4])     # If ghost is on the left most cell, can only go Up, Down and Right
            elif(list[0]==0):
                    direction=np.random.choice([1,3,4])     # If ghost is on the top most cell, can only go Left, Down and Right
            elif(list[0]==(variables.GRID_SIZE - 1)):
                    direction=np.random.choice([1,2,4])     # If ghost is on the bottom most cell, can only go Left, Up and Right
            elif(list[1]==(variables.GRID_SIZE - 1)):
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
                if (my_grid[list[0]+1][list[1]]==0 or my_grid[list[0]+1][list[1]]%10==0) and (list[0]<variables.GRID_SIZE) : #OPEN CELL
                    my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                    my_grid[list[0]+1][list[1]]=my_grid[list[0]+1][list[1]]-10
                    list[0]=list[0]+1
                elif (my_grid[list[0]+1][list[1]]==1 or my_grid[list[0]+1][list[1]]%10!=0) and (list[0]<variables.GRID_SIZE): #BLOCKED CELL
                    directionIfBlocked=np.random.randint(low=0, high=2) #0=Stay, 1 =Go inside the Block
                    if directionIfBlocked==1:
                        # print('MOVE TO BLOCKED')
                        my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                        my_grid[list[0]+1][list[1]]=my_grid[list[0]+1][list[1]]-10
                        list[0]=list[0]+1
                    # else: print('STAY @ CURRENT')#STAY -NO CHANGE IF WALL IS BLOCKED
            else :#GO-RIGHT
                if (my_grid[list[0]][list[1]+1]==0 or my_grid[list[0]][list[1]+1]%10==0) and (list[1]<variables.GRID_SIZE) : #OPEN CELL
                    my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                    my_grid[list[0]][list[1]+1]=my_grid[list[0]][list[1]+1]-10
                    list[1]=list[1]+1
                elif (my_grid[list[0]][list[1]+1]==1 or my_grid[list[0]][list[1]+1]%10!=0) and (list[1]<variables.GRID_SIZE): #BLOCKED CELL
                    directionIfBlocked=np.random.randint(low=0, high=2) #0=Stay, 1 =Go inside the Block
                    if directionIfBlocked==1:
                        # print('MOVE TO BLOCKED')
                        my_grid[list[0]][list[1]]=my_grid[list[0]][list[1]]+10
                        my_grid[list[0]][list[1]+1]=my_grid[list[0]][list[1]+1]-10
                        list[1]=list[1]+1
                    # else: print('STAY @ CURRENT')#STAY -NO CHANGE IF WALL IS BLOCKED



    # To get randomly generated coordinates to spawn ghosts.
    def get_ghost_cell_index(self, maze: Maze, invalid_indices):
        while True:
            row_index = np.random.randint(0, variables.GRID_SIZE)
            column_index = np.random.randint(0, variables.GRID_SIZE)
            # print('Random coordinate of Ghost populated : '+str(row_index)+','+str(column_index))
            # Checks if the randomly generated coordinates is not within invalid_indices, and then returns the coordinates.
            if [row_index,column_index] not in invalid_indices:
                #print('Indices are valid.')
                if row_index==0 and column_index==0:
                    print('row_index==0 and column_index==0; invalid_indices : '+ str(invalid_indices))
                    continue
                if maze.my_grid[row_index,column_index]==1:
                    print('Generated ghost on Blocked wall : '+str(row_index)+','+str(column_index))
                if (algorithms.depth_first_search(maze.my_grid, row_index, column_index)):
                    # print('Ghost populated')
                    return row_index, column_index
            else:
                # print('Invalid Indices found')
                continue    # Can remove this in final code
