"""
Created on Fri Aug 28 00:02:56 2020

@author: wialsh

@e-mail: hebiyaozizhou@gmail.com
"""


import sys, os
import datetime

root_path = '/'.join(os.path.split(os.path.realpath(__file__))[0].split(os.sep)[:-1])
tsplib_path = os.path.join(root_path, 'data', 'dataset', 'tsplib_data')
tsp_path = os.path.join(root_path, 'data', 'dataset')





_get_tsplib_abs_path = lambda x: os.path.join(tsplib_path, x).replace('\\', '/')
_get_tsp_abs_path = lambda x: os.path.join(tsp_path, x).replace('\\', '/')

def get_abs_path(*args):
    return os.path.join(*args).replace('\\', '/')
