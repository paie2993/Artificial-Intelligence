# -*- coding: utf-8 -*-
import functools
from copy import deepcopy
from random import randint, random, choice
from utils import *
from functools import reduce


# the class Gene can be replaced with int or float, or other types
# depending on your problem's representation

class Map:
    def __init__(self, n=MAP_LENGTH, m=MAP_LENGTH):
        self.n = n
        self.m = m
        self.surface = [[0 for j in range(m)] for i in range(n)]

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
    def __init__(self):
        choiceDir = choice(DIRECTIONS)
        self.code = [choiceDir[0], choiceDir[1]]


class Chromosome:
    def __init__(self, initialX, initialY, chromosomeSize):
        rootGene = Gene()
        rootGene.code = [initialX, initialY]
        self.root = rootGene
        self.genes = [Gene() for i in range(chromosomeSize)]


def switch(first, second):
    aux = first
    first = second
    second = aux
    return first, second


class Individual:
    def __init__(self, initialX=INITIAL_X, initialY=INITIAL_Y, chromosomeSize=INDIVIDUAL_CHROMOSOME_SIZE, mapM=Map()):
        self.__mapM = mapM
        self.__chromosomeSize = chromosomeSize
        self.__chromosome = Chromosome(initialX, initialY, chromosomeSize)
        self.__fitness = None

    def getChromosome(self):
        return self.__chromosome

    def fitness(self):
        # 1. number of objectives       : single
        # 2. direction of optimization  : max
        # 3. precision                  : deterministic

        # higher number of empty squared covered means better individual

        # 1. paths must be inside map (valid squares)
        # 2. paths must not include bricks
        # 3. paths must cover as many empty squares as possible

        # build the path, equivalent to the solution presented by the Individual
        rootSquare = self.__chromosome.root.code
        directions = [gene.code for gene in self.__chromosome.genes]

        path = deepcopy([rootSquare])
        for direction in directions:
            previous = path[-1]
            currentX = previous[0] + direction[0]
            currentY = previous[1] + direction[1]
            path.append([currentX, currentY])

        # 1. penalize Individuals who's chromosome contains invalid genes or genes representing bricks
        nonValid = 0
        for square in path:
            if not self.__mapM.isValid(square) or self.__mapM.isBrick(square):
                nonValid += 1  # how many non-valid of brick squares are on the path

        # 2. paths must cover as many empty squares as possible
        seenSquares = set()
        for square in path:
            if self.__mapM.isValid(square):
                self.__mapM.visibleSquares(square, seenSquares)

        # 3. fitness = number of seen squares - non-valid squares
        fitnessValue = len(seenSquares) + nonValid
        if nonValid > 0:
            # by adding nonValid squares as positive value to the fitness, then negating the fitness values if nonValid
            # is not zero, paths that contain bricks or invalid squares are deterred
            fitnessValue = - fitnessValue

        self.__fitness = fitnessValue
        return fitnessValue

    #     old     |      new
    # -------------------------
    #    good     |     bad   ==> keep the old value
    #    good     |     good  ==> save the new value
    #    bad      |     bad   ==> save the new value
    #    bad      |     good  ==> save the new value

    # coding:   good = true
    #           bad  = false
    # Uses random resetting mutation
    def mutate(self, mutateProbability=MUTATE_PROBABILITY):
        rootSquare = self.__chromosome.root.code
        prev = [rootSquare[0], rootSquare[1]]
        oldQuality = True
        newQuality = False
        for gene in self.__chromosome.genes:
            currentX = prev[0] + gene.code[0]
            currentY = prev[1] + gene.code[1]
            currentPos = [currentX, currentY]

            if random() < mutateProbability:
                newDirection = choice(DIRECTIONS)
                newX = prev[0] + newDirection[0]
                newY = prev[1] + newDirection[1]
                newPos = [newX, newY]

                if self.__mapM.isValid(currentPos) and not self.__mapM.isBrick(currentPos):
                    oldQuality = True
                else:
                    oldQuality = False

                if self.__mapM.isValid(newPos) and not self.__mapM.isBrick(newPos):
                    newQuality = True
                else:
                    newQuality = False

                if oldQuality and not newQuality:
                    prev = [currentX, currentY]
                else:
                    gene.code = [newDirection[0], newDirection[1]]
                    prev = [newX, newY]
            else:
                prev = [currentX, currentY]

    # Implements N-cutting point crossover strategy
    def crossover(self, otherParent, crossoverProbability=CROSSOVER_PROBABILITY):
        nCuttingPoints = N_CUTTING_POINTS
        # variant: all the genes that can represent cutting points (index of the respective genes)
        variants = [i for i in range(self.__chromosomeSize)]

        offspring1, offspring2 = \
            Individual(self.__chromosome.root.code[0], self.__chromosome.root.code[1], self.__chromosomeSize,
                       self.__mapM), \
            Individual(self.__chromosome.root.code[0], self.__chromosome.root.code[1], self.__chromosomeSize,
                       self.__mapM)

        # the n-cutting points are chosen arbitrarily
        cuttingPoints = []
        for i in range(nCuttingPoints):
            randChoice = choice(variants)
            variants.remove(randChoice)
            cuttingPoints.append(randChoice)
        # sorting the cuttingPoints (which are indexes) ascending by value is very important; we'll see right below
        cuttingPoints.sort()

        # just copy the references to the parents, so we can switch them without affecting variables from
        # the outer scope
        firstParent = self
        secondParent = otherParent

        for i in range(self.__chromosomeSize):
            if cuttingPoints[0] == i:
                # switch parents
                firstParent, secondParent = switch(firstParent, secondParent)

                # passed a cutting point, parents were switched
                cuttingPoints.pop(0)

            offspring1.__chromosome.genes[i].code = deepcopy(firstParent.genes[i].code)
            offspring2.__chromosome.genes[i].code = deepcopy(secondParent.genes[i].code)

        return offspring1, offspring2
        # TODO: from a crossover, try to select a random one, or one that is beneficial


class Population:
    def __init__(self, populationSize=POPULATION_SIZE, initialX=INITIAL_X, initialY=INITIAL_Y,
                 individualChromosomeSize=INDIVIDUAL_CHROMOSOME_SIZE, mapM=Map()):

        self.__populationSize = populationSize
        self.__individuals = [Individual(initialX, initialY, individualChromosomeSize, mapM) for i in
                              range(populationSize)]

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
    # Implements rank selection
    def selection(self, k=SELECTION_SIZE):
        if k < 2:
            raise Exception("Can't select less than 2 individuals for reproduction: k = " + str(k))

        if k % 2 != 0:
            raise Exception("Can't select an odd number of individuals for reproduction: k = " + str(k))

        selectionPressure = SELECTION_PRESSURE
        if selectionPressure <= 1 or selectionPressure > 2:
            raise Exception("Selection pressure poorly chosen: " + str(selectionPressure))

        # there is no point in figuring out how to select from a population
        # with only one individual; hope for mutations
        if self.__populationSize <= 1:
            return deepcopy(self.__individuals * k)

        # sort individuals based on their fitness
        rankedList = [individual for individual in self.__individuals]
        # the fittest should be the last, with the highest rank <==> index (equivalent)
        rankedList.sort(reverse=False, key=Individual.fitness)

        # pair every individual with their linear ranking
        linearlyRankedList = []
        for i in range(len(rankedList)):
            # the lowest rank is 1, so for the element with index i, rank is i + 1 (indexing starts from 0)
            linearlyRankedList.append((rankedList[i], self.__linearRanking(selectionPressure, i + 1)))
        # order individuals such that the fittest are the first, the weakest last
        linearlyRankedList.reverse()

        # self.__populationSize == len(rankedList) == len(linearlyRankedList)

        # select k winners
        winners = []
        for i in range(k):
            threshold = random()
            partialSum = 0
            j = 0
            while partialSum < threshold and j < len(linearlyRankedList):
                partialSum += linearlyRankedList[j][1]
                # if the partial sum passes the threshold when the value of the current's individual linear rank
                # is added, then add the current individual to the list of winners
                if partialSum >= threshold:
                    winners.append(linearlyRankedList[j][0])
                    break
                j += 1

        for win in winners:
            print("fitness = " + str(win.fitness()))

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
        arena.sort(reverse=True, key=self.sortFunc)
        while len(arena) > self.__populationSize:
            # keep removing the weakest individuals until the demographics stabilizes
            arena.pop(-1)

        # at the end of the competition, the surviving individuals in the arena form our population
        self.__individuals = arena
        # TODO: make sure that Individuals with invalid squares are thrown outside


def matingSeason(winners, crossoverProbability=CROSSOVER_PROBABILITY):
    if len(winners) % 2 != 0:
        raise Exception("One individual does not have a mate.")

    # beforeBreak is added as a guard against infinite loops
    beforeBreak = BEFORE_BREAK
    offspring = []

    # winners should contain an even numbers of individuals
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

        winners.remove(parent1)
        winners.remove(parent2)

        offspring1, offspring2 = parent1.crossover(parent2, crossoverProbability)
        offspring.append(offspring1)
        offspring.append(offspring2)

    return offspring
