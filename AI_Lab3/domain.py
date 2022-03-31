# -*- coding: utf-8 -*-
import time
from copy import deepcopy
from random import randint, random
from utils import *
from functools import reduce


# the class Gene can be replaced with int or float, or other types
# depending on your problem's representation

class Map:
    def __init__(self, n=mapLength, m=mapLength):
        self.n = n
        self.m = m
        self.surface = [[0 for j in range(self.n)] for i in range(self.m)]

    def randomMap(self, fill=RANDOM_MAP_FILL):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def isValid(self, square):
        return True if 0 <= square[0] < self.n and 0 <= square[1] < self.m else False

    def isBrick(self, square):
        if not self.isValid(square):
            raise Exception("invalid square: " + str(square))
        return True if self.surface[square[0]][square[1]] == 1 else False

    # square: pair of coordinates x,y
    # seenSquares: set of pairs of coordinates
    def visibleSquares(self, square, seenSquares):
        if not self.isValid(square):
            raise Exception("invalid square: " + str(square))

        # from inside a brick, neighbouring squares are not visible
        if self.isBrick(square):
            return

        x = square[0]
        y = square[1]
        seenSquares.add((x, y))
        for var in v:
            xx = x + var[0]
            yy = y + var[1]
            while self.isValid([xx, yy]) and not self.isBrick([xx, yy]):
                seenSquares.add((xx, yy))
                xx = xx + var[0]
                yy = yy + var[1]

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string


def areNeighbours(firstSquare, secondSquare):
    if firstSquare == secondSquare:
        return True
    for var in v:
        if [firstSquare[0] + var[0], firstSquare[1] + var[1]] == secondSquare:
            return True
    return False


class Gene:
    def __init__(self, lower, upper):
        self.code = [randint(lower, upper), randint(lower, upper)]
        # random initialise the Gene according to the representation


class Individual:
    def __init__(self, chromosomeSize=0, mapM=Map()):
        self.__chromosomeSize = chromosomeSize
        # Linear discrete non-binary integer random representation
        self.__chromosome = [Gene(0, mapM.n) for i in range(self.__chromosomeSize)]
        self.__fitness = None
        self.__mapM = mapM

    def getChromosome(self):
        return self.__chromosome

    def fitness(self):
        # 1. number of objectives       : single
        # 2. direction of optimization  : max
        # 3. precision                  : deterministic

        # higher number of empty squared covered means better individual

        # 1. paths must be inside map (valid squares)
        # 1. paths must be cohesive (no jumping)
        # 2. paths must not include bricks
        # 3. paths must cover as many empty squares as possible

        # discontinuous sections of the map
        nonContinuous = 0
        for i in range(self.__chromosomeSize - 1):
            if not areNeighbours(self.__chromosome[i].code, self.__chromosome[i + 1].code):
                nonContinuous += 1

        # paths must not include bricks and all squares must be inside the map
        nonValid = 0
        for gene in self.__chromosome:
            if not self.__mapM.isValid(gene.code) or self.__mapM.isBrick(gene.code):
                nonValid += 1

        # paths must cover as many empty squares as possible
        seenSquares = set()
        for gene in self.__chromosome:
            if self.__mapM.isValid(gene.code):
                self.__mapM.visibleSquares(gene.code, seenSquares)

        print("Passed")

        # fitness = - number of seen squares * (discontinuous tracks + bricks)
        fitnessValue = - len(seenSquares) * (nonContinuous + nonValid)
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

    # Implements uniform crossover
    def crossover(self, otherParent, crossoverProbability=0.5):
        offspring1, offspring2 = Individual(self.__chromosomeSize, self.__mapM), Individual(self.__chromosomeSize,
                                                                                            self.__mapM)

        for i in range(self.__chromosomeSize):
            r = random()
            if r < crossoverProbability:
                offspring1.__chromosome[i].code = deepcopy(self.__chromosome[i].code)
                offspring2.__chromosome[i].code = deepcopy(otherParent.__chromosome[i].code)
            else:
                offspring1.__chromosome[i].code = deepcopy(self.__chromosome[i].code)
                offspring2.__chromosome[i].code = deepcopy(otherParent.__chromosome[i].code)

        return offspring1, offspring2


class Population:
    def __init__(self, populationSize=1, individualChromosomeSize=1, mapM=Map()):
        self.__populationSize = populationSize
        self.__individuals = [Individual(individualChromosomeSize, mapM) for i in range(populationSize)]

    def getIndividuals(self):
        return self.__individuals

    def evaluate(self):
        fitnesses = [individual.fitness() for individual in self.__individuals]
        return reduce(lambda a, b: a + b, fitnesses)

    def __linearRanking(self, selectionPressure, rank):
        if selectionPressure <= 1 or selectionPressure > 2:
            raise Exception("Selection pressure poorly chosen: " + str(selectionPressure))
        if self.__populationSize <= 1:
            raise Exception(
                "Cannot compute linear ranking when the population size is <= 1: " + str(self.__populationSize))
        if rank < 1:
            raise Exception("Rank incorrectly specified: " + str(rank))
        return (2 - selectionPressure) / self.__populationSize + \
               2 * rank * (selectionPressure - 1) / (self.__populationSize * (self.__populationSize - 1))

    # perform a selection of k individuals from the population
    # and returns that selection
    # 1. proportional selection
    # 2. rank selection
    # 3. tournament selection
    # Implements rank selection
    def selection(self, k=SELECTION_SIZE):
        if k < 2:
            raise Exception("Can't select less than 2 individuals for reproduction: k = " + str(k))

        selectionPressure = SELECTION_PRESSURE
        if selectionPressure <= 1 or selectionPressure > 2:
            raise Exception("Selection pressure poorly chosen: " + str(selectionPressure))

        # there is no point in figuring out how to select from a population
        # with only one individual; hope for mutations
        if self.__populationSize <= 1:
            return deepcopy(self.__individuals * k)

        # sort individuals based on their fitness
        rankedList = deepcopy(self.__individuals)
        # the fittest is the last
        rankedList.sort(key=Individual.fitness)

        # pair every individual with their linear ranking
        linearlyRankedList = []
        for i in range(self.__populationSize):
            # the lowest rank is 1, so for the element with index i, rank is i + 1 (indexing starts from 0)
            linearlyRankedList.append((self.__individuals[i], self.__linearRanking(selectionPressure, i + 1)))
        # order individuals such that the fittest are the first, the weakest last
        linearlyRankedList.reverse()

        # select k winners
        winners = []
        for i in range(k):
            threshold = random()
            partialSum = 0
            j = 0
            while partialSum < threshold and j < self.__populationSize:
                partialSum += linearlyRankedList[j][1]
                # if the partial sum passes the threshold when the value of the current's individual linear rank
                # is added, then add the current individual to the list of winners
                if partialSum >= threshold:
                    winners.append(linearlyRankedList[j][0])
                j += 1

        return winners

    def mutationSeason(self, mutateProbability=MUTATE_PROBABILITY):
        for individual in self.__individuals:
            individual.mutate(mutateProbability)

    # challengers: list of Individuals
    def survivalOfTheFittest(self, challengers):
        for challenger in challengers:
            if not isinstance(challenger, Individual):
                raise Exception("Only Individuals can enter the population")

        arena = self.__individuals + challengers

        # ELITISM: only the fittest survive from one generation to another
        arena.sort(reverse=True, key=Individual.fitness)
        while len(arena) > self.__populationSize:
            arena.pop(-1)
        self.__individuals = arena


def matingSeason(winners, crossoverProbability=CROSSOVER_PROBABILITY):
    beforeBreak = BEFORE_BREAK
    offspring = []
    while len(winners) > 0:

        first = randint(0, len(winners))
        second = randint(0, len(winners))
        i = 0
        while first != second and i < beforeBreak:
            first = randint(0, len(winners))
            second = randint(0, len(winners))
        if first == second:
            break

        parent1 = winners[first]
        parent2 = winners[second]

        i1 = winners.index(parent1)
        winners.remove(parent1)
        i2 = winners.index(parent2)
        winners.remove(parent2)

        offspring1, offspring2 = parent1.crossover(parent2, crossoverProbability)
        offspring.append(offspring1)
        offspring.append(offspring2)

    return offspring
