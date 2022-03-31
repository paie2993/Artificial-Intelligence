# -*- coding: utf-8 -*-

import pickle
from domain import *


class Repository:
    def __init__(self):
        self.__populations = []
        self.map = Map()

    def createPopulation(self, args):
        # TODO: args = [populationSize, individualGenomeSize] -- you can add more args
        lower = 0
        upper = self.map.n
        return Population(args[0], args[1], 0, upper, self.map)

    # TODO : add the other components for the Repository:
    #    load and save from file, etc
