import random

import globals
from entity import Population, City, Cities, Routes


class GAMyAlgo:
    """
    The main helper class for Genetic Algorithm to perform crossover, mutation on populations to evolve them
    """
    @classmethod
    def evolvePopulation(cls, pop):
        """
        Evolve pop
        """
        return None

    @classmethod
    def crossover(cls, parent1, parent2):
        """
        Function to implement crossover operation
        """
        return None

    @classmethod
    def mutate(cls, route):
        """
        Mutation operation
        """
        pass

    @classmethod
    def tournamentSelection(cls, pop):
        """
        Tournament Selection: choose a random set of chromosomes and find the fittest among them
        """
        return None
