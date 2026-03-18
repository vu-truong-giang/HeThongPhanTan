
import threading

counter = 0
lock = threading.RLock()

def inner():
    global counter
    with lock:
        counter += 1

def outer():
    with lock:
        inner()

threads = []

for i in range(5):
    t = threading.Thread(target=outer)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Counter:", counter)