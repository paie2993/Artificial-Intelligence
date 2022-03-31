# -*- coding: utf-8 -*-

import pickle
from domain import *


class Repository:
    def __init__(self, mapM=Map()):
        self.__mapM = mapM
        self.__population = None

    def setMap(self, mapM):
        self.__mapM = mapM

    def createPopulation(self, populationSize=POPULATION_SIZE, individualChromosomeSize=INDIVIDUAL_CHROMOSOME_SIZE):
        population = Population(populationSize, individualChromosomeSize, self.__mapM)
        self.__population = population
        return population

    #    add the other components for the Repository:
    #    load and save from file, etc

    def loadMap(self, fileName):
        mapM = pickle.load(fileName)
        return
