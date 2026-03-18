import multiprocessing
import time

def worker(name, first, second):
    print(f"{name}: Acquiring first resource")
    with first:
        print(f"{name}: Acquired first resource")
        time.sleep(1)

        print(f"{name}: Waiting for second resource")
        acquired = second.acquire(timeout=2)

        if acquired:
            try:
                print(f"{name}: Acquired second resource")
            finally:
                second.release()
        else:
            print(f"{name}: Timeout -> tránh deadlock")

if __name__ == "__main__":
    # 3 tài nguyên
    R1 = multiprocessing.Lock()
    R2 = multiprocessing.Lock()
    R3 = multiprocessing.Lock()

    # 3 process tạo vòng tròn
    p1 = multiprocessing.Process(target=worker, args=("P1", R1, R2))
    p2 = multiprocessing.Process(target=worker, args=("P2", R2, R3))
    p3 = multiprocessing.Process(target=worker, args=("P3", R3, R1))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()