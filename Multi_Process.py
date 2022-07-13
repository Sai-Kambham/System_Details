import multiprocessing
import FIFO
import LIFO

fifo = FIFO.FCFS()
lifo = LIFO.LCFS()

class Multi_Process:
    def Concurrent_Processing(self):
        proc1 = multiprocessing.Process(target=fifo.processData)
        proc2 = multiprocessing.Process(target=lifo.processData)

        proc1.start()
        proc2.start()
        proc1.join()
        proc2.join()



