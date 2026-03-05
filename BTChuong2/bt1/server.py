import socket

HOST = '0.0.0.0'
PORT = 12345

server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server_socket.bind((HOST,PORT))
server_socket.listen(5)
print(f"server đang lắng nghe tại cổng {PORT}")

while True:
    client_socket , addr = server_socket.accept()
    print(f"Kết nối từ {addr}")

    data = client_socket.recv(1024).decode('utf-8')
    print("Client gửi : ", data)

    response = "Server đã nhận thông điệp"
    client_socket.send(response.encode('utf-8'))

    client_socket.close()
