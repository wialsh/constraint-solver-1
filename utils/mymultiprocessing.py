"""
Created on Fri Oct 18 17:38:58 2019

@author: wialsh

e-mail: hebiyaozizhou@gmail.com
"""


import multiprocessing as mp
from random import uniform, randrange
import time


# def flop_no(rand_nos, a, b):
#     cals = []
#     for r in rand_nos:
#         cals.append(r + a * b)
#     return cals
#
#
# def flop(val, a, b, out_queue):
#     cals = []
#     for v in val:
#         cals.append(v + a * b)
#     # out_queue.put(cals)
#     # time.sleep(3)
#
#
# def concurrency():
#     out_queue = mp.Queue()
#     a = 3.3
#     b = 4.4
#     rand_nos = [uniform(1, 4) for i in range(1000000)]
#     print(len(rand_nos))
#     # for i in range(5):
#     start_time = time.time()
#     p1 = mp.Process(target=flop, args=(rand_nos[:250000], a, b, out_queue))
#     p2 = mp.Process(target=flop, args=(rand_nos[250000:500000], a, b, out_queue))
#     p3 = mp.Process(target=flop, args=(rand_nos[500000:750000], a, b, out_queue))
#     p4 = mp.Process(target=flop, args=(rand_nos[750000:], a, b, out_queue))
#
#     p1.start()
#     p2.start()
#     p3.start()
#     p4.start()
#
#     # print(len(out_queue.get()))
#     # print(len(out_queue.get()))
#     # print(len(out_queue.get()))
#     # print(len(out_queue.get()))
#
#
#     p1.join()
#     p2.join()
#     p3.join()
#     p4.join()
#
#     print("Running time parallel: ", time.time() - start_time, "secs")
#
#
#
# def no_concurrency():
#     a = 3.3
#     b = 4.4
#     rand_nos = [uniform(1, 4) for i in range(1000000)]
#     start_time = time.time()
#     cals = flop_no(rand_nos, a, b)
#     print("Running time serial: ", time.time() - start_time, "secs")

###########################
def flop_no(rand_nos, a, b):
    cals = []
    for r in rand_nos:
        cals.append(r + a * b)
    return cals

def flop(val, a, b, out_queue, start):
    print('here')
    # start.wait()
    cals = []
    for v in val:
        cals.append(v + a * b)
    # out_queue.put(cals)
    # time.sleep(3)

def concurrency():

    out_queue = mp.Queue()
    start = mp.Event()
    a = 3.3
    b = 4.4
    rand_nos = [uniform(1, 4) for i in range(1000000)]
    start_time = time.time()
    print(len(rand_nos))
    # for i in range(5):
    p1 = mp.Process(target=flop, args=(rand_nos[:250000], a, b, out_queue, start))
    p2 = mp.Process(target=flop, args=(rand_nos[250000:500000], a, b, out_queue, start))
    p3 = mp.Process(target=flop, args=(rand_nos[500000:750000], a, b, out_queue, start))
    p4 = mp.Process(target=flop, args=(rand_nos[750000:], a, b, out_queue, start))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    # time.sleep(5) # Wait for processes to start.  See Barrier in Python 3.2+ for a better solution.
    print("go")
    # start.set()

    # print(len(out_queue.get()))
    # print(len(out_queue.get()))
    # print(len(out_queue.get()))
    # print(len(out_queue.get()))
    print("Running time parallel: ", time.time() - start_time, "secs")

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    print("Running time parallel(end): ", time.time() - start_time, "secs")

def no_concurrency():
    a = 3.3
    b = 4.4
    rand_nos = [uniform(1, 4) for i in range(1000000)]
    start_time = time.time()
    cals = flop_no(rand_nos, a, b)
    print("Running time serial: ", time.time() - start_time, "secs")


class MyMultiprocessing(object):
    def __init__(self, ):
        self.__start = mp.Event()

    def from_array(self, func, n):

        processes = [mp.Process(target=func, args=(i,))for i in range(n)]

        [p.start() for p in processes]

        [p.join() for p in processes]




if __name__ == '__main__':
    concurrency()
    no_concurrency()