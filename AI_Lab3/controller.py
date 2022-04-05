import datetime

from repository import *


class Controller:
    def __init__(self, repository=Repository()):
        self.__repository = repository

    def getRepository(self):
        return self.__repository

    def __iteration(self, population, k=SELECTION_SIZE, crossoverProbability=CROSSOVER_PROBABILITY):
        # selection of parents
        winners = population.selection(k)

        # create offspring by crossover of the parents
        offspring = matingSeason(winners, crossoverProbability)

        # apply some mutations
        mutateProbability = MUTATE_PROBABILITY
        population.mutationSeason(mutateProbability)

        # selection of the survivors
        population.survivalOfTheFittest(offspring)

    def __run(self, population, noIterations=NO_ITERATIONS, k=SELECTION_SIZE,
              crossoverProbability=CROSSOVER_PROBABILITY):

        fitnesses = []

        for i in range(noIterations):
            self.__iteration(population, k, crossoverProbability)
            # save the information needed for the statistics
            currentFitness = population.evaluate()
            fitnesses.append(currentFitness)
            # print(currentFitness)

        return fitnesses

    def solver(self, totalRuns=TOTAL_RUNS, noIterations=NO_ITERATIONS, populationSize=POPULATION_SIZE,
               initialX=INITIAL_X, initialY=INITIAL_Y, individualChromosomeSize=INDIVIDUAL_CHROMOSOME_SIZE,
               k=SELECTION_SIZE, crossoverProbability=CROSSOVER_PROBABILITY):

        # run the algorithm
        statistics = []
        for i in range(totalRuns):
            print("run " + str(i))

            startTime = datetime.datetime.now()

            # seed the run
            runSeed = choice(SEEDS)
            seed(runSeed)

            # create the population,
            population = self.__repository.createPopulation(populationSize, initialX, initialY,
                                                            individualChromosomeSize)

            # runResult = all the fitnesses from every iteration, for the currently tested population
            runResults = self.__run(population, noIterations, k, crossoverProbability)

            endTime = datetime.datetime.now()
            runTime = endTime - startTime

            # i = integer, number of the run
            # runSeed = integer, seed of the run
            # runResults = list of integers, representing the fitnesses of the population at every iteration
            statistics.append([i, runSeed, runResults, runTime])

            print("---------------------------------------------------------")

        return statistics


def buildPath(rootSquare, directions):
    path = [rootSquare]
    for direction in directions:
        previous = path[-1]
        currentX = previous[0] + direction[0]
        currentY = previous[1] + direction[1]
        path.append([currentX, currentY])
    return path
