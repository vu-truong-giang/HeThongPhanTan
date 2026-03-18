import multiprocessing
import time
from primeUtils import prime_sum

if __name__ == "__main__":

    numbers = list(range(1, 1000001))

    n_process = int(input("Nhập số tiến trình: "))

    step = (len(numbers) + 1) // n_process

    tasks = []

    for i in range(n_process):
        start = i * step

        if i == n_process - 1:
            end = len(numbers)
        else:
            end = start + step

        tasks.append((start, end))

    print("Các đoạn xử lý:", tasks)  # debug

    start_time = time.time()

    with multiprocessing.Pool(n_process) as pool:
        results = pool.starmap(prime_sum, tasks)

    total = sum(results)

    end_time = time.time()

    print("Tổng số nguyên tố =", total)
    print("Thời gian:", end_time - start_time)