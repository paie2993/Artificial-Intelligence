# -*- coding: utf-8 -*-

# Creating some colors
BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

# define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]

# define map size


# define square size
U = 20

# functionality constants
RANDOM_MAP_FILL = 0.2
MAP_LENGTH = 30
INITIAL_X = 10
INITIAL_Y = 10
TOTAL_RUNS = 2
NO_ITERATIONS = 50
POPULATION_SIZE = 50
INDIVIDUAL_CHROMOSOME_SIZE = 50
SELECTION_SIZE = 50
SELECTION_PRESSURE = 1.9
CROSSOVER_PROBABILITY = 0.5
MUTATE_PROBABILITY = 0.004

BEFORE_BREAK = 5000
SPEED = 1
MARK_SEEN = True
SEEDS = [66, 45, 15, 61, 6, 30, 36, 84, 7, 15, 92, 24, 42, 101, 69, 120, 18, 99, 29, 68, 88, 51, 60, 75, 5, 188, 52, 82,
         11, 21, 92, 58, 85, 77, 34, 25, 75, 38, 90, 23, 2, 73, 34, 79, 44, 85, 23, 7, 31, 38, 90, 47, 71, 61]


UP_DIR = [-1, 0]
LEFT_DIR = [0, -1]
DOWN_DIR = [1, 0]
RIGHT_DIR = [0, 1]
# STAY_DIR = [0, 0]
# DIRECTIONS = [STAY_DIR, UP_DIR, LEFT_DIR, DOWN_DIR, RIGHT_DIR]
DIRECTIONS = [UP_DIR, LEFT_DIR, DOWN_DIR, RIGHT_DIR]

N_CUTTING_POINTS = 5
