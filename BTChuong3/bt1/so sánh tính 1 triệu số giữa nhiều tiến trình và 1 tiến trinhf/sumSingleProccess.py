import time 

numbers = list(range(1,1000001))

start_time = time.time()
total_sum = sum(numbers)
end_time = time.time()

print("Tổng : ", total_sum)
print("Thời gian thực hiện : ", end_time - start_time)