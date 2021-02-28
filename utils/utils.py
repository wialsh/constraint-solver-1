# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 11:37:14 2019

@author: wialsh
"""
from typing import List, Any
import os, shutil, sys

def list_of_groups(data, cut):
    #type: (List[Any], int) -> List[List[Any]]
    '''
    :param data:
    :param cut: the number of split
    :return: listA => list[lsta0, lsta1, ...]
        list(zip(*(range(10),) *3))
        list(zip(*(iter(range(10)),) *3))
    '''
    data_zip = zip(*(iter(data),) *cut)
    data_groups = [list(d) for d in data_zip]
    count = len(data) % cut
    data_groups.append(data[-count:]) if count !=0 else data_groups
    return data_groups



def join(*text):
    if sys.platform == 'win32':
        f = os.path.join(*text)
        return f.replace('\\', '/')
    else:
        return os.path.join(*text)


def rm(*args):
    files = args
    # res = [__rm(file) for file in files]
    res = [__rm_new(file) for file in files]
    return res

def __rm(file):
    try:
        if os.path.isfile(file):
            os.remove(file)
        else:
            path = join(file)
            shutil.rmtree(path)
    except:
        try:
            path = join(file)
            shutil.rmtree(path)
        except:
            return False
    return True

def __rm_new(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
        else:
            files = os.listdir(path)
            for file in files:
                path_file = os.path.join(path, file)
                if os.path.isfile(path_file):
                    os.remove(path_file)
                else:
                    __rm_new(path_file)
    except:
        return False
    return True



class InputError(ValueError):
    pass

class InputFormatError(ValueError):
    pass
