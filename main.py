import logging
import time
import random
import argparse
import os

import progressbar

import globals
from entity import City, Cities, Population
from ga import GABaseline
from util import Logger, plotGD

logging.getLogger('matplotlib.font_manager').disabled = True


def runGA4mTSP(dataPath=None, GA_type='baseline', logr=None):
    pbar = progressbar.ProgressBar()

    # Add Cities
    if dataPath is None:
        for i in range(globals.numCities):
            Cities.addCity(City(cid=i))
        logr.log('> Randomly generated %d cities\n' % globals.numCities)
    else:
        # Load from instances
        logr.log('> Loading cities from %s\n' % dataPath)
        with open(dataPath) as f:
            lines = f.readlines()
            for line in lines:
                items = line.strip().split(' ')
                if len(items) == 1:     # first line
                    logr.log('\t>> %d cities in total to be loaded\n' % int(items[0]))
                else:
                    Cities.addCity(City(x=int(items[1]), y=int(items[2]), cid=int(items[0]) - 1))
        logr.log('> %d cities loaded from %s\n' % (Cities.numberOfCities(), dataPath))
    if globals.maxNDistCal != -1:
        globals.maxNDistCal *= Cities.numberOfCities()

    if globals.seedValue is not None:
        random.seed(globals.seedValue)

    # Initial solution
    pop = Population(globals.populationSize, True)
    globalRoute = pop.getFittest()
    logr.log('> Initial distance: %.6f\n' % globalRoute.getDistance())

    # Specify GA
    if GA_type == 'baseline':
        GA = GABaseline
    else:
        GA = GABaseline

    # Start GA
    logr.log('> Starting running GA.\n')
    logr.log('\t>> cities = %d, salesmen = %d\n' % (Cities.numberOfCities(), globals.numSalesmen))
    logr.log('\t>> Generations = %d, PopulationSize = %d, TournamentSize = %d\n' %
             (globals.numGenerations, globals.populationSize, globals.tournamentSize))
    genCnt = 0
    xAxis = []  # Generation count
    yAxis = []  # Fittest value (distance)
    startT = time.time()
    for i in pbar(range(globals.numGenerations)):
        if globals.maxNDistCal != -1 and Cities.distCalCnt > globals.maxNDistCal:
            break

        pop = GA.evolvePopulation(pop)
        localRoute = pop.getFittest()

        if globalRoute.getDistance() > localRoute.getDistance():
            globalRoute = localRoute

        yAxis.append(localRoute.getDistance())
        xAxis.append(genCnt + 1)
        genCnt += 1
    endT = time.time()

    # Record data
    logr.log('# Generation Distance\n')
    for i in range(len(xAxis)):
        logr.log('%% %d %.6f\n' % (xAxis[i], yAxis[i]))

    # Record detailed results
    logr.log('> Finished %d generations. GA Runtime = %.4f sec\n' % (genCnt, endT - startT))
    logr.log('> Final distance: %.6f\n' % globalRoute.getDistance())
    logr.log('> Final Route:\n%s\n' % globalRoute)

    # Plot
    figPath = os.path.join(globals.figSaveDir, '%s.png' % logr.time_tag)
    plotGD(xAxis, yAxis, label='baseline', logr=logr, save=True, saveFigPath=figPath, show=True)


if __name__ == '__main__':
    """
    The depot is the first city (city 0).
    > Usage Example:
        python main.py -d instances/mtsp51.txt -ga baseline -g 200 -p 100 -m 5 -dc 20000
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', type=str, default=None, help='Data instance of cities, default = %s' % str(None))
    parser.add_argument('-ga', '--ga', type=str, default=globals.ALGO_DEFAULT, help='Specify which GA algorithm to run, default = %s' % globals.ALGO_DEFAULT)
    parser.add_argument('-ld', '--log_dir', type=str, default=globals.LOG_DIR_DEFAULT, help='Specify where to create a log file. default = %s' % globals.LOG_DIR_DEFAULT)
    parser.add_argument('-g', '--generation', type=int, default=globals.numGenerations, help='Specify the number of generations to run, default = %d' % globals.numGenerations)
    parser.add_argument('-p', '--population', type=int, default=globals.populationSize, help='Specify the population size, default = %d' % globals.populationSize)
    parser.add_argument('-t', '--tournament', type=int, default=globals.tournamentSize, help='Specify the tournament size, default = %d' % globals.tournamentSize)
    parser.add_argument('-m', '--salesmen', type=int, default=globals.numSalesmen, help='Specify the number of salesmen, default = %d' % globals.numSalesmen)
    parser.add_argument('-dc', '--distCal', type=int, default=globals.maxNDistCal, help='Specify the maximum number of distance calculations allowed (a factor which will be multiplied by N later), default = %d' % globals.maxNDistCal)

    FLAGS, unparsed = parser.parse_known_args()

    logger = Logger(activate=True, logging_folder=FLAGS.log_dir) if FLAGS.log_dir else Logger(activate=False)
    globals.numGenerations = FLAGS.generation
    globals.populationSize = FLAGS.population
    globals.tournamentSize = FLAGS.tournament
    globals.numSalesmen = FLAGS.salesmen
    globals.maxNDistCal = FLAGS.distCal

    # Run GA
    runGA4mTSP(dataPath=FLAGS.data, GA_type=FLAGS.ga, logr=logger)

    logger.close()
