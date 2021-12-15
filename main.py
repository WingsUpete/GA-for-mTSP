import time

from galogic import *
import matplotlib.pyplot as plt
import progressbar

pbar = progressbar.ProgressBar()

# Add Cities
for i in range(numCities):
    Cities.addCity(City(cid=i))

if seedValue is not None:
    random.seed(seedValue)
yaxis = []  # Fittest value (distance)
xaxis = []  # Generation count

pop = Population(populationSize, True)
globalRoute = pop.getFittest()
print('Initial minimum distance: %.6f' % globalRoute.getDistance())

# Start evolving
startT = time.time()
for i in pbar(range(numGenerations)):
    pop = GA.evolvePopulation(pop)
    localRoute = pop.getFittest()
    if globalRoute.getDistance() > localRoute.getDistance():
        globalRoute = localRoute
    yaxis.append(localRoute.getDistance())
    xaxis.append(i)
endT = time.time()
print('GA Runtime = %.4f sec' % (endT - startT))

print('Global minimum distance: %.6f' % globalRoute.getDistance())
print('Final Route:\n%s' % globalRoute)

fig = plt.figure()

plt.plot(xaxis, yaxis, 'r-')
plt.show()
