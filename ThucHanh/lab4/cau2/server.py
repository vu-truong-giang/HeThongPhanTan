import socket
import threading

counter = 0
lock = threading.Lock()

def handle_client(conn):
    global counter

    with lock:
        counter += 1
        current = counter

    conn.send(f"Request number: {current}".encode())
    conn.close()

server = socket.socket()
server.bind(("127.0.0.1", 9999))
server.listen()

print("Server chạy...")

while True:
    conn, addr = server.accept()
    t = threading.Thread(target=handle_client, args=(conn,))
    t.start()