# -*- coding: utf-8 -*-
"""
Created on Tue Apr 03 12:18:02 2018

@author: user
"""
import matplotlib.pyplot as plt
# coding:utf-8
import matplotlib

matplotlib.use(u'qt4agg')
# 指定默认字体
matplotlib.rcParams[u'font.sans-serif'] = [u'SimHei']
matplotlib.rcParams[u'font.family'] = u'sans-serif'
# 解决负号'-'显示为方块的问题
matplotlib.rcParams[u'axes.unicode_minus'] = False

import sys, os
import numpy as np

root_path = '/'.join(os.path.split(os.path.realpath(__file__))[0].split(os.sep)[:-1])
save_path = os.path.join(root_path, 'outputs')


def visualize(route_info, coords=None, algorithm_name=None, name='test', method=None):
    epoch_info = route_info['epoch_info']
    y = epoch_info['distance']
    x = list(range(len(epoch_info['distance'])))

    plt.title(f"{algorithm_name}: {name}")
    plt.xlabel("epoch")
    plt.plot(x, y)

    if method:
        img_file_path = os.path.join(save_path, method, f'{name}_distance.png')
    else:
        img_file_path = os.path.join(save_path, f'{name}_distance.png')

    if name:
        plt.savefig(img_file_path, dpi=500, bbox_inches="tight")
        plt.close()
    else:
        plt.show()

    if coords is not None:
        elite_dict = route_info['elite']
        best_dist = elite_dict['best_dist']
        best_route = elite_dict['best_route']
        city_nums = max(best_route)
        coords = np.array(coords)
        plt.plot(coords[:, 0], coords[:, 1], "r.", marker=u"$\cdot$")
        plt.xlim([int(min(coords[:, 0]) - \
                      min(coords[:, 0]) * 0.5),
                  int(max(coords[:, 0]) + \
                      max(coords[:, 0]) * 0.1)])

        plt.ylim([int(min(coords[:, 1]) - \
                      min(coords[:, 1]) * 0.5),
                  int(max(coords[:, 1]) + \
                      max(coords[:, 1]) * 0.1)])

        # print(best_route)
        for k in range(city_nums):
            i, j = int(best_route[k]), int(best_route[k + 1])
            plt.plot([coords[i, 0], coords[j, 0]],
                     [coords[i, 1], coords[j, 1]], "k")

        ax = plt.gca()
        ax.set_title(f"{name}: {round(best_dist, 1)}")
        # ax.set_xlabel("X")
        # ax.set_ylabel("Y")
        plt.axis('off')
        if method:
            img_file_path = os.path.join(save_path, method, f'{name}_best_route.png')
        else:
            img_file_path = os.path.join(save_path, f'{name}_best_route.png')
        if name:
            plt.savefig(img_file_path, dpi=500, bbox_inches="tight")
            plt.close()
        else:
            plt.show()



