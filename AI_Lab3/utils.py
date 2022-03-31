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
mapLength = 20

# define square size
U = 20

# functionality constants
RANDOM_MAP_FILL = 0.2
TOTAL_RUNS = 30
NO_ITERATIONS = 30
POPULATION_SIZE = 2
INDIVIDUAL_CHROMOSOME_SIZE = 1
SELECTION_SIZE = 2
SELECTION_PRESSURE = 1.6
CROSSOVER_PROBABILITY = 0.5
MUTATE_PROBABILITY = 0.04

BEFORE_BREAK = 5000
SPEED = 1
MARK_SEEN = True
