from inspect import CO_VARARGS, CO_VARKEYWORDS
from threading import Thread, Condition

cv = Condition()
thread_printer = 1

class printThread(Thread):

    def __init__(self, id, num_prints):
        Thread.__init__(self)
        self.id = id
        self.num_prints = num_prints

    def predicate(self):
        global thread_printer
        result = self.id == thread_printer
        if result:
            thread_printer = thread_printer % 3 + 1
        return result

    def run(self):
        global cv
        for _ in range(num_prints):
            with cv:
                cv.wait_for(self.predicate)
                print(self.id, end = '')
                cv.notify_all()

if __name__ == '__main__':
    num_prints = int(input())

    threads = [printThread(id + 1, num_prints) for id in range(3)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()