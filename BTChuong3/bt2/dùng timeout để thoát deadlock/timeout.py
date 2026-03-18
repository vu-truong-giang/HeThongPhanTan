import multiprocessing
import time

lock1 = multiprocessing.Lock()
lock2 = multiprocessing.Lock()

def proccess1():
    print("Process 1: Acquiring lock 1")
    with lock1:
        print("Process 1: Acquired lock 1")
        time.sleep(1)

        print("Process 1: Acquiring lock 2")
        acquired = lock2.acquire(timeout=2)

        if acquired:
            try:
                print("Process 1: Acquired lock 2")
            finally:
                lock2.release()
        else:
            print("Process 1: Timeout while acquiring lock 2")

def proccess2():
    print("Process 2: Acquiring lock 2")
    with lock2:
        print("Process 2: Acquired lock 2")
        time.sleep(1)

        print("Process 2: Acquiring lock 1")
        acquired = lock1.acquire(timeout=2)

        if acquired:
            try:
                print("Process 2: Acquired lock 1")
            finally:
                lock1.release()
        else:
            print("Process 2: Timeout while acquiring lock 1")

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=proccess1)
    p2 = multiprocessing.Process(target=proccess2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()