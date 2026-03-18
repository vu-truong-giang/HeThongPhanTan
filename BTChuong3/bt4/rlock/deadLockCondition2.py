import threading
import time

counter = 0

def add_one():
    global counter
    temp = counter         
    time.sleep(0.001)       
    counter = temp + 1      
def increment():
    add_one()

threads = []

for i in range(5):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Counter:", counter)