import multiprocessing
import time

# cho phép tối đa 2 process dùng tài nguyên
sem = multiprocessing.Semaphore(2)

def worker(name):
    print(f"{name} waiting...")
    with sem:
        print(f"{name} using resource")
        time.sleep(2)
    print(f"{name} released resource")

if __name__ == "__main__":
    processes = []

    for i in range(4):
        p = multiprocessing.Process(target=worker, args=(f"P{i}",))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()