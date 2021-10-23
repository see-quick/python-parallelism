#!/usr/bin/python
import multiprocessing
import os

class ComplexObject:

    _something = None
    _something_more = None

    def __init__(self, instance_var1, instance_var2):
        self.instance_var1 = instance_var1
        self.instance_var2 = instance_var2

class MyProces(multiprocessing.Process):

    # static member of class (    # shared counter across all processes)
    _shared_solver = None

    def __init__(self, pipe):
        super().__init__()
        print("CONSTRUCTOR HAS BEEN CALLED")
        self.pipe = pipe

    def run(self, ) -> None:
        print("RUN METHOD HAS BEEN CALLED")
        print('Process ID: ', os.getpid())

        complexObject = ComplexObject("10", [10, 20, 30])
        ComplexObject._something = 20.0
        ComplexObject._something_more = "dasdasdasHellpo"

        self.pipe.send(complexObject)


class AnotherProcess(multiprocessing.Process):

    # static member of class (    # shared counter across all processes)
    _shared_solver = None

    def __init__(self, pipe):
        super().__init__()
        print("CONSTRUCTOR HAS BEEN CALLED")
        self.pipe = pipe

    def run(self, ) -> None:
        print("RUN METHOD HAS BEEN CALLED")
        print('Process ID: ', os.getpid())

        complexObj = self.pipe.recv()
        print(str(complexObj.instance_var1))
        print(str(complexObj.instance_var2))
        print(str(ComplexObject._something))
        print(str(ComplexObject._something_more))

counter = multiprocessing.Value('i', 0)

# checking that only main process can create another processes
if __name__ == '__main__':
    conn1, conn2 = multiprocessing.Pipe()

    myProcessInstance = MyProces(conn1)
    myAnotherProcesInstacne = AnotherProcess(conn2)

    myProcessInstance.start()
    myAnotherProcesInstacne.start()

    myProcessInstance.join()
    myAnotherProcesInstacne.join()