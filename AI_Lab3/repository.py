# -*- coding: utf-8 -*-

import pickle
from domain import *


class Repository:
    def __init__(self, mapM=Map()):
        self.__mapM = mapM
        self.__populations = None

    def getMap(self):
        return self.__mapM

    def getPopulations(self):
        return self.__populations

    def setMap(self, mapM):
        self.__mapM = mapM

    def createPopulation(self, populationSize=POPULATION_SIZE, individualChromosomeSize=INDIVIDUAL_CHROMOSOME_SIZE):
        population = Population(populationSize, individualChromosomeSize, self.__mapM)
        self.__populations.append(population)
        return population

    #    add the other components for the Repository:
    #    load and save from file, etc

