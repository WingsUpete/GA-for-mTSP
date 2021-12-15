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
                newRoute = Route()              # Create empty route
                newRoute.generateIndividual()   # Add route sequences
                self.routes.append(newRoute)    # Add route to the population

    def saveRoute(self, index, route):
        """
        Saves the route passed as argument at index
        """
        self.routes[index] = route

    def getRoute(self, index):
        """
        Returns route at index
        """
        return self.routes[index]

    def getFittest(self):
        """
        Returns route with maximum fitness value
        """
        fittest = self.routes[0]

        for i in range(1, self.populationSize):
            if self.getRoute(i).getFitness() >= fittest.getFitness():
                fittest = self.getRoute(i)

        return fittest

    def populationSize(self):
        return int(self.populationSize)

    def equals(self, pop):
        """
        Equate current population values to that of pop
        """
        self.routes = pop.routes
