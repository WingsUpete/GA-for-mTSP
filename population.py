"""
Collection of routes (chromosomes)
"""
from route import *


class Population:
    routes = []

    # Good old constructor
    def __init__(self, populationSz, initialise):
        self.populationSize = populationSz
        if initialise:
            for i in range(populationSz):
                newRoute = Route()  # Create empty route
                newRoute.generateIndividual()  # Add route sequences
                self.routes.append(newRoute)  # Add route to the population

    # Saves the route passed as argument at index
    def saveRoute(self, index, route):
        self.routes[index] = route

    # Returns route at index
    def getRoute(self, index):
        return self.routes[index]

    # Returns route with maximum fitness value
    def getFittest(self):
        fittest = self.routes[0]

        for i in range(1, self.populationSize):
            if fittest.getFitness() <= self.getRoute(i).getFitness():
                fittest = self.getRoute(i)

        return fittest

    def populationSize(self):
        return int(self.populationSize)

    # Equate current population values to that of pop
    def equals(self, pop):
        self.routes = pop.routes
