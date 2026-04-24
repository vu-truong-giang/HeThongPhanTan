import socket

NODE_ID = 1
HOST = "127.0.0.1"
PORT = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"[Node {NODE_ID}] Dang chay tai {HOST}:{PORT}")

while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode()

    if msg.startswith("HEARTBEAT"):
        print(f"[Node {NODE_ID}] Nhan {msg}")
    elif msg.startswith("COORDINATOR"):
        print(f"[Node {NODE_ID}] Nhan thong bao leader moi: {msg}")
    elif msg.startswith("ELECTION"):
        print(f"[Node {NODE_ID}] Nhan ELECTION: {msg}")
    else:
        print(f"[Node {NODE_ID}] Nhan: {msg}")