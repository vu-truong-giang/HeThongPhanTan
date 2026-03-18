from concurrent.futures import ThreadPoolExecutor
import time
from primeUtils import prime_sum

start_range = 1
end_range = 1000000
n_thread = 4

step = (end_range - start_range + 1) // n_thread

tasks = []

for i in range(n_thread):
    start = start_range + i * step

    if i == n_thread - 1:
        end = end_range
    else:
        end = start + step - 1

    tasks.append((start, end))

start_time = time.time()

with ThreadPoolExecutor(max_workers=n_thread) as executor:
    results = list(executor.map(lambda x: prime_sum(*x), tasks))

total = sum(results)

end_time = time.time()

print("Tổng số nguyên tố =", total)
print("Thời gian Thread:", end_time - start_time)