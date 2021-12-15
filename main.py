import logging
import time
import random

import progressbar

from globals import *
from entity import City, Cities, Population
from ga import GABaseline
from util import Logger, plotGD

logging.getLogger('matplotlib.font_manager').disabled = True


def runGA4mTSP(dataPath=None, GA_type='baseline', logr=None):
    pbar = progressbar.ProgressBar()

    # Add Cities
    if dataPath is None:
        for i in range(numCities):
            Cities.addCity(City(cid=i))
        logr.log('> Randomly generated %d cities\n' % numCities)
    else:
        # Load from instances
        logr.log('> Loading cities from %s\n' % dataPath)
        with open(dataPath) as f:
            lines = f.readlines()
            for line in lines:
                items = line.strip().split(' ')
                if len(items) == 1:     # first line
                    logr.log('>> %d cities in total to be loaded\n' % int(items[0]))
                else:
                    Cities.addCity(City(x=int(items[1]), y=int(items[2]), cid=int(items[0]) - 1))
        logr.log('> %d cities loaded from %s\n' % (Cities.numberOfCities(), dataPath))

    if seedValue is not None:
        random.seed(seedValue)

    # Initial solution
    pop = Population(populationSize, True)
    globalRoute = pop.getFittest()
    logr.log('> Initial distance: %.6f\n' % globalRoute.getDistance())

    # Specify GA
    if GA_type == 'baseline':
        GA = GABaseline
    else:
        GA = GABaseline

    # Start GA
    logr.log('> Starting running GA.\n')
    logr.log('>> cities = %d, salesmen = %d\n' % (Cities.numberOfCities(), numSalesmen))
    logr.log('>> Generations = %d, PopulationSize = %d, TournamentSize = %d\n' %
             (numGenerations, populationSize, tournamentSize))
    genCnt = 1
    xAxis = []  # Generation count
    yAxis = []  # Fittest value (distance)
    startT = time.time()
    for i in pbar(range(numGenerations)):
        pop = GA.evolvePopulation(pop)
        localRoute = pop.getFittest()

        if globalRoute.getDistance() > localRoute.getDistance():
            globalRoute = localRoute

        yAxis.append(localRoute.getDistance())
        xAxis.append(genCnt)
        genCnt += 1
    endT = time.time()

    # Record data
    logr.log('# Generation Distance\n')
    for i in range(len(xAxis)):
        logr.log('%% %d %.6f\n' % (xAxis[i], yAxis[i]))

    # Record detailed results
    logr.log('> GA Runtime = %.4f sec\n' % (endT - startT))
    logr.log('> Final distance: %.6f\n' % globalRoute.getDistance())
    logr.log('> Final Route:\n%s\n' % globalRoute)

    # Plot
    figPath = os.path.join(figSaveDir, '%s.png' % logr.time_tag)
    plotGD(xAxis, yAxis, label='baseline', logr=logr, save=True, saveFigPath=figPath, show=True)


if __name__ == '__main__':
    logger = Logger()
    runGA4mTSP(dataPath=None, GA_type='baseline', logr=logger)
    logger.close()
