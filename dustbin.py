"""
Represents nodes in the problem graph or network.
Location coordinates can be passed while creating the object or they
will be assigned random values.
"""
import math

from globals import *


class Dustbin:
    # Good old constructor
    def __init__(self, x=None, y=None):
        if x is None and y is None:
            self.x = random.randint(0, xMax)
            self.y = random.randint(0, yMax)
        else:
            self.x = x
            self.y = y

    def distanceTo(self, db):
        """
        Returns distance to the dustbin passed as argument
        """
        return math.sqrt(math.pow(self.x - db.x, 2) + math.pow(self.y - db.y, 2))

    def __str__(self):
        """
        Gives string representation of the Object with coordinates
        """
        return '(%.f,%.f)' % (float(self.x), float(self.y))

    def checkNull(self):
        """
        Check if coordinates have been assigned or not
        Dustbins with (-1, -1) as coordinates are created during creation on chromosome objects
        """
        return self.x == -1
