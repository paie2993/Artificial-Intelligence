# -*- coding: utf-8 -*-

import pickle
from random import choice
from random import seed
from domain import *


class Repository:
    def __init__(self, mapM=Map(MAP_LENGTH, MAP_LENGTH)):
        self.__mapM = mapM
        self.__populations = None

    def getMap(self):
        return self.__mapM

    def setMap(self, mapM):
        self.__mapM = mapM

    def getPopulations(self):
        return self.__populations

    def createPopulation(self, populationSize=POPULATION_SIZE, initialX=INITIAL_X, initialY=INITIAL_Y,
                         individualChromosomeSize=INDIVIDUAL_CHROMOSOME_SIZE):

        population = Population(populationSize, initialX, initialY, individualChromosomeSize, self.__mapM)

        if self.__populations is None:
            self.__populations = [population]
        else:
            self.__populations.append(population)
        return population

    #    add the other components for the Repository:
    #    load and save from file, etc
