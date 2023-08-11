import pygame
import time
import random
from utils import variables, algorithms
from maze import Maze
from ghosts import Ghosts
from agent import Agent

# Maze Variables
grid = []
visited = []
agent_type = variables.AGENT_TYPE
num_ghosts = variables.MIN_GHOST
agentSurvivability = []

# Pygame visualizer variables
window_size = variables.GRID_WIDTH*variables.GRID_SIZE + variables.GRID_WIDTH*2 # 440

# Pygame Initialize
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((window_size, window_size + 50))
pygame.display.set_caption("Ghosts in the Maze")
clock = pygame.time.Clock()

# Import images
IMG_GHOST = pygame.image.load('Images/Ghost.jpeg').convert_alpha()

# Draw Text Function
text_font = pygame.font.SysFont(name=variables.FONT_NAME, size=variables.FONT_SIZE, bold=variables.FONT_BOLD, italic=variables.FONT_ITALIC)
def draw_text(text, x, y):
    img = text_font.render(text, True, variables.FONT_COLOR)
    screen.blit(img, (x, y))

def simulation_stats():
    draw_text("Agent : "+str(agent_type), 20, window_size)
    draw_text("Nr of Ghosts : "+str(num_ghosts), 20, window_size + 15)
    draw_text("Simulation : "+str(agentSurvivability), 20, window_size + 30)

# Initialize Maze, Ghosts and Agent
def init_maze_ghost_agent():
    global maze, ghosts, agent, path_determined, agent_position, RECT_CURRCELL
    maze = Maze()
    ghosts = Ghosts(maze, num_ghosts=num_ghosts)
    agent = Agent(agent_type)
    if agent.get_agent_type() == 1:
        path_determined = agent.agent_one_traversal(maze)       # Agemt 1 Path
        agent_position = (variables.START_X, variables.START_Y)
    elif agent.get_agent_type() == 2:
        agent_position = (variables.START_X, variables.START_Y)
        path_determined = agent.agent_two_traversal(maze, agent_position)       # Agemt 2 Path
    RECT_CURRCELL = pygame.Rect(agent_position[0], agent_position[1], variables.GRID_WIDTH, variables.GRID_WIDTH)       # for Agent

# build the gridd
def build_grid():       # Need to set maze grid, path_determined, agent, RECT_CURRCELL
    global agent, maze, path_determined

    screen.fill(variables.CLR_BACKGROUND)        # Coloring the bg black
    x, y, w = variables.START_X, variables.START_Y, variables.GRID_WIDTH
    env_grid = maze.get_my_grid()

    # Agent based conditions
    if agent.get_agent_type() == 1:
        pass
    elif agent.get_agent_type() == 2:
        path_determined = agent.agent_two_traversal(maze, agent_position)
        # agent_position = (variables.START_X, variables.START_Y)

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
            if ((i, j) in path_determined.keys()):
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
    # Drawing win position
    RECT_PATH = pygame.Rect(x - w + 1, y + 1, variables.GRID_WIDTH - 1, variables.GRID_WIDTH - 1)  # To not overwrite lines
    pygame.draw.rect(screen, variables.CLR_PATH, RECT_PATH)
    # Drawing Agent
    RECT_CURRCELL.x = variables.GRID_WIDTH * agent_position[1] + variables.GRID_WIDTH
    RECT_CURRCELL.y = variables.GRID_WIDTH * agent_position[0] + variables.GRID_WIDTH
    pygame.draw.rect(screen, variables.CLR_CURRCELL, RECT_CURRCELL)


init_maze_ghost_agent()

running = True
simulation = True
build_grid()
while running:
    clock.tick(variables.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if simulation == False:
        if len(agentSurvivability) < variables.SIMULATIONS_PER_SETTING:
            init_maze_ghost_agent()
            simulation = True
        else:
            if 1 in agentSurvivability:
                num_ghosts += 1
                agentSurvivability = []
                init_maze_ghost_agent()
                simulation = True
        time.sleep(variables.WAIT_TIME_AFTER_EACH_RESULT)



    if simulation == True:
        ghosts.ghostmovement(maze.my_grid)
        nextLocA1 = path_determined[agent_position]
        
        print(agent_position)
        agent_position = nextLocA1
        build_grid()     # Building the lines
        simulation_stats()
        if agent_position == (variables.GRID_SIZE - 1, variables.GRID_SIZE - 1) or maze.my_grid[agent_position[0]][agent_position[1]] != 0:
            if maze.my_grid[agent_position[0]][agent_position[1]] != 0:
                agentSurvivability.append(0)
                draw_text("Agent Lost!", 300, window_size)
            elif agent_position == (variables.GRID_SIZE - 1, variables.GRID_SIZE - 1):
                agentSurvivability.append(1)
                draw_text("Agent Won!!!", 300, window_size)
            simulation = False
        pygame.display.update()
        