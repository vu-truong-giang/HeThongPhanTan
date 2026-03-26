import socket 
import json 
from data import students


def find_std_by_id(std_id):
    for student in students:
        if student["id"] == std_id:
            return student
    return None

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen()

print("Server is listening on port 65432...")

while True: 
    conn, addr = server_socket.accept()

    print(f"Connected by {addr}")
    try:
        std_id = int(conn.recv(1024).decode())
        student = find_std_by_id(std_id)

        if student:
            response = json.dumps(student)
        else:
            response = json.dumps({"error": "Student not found"})
    except ValueError:
        response = json.dumps({"error": "Invalid student ID"})
    conn.send(response.encode())
    conn.close()