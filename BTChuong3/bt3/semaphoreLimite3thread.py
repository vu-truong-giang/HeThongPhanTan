import threading
import time
import random

# Semaphore giới hạn 3 luồng
semaphore = threading.Semaphore(3)

def access_resource(user_id):
    print(f"User {user_id} đang chờ...")

    # xin vào
    semaphore.acquire()
    print(f"User {user_id} đã vào hệ thống")

    # giả lập xử lý
    time.sleep(random.randint(1, 3))

    print(f"User {user_id} rời hệ thống")

    # trả slot
    semaphore.release()


threads = []

# tạo 10 luồng
for i in range(10):
    t = threading.Thread(target=access_resource, args=(i,))
    threads.append(t)
    t.start()

# đợi tất cả xong
for t in threads:
    t.join()

print("Tất cả user đã xong")