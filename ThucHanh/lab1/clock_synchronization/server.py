import socket
import time

server = socket.socket()
server.bind(("localhost", 6000))
server.listen()

print("⏰ Time Server đang chạy...")

while True:
    conn, addr = server.accept()

    conn.recv(1024)  # nhận request

    server_time = time.time()

    conn.send(str(server_time).encode())
    conn.close()