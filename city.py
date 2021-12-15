import math
import random

from globals import *


class City:
    """
    Represents nodes in the problem graph or network.
    Location coordinates can be passed while creating the object or they will be assigned random values.
    """
    # Good old constructor
    def __init__(self, x=None, y=None, cid=-1):
        self.id = cid
        if x is None and y is None:
            self.x = random.randint(0, xMax)
            self.y = random.randint(0, yMax)
        else:
            self.x = x
            self.y = y

    def distanceTo(self, ct):
        """
        Returns distance to the dustbin passed as argument
        """
        return math.sqrt(math.pow(self.x - ct.x, 2) + math.pow(self.y - ct.y, 2))

    def __str__(self):
        """
        Gives string representation of the Object with coordinates
        """
        return '(%.f,%.f)' % (float(self.x), float(self.y))

    def checkNull(self):
        """
        Check if coordinates have been assigned or not
        Cities with (-1, -1) as coordinates are created during creation on chromosome objects
        """
        return self.x == -1


class Cities:
    """
    Holds all the dustbin objects and is used for creation of chromosomes by jumbling their sequence
    """
    cities = []

    @classmethod
    def addCity(cls, ct):
        cls.cities.append(ct)

    @classmethod
    def getCity(cls, index):
        return cls.cities[index]

    @classmethod
    def numberOfCities(cls):
        return len(cls.cities)
