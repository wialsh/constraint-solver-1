"""
Created on Thu Aug 27 23:57:27 2020

@author: wialsh

@e-mail: hebiyaozizhou@gmail.com
"""

import os
import json

root_path = '/'.join(os.path.split(os.path.realpath(__file__))[0].split(os.sep)[:-1])
tsp_path = os.path.join(root_path, 'data', 'dataset')
files = list(filter(lambda x: 'ReportData' in x, os.listdir(tsp_path)))
names = list(map(lambda x: x.split('.')[0], files))

class TSPData(object):
    def __init__(self):
        self.get_tsp_abs_path = lambda x: os.path.join(tsp_path, x).replace('\\', '/')
        self.file_dict = dict(zip(names, files))

    def load(self):
        for name, file in self.file_dict.items():
            with open(self.get_tsp_abs_path(file)) as fp:
                yield name, json.load(fp)


    def __iter__(self):
        for name, data in self.load():
            # if name == 'ReportData-7000-req':
            yield name, data
