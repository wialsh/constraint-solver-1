# -*- coding: utf-8 -*-
"""
Created on Fri May 25 16:56:56 2018

@author: wialsh
"""
import numpy as np

from models.dataset import Data_and_Param, Elite

class GeneticAlgorithmConstrainedOptimization:
    def __init__(self, chrom_size=4):
        self.dap = Data_and_Param(chrom_size)
        self.elite = Elite()
        
    def update_param(self, data, route):
        self.dap.update(data, route)
        self.dap.processing()
    
    def select(self, roulette=True):
        batch = self.dap.population.shape[0]
        if roulette:
            roulette_ = self.fitness.cumsum()
            roulette_ /= roulette_[-1]
            random_ = np.random.rand(batch)
            idx = ((roulette_ - random_[:, np.newaxis])<0).sum(axis=1)
            self.dap.population = self.dap.population[idx]
        else:
            sort_ = np.argsort(self.fitness)[::-1]
            reserved = int(self.dap.chrom_size * 0.6)
            population_ = self.dap.initialize(self.dap.chrom_size-reserved)
            population = self.dap.population[sort_[:reserved]]
            self.dap.population = np.vstack((population, population_))
            
    def crossover(self, is_shuffle=True):
        n, m = self.dap.population.shape
        if is_shuffle:
            ancestor_ = self.dap.population.copy()
            np.random.shuffle(ancestor_)
        else:
            fitness_sort = np.argsort(self.fitness)[::-1]
            ancestor_ = self.dap.population[fitness_sort]
        uniform_ = np.random.rand(self.dap.chrom_size)
        prob = self.dap.opt.crossover_prob
        cross_idx = uniform_ < prob
        if np.sum(cross_idx) <= 1: return None
        batch = np.sum(cross_idx)   
        maternal_ = np.arange(batch)+1
        spill_ =  maternal_[-1]
        maternal_[-1] = spill_ if spill_<n else 0
        maternal_ = ancestor_[maternal_]
        ancestor_ = ancestor_[:batch]
        point_ = np.random.randint(m, size=batch)
        offspring = map(self._one_point_cross, ancestor_, maternal_, point_)
        offspring = np.array(offspring).reshape((-1, m))
        self.dap.population = offspring.copy()
              
    @staticmethod
    def _one_point_cross(ancestor, maternal, point):
        cx0 = ancestor[point:].copy()
        cx1 = maternal[point:].copy()
        ancestor[point:] = cx1
        maternal[point:] = cx0
        return [ancestor, maternal]

    def mutation(self):
        n, m = self.dap.population.shape
        uniform_ = np.random.random(n)
        mu_idx = uniform_ < self.dap.opt.mutation_prob        
        batch = sum(mu_idx)
        if batch:
            n_mu_idx = np.nonzero(mu_idx)[0]
            pm_point = np.random.randint(m , size=batch)
            mu_values = self.dap.population[n_mu_idx, pm_point]
            mu_values = 2 - 2 ** mu_values
            self.dap.population[n_mu_idx, pm_point] = mu_values        
    
    def elitism(self):
        #update_parent_worst_individual
        if np.max(self.fitness) < self.elite.best_fitness:
            pop_worst = np.argmin(self.fitness) #child_fitness
            #parent_best_tour
            self.dap.population[pop_worst] = self.elite.best_individual.copy()
        fitness_sort = np.argsort(self.fitness)[::-1]
        idx = fitness_sort[:self.dap.chrom_size]
        self.dap.population = self.dap.population[idx]
        self.fitness = self.fitness[idx]
    def update_elite(self, route_time_mat):
        self.elite.update(self.fitness, self.dap.population, route_time_mat)
    
    def evaluate(self):
        batch = self.dap.population.shape[0]
        stay_and_speed = self.dap.decode()
        self.dap.ttp.create_time_series(batch)
        self.dap.ttp.business_update(self.dap.businessTime)
        route_time_mat = self.dap.ttp.evaluate(batch, self.dap.route, stay_and_speed)
        #route_time_mat.shape = (batch, n_city, 4L)
        fitness_ = (route_time_mat[:, :, 1] - route_time_mat[:, :, 0]) / self.dap.stay_time_mat[:, -1]
        fitness_[fitness_ > 1] = 1
        #fitness_ **= 1
        city_rate = route_time_mat[:, :, 2].sum(axis=1)/self.dap.n_city
        self.fitness = np.dot(fitness_, self.dap.score)
        self.fitness += city_rate
        self.route_time_mat = route_time_mat

if __name__ == '__main__':
    print("dangerous")
##-*- End -*-## 