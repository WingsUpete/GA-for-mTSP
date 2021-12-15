import logging
import time

import progressbar

from galogic import *
from util import Logger, plotGD

logging.getLogger('matplotlib.font_manager').disabled = True


def runGA4mTSP():
    pbar = progressbar.ProgressBar()

    # Add Cities
    for i in range(numCities):
        Cities.addCity(City(cid=i))

    if seedValue is not None:
        random.seed(seedValue)

    # Initial solution
    pop = Population(populationSize, True)
    globalRoute = pop.getFittest()
    logger.log('> Initial minimum distance: %.6f\n' % globalRoute.getDistance())

    # Start GA
    logger.log('> Starting running GA.\n')
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
    logger.log('# Generation Distance\n')
    for i in range(len(xAxis)):
        logger.log('%% %d %.6f\n' % (xAxis[i], yAxis[i]))

    # Record detailed results
    logger.log('> GA Runtime = %.4f sec\n' % (endT - startT))
    logger.log('> Global minimum distance: %.6f\n' % globalRoute.getDistance())
    logger.log('> Final Route:\n%s\n' % globalRoute)

    # Plot
    figPath = os.path.join(figSaveDir, '%s.png' % logger.time_tag)
    plotGD(xAxis, yAxis, label='baseline', logr=logger, save=True, saveFigPath=figPath, show=True)


if __name__ == '__main__':
    logger = Logger()
    runGA4mTSP()
    logger.close()
