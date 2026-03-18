#### Tính tổng 1 triệu số bằng process pool 

import multiprocessing
import time


def partial_sum(data):
    return sum(data)

if __name__ == "__main__":
    numbers = list(range(1,1000001))

    n_process = int(input("Nhập số tiến trình :"))
    
    chuck_size = len(numbers) // n_process

    chucks = []


    for i in range(n_process):
        start = i * chuck_size
        end = start + chuck_size
        chucks.append(numbers[start:end])
    
    start_time = time.time()

    with multiprocessing.Pool(n_process) as pool:
        result = pool.map(partial_sum, chucks)
    
    total_sum = sum(result)

    end_time = time.time()

    print("Tổng : ", total_sum)
    print("Thời gian thực hiện : ", end_time - start_time)