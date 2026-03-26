import socket 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 65432))

std_id = input("Enter stdunet id:")
client_socket.send(std_id.encode())

response = client_socket.recv(1024).decode()
print("Response from server:", response)

client_socket.close()