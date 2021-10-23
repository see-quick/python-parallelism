#!/usr/bin/python

import multiprocessing as mp
import os

class MyProces(mp.Process):

    # static member of class (    # shared counter across all processes)
    shared_data = None

    def __init__(self, myOwnMutex, garlic_count, class_shared_data):
        super().__init__()
        print("CONSTRUCTOR HAS BEEN CALLED")
        self.myOwnMutex = myOwnMutex
        self.garlic_count = garlic_count
        self.class_shared_data = class_shared_data

    def run(self, ) -> None:
        print("RUN METHOD HAS BEEN CALLED")
        print('Process ID: ', os.getpid())

        for i in range(10000):
            self.myOwnMutex.acquire()
            self.garlic_count.value += 1
            self.class_shared_data.value += 1
            self.myOwnMutex.release()

counter = mp.Value('i', 0)

# checking that only main process can create another processes
if __name__ == '__main__':
    myOwnMutex = mp.Lock()
    MyProces.shared_data = mp.Value('i', 0)
    processes = []
    for i in range(5):
        myProcessInstance = MyProces(myOwnMutex, counter, MyProces.shared_data)
        myProcessInstance.start()
        processes.append(myProcessInstance)

    for p in processes:
        p.join()

    print('We should buy', counter, 'garlic.')
    print('Shared data', MyProces.shared_data, 'garlic.')