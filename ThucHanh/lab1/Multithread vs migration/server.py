import socket
import json
import threading
from client_server_architecture.data import students


def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        query = conn.recv(1024).decode()
        print(f"Received query: {query}")

        result= []

        for std in students:
            if eval(query):
                result.append(std)
        
        res = json.dumps(result, indent = 2)
        conn.send(res.encode())
    except Exception as e:
        error_msg = json.dumps({"error": str(e)})
        conn.send(error_msg.encode())

    finally:
        print(f"[-] Client {addr} disconnected")
        conn.close()

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind('localhost', 65432)
server.listen()
print("Server is listening on port 65432...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target = handle_client, args=(conn, addr))
    thread.start()

    