# -*- coding: utf-8 -*-
"""
Created on Tue Apr 03 12:12:58 2018

@author: wialsh
"""
import tqdm
import numpy as np

def make_route_info():
    route_info = dict()
    epoch_info = dict()
    elite_dict = dict()
    elite_dict['best_fitness'] = float('-inf')
    elite_dict['best_route'] = None
    elite_dict['best_dist'] = float('inf')
    elite_dict['epoch'] = -1

    epoch_info['fitness'] = []
    epoch_info['distance'] = []
    route_info['epoch_info'] = epoch_info
    route_info['elite'] = elite_dict
    return route_info


def calc_elite(population, fitness, route_dist, fitness_index, route_info, epoch):
    elite_dict = route_info['elite']
    current_best_fitness = fitness[fitness_index[-1]]
    best_fitness_index = fitness_index[-1]
    current_best_dist = float(route_dist[best_fitness_index])
    if current_best_fitness > elite_dict['best_fitness']:
        current_best_route = population[best_fitness_index].tolist()
        elite_dict['best_fitness'] = float(current_best_fitness)
        elite_dict['best_route'] = current_best_route
        elite_dict['best_dist'] = current_best_dist
        elite_dict['epoch'] = epoch

    epoch_info = route_info['epoch_info']
    fitness = epoch_info['fitness']
    distance = epoch_info['distance']
    fitness.append(current_best_fitness)
    distance.append(current_best_dist)


class Indexer(object):
    def __init__(self, n, m, build_y_index_func, onlyStart=False):
        self.n = n
        self.m = m
        self.onlyStart = onlyStart
        self.city_vec = np.arange(m)
        self.ants = np.arange(n)
        self.y_mat = np.zeros((m, m), dtype=np.int)
        self.x_mat = (np.arange(n) * m).reshape((n, 1))
        self.x_mat_ravel = (np.arange(n) * m)
        self.loop_city_vec = self.city_vec.tolist() + [self.city_vec.tolist()[0]]
        self.y_mat[:] = self.city_vec

        self.city_mat =  np.zeros((n, m), dtype=np.int)
        self.city_mat[:] = self.city_vec

        if callable(build_y_index_func):
            build_y_index_func(self.y_mat, self.city_vec.tolist(), m)

    @property
    def size(self):
        return self.n, self.m


class AntColonyAlgorithm(object):
    def __init__(self, name, line, alpha=1, beta=5, quantity=10, rho=0.5, epochs=100,
                 init_tau_average=False, use_momentum=True, onlyStart=False, method='cycle',
                 early_stopping_rounds=None):
        # type: (str, np.ndarray, int, int, int, float, int, bool, bool, bool, str, int) -> None
        m = line.shape[1]
        ant_nums = max(int(m / 3 * 2), 20)
        self.name = name
        self.line = line

        self.alpha = alpha
        self.beta = beta
        self.quantity = quantity
        self.rho = rho

        self._method = method
        self.use_momentum = use_momentum
        self.epochs = epochs
        self.early_stopping_rounds = early_stopping_rounds

        self.index = Indexer(ant_nums, m, self.build_y_index, onlyStart)

        #init pheromone.
        if init_tau_average:
            self.TAU = np.ones((m, m)) #pheromone
        else:
            self.TAU = np.ones((m, m))
        self.ETA  = 1.0 / ((self.line + np.eye(m)) * 1e20)

    @staticmethod
    def build_y_index(y_mat, city_vec, m):
        for i in range(m):
            y_mat[i] = city_vec[i:] + city_vec[:i]

    def _reset_population(self):
        n, m = self.index.size
        population = np.ones((n, m), dtype=np.int) * -1
        if n <= m:
            population[:, 0] = np.random.permutation(self.index.city_vec)[:n]
        else:
            population[:m, 0] = np.random.permutation(self.index.city_vec)
            population[m:, 0] = np.random.randint(m, size=n - m)
        return population

    def travelling(self):
        early_stopping_rounds = self.early_stopping_rounds
        route_info = make_route_info()

        n, m = self.index.size
        for epoch in tqdm.tqdm(range(self.epochs), desc=f'{self.name}: {m}'):
            population = self._reset_population()

            route_dist, fitness, fitness_index = self._visiting(population, n, m)

            if self._method == 'cycle':
                self._update_tau_cycle_schema(population, route_dist, n, m)
            elif self._method == 'quantity':
                self._update_tau_quantity(population, n, m)
            else:
                raise Exception(self._method)

            calc_elite(population, fitness, route_dist, fitness_index, route_info, epoch)

            if early_stopping_rounds is not None and epoch - route_info['elite']['epoch'] > early_stopping_rounds:
                break
        return route_info

    def _visiting(self, population, n, m):

        route_dist = np.zeros(n)
        city_mat = self.index.city_mat.copy()
        mask = np.ones_like(population, dtype=np.bool)
        ants = self.index.ants
        for j in range(1, m):
            current_visiting_city = population[:, [j - 1]]

            mask[ants, current_visiting_city.ravel()] = False
            unvisit_city = city_mat[mask].reshape((n, m - j))

            tau = self.TAU[current_visiting_city, unvisit_city]
            eta = self.ETA[current_visiting_city, unvisit_city]

            pheromones = np.power(tau, self.alpha) * np.power(eta, self.beta)
            pheromones = pheromones / pheromones.sum(axis=1, keepdims=True)

            roulette_mat = pheromones.cumsum(axis=1)
            roulette_mat -= np.random.rand(n, 1)

            next_visit_city = unvisit_city[ants, np.argmax(roulette_mat > 0, axis=1)]
            population[:, j] = next_visit_city

            route_i_j_dist = self.line[current_visiting_city.ravel(), next_visit_city]
            if not self.index.onlyStart:
                route_i_j_dist[next_visit_city == 0] = 0
            route_dist += route_i_j_dist

        route_i_j_dist = self.line[population[:, -1], population[:, 0]]
        if not self.index.onlyStart:
            route_i_j_dist[population[:, 0] == 0] = 0
        route_dist += route_i_j_dist

        fitness = 1 / np.log(route_dist + 2)
        fitness_index = np.argsort(fitness)
        return route_dist, fitness, fitness_index

    def _update_tau_cycle_schema(self, population, route_dist, n, m):
        delta_tau = self.quantity / route_dist
        start_index = np.argmin(population, axis=1)
        tau = np.zeros((m, m))
        population_ravel = population.ravel()
        index = (self.index.x_mat + self.index.y_mat[start_index]).ravel()
        tmp_population = population_ravel[index].reshape(n, m).tolist()
        for i in range(n):
            route = tmp_population[i] + tmp_population[i][:1]
            tau[route[:-1], route[1:]] += delta_tau[i]

        if self.use_momentum:
            self.TAU = (1 - self.rho) * self.TAU + tau
        else:
            self.TAU = (1 - self.rho) * self.TAU + self.rho * tau

    def _update_tau_quantity(self, population, n, m):
        tau = np.zeros((m, m))
        
        population_j = population[:, self.index.loop_city_vec[1:]]
        city_i_all = population.ravel()
        city_j_all = population_j.ravel()
        dist_mat = self.line[city_i_all, city_j_all].reshape((n, m))
        dist_mat[dist_mat<1] = 1
        for k in range(n):
            city_i = population[k]
            city_j = population_j[k]
            tau[city_i, city_j] += self.quantity / dist_mat[k]

        if self.use_momentum:
            self.TAU = (1 - self.rho) * self.TAU + tau
        else:
            self.TAU = (1 - self.rho) * self.TAU + self.rho * tau

    def _update_tau_quantity_1(self, population, route_dist, n, m):
        tau = np.zeros((m, m))

        population_j = population[:, self.index.loop_city_vec[1:]]
        city_i_all = population.ravel()
        city_j_all = population_j.ravel()
        dist_mat = self.line[city_i_all, city_j_all].reshape((n, m))
        dist_mat[dist_mat<1] = 1
        
        for k in range(n):
            city_i = population[k]
            city_j = population_j[k]
            tau[city_i, city_j] += self.quantity / (dist_mat[k] + route_dist[k] / m)

        if self.use_momentum:
            self.TAU = self.TAU + (1 - self.rho) * tau
        else:
            self.TAU = self.rho * self.TAU + (1 - self.rho) * tau
