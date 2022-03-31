from repository import *


class Controller:
    def __init__(self, repository=Repository()):
        self.__repository = repository

    def getRepository(self):
        return self.__repository

    def __iteration(self, population, k=SELECTION_SIZE):
        # selection of parents
        winners = population.selection(k)

        # create offspring by crossover of the parents
        crossoverProbability = CROSSOVER_PROBABILITY
        offspring = matingSeason(winners, crossoverProbability)

        # apply some mutations
        mutateProbability = MUTATE_PROBABILITY
        population.mutationSeason(mutateProbability)

        # selection of the survivors
        population.survivalOfTheFittest(offspring)

    def __run(self, population, noIterations=NO_ITERATIONS):
        fitnesses = []

        for i in range(noIterations):
            self.__iteration(population)
            # save the information needed for the statistics
            currentFitness = population.evaluate()
            fitnesses.append(currentFitness)

        return fitnesses

    def solver(self, totalRuns=TOTAL_RUNS, noIterations=NO_ITERATIONS, populationSize=POPULATION_SIZE,
               individualChromosomeSize=INDIVIDUAL_CHROMOSOME_SIZE):

        # run the algorithm
        statistics = []
        for i in range(totalRuns):
            # create the population,
            population = self.__repository.createPopulation(populationSize, individualChromosomeSize)

            # runResult = all the fitnesses from every iteration, for the currently tested population
            runResults = self.__run(population, noIterations)

            statistics.append(runResults)

        return statistics
