import random

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


def plotGD(xs, ys, label='GA', logr=None, save=True, saveFigPath=None, show=True):
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
