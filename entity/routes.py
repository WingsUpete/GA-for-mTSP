import random

from globals import *
from .city import City, Cities
from util import route_lengths


class Routes:
    """
    Represents the chromosomes in GA's population.
    The object is collection of individual routes taken by trucks.
    """
    # Good old constructor
    def __init__(self, routes=None):
        # 2D (m, ?) array which is collection of respective routes taken by trucks
        self.routes = []
        # 1D (n-1,) array having routes in a series - used during crossover operation
        self.base = []
        # 1D (m,) array having route lengths (here, route length = number of nodes)
        self.routeLengths = route_lengths()

        for i in range(numSalesmen):
            self.routes.append([])

        # fitness value and total distance of all routes
        self.fitness = 0
        self.distance = 0

        # creating empty routes
        if routes is None:
            for i in range(Cities.numberOfCities() - 1):
                self.base.append(City(-1, -1))
        else:
            self.routes = routes

    def generateIndividual(self):
        """
        we have all route lengths summed up as upper = n+m-1
        1. For each route, length is 1 + (l-1) = l;
        2. For all routes, lengths add up to n+m-1 - m = n-1, using up all nodes except node 0
        """
        # put 1st member of Cities as it is (It represents the initial node) and shuffle the rest before adding
        for d_index in range(1, Cities.numberOfCities()):
            self.base[d_index - 1] = Cities.getCity(d_index)
        random.shuffle(self.base)

        k = 0
        for i in range(numSalesmen):
            self.routes[i].append(Cities.getCity(0))  # add same first node for each route
            for j in range(self.routeLengths[i] - 1):
                self.routes[i].append(self.base[k])  # add shuffled values for rest
                k += 1

    def getCity(self, i, j):
        """
        Returns j_th city in i_th route
        """
        return self.routes[i][j]

    def setCity(self, i, j, db):
        """
        Sets value of j_th city in i_th route
        """
        self.routes[i][j] = db
        # refresh metrics
        self.fitness = 0
        self.distance = 0

    def getFitness(self):
        """
        Returns the fitness value of routes
        """
        if self.fitness == 0:
            self.fitness = 1 / self.getDistance()

        return self.fitness

    def getDistance(self):
        """
        Returns total distance covered in all subroutes
        """
        if self.distance == 0:
            routeDistance = 0

            for i in range(numSalesmen):
                for j in range(self.routeLengths[i]):
                    fromCity = self.getCity(i, j)

                    if j + 1 < self.routeLengths[i]:
                        destinationCity = self.getCity(i, j + 1)
                    else:
                        destinationCity = self.getCity(i, 0)

                    routeDistance += fromCity.distanceTo(destinationCity)

            self.distance = routeDistance

        return self.distance

    def containsCity(self, ct):
        """
        Checks if the routes contain a particular city
        """
        return ct in self.base  # base <-> routes

    def __str__(self):
        """
        Returns routes in the form of a string
        """
        geneString = ''
        for i in range(numSalesmen):
            geneString += 'Truck %d [len = %d]: ' % (i, self.routeLengths[i])
            subRouteStr = []
            for j in range(self.routeLengths[i]):
                subRouteStr.append(str(self.getCity(i, j).id))
            geneString += ' --> '.join(subRouteStr)
            if i != numSalesmen - 1:
                geneString += '\n'

        return geneString
