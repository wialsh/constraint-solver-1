# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:19:18 2019

@author: wialsh

E-mail: hebiyaozizhou@gmail.com
"""

import threading
import traceback

class MyThreading(threading.Thread):

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.n = kwargs.get('n', -1)

        kwargs.pop('n', None)

        self.args = args
        self.kwargs = kwargs


    def run(self):
        try:
            self.result = self.func(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            self.result = None
        finally:
            del self.func, self.args, self.kwargs

    def get_result(self):
        return self.result
