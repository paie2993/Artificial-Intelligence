from repository import *
from random import choice


class Controller:
    def __init__(self, repository=Repository()):
        self.__repository = repository

    def setMap(self, mapM):
        self.__repository.setMap(mapM)

    def iteration(self, population, k=SELECTION_SIZE):
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

    def run(self, population, noIterations=NO_ITERATIONS):
        fitnesses = []

        for i in range(noIterations):
            self.iteration(population)
            # save the information needed for the statistics
            currentFitness = population.evaluate()
            fitnesses.append(currentFitness)

        return fitnesses

    def solver(self, totalRuns=TOTAL_RUNS, populationSize=POPULATION_SIZE, individualChromosomeSize=INDIVIDUAL_CHROMOSOME_SIZE):
        # create the population,
        population = self.__repository.createPopulation(populationSize, individualChromosomeSize)
        noIterations = NO_ITERATIONS

        # run the algorithm
        results = []
        for i in range(totalRuns):
            runResults = self.run(population, noIterations)
            results.append(runResults)

        # return the results and the statistics
        return results