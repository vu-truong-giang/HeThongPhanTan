import threading
import time

counter = 0 #GIL

def increment():
    global counter
    for i in range(10):
        temp = counter
        time.sleep(0.00001)   # làm chậm để tạo race condition
        counter = temp + 1
threads = []

for i in range(5):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Counter:", counter)

##Kết quả mong đợi 5 thread × 100000 = 500000