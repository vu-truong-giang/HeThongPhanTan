import socket
import threading

HOST = "127.0.0.1"
PORT = 9999

def run_client(i):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        message = f"Hello from client {i}"
        client.send(message.encode())

        response = client.recv(1024).decode()
        print(f"Client {i} nhan: {response}")

        client.close()
    except Exception as e:
        print(f"Client {i} loi: {e}")

threads = []

for i in range(1, 51):
    t = threading.Thread(target=run_client, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Da gui xong 50 request")