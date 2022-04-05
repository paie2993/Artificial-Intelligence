# -*- coding: utf-8 -*-


# imports
from statistics import mean, stdev

from gui import *
from repository import *
from domain import *
from controller import Controller, buildPath
import matplotlib.pyplot as plt


class UI:
    def __init__(self):
        self.__parameters = {
            "randomMapFill": RANDOM_MAP_FILL,
            "mapLength": MAP_LENGTH,
            "initialX": INITIAL_X,
            "initialY": INITIAL_Y,
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
        self.__statistics = None
        self.__controller = None

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

    def menuParametersSetup(self):
        print("a. view parameters\n" +
              "b. random map fill\n" +
              "c. map length\n" +
              "d. initial x\n" +
              "e. initial y\n" +
              "f. total runs\n" +
              "g. iterations per run\n" +
              "h. population size\n" +
              "i. individual chromosome size\n" +
              "j. selection size\n" +
              "k. selection pressure\n" +
              "l. crossover probability\n" +
              "m. mutate probability\n" +
              "x. back\n\n")

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
                self.__mapM = Map(self.__parameters["mapLength"])
                self.__mapM.randomMap(self.__parameters["randomMapFill"])
            elif option == "b":
                fileName = input("file name = ").strip()
                if whitespace in fileName:
                    print("Spaces are not allowed in file names: " + fileName)
                else:
                    try:
                        self.__mapM = pickle.load(open(fileName, "rb"))
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
                print()
                self.runParametersSetup()
            elif option == "b":
                self.runSolver()
            elif option == "c":
                self.runVisualiseStatistics()
            elif option == "d":
                self.runViewDrone()
                pass
            elif option == "x":
                done = True
            else:
                print("Invalid command")
                time.sleep(0.5)

    def runParametersSetup(self):
        done = False
        while not done:
            self.menuParametersSetup()
            option = input("Option: ").strip().lower()
            if option == "a":
                for key in self.__parameters:
                    print(key + ": " + str(self.__parameters[key]))
                print()
            elif option == "b":
                try:
                    value = float(input("random map fill (0 < x < 1) = "))
                    self.__parameters["randomMapFill"] = value
                except Exception as ex:
                    print(ex)
            elif option == "c":
                try:
                    value = int(input("map length (2 < x) = "))
                    self.__parameters["mapLength"] = value
                except Exception as ex:
                    print(ex)
            elif option == "d":
                try:
                    value = int(input("initial X (0 < x < mapLength) = "))
                    self.__parameters["initialX"] = value
                except Exception as ex:
                    print(ex)
            elif option == "e":
                try:
                    value = int(input("initial Y (0 < x < mapLength) = "))
                    self.__parameters["initialY"] = value
                except Exception as ex:
                    print(ex)
            elif option == "f":
                try:
                    value = int(input("total runs (1 <= x <= 60) = "))
                    self.__parameters["totalRuns"] = value
                except Exception as ex:
                    print(ex)
            elif option == "g":
                try:
                    value = int(input("iterations per run (1 <= x) = "))
                    self.__parameters["iterationsPerRun"] = value
                except Exception as ex:
                    print(ex)
            elif option == "h":
                try:
                    value = int(input("population size (2 <= x) = "))
                    self.__parameters["populationSize"] = value
                except Exception as ex:
                    print(ex)
            elif option == "i":
                try:
                    value = int(input("individual chromosome size (1 <= x) = "))
                    self.__parameters["individualChromosomeSize"] = value
                except Exception as ex:
                    print(ex)
            elif option == "j":
                try:
                    value = int(input("selection size (2 <= x) = "))
                    self.__parameters["selectionSize"] = value
                except Exception as ex:
                    print(ex)
            elif option == "k":
                try:
                    value = float(input("selection pressure (1 < x <= 2) = "))
                    self.__parameters["selectionPressure"] = value
                except Exception as ex:
                    print(ex)
            elif option == "l":
                try:
                    value = float(input("crossover probability (0 <= x <= 1) = "))
                    self.__parameters["crossoverProbability"] = value
                except Exception as ex:
                    print(ex)
            elif option == "m":
                try:
                    value = float(input("mutate probability (0 < x <= 1) = "))
                    self.__parameters["mutateProbability"] = value
                except Exception as ex:
                    print(ex)
            elif option == "x":
                done = True
            else:
                print("Invalid command")
                time.sleep(0.5)

    def runSolver(self):
        if self.__mapM is None:
            print("No map defined")
            return
        # instantiate the necessary objects
        repository = Repository(self.__mapM)
        self.__controller = Controller(repository)

        # initialize the arguments for the solver
        totalRuns = self.__parameters["totalRuns"]
        noIterations = self.__parameters["iterationsPerRun"]
        populationSize = self.__parameters["populationSize"]
        initialX = self.__parameters["initialX"]
        initialY = self.__parameters["initialY"]
        individualChromosomeSize = self.__parameters["individualChromosomeSize"]
        k = self.__parameters["selectionSize"]
        crossoverProbability = self.__parameters["crossoverProbability"]

        # run the solver and retrieve the information
        statistics = self.__controller.solver(totalRuns, noIterations, populationSize, initialX, initialY,
                                              individualChromosomeSize, k, crossoverProbability)
        self.__statistics = statistics

    def preconditionsValidation(self):
        if self.__controller is None:
            print("Controller is not initialized (consider running the solver first)")
            return False
        repository = self.__controller.getRepository()
        if repository is None:
            print("Repository is not initialized (consider running the solver first)")
            return False
        populations = repository.getPopulations()
        if populations is None or len(populations) == 0:
            print("There aren't any paths available (consider running the solver first)")
            return False
        return True

    def runVisualiseStatistics(self):
        firstCondition = self.preconditionsValidation()
        if firstCondition:
            if self.__statistics is None or len(self.__statistics) == 0:
                print("There isn't any statistical data about the solutions (consider running the solver first)")
                return
            else:
                print("No. run|\tSeed for random|\tFitness|\t\ttStandard deviation|")
                for statistic in self.__statistics:
                    avgFitness = mean(statistic[2])
                    stdFitness = stdev(statistic[2])
                    print(str(statistic[0]) + "\t\t\t" + str(statistic[1]) + "\t\t\t\t" + str(avgFitness) + "\t" + str(
                        stdFitness))

                    iterations = [i for i in range(len(statistic[2]))]
                    fitnesses = statistic[2]
                    plt.plot(iterations, fitnesses)
                    plt.xlabel("iterations")
                    plt.ylabel("fitnesses")
                    plt.show()
                    time.sleep(1)

    def runViewDrone(self):
        condition = self.preconditionsValidation()
        if condition:
            self.runChoosePopulation(self.__controller.getRepository().getPopulations())

    def runChoosePopulation(self, populations):
        numberOfPopulations = len(populations)
        done = False
        while not done:
            print("There are " + str(numberOfPopulations) + " populations.")
            option = input("Choose one (from 0 to " + str(numberOfPopulations - 1) + " , x to quit): ").strip().lower()
            if option == "x":
                done = True
            else:
                populationNumber = -1
                try:
                    populationNumber = int(option)
                except Exception as ex:
                    print(ex)
                    print("Invalid option: " + option)
                    time.sleep(0.5)
                if populationNumber < 0 or populationNumber >= numberOfPopulations:
                    print("Invalid population number")
                    time.sleep(0.5)
                else:
                    population = populations[populationNumber]
                    self.runChooseIndividual(population)

    def runChooseIndividual(self, population):
        numberOfIndividuals = len(population.getIndividuals())
        done = False
        while not done:
            print("There are " + str(numberOfIndividuals) + " individuals in the population.")
            option = input("Choose one (from 0 to " + str(numberOfIndividuals - 1) + " , x to quit): ").strip().lower()
            if option == "x":
                done = True
            else:
                individualNumber = -1
                try:
                    individualNumber = int(option)
                except Exception as ex:
                    print(ex)
                    print("Invalid option: " + option)
                    time.sleep(0.5)
                if individualNumber < 0 or individualNumber >= numberOfIndividuals:
                    print("Invalid individual number: " + str(individualNumber))
                    time.sleep(0.5)
                else:
                    currentMap = self.__controller.getRepository().getMap()

                    individual = population.getIndividuals()[individualNumber]
                    rootSquare = individual.getChromosome().root.code
                    directions = [gene.code for gene in individual.getChromosome().genes]

                    path = buildPath(rootSquare, directions)
                    speed = SPEED
                    markSeen = MARK_SEEN

                    movingDrone(currentMap, path, speed, markSeen)
