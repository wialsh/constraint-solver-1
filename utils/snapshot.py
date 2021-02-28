# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 12:00:40 2019

@author: wialsh

E-mail: hebiyaozizhou@gmail.com
"""
from typing import Any
import pickle, os
import numpy as np

def snapshot(nfile, data):
    #type: (str, Any) -> None
    st0 = np.random.get_state()
    with open(nfile, 'wb') as fid:
        pickle.dump(st0, fid, pickle.HIGHEST_PROTOCOL)
        if isinstance(data, str):
            pickle.dump(data, fid, pickle.HIGHEST_PROTOCOL)
        else:
            [pickle.dump(d, fid, pickle.HIGHEST_PROTOCOL) for d in range(data)]

def from_snapshot(nfile):
    #type: (str) -> Any
    with open(nfile, 'rb') as fid:
        # st0 = pickle.load(fid)
        while True:
            try:
                yield pickle.load(fid)
            except:
                break
        # np.random.set_state(st0)


def snapshot2(data, fid):
    pickle.dump(data, fid, pickle.HIGHEST_PROTOCOL)



       
    