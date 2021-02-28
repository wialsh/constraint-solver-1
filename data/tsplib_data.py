"""
Created on Thu Aug 27 23:56:01 2020

@author: wialsh

@e-mail: hebiyaozizhou@gmail.com
"""
import os
import json

import numpy as np
from sklearn.neighbors import DistanceMetric
euclidean = DistanceMetric.get_metric('euclidean')

from data._base import tsplib_path
from data._base import _get_tsplib_abs_path


file_list = list(filter(lambda x: '-' in x, os.listdir(tsplib_path)))

class TSPLIBData(object):
    def __init__(self):
        self._data_list = []

    def load(self):
        data_list = []
        for file in file_list:
            with open(_get_tsplib_abs_path(file)) as fp:
                data = json.load(fp)
                # self._views(data)
                data_list.append(data)
        return data_list


    def _views(self, data):
        print(json.dumps(data, indent=2))
        print(data)

    def __iter__(self):
        for data_dict in self.load():
            if len(data_dict['data']) == 0:
                continue
            elif data_dict['data'].get('DIMENSION', 0) > 500:
                continue
            elif 'NODE_COORD_SECTION' in data_dict['data']:
                data_dict['coords'] = data_dict['data']['NODE_COORD_SECTION']
                data_dict['line'] = euclidean.pairwise(data_dict['data']['NODE_COORD_SECTION'])
            elif 'DISPLAY_DATA_SECTION' in data_dict['data']:
                data_dict['coords'] = data_dict['data']['DISPLAY_DATA_SECTION']
                data_dict['line'] = euclidean.pairwise(data_dict['data']['DISPLAY_DATA_SECTION'])
            elif 'EDGE_WEIGHT_SECTION' in data_dict['data']:
                # dist_mat = np.array(data_dict['data']['EDGE_WEIGHT_SECTION'])
                # try:
                #     if dist_mat.shape[0] != dist_mat.shape[1]:
                #         continue
                #     else:
                #         data_dict['dist_mat'] = dist_mat
                # except:
                #     continue
                continue
            else:
                continue

            yield data_dict['data']['NAME'], data_dict

if __name__ == '__main__':
    tsp_data = TSPLIBData()
    tsp_data.load()
