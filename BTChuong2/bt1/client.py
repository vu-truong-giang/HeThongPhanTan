import socket 

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))

message = input("Nhập thông điệp gửi server : ")
client_socket.send(message.encode('utf-8'))

response = client_socket.recv(1024).decode('utf-8')
print("Server phản hồi : ", response)

client_socket.close()