import socket
import json

def process_string(s):
    # ❗ kiểm tra chuỗi rỗng
    if not s.strip():
        return {
            "error": "Chuoi rong"
        }

    words = s.split()

    return {
        "word_count": len(words),
        "length": len(s),
        "reversed": s[::-1]
    }

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9999))
server.listen(5)

print("Server dang chay...")

while True:
    client, addr = server.accept()
    data = client.recv(1024).decode()

    result = process_string(data)

    client.send(json.dumps(result).encode())
    client.close()