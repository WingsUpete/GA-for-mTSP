import random
import os
import sys

import matplotlib.pyplot as plt


def random_range(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(range(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]


def route_lengths(nCities, nSalesmen):
    """
    Randomly distribute number of cities to subroutes
    Maximum and minimum values are maintained to reach optimal result
    """
    upper = (nCities + nSalesmen - 1)
    fa = upper / nSalesmen * 1.6  # max route length
    fb = upper / nSalesmen * 0.6  # min route length
    a = random_range(nSalesmen, upper)
    while 1:
        if all(fb < i < fa for i in a):
            break
        else:
            a = random_range(nSalesmen, upper)
    return a


def plotGD(xs, ys, label='GA', logr=None, save=True, saveFigPath=None, show=False):
    plt.figure()
    plt.plot(xs, ys, color='red', label=label)
    plt.title('Generation - Distance Curve')
    plt.xlabel('Generation')
    plt.ylabel('Distance')
    plt.legend(loc='upper right')
    plt.tight_layout()

    if save:
        plt.savefig(saveFigPath)
        logr.log('> Generation - Distance curve saved to %s.\n' % saveFigPath)

    if show:
        plt.show()


def path2FileNameWithoutExt(path):
    """
    get file name without extension from path
    :param path: file path
    :return: file name without extension
    """
    return os.path.splitext(os.path.basename(path))[0]


def plotGDWithLog(log_path, label='GA', save=True, saveFigPath=None, show=True):
    if not os.path.exists(log_path):
        sys.stderr.write('[plotGDWithLog] %s does not exist!\n' % log_path)
        exit(-1000)
    xAxis, yAxis = [], []
    with open(log_path) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('%'):
                items = line.split(' ')
                xAxis.append(int(items[1]))
                yAxis.append(float(items[2]))
    plotGD(xAxis, yAxis, label=label, save=save, saveFigPath=saveFigPath, show=show)


def extractFinalDistFromLog(log_path):
    if not os.path.exists(log_path):
        sys.stderr.write('[extractFinalDistFromLog] %s does not exist!\n' % log_path)
        exit(-1000)

    with open(log_path) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('> Final distance'):
                return float(line.split(' ')[-1])


def extractFinalDistListFromLogDir(log_dir):
    if not os.path.exists(log_dir):
        sys.stderr.write('[extractFinalDistListFromLogDir] %s does not exist!\n' % log_dir)
        exit(-1001)

    res = []
    for file in os.listdir(log_dir):
        res.append(extractFinalDistFromLog(os.path.join(log_dir, file)))
    return res


if __name__ == '__main__':
    # Test
    logPath = '../log/mtsp100_baseline_30_5_1000_100_10_20211216_03_35_04/20211216_03_35_05.log'
    # plotGDWithLog(log_path=logPath, label='baseline', save=False, show=True)
    # print(extractFinalDistFromLog(log_path=logPath))

    logDir = '../log/mtsp100_baseline_30_5_1000_100_10_20211216_03_35_04/'
    print(extractFinalDistListFromLogDir(log_dir=logDir))
