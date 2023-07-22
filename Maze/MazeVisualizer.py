import pygame
import time
import random

grid_size = 400
fps = 30

WHITE = (255,255,255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)

# Pygame Initialize
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((grid_size, grid_size))
pygame.display.set_caption("Maze Generator")
clock = pygame.time.Clock()

# Maze Variables
x, y, w, = 0, 0, 20
grid = []
visited = []
stack = []
solution = []

# build the gridd
def build_grid(x, y, w):
    for i in range(1, 21):
        x = 20      # to start position
        y += 20     # new row
        for j in range(1, 21):
            pygame.draw.line(screen, WHITE, [x, y], [x+w, y])   # Cell top
            pygame.draw.line(screen, WHITE, [x+w, y], [x+w, y+w])   # Cell right
            pygame.draw.line(screen, WHITE, [x, y], [x, y+w])   # Cell left
            pygame.draw.line(screen, WHITE, [x, y+w], [x+w, y+w])   # Cell top
            pygame.draw.line(screen, WHITE, [x, y], [x+w, y])   # Cell top
            grid.append((x, y))     # add cell to grid list
            x += 20     # move cell to new position

build_grid(x, y, w)

running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
