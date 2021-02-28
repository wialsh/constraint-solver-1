# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 10:04:12 2018

@author: wialsh

paper:
    ir.lib.szu.edu.cn:8080/bitstream/244041/2184/1/改进混合蛙跳算法求解旅行商问题.pdf
"""
##-*- Modified shuffled frog-leaping algorithm to solve traveling salesman problem -*-##
import numpy as np
import random

class CycleCrossover:
    
    def crossover(self, ancestor):
        ancestor_ = ancestor[:, :2, :]
        n, _, m = ancestor_.shape
        m_ = np.arange(m)
        ancestorA = ancestor_[:, 1, :]
        ancestorB = ancestor_[:, 0, :]
        childA = np.nonzero(ancestorA[:, np.newaxis] == ancestorB.reshape((n, m, 1)))[2].reshape((n,m))
        childB = np.nonzero(ancestorB[:, np.newaxis] == ancestorB.reshape((n, m, 1)))[2].reshape((n,m))
        childA_idx0 = childA == m_
#        childB_idx0 = childB == m_
        childAB_idx = childA == childB
        childA_idx  = childA_idx0 | childAB_idx
#        childB_idx  = childB_idx0 | childAB_idx
        childA = np.zeros((n, m)).astype(np.int32)
#        childB = np.zeros((n, m)).astype(np.int32)
        childA[childA_idx] = ancestorA[childA_idx]     
#        childB[childA_idx] = ancestorB[childA_idx]
        
        childA_idx = childA_idx==False
        childA[childA_idx] = ancestorB[childA_idx]
#        childB[childA_idx] = ancestorA[childA_idx]
        return childA