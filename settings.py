import math

RES = WIDTH, HEIGHT = 900, 600
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 0

PLAYER_POS = 1.5, 5   # initial location
PLAYER_ANGLE = 0  # initial angle
PLAYER_SPEED = 0.04  # how fast
PLAYER_ROT_SPEED = 0.02  #how fast you can rotate
PLAYER_SIZE_SCALE = 5

MOUSE_SENSITIVITY = 0.003
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT


FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
max_uses = 5

import pygame

map_data = []

with open("RandomMaze", "r") as file:
    for line in file:
        row = line.strip().split(",")
        map_data.append(row)

# Convert the map data to the desired format
mini_map = []
for row in map_data:
    mini_row = []
    for cell in row:
        if cell == "_":
            mini_row.append("_")
        else:
            mini_row.append(int(cell))
    mini_map.append(mini_row)
class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value != "_":
                    self.world_map[(i, j)] = value

    def draw(self):
        [pygame.draw.rect(self.game.screen, 'darkgrey', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]
