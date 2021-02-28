# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:28:02 2019

@author: wialsh

E-mail: hebiyaozizhou@gmail.com
"""
import time

class Timer(object):
    """A simple timer."""
    def __init__(self):
        self.total_time = 0.
        self.calls = 0
        self.start_time = 0.
        self.diff = 0.
        self.average_time = 0.
        self.origin_time = time.time()
        self.tic()

    def tic(self):
        # using time.time instead of time.clock because time time.clock
        # does not normalize for multithreading
        self.start_time = time.time()

    def toc(self, average=False, reset_time=True, ndigits=2):
        self.diff = round(time.time() - self.start_time, ndigits)
        self.total_time += self.diff
        self.calls += 1
        self.average_time = self.total_time / self.calls
        if reset_time:
            self.tic()
        if average:
            return self.average_time
        else:
            return self.diff

    def too(self, ndigits=2):
        self.origin_diff = round(time.time() - self.origin_time, ndigits)
        return self.origin_diff


    def get_iso8601(self, follow_on=False):
        start = self.__get_start(follow_on)
        self.end = time.time()
        self.__iso8601 = self.__strftime(self.end - start)
        return self.__iso8601

    def get_costime(self, follow_on=False):
        start = self.__get_start(follow_on)
        self.end = time.time()
        return round(self.end - start, 1)

    def __get_start(self, follow_on):
        try:
            start = self.end if follow_on else self.start_time
        except:
            start = self.start_time
        return start

    def __strftime(self, second):
        m, s = divmod(second, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        if not d:
            return "%d:%02d:%02d" % (h, m, s)
        return "%d %d:%02d:%02d" % (d, h, m, s)

    @property
    def iso8601(self):
        try:
            return self.__iso8601
        except:
            return ''