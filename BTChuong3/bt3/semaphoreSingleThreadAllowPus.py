import threading
import time

# chỉ 1 luồng được ghi
write_semaphore = threading.Semaphore(1)

def write_file(thread_id):
    write_semaphore.acquire()

    with open("output.txt", "a") as f:
        print(f"Thread {thread_id} đang ghi file...")
        f.write(f"Thread {thread_id} ghi vào file\n")
        time.sleep(1)

    print(f"Thread {thread_id} ghi xong")

    write_semaphore.release()


threads = []

for i in range(5):
    t = threading.Thread(target=write_file, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Ghi file hoàn tất")