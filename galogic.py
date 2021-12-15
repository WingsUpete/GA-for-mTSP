"""
The main helper class for Genetic Algorithm to perform
crossover, mutation on populations to evolve them
"""
from population import *
from globals import *
from city import City, Cities


class GA:
    @classmethod
    def evolvePopulation(cls, pop):
        """
        Evolve pop
        """
        newPopulation = Population(pop.populationSize, False)

        elitismOffset = 0
        # If fittest chromosome has to be passed directly to next generation
        if elitism:
            newPopulation.saveRoute(0, pop.getFittest())
            elitismOffset = 1

        # Performs tournament selection followed by crossover to generate child
        for i in range(elitismOffset, newPopulation.populationSize):
            parent1 = cls.tournamentSelection(pop)
            parent2 = cls.tournamentSelection(pop)
            child = cls.crossover(parent1, parent2)
            # Adds child to next generation
            newPopulation.saveRoute(i, child)

        # Performs Mutation
        for i in range(elitismOffset, newPopulation.populationSize):
            cls.mutate(newPopulation.getRoute(i))

        return newPopulation

    @classmethod
    def crossover(cls, parent1, parent2):
        """
        Function to implement crossover operation
        """
        child = Routes()
        child.base.append(City(-1, -1))  # since size is (numCities - 1) by default
        startPos = 0
        endPos = 0
        while startPos >= endPos:
            startPos = random.randint(1, numCities - 1)
            endPos = random.randint(1, numCities - 1)

        parent1.base = [parent1.routes[0][0]]
        parent2.base = [parent2.routes[0][0]]

        for i in range(numTrucks):
            for j in range(1, parent1.routeLengths[i]):
                parent1.base.append(parent1.routes[i][j])

        for i in range(numTrucks):
            for j in range(1, parent2.routeLengths[i]):
                parent2.base.append(parent2.routes[i][j])

        for i in range(1, numCities):
            if i < endPos < startPos:
                child.base[i] = parent1.base[i]

        for i in range(numCities):
            if not (child.containsCity(parent2.base[i])):
                for i1 in range(numCities):
                    if child.base[i1].checkNull():
                        child.base[i1] = parent2.base[i]
                        break

        k = 0
        child.base.pop(0)
        for i in range(numTrucks):
            child.routes[i].append(Cities.getCity(0))  # add same first node for each routes
            for j in range(child.routeLengths[i] - 1):
                child.routes[i].append(child.base[k])  # add shuffled values for rest
                k += 1
        return child

    @classmethod
    def mutate(cls, route):
        """
        Mutation operation
        """
        index1 = 0
        index2 = 0
        while index1 == index2:
            index1 = random.randint(0, numTrucks - 1)
            index2 = random.randint(0, numTrucks - 1)
        # print ('Indexes selected: ' + str(index1) + ',' + str(index2))

        # generate replacement range for 1
        route1startPos = 0
        route1lastPos = 0
        while route1startPos >= route1lastPos or route1startPos == 1:
            route1startPos = random.randint(1, route.routeLengths[index1] - 1)
            route1lastPos = random.randint(1, route.routeLengths[index1] - 1)

        # generate replacement range for 2
        route2startPos = 0
        route2lastPos = 0
        while route2startPos >= route2lastPos or route2startPos == 1:
            route2startPos = random.randint(1, route.routeLengths[index2] - 1)
            route2lastPos = random.randint(1, route.routeLengths[index2] - 1)

        # print ('startPos, lastPos: ' + str(route1startPos) + ',' + str(route1lastPos) + ',' + str(route2startPos) + ',' + str(route2lastPos))
        swap1 = []  # values from 1
        swap2 = []  # values from 2

        if random.randrange(1) < mutationRate:
            # pop all the values to be replaced
            for i in range(route1startPos, route1lastPos + 1):
                swap1.append(route.routes[index1].pop(route1startPos))

            for i in range(route2startPos, route2lastPos + 1):
                swap2.append(route.routes[index2].pop(route2startPos))

            del1 = (route1lastPos - route1startPos + 1)
            del2 = (route2lastPos - route2startPos + 1)

            # add to new location by pushing
            route.routes[index1][route1startPos:route1startPos] = swap2
            route.routes[index2][route2startPos:route2startPos] = swap1

            route.routeLengths[index1] = len(route.routes[index1])
            route.routeLengths[index2] = len(route.routes[index2])

    @classmethod
    def tournamentSelection(cls, pop):
        """
        Tournament Selection: choose a random set of chromosomes and find the fittest among them
        """
        tournament = Population(tournamentSize, False)

        for i in range(tournamentSize):
            randomInt = random.randint(0, pop.populationSize - 1)
            tournament.saveRoute(i, pop.getRoute(randomInt))

        fittest = tournament.getFittest()
        return fittest
