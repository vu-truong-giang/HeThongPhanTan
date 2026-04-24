import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999))

msg = input("Nhập chuỗi: ")
client.send(msg.encode())

response = client.recv(1024).decode()
print("Kết quả:", response)

client.close()