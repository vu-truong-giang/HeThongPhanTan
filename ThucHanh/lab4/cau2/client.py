import socket

HOST = "127.0.0.1"
PORT = 9999
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

message = f"Hello from client {PORT}"
client.send(message.encode())

response = client.recv(1024).decode()
print(f"Client {PORT} nhan: {response}")

client.close()