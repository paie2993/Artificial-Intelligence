# -*- coding: utf-8 -*-

from random import randint, random
from utils import *
import numpy as np


# the class Gene can be replaced with int or float, or other types
# depending on your problem's representation

class Map:
    def __init__(self, n=mapLength, m=mapLength):
        self.n = n
        self.m = m
        self.surface = [[0 for j in range(self.n)] for i in range(self.m)]

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def isValid(self, square):
        return True if 0 <= square[0] < self.n and 0 <= square[1] < self.m else False

    def isBrick(self, square):
        if not self.isValid(square):
            raise Exception("invalid square: " + square)
        return True if self.surface[square[0]][square[1]] == 1 else False

    # square: pair of coordinates x,y
    # seenSquares: set of pairs of coordinates
    def visibleSquares(self, square, seenSquares):
        if not self.isValid(square):
            raise Exception("invalid square: " + square)

        # from inside a brick, neighbouring squares are not visible
        if self.isBrick(square):
            return

        x = square[0]
        y = square[1]
        for var in v:
            xx = x + var[0]
            yy = y + var[1]
            while self.isValid([xx, yy]) and not self.isBrick([xx, yy]):
                seenSquares.add([xx, yy])
                xx = x + var[0]
                yy = y + var[1]

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string


def areNeighbours(firstSquare, secondSquare):
    for var in v:
        if [firstSquare[0] + var[0], firstSquare[1] + var[1]] == secondSquare or firstSquare == secondSquare:
            return True
    return False


class Gene:
    def __init__(self, lower, upper):
        self.code = [randint(lower, upper), randint(lower, upper)]
        # random initialise the Gene according to the representation


class Individual:
    def __init__(self, chromosomeSize=0, mapM=Map()):  # subject to change
        self.__chromosomeSize = chromosomeSize
        # Linear discrete non-binary integer random representation
        self.__chromosome = [Gene(0, mapM.n) for i in range(self.__chromosomeSize)]  # subject to change
        self.__fitness = None
        self.__mapM = mapM

    def fitness(self):
        # 1. number of objectives       : single
        # 2. direction of optimization  : max
        # 3. precision                  : deterministic

        # higher number of empty squared covered means better individual

        # 1. paths must be cohesive (no jumping)
        # 2. paths must not include bricks
        # 3. paths must cover as many empty squares as possible

        # discontinuous sections of the map
        nonContinuous = 0
        for i in range(self.__chromosomeSize - 1):
            if not areNeighbours(self.__chromosome[i].code, self.__chromosome[i + 1].code):
                nonContinuous += 1

        # paths must not include bricks
        bricks = 0
        for gene in self.__chromosome:
            if self.__mapM.isBrick(gene.code):
                bricks += 1

        # paths must cover as many empty squares as possible
        seenSquares = set()
        for gene in self.__chromosome:
            self.__mapM.visibleSquares(gene.code, seenSquares)

        # fitness = - number of seen squares * (discontinuous tracks + bricks)
        fitnessValue = - len(seenSquares) * (nonContinuous + bricks)
        self.__fitness = fitnessValue
        return fitnessValue

    # Implements creep mutation
    def __creepMutation(self, creepValue, signProbability, mutateProbability, gene, coordinate):
        if coordinate not in [0, 1]:
            raise Exception("Index out of range: " + coordinate)
        if random() < mutateProbability:
            value = creepValue
            if random() < signProbability:
                value = -value
            gene.code[coordinate] = abs(gene.code[0] + value) % self.__mapM.n

    # Uses creep mutation
    def mutate(self, mutateProbability=0.04):
        creepValue = max(1, int(self.__mapM.n / self.__chromosomeSize))
        signProbability = 0.5

        for gene in self.__chromosome:
            self.__creepMutation(creepValue, signProbability, mutateProbability, gene, 0)
            self.__creepMutation(creepValue, signProbability, mutateProbability, gene, 1)

    def crossover(self, otherParent, crossoverProbability=0.8):
        offspring1, offspring2 = Individual(self.__chromosomeSize), Individual(self.__chromosomeSize)
        if random() < crossoverProbability:
            pass
            # perform the crossover between the self and the otherParent 

        return offspring1, offspring2


class Population:
    def __init__(self, populationSize=0, individualChromosomeSize=0, lower=0, upper=0, mapM=Map()):
        self.__populationSize = populationSize
        self.__individuals = [Individual(individualChromosomeSize, mapM) for i in range(populationSize)]

    def evaluate(self):
        # evaluates the population
        for individual in self.__individuals:
            individual.fitness()

    def selection(self, k=0):
        # perform a selection of k individuals from the population
        # and returns that selection
        pass
