import threading

lock = threading.Lock()

def inner():
    lock.acquire()
    print("Inner running")
    lock.release()

def outer():
    lock.acquire()
    print("Outer running")
    inner()
    lock.release()

t = threading.Thread(target=outer)
t.start()


#Vấn đề xảy ra

#Thread đã lock ở outer()

#Khi gọi inner() → lock tiếp lần nữa

#Nhưng Lock thường không cho phép cùng thread lock lần 2

#→ chương trình bị treo (deadlock)