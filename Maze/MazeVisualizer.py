import pygame
import time
import random
from utils import variables, algorithms
from maze import Maze
from ghosts import Ghosts

# Maze Variables
grid = []
visited = []
stack = []
solution = []

# Pygame visualizer variables
window_size = variables.GRID_WIDTH*variables.GRID_SIZE + variables.GRID_WIDTH*2 # 440
fps = 5

# Pygame Initialize
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Ghosts in the Maze")
clock = pygame.time.Clock()

# Import images
IMG_GHOST = pygame.image.load('Images/Ghost.jpeg').convert_alpha()

# build the gridd
def build_grid(maze):
    screen.fill((0,0,0))        # Coloring the bg black
    x, y, w = 0, 0, variables.GRID_WIDTH
    env_grid = maze.get_my_grid()
    for i in range(variables.GRID_SIZE):            # To draw the lines
        x = w      # to start position
        y += w     # new row
        grid.append([])
        for j in range(variables.GRID_SIZE):
            # Drawing the Walls
            if ((env_grid[i][j] % 10) != 0):
                RECT_WALL = pygame.Rect(x, y, variables.GRID_WIDTH, variables.GRID_WIDTH)
                pygame.draw.rect(screen, variables.CLR_WALL, RECT_WALL)
            # Drawing determined path
            if ((i, j) in aStarPathDetermined.keys()):
                RECT_PATH = pygame.Rect(x, y, variables.GRID_WIDTH, variables.GRID_WIDTH)
                pygame.draw.rect(screen, variables.CLR_PATH, RECT_PATH)
            # Putting ghosts
            if (env_grid[i][j] < 0):
                RECT_GHOST = IMG_GHOST.get_rect(topleft = (x + variables.ADJUSTER1, y))
                screen.blit(IMG_GHOST, RECT_GHOST)
            # Drawing the walls
            pygame.draw.line(screen, variables.CLR_LINE, [x, y], [x+w, y])   # Cell top
            pygame.draw.line(screen, variables.CLR_LINE, [x+w, y], [x+w, y+w])   # Cell right
            pygame.draw.line(screen, variables.CLR_LINE, [x, y], [x, y+w])   # Cell left
            pygame.draw.line(screen, variables.CLR_LINE, [x, y+w], [x+w, y+w])   # Cell top
            grid[i].append((x, y))     # add cell to grid list
            x += w     # move cell to new position


maze = Maze()
ghosts = Ghosts(maze, num_ghosts=8)
aStarPathDetermined = algorithms.a_star(maze.my_grid)       # Agemt 1 Path
print(aStarPathDetermined)
a_one_pos = (variables.START_X, variables.START_Y)
build_grid(maze)
print(maze.get_my_grid())


# RECT_GHOST = IMG_GHOST.get_rect(topleft = (grid[0][0][0] + variables.ADJUSTER1, grid[0][0][1]))
# pos_currcell_x = grid[10][4][0]
# pos_currcell_y = grid[10][4][1]
# RECT_CURRCELL = pygame.Rect(grid[10][4][0], grid[10][4][1], variables.GRID_WIDTH, variables.GRID_WIDTH)
RECT_CURRCELL = pygame.Rect(variables.START_X, variables.START_Y, variables.GRID_WIDTH, variables.GRID_WIDTH)

running = True
simulation = True
build_grid(maze)
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if simulation == True:
        if a_one_pos == (variables.GRID_SIZE - 1, variables.GRID_SIZE - 1) or maze.my_grid[a_one_pos[0]][a_one_pos[1]] != 0:
            simulation = False
            # running = False
            # break
        else:
            nextLocA1 = aStarPathDetermined[a_one_pos]
        ghosts.ghostmovement(maze.my_grid)
        
        pygame.draw.rect(screen, variables.CLR_CURRCELL, RECT_CURRCELL)
        pygame.display.update()
        RECT_CURRCELL.x = variables.GRID_WIDTH * nextLocA1[1] + variables.GRID_WIDTH
        RECT_CURRCELL.y = variables.GRID_WIDTH * nextLocA1[0] + variables.GRID_WIDTH

        build_grid(maze)     # Building the lines
        print(a_one_pos)

        a_one_pos = nextLocA1




def agentRun():
    pass
