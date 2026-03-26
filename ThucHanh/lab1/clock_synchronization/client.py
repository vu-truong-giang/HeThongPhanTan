import socket
import time
import random

# 🔥 giả lập clock lệch
offset = random.uniform(-5, 5)  # lệch từ -5 đến +5 giây

def local_time():
    return time.time() + offset

client = socket.socket()
client.connect(("localhost", 6000))

t0 = local_time()
client.send(b"time")

server_time = float(client.recv(1024).decode())

t1 = local_time()

# tính RTT
RTT = t1 - t0

# 🔥 thời gian sau đồng bộ
new_time = server_time + RTT / 2

print("⏰ Thời gian trước:", local_time())
print("⏰ Server time   :", server_time)
print("⏰ RTT           :", RTT)
print("⏰ Sau đồng bộ   :", new_time)

client.close()


