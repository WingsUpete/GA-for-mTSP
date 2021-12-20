"""
Contains all global variables specific to simulation
"""
import os

# General settings
nIndependentRuns = 30
ALGO_DEFAULT = 'baseline'
LOG_DIR_DEFAULT = 'log/'

figSaveDir = 'fig/'
if not os.path.exists(figSaveDir):
    os.mkdir(figSaveDir)

seedValue = None   # if random seed is set, is it meaningful for us to repeat running 30 times? Set to None now

# GA settings
numGenerations = 70
maxNDistCal = -1
populationSize = 100
tournamentSize = 10
mutationRate = 0.02
elitism = True  # If fittest chromosome has to be passed directly to next generation

# Salesmen
numSalesmen = 5

# Defines range for coordinates when cities are randomly scattered
xMax = 1000
yMax = 1000
numCities = 200
