from routes import *


class Population:
    """
    Collection of routes (chromosomes)
    """
    routes = []

    # Good old constructor
    def __init__(self, populationSz, initialise):
        self.populationSize = populationSz
        if initialise:
            for i in range(populationSz):
                newRoute = Routes()             # Create empty routes
                newRoute.generateIndividual()   # Generate routes sequences
                self.routes.append(newRoute)    # Add routes to the population

    def saveRoute(self, index, curRoutes):
        """
        Saves the routes passed as argument at index
        """
        self.routes[index] = curRoutes

    def getRoute(self, index):
        """
        Returns routes at index
        """
        return self.routes[index]

    def getFittest(self):
        """
        Returns routes with maximum fitness value
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
