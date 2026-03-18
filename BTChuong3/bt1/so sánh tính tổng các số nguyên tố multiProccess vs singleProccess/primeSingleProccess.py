import time 
from primeUtils import prime_sum , is_prime

numbers = list(range(1,1000001))

start_time = time.time()

total_sum = prime_sum(1, 1000001)

end_time = time.time()

print("Tổng số nguyên tố =", total_sum)
print("Thời gian thực hiện : ", end_time - start_time)