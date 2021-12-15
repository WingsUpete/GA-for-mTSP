import argparse
from datetime import datetime
import os
import time

import globals
from util import path2FileNameWithoutExt


if __name__ == '__main__':
    """
    Folder Name: <data>_<algo>_<runTimes>_<m>_<gen>_<pop>_<tournament>_<time>
    > Usage Example:
        python runMultiple.py -d instances/mtsp51.txt -ga baseline -so 0 -m 5 -g 200 -p 100 -dc 20000 -r 30
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', type=str, default=None, help='Data instance of cities, default = %s' % str(None))
    parser.add_argument('-ga', '--ga', type=str, default=globals.ALGO_DEFAULT, help='Specify which GA algorithm to run, default = %s' % globals.ALGO_DEFAULT)
    parser.add_argument('-ld', '--log_dir', type=str, default=globals.LOG_DIR_DEFAULT, help='Specify where to create a log file. default = %s' % globals.LOG_DIR_DEFAULT)
    parser.add_argument('-so', '--stdout', type=int, default=1, help='Specify whether to log to stdout. default = %s' % str(True))
    parser.add_argument('-m', '--salesmen', type=int, default=globals.numSalesmen, help='Specify the number of salesmen, default = %d' % globals.numSalesmen)
    parser.add_argument('-g', '--generation', type=int, default=globals.numGenerations, help='Specify the number of generations to run, default = %d' % globals.numGenerations)
    parser.add_argument('-p', '--population', type=int, default=globals.populationSize, help='Specify the population size, default = %d' % globals.populationSize)
    parser.add_argument('-t', '--tournament', type=int, default=globals.tournamentSize, help='Specify the tournament size, default = %d' % globals.tournamentSize)
    parser.add_argument('-dc', '--distCal', type=int, default=globals.maxNDistCal, help='Specify the maximum number of distance calculations allowed (a factor which will be multiplied by N later), default = %d' % globals.maxNDistCal)
    parser.add_argument('-r', '--runTimes', type=int, default=globals.nIndependentRuns, help='Specify the number of times to run independently, default = %d' % globals.nIndependentRuns)
    parser.add_argument('-pbar', '--pbar', type=int, default=0, help='Specify whether to show progress bar (for ipynb), default = %d' % 0)

    FLAGS, unparsed = parser.parse_known_args()

    # Handle directories
    data_tag = path2FileNameWithoutExt(FLAGS.data) if FLAGS.data else 'random'
    general_time_tag = datetime.now().strftime("%Y%m%d_%H_%M_%S")
    runDir = '%s_%s_%d_%d_%d_%d_%d_%s/' % (
        data_tag, FLAGS.ga, FLAGS.runTimes,
        FLAGS.salesmen, FLAGS.generation, FLAGS.population, FLAGS.tournament,
        general_time_tag
    )
    # Fig Dir
    figSaveDir = os.path.join(globals.figSaveDir, runDir)
    os.mkdir(figSaveDir)
    # Log Dir
    if FLAGS.log_dir and FLAGS.log_dir != 'None':
        runLogDir = os.path.join(FLAGS.log_dir, runDir)
        os.mkdir(runLogDir)
    else:
        runLogDir = None

    # Starting running
    print('>>> Total independent runs = %d <<<' % FLAGS.runTimes)
    for i in range(FLAGS.runTimes):
        print('------------------------------------------------------------------------------------------------------')
        print('Round %d' % (i + 1))

        os.system('python main.py -d %s -ga %s -ld %s -so %d -fd %s -m %d -g %d -p %d -t %d -dc %d -rid %d -pbar %d' % (
            FLAGS.data, FLAGS.ga, runLogDir, FLAGS.stdout, figSaveDir,
            FLAGS.salesmen, FLAGS.generation, FLAGS.population, FLAGS.tournament, FLAGS.distCal,
            i + 1, FLAGS.pbar
        ))

        time.sleep(1)   # Wait for 1 sec, then go to next round
    print('------------------------------------------------------------------------------------------------------')
    print('>>> %d runs all finished <<<' % FLAGS.runTimes)
