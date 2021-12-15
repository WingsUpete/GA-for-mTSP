"""
Represents the chromosomes in GA's population.
The object is collection of individual routes taken by trucks.
"""
from routemanager import *
from globals import *
from dustbin import Dustbin


class Route:
    # Good old constructor
    def __init__(self, route=None):
        # 2D (m, ?) array which is collection of respective routes taken by trucks
        self.route = []
        # 1D (n-1,) array having routes in a series - used during crossover operation
        self.base = []
        # 1D (m,) array having route lengths (here, route length = number of nodes)
        self.routeLengths = route_lengths()

        for i in range(numTrucks):
            self.route.append([])

        # fitness value and total distance of all routes
        self.fitness = 0
        self.distance = 0

        # creating empty route
        if route is None:
            for i in range(RouteManager.numberOfDustbins() - 1):
                self.base.append(Dustbin(-1, -1))
        else:
            self.route = route

    def generateIndividual(self):
        """
        we have all route lengths summed up as upper = n+m-1
        1. For each route, length is 1 + (l-1) = l;
        2. For all routes, lengths add up to n+m-1 - m = n-1, using up all nodes except node 0
        """
        # put 1st member of RouteManager as it is (It represents the initial node) and shuffle the rest before adding
        for dindex in range(1, RouteManager.numberOfDustbins()):
            self.base[dindex - 1] = RouteManager.getDustbin(dindex)
        random.shuffle(self.base)

        k = 0
        for i in range(numTrucks):
            self.route[i].append(RouteManager.getDustbin(0))  # add same first node for each route
            for j in range(self.routeLengths[i] - 1):
                self.route[i].append(self.base[k])  # add shuffled values for rest
                k += 1

    def getDustbin(self, i, j):
        """
        Returns j_th dustbin in i_th route
        """
        return self.route[i][j]

    def setDustbin(self, i, j, db):
        """
        Sets value of j_th dustbin in i_th route
        """
        self.route[i][j] = db
        # refresh metrics
        self.fitness = 0
        self.distance = 0

    def getFitness(self):
        """
        Returns the fitness value of route
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

            for i in range(numTrucks):
                for j in range(self.routeLengths[i]):
                    fromDustbin = self.getDustbin(i, j)

                    if j + 1 < self.routeLengths[i]:
                        destinationDustbin = self.getDustbin(i, j + 1)
                    else:
                        destinationDustbin = self.getDustbin(i, 0)

                    routeDistance += fromDustbin.distanceTo(destinationDustbin)

            self.distance = routeDistance

        return self.distance

    def containsDustbin(self, db):
        """
        Checks if the route contains a particular dustbin
        """
        return db in self.base  # base <-> route

    def __str__(self):
        """
        Returns route in the form of a string
        """
        geneString = ''
        for i in range(numTrucks):
            geneString += 'Truck %d [len = %d]: ' % (i, self.routeLengths[i])
            subRouteStr = []
            for j in range(self.routeLengths[i]):
                subRouteStr.append(str(self.getDustbin(i, j)))
            geneString += ' -> '.join(subRouteStr)
            geneString += '\n'

        return geneString
