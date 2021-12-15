"""
Contains all global variables specific to simulation
"""
import os

seedValue = 1   # TODO: if random seed is set, is it meaningful for us to repeat running 30 times?
numGenerations = 70
# size of population
populationSize = 100
mutationRate = 0.02
tournamentSize = 10
elitism = True  # If fittest chromosome has to be passed directly to next generation
# number of trucks
numSalesmen = 10

# Defines range for coordinates when cities are randomly scattered
xMax = 1000
yMax = 1000
numCities = 200

# Others
figSaveDir = 'fig/'
if not os.path.exists(figSaveDir):
    os.mkdir(figSaveDir)
