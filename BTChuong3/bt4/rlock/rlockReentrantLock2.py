import threading
import time

counter = 0

lock = threading.RLock()

def add_one():
    global counter
    with lock:
        counter += 1


def increment():
    with lock:
        add_one()


threads = []

for i in range(5):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Counter:", counter)