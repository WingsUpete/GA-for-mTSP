import logging
import time
import random
import argparse
import os

import progressbar

import globals
from entity import City, Cities, Population
from ga import GABaseline, GAMyAlgo
from util import Logger, plotGD

logging.getLogger('matplotlib.font_manager').disabled = True


def runGA4mTSP(dataPath=None, GA_type=globals.ALGO_DEFAULT, logr=None, maxNDC=globals.maxNDistCal, showPbar=False):
    pbar = progressbar.ProgressBar() if showPbar else None

    # Add Cities
    if dataPath is None:
        for i in range(globals.numCities):
            Cities.addCity(City(cid=i))
        logr.log('> Randomly generated %d cities\n' % Cities.numberOfCities())
    else:
        # Load from instances
        logr.log('> Loading cities from %s\n' % dataPath)
        with open(dataPath) as f:
            lines = f.readlines()
            for line in lines:
                items = line.strip().split(' ')
                if len(items) == 1 and items[0] != '':     # first line
                    logr.log('\t>> %d cities in total to be loaded\n' % int(items[0]))
                elif len(items) == 3:
                    Cities.addCity(City(x=int(items[1]), y=int(items[2]), cid=int(items[0]) - 1))
                else:
                    continue
        globals.numCities = Cities.numberOfCities()
        logr.log('> %d cities loaded from %s\n' % (Cities.numberOfCities(), dataPath))
    if maxNDC != -1:
        maxNDC *= Cities.numberOfCities()

    if globals.seedValue is not None:
        random.seed(globals.seedValue)

    # Initial solution
    pop = Population(globals.populationSize, True)
    globalRoute = pop.getFittest()
    logr.log('> Initial distance: %.6f\n' % globalRoute.getDistance())

    # Specify GA
    if GA_type == 'baseline':
        GA = GABaseline
    elif GA_type == 'myAlgo':
        GA = GAMyAlgo
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
    GA_Iterations = pbar(range(globals.numGenerations)) if pbar else range(globals.numGenerations)
    for i in GA_Iterations:
        if maxNDC != -1 and Cities.distCalCnt > maxNDC:
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
    logr.log('> Finished %d generations with %d distance calculations. GA Runtime = %.4f sec\n'
             % (genCnt, Cities.distCalCnt, endT - startT))
    logr.log('> Final distance: %.6f\n' % globalRoute.getDistance())
    logr.log('> Final Route:\n%s\n' % globalRoute)

    # Plot
    figPath = os.path.join(globals.figSaveDir, '%s.png' % logr.time_tag)
    plotGD(xAxis, yAxis, label='baseline', logr=logr, save=True, saveFigPath=figPath, show=False)


if __name__ == '__main__':
    """
    The depot is the first city (city 0).
    Folder Name: <data>_<algo>_<runTimes>_<m>_<gen>_<pop>_<tournament>_<time>
    > Usage Example:
        python main.py -d instances/mtsp51.txt -ga baseline -so 1 -m 5 -g 200 -p 100 -dc 20000
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', type=str, default=None, help='Data instance of cities, default = %s' % str(None))
    parser.add_argument('-ga', '--ga', type=str, default=globals.ALGO_DEFAULT, help='Specify which GA algorithm to run, default = %s' % globals.ALGO_DEFAULT)
    parser.add_argument('-ld', '--log_dir', type=str, default=globals.LOG_DIR_DEFAULT, help='Specify where to create a log file. default = %s' % globals.LOG_DIR_DEFAULT)
    parser.add_argument('-so', '--stdout', type=int, default=1, help='Specify whether to log to stdout. default = %d' % 1)
    parser.add_argument('-fd', '--fig_dir', type=str, default=globals.figSaveDir, help='Specify where to store a figure. default = %s' % globals.figSaveDir)
    parser.add_argument('-m', '--salesmen', type=int, default=globals.numSalesmen, help='Specify the number of salesmen, default = %d' % globals.numSalesmen)
    parser.add_argument('-g', '--generation', type=int, default=globals.numGenerations, help='Specify the number of generations to run, default = %d' % globals.numGenerations)
    parser.add_argument('-p', '--population', type=int, default=globals.populationSize, help='Specify the population size, default = %d' % globals.populationSize)
    parser.add_argument('-t', '--tournament', type=int, default=globals.tournamentSize, help='Specify the tournament size, default = %d' % globals.tournamentSize)
    parser.add_argument('-dc', '--distCal', type=int, default=globals.maxNDistCal, help='Specify the maximum number of distance calculations allowed (a factor which will be multiplied by N later), default = %d' % globals.maxNDistCal)
    parser.add_argument('-rid', '--runID', type=int, default=1, help='Specify the run index for multiple runs, default = %d' % 1)
    parser.add_argument('-pbar', '--pbar', type=int, default=0, help='Specify whether to show progress bar (for ipynb), default = %d' % 0)

    FLAGS, unparsed = parser.parse_known_args()

    # Update global variables
    globals.figSaveDir = FLAGS.fig_dir

    globals.numSalesmen = FLAGS.salesmen
    globals.numGenerations = FLAGS.generation
    globals.populationSize = FLAGS.population
    globals.tournamentSize = FLAGS.tournament

    if FLAGS.log_dir and FLAGS.log_dir != 'None':
        logger = Logger(activate=True, logging_folder=FLAGS.log_dir, std_out=(FLAGS.stdout == 1))
    else:
        logger = Logger(activate=False)
    logger.log('--> Running ID = %d\n' % FLAGS.runID)

    # Extra process to avoid None type as a str 'None'
    if FLAGS.data:
        FLAGS.data = None if FLAGS.data == 'None' else FLAGS.data

    # Run GA
    runGA4mTSP(dataPath=FLAGS.data, GA_type=FLAGS.ga, logr=logger, maxNDC=FLAGS.distCal, showPbar=(FLAGS.pbar == 1))

    logger.close()
