# -*- coding: utf-8 -*-


# imports
from gui import *
from controller import *
from repository import *
from domain import *


class UI:
    def __init__(self):
        self.__parameters = {
            "randomMapFill": RANDOM_MAP_FILL,
            "totalRuns": TOTAL_RUNS,
            "iterationsPerRun": NO_ITERATIONS,
            "populationSize": POPULATION_SIZE,
            "individualChromosomeSize": INDIVIDUAL_CHROMOSOME_SIZE,
            "selectionSize": SELECTION_SIZE,
            "selectionPressure": SELECTION_PRESSURE,
            "crossoverProbability": CROSSOVER_PROBABILITY,
            "mutateProbability": MUTATE_PROBABILITY
        }
        self.__mapM = None

    def mainMenu(self):
        print("1. map options\n" +
              "2. EA options\n" +
              "x. exit\n\n")

    def menuMap(self):
        print("a. create random map\n" +
              "b. load a map\n" +
              "c. save a map\n" +
              "d. visualise map\n"
              "x. back\n\n")

    def menuEA(self):
        print("a. parameters setup\n" +
              "b. run the solver\n" +
              "c. visualise the statistics\n" +
              "d. view the drone moving on a path\n" +
              "x. back\n\n")

    def menuParameters(self):
        done = False
        while not done:
            pass

    def runMain(self):
        done = False
        while not done:
            self.mainMenu()
            option = input("Option: ").strip()
            if option == "1":
                self.runMap()
            elif option == "2":
                self.runEA()
            elif option == "x":
                print("Goodbye!")
                time.sleep(0.5)
                done = True
            else:
                print("Invalid command")
                time.sleep(0.5)

    def runMap(self):
        whitespace = " "
        done = False
        while not done:
            self.menuMap()
            option = input("Option: ").strip().lower()
            if option == "a":
                mapM = Map()
                mapM.randomMap(RANDOM_MAP_FILL)
            elif option == "b":
                fileName = input("file name = ").strip()
                if whitespace in fileName:
                    print("Spaces are not allowed in file names: " + fileName)
                else:
                    try:
                        mapM = pickle.load(open(fileName, "rb"))
                    except Exception as ex:
                        print(ex)
            elif option == "c":
                if self.__mapM is None:
                    print("No map has been created")
                else:
                    fileName = input("file name = ").strip()
                    if whitespace in fileName:
                        print("Spaces are not allowed in file names")
                    else:
                        try:
                            pickle.dump(self.__mapM, open(fileName, "wb"))
                        except Exception as ex:
                            print(ex)
            elif option == "d":
                if self.__mapM is None:
                    print("No map has been created")
                else:
                    print(self.__mapM)
            elif option == "x":
                done = True
            else:
                print("Invalid command")
                time.sleep(0.5)

    def runEA(self):
        done = False
        while not done:
            self.menuEA()
            option = input("Option: ").strip().lower()
            if option == "a":
                pass
            elif option == "b":
                pass
            elif option == "c":
                pass
            elif option == "d":
                pass
            elif option == "x":
                done = True
            else:
                print("Invalid command")
                time.sleep(0.5)

#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markSeen)
#              ATENTION! the function doesn't check if the path passes trough walls
