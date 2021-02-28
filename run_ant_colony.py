"""
Created on Sun Aug 30 00:04:34 2020

@author: wialsh

@e-mail: hebiyaozizhou@gmail.com
"""
import datetime
import os
import numpy as np
import pandas as pd

from models._ant_colony_travel import AntColonyAlgorithm
import visual

from data import TSPLIBData
from data import TSPData
from data import TSPGoogleData

from utils import haversine


def run_ant_colony_algorithm(tsp_data, method, file, columns):
    results = []
    for name, data_dict in tsp_data:
        if 'line' not in data_dict:
            print(data_dict['data'])
            data_dict['line'] = haversine.haversine_matrix(data_dict['data']).tolist()
        line = np.array(data_dict['line'])
        print(f'line.shape={line.shape}')
        t1 = datetime.datetime.now()
        ant_colony_algorithm = AntColonyAlgorithm(name, line, epochs=500, method=method, early_stopping_rounds=100)
        route_info = ant_colony_algorithm.travelling()
        print(route_info)
        cost = datetime.datetime.now() - t1
        best_dist = route_info['elite']['best_dist']
        results.append([name, int(line.shape[1]), best_dist, 'ant colony', method, cost, datetime.datetime.now()])
        print(f'name: {name}, best_dist: {best_dist}, cost: {cost}')
        assert best_dist > 0
        if 'data' in data_dict or 'coords' in data_dict:
            if 'coords' in data_dict:
                coords = data_dict['coords']
            else:
                coords = data_dict['data']
            print(best_dist)
            print(np.array(coords)[route_info['elite']['best_route']].tolist())
        else:
            coords = None
        visual.visualize(route_info, coords, algorithm_name='AntColonyAlgorithm', name=name, method=method)

    if file is not None:
        results = pd.DataFrame(results, columns=columns)
        results['cost_time'] = results['cost_time'].apply(lambda x: x.value / 10 ** 9)
        results.to_csv(file, index=False, header=False, mode='a')

def main():
    method = 'cycle'
    # method = 'quantity'

    tsplib_data = TSPLIBData()

    file = f'outputs/tsp_result.csv'
    columns = ['name', 'city_length', 'distance', 'algorithm', 'method', 'cost_time', 'dt']
    if not os.path.exists(file):
        pd.DataFrame([], columns=columns).to_csv(
            file, index=False
        )

    run_ant_colony_algorithm(tsplib_data, method, file, columns)

    tsp_data = TSPData()
    run_ant_colony_algorithm(tsp_data, method, file, columns)

    tsp_google_data = TSPGoogleData()
    run_ant_colony_algorithm(tsp_google_data, method, file, columns)


if __name__ == '__main__':
    main()
