import multiprocessing
import time
import os

def worker(lock1, lock2, name, deadlock_flag):
    print(f"{name}: Acquiring lock1")
    with lock1:
        print(f"{name}: Acquired lock1")
        time.sleep(1)

        print(f"{name}: Waiting for lock2")
        acquired = lock2.acquire(timeout=2)

        if acquired:
            try:
                print(f"{name}: Acquired lock2")
            finally:
                lock2.release()
        else:
            print(f"{name}: Deadlock detected!")
            deadlock_flag.value = 1   # báo về main

if __name__ == "__main__":
    lock1 = multiprocessing.Lock()
    lock2 = multiprocessing.Lock()

    deadlock_flag = multiprocessing.Value('i', 0)

    p1 = multiprocessing.Process(target=worker, args=(lock1, lock2, "P1", deadlock_flag))
    p2 = multiprocessing.Process(target=worker, args=(lock2, lock1, "P2", deadlock_flag))

    p1.start()
    p2.start()

    # Theo dõi
    while True:
        if deadlock_flag.value == 1:
            print("Main: Deadlock detected -> killing processes")
            p1.terminate()
            p2.terminate()
            break

        if not p1.is_alive() and not p2.is_alive():
            break

        time.sleep(0.5)

    p1.join()
    p2.join()