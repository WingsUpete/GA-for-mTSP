import os
import sys

import time
import copy
import math
import random
import numpy as np

from scipy.stats import mannwhitneyu

# 统计计算了多少次欧式距离（需要满足少于或等于20000*N次）
num_of_cal_pairs = 0


# 计算两个点之间的欧式距离
def euclidean_distance(point1, point2):
    global num_of_cal_pairs
    num_of_cal_pairs += 1
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# 读取数据集到 numpy ndarray 数组
def read_dataset(filepath):
    with open(filepath) as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    num_of_nodes = int(lines[0])
    coordinate_of_nodes = np.zeros((num_of_nodes, 2))
    for line in lines[1:]:
        line = line.split(' ')
        if len(line) != 3:
            break
        coordinate_of_nodes[int(line[0]) - 1, 0] = float(line[1])
        coordinate_of_nodes[int(line[0]) - 1, 1] = float(line[2])

    return num_of_nodes, coordinate_of_nodes


# 种群中的一个个体
# chromosome 为二维数组，每个旅行商的路径为一纬数组，不包括起点和终点
class Individual:

    def __init__(self):
        self.chromosome = None
        self.distance = None
        self.num_of_nodes = None
        self.num_of_salesman = None

    # 随机初始化，每个城市随机赋给一个旅行商的随机位置
    def random_init(self, num_of_nodes, num_of_salesman):
        self.num_of_nodes = num_of_nodes
        self.num_of_salesman = num_of_salesman
        self.chromosome = [[] for _ in range(num_of_salesman)]
        for node in range(1, num_of_nodes):
            sales = random.randint(0, num_of_salesman - 1)
            self.chromosome[sales].insert(random.randint(0, len(self.chromosome[sales])), node)

    # 计算对应 chromosome 的总距离
    def cal_distance(self, coordinate_of_nodes):
        total_distance = 0.0
        for salesman in self.chromosome:
            distance = 0.0
            if len(salesman) != 0:
                distance += euclidean_distance(coordinate_of_nodes[0],
                                               coordinate_of_nodes[salesman[0]])
                distance += euclidean_distance(coordinate_of_nodes[0],
                                               coordinate_of_nodes[salesman[-1]])
            for ind in range(1, len(salesman)):
                distance += euclidean_distance(coordinate_of_nodes[salesman[ind - 1]],
                                               coordinate_of_nodes[salesman[ind]])
            total_distance += distance
        self.distance = total_distance

    # 对 chromosome 按照一定的概率变异
    # 一定的概率随机的两个城市互换（包括不同旅行商的位置）
    # 一定的概率随机将一个城市插入任意位置
    def mutate(self, probability):
        if random.uniform(0, 1) < probability:
            self.distance = None

            node1 = random.randint(1, self.num_of_nodes - 1)
            node2 = random.randint(1, self.num_of_nodes - 1)
            if node1 != node2:
                for i in range(len(self.chromosome)):
                    for j in range(len(self.chromosome[i])):
                        if self.chromosome[i][j] == node1:
                            self.chromosome[i][j] = node2
                        elif self.chromosome[i][j] == node2:
                            self.chromosome[i][j] = node1
        if random.uniform(0, 1) < probability:
            self.distance = None

            node = random.randint(1, self.num_of_nodes - 1)
            sales = random.randint(0, self.num_of_salesman - 1)
            if node not in self.chromosome[sales]:
                for i in range(len(self.chromosome)):
                    for j in range(len(self.chromosome[i])):
                        if self.chromosome[i][j] == node:
                            del self.chromosome[i][j]
                            break
                self.chromosome[sales].insert(random.randint(0, len(self.chromosome[sales])), node)


# 一整个演化的种群
# individuals 保存种群，offsprings 保存选择交叉后获得的子代
# survivals，把父代和子代放在一起，保存较好的个体
class Population:

    def __init__(self):
        self.individuals = []
        self.offsprings = []
        self.num_of_nodes = None
        self.num_of_salesman = None
        self.coordinate_of_nodes = None

    # 初始化种群
    def initialization(self, pop_size, num_of_nodes, num_of_salesman, coordinate_of_nodes):
        self.num_of_nodes = num_of_nodes
        self.num_of_salesman = num_of_salesman
        self.coordinate_of_nodes = coordinate_of_nodes
        self.individuals = []
        for _ in range(pop_size):
            individual = Individual()
            individual.random_init(num_of_nodes, num_of_salesman)
            self.individuals.append(individual)

    # 对所有 distance 为 None 的个体，计算距离
    def evaluation(self):
        for ind in self.individuals:
            if ind.distance is None:
                ind.cal_distance(self.coordinate_of_nodes)
        for off in self.offsprings:
            if off.distance is None:
                off.cal_distance(self.coordinate_of_nodes)

    # 选择，随机排列父代，两次随机排列对应的位置的，进行tournament selection，0.8的概率选好的，0.2的概率选坏，相同则各0.5
    def selection(self, probabilty=0.8):
        selection = []
        shuffle_1 = [i for i in range(len(self.individuals))]
        random.shuffle(shuffle_1)
        shuffle_2 = [i for i in range(len(self.individuals))]
        random.shuffle(shuffle_2)
        for i in range(len(self.individuals)):
            if shuffle_1[i] < shuffle_2[i]:
                selection.append(shuffle_1[i] if random.uniform(0, 1) < probabilty else shuffle_2[i])
            elif shuffle_1[i] > shuffle_2[i]:
                selection.append(shuffle_2[i] if random.uniform(0, 1) < probabilty else shuffle_1[i])
            else:
                selection.append(shuffle_1[i] if random.uniform(0, 1) < 0.5 else shuffle_2[i])
        return selection

    # 进行选择和交叉操作，获得子代
    def crossover(self, probabilty=0.5):
        # 进行两次选择，得到一组父代
        selection_1 = self.selection()
        selection_2 = self.selection()

        # 不进行交叉操作，对于每一对父代，0.5的概率，一对中较好的变成变成子代
        for i in range(len(selection_1)):
            if random.uniform(0, 1) > probabilty:
                best_one = self.individuals[selection_1[i]] if selection_1[i] < selection_2[i] else self.individuals[
                    selection_2[i]]
                self.offsprings.append(copy.deepcopy(best_one))

    # 按照一定的概率对子代进行变异操作
    def mutation(self, probabilty=0.2):
        for off in self.offsprings:
            off.mutate(probabilty)

    # 子代和父代的个体放在一起，保留 distance 花销较小的个体
    def survival(self):
        darwin_space = []
        for ind in self.individuals:
            darwin_space.append(ind)
        for off in self.offsprings:
            darwin_space.append(off)

        darwin_space = sorted(darwin_space, key=lambda x: x.distance)

        self.individuals = darwin_space[:len(self.individuals)]
        self.offsprings = []


class JingranGA:
    def __init__(self, logger=None):
        self.dataset_path = None
        self.num_of_nodes = None
        self.coordinate_of_nodes = None
        self.max_num_of_cal_pairs = None

        self.generation = None
        self.best_distance_history = None
        self.best_route_history = None
        self.num_of_cal_pairs_history = None

        self.finished_time = None

        self.logger = logger

    def fit(self, dataset_path):
        start_time = time.time()

        # 初始化 num_of_cal_pairs，读取数据集
        global num_of_cal_pairs
        num_of_cal_pairs = 0
        self.dataset_path = dataset_path
        self.num_of_nodes, self.coordinate_of_nodes = read_dataset(dataset_path)
        self.max_num_of_cal_pairs = self.num_of_nodes * 20000
        if self.logger:
            self.logger.log('dataset loaded. the path of dataset {}'.format(dataset_path))
            self.logger.log('num_of_cal_pairs should not larger than {}'.format(self.max_num_of_cal_pairs))
        else:
            print('dataset loaded. the path of dataset {}'.format(dataset_path))
            print('num_of_cal_pairs should not larger than {}'.format(self.max_num_of_cal_pairs))

        self.best_distance_history = []
        self.best_route_history = []
        self.num_of_cal_pairs_history = []

        # 初始化种群
        population = Population()
        population.initialization(pop_size=100,
                                  num_of_nodes=self.num_of_nodes,
                                  num_of_salesman=5,
                                  coordinate_of_nodes=self.coordinate_of_nodes)
        if self.logger:
            self.logger.log('population init')
        else:
            print('population init')

        # 进行选择交叉变异，直到达到停止条件
        self.generation = 0
        while True:
            # 判断是否超过停止条件，超过则停止，没超过进行survival操作
            population.evaluation()
            if num_of_cal_pairs > self.max_num_of_cal_pairs:
                break
            population.survival()
            self.generation += 1
            self.best_distance_history.append(population.individuals[0].distance)
            self.best_route_history.append(population.individuals[0].chromosome)
            self.num_of_cal_pairs_history.append(num_of_cal_pairs)

            last_num_of_cal_pairs = num_of_cal_pairs

            population.crossover()
            population.mutation()

        self.finished_time = time.time() - start_time
        if self.logger:
            self.logger.log('finished, time {} seconds'.format(self.finished_time))
        else:
            print('finished, time {} seconds'.format(self.finished_time))

    def print_best(self):
        if self.logger:
            self.logger.log('generation {}, num_of_cal_pairs {}, best distance {}\nbest route: {}'.format(self.generation, self.num_of_cal_pairs_history[-1], self.best_distance_history[-1], self.best_route_history[-1]))
        else:
            print('generation {}, num_of_cal_pairs {}, best distance {}\nbest route: {}'.format(self.generation, self.num_of_cal_pairs_history[-1], self.best_distance_history[-1], self.best_route_history[-1]))

    def save_history_to_file(self, filename, samplename):
        with open(filename, 'a+') as f:
            f.write('------\n')
            f.write('{}, {}, {}, {}\n'.format(samplename,
                                              self.dataset_path,
                                              self.max_num_of_cal_pairs,
                                              self.finished_time))
            for i in range(self.generation):
                f.write('{}, {}, {}, {}\n'.format(i + 1,
                                                  self.best_distance_history[i],
                                                  self.num_of_cal_pairs_history[i],
                                                  self.best_route_history[i]))
            f.write('\n\n')
