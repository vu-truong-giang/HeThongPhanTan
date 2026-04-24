import socket
import time

NODE_ID = 3
HOST = "127.0.0.1"
PORT = 5003

NODE1_ADDR = ("127.0.0.1", 5001)
NODE2_ADDR = ("127.0.0.1", 5002)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.settimeout(1)

print(f"[Node {NODE_ID}] Dang chay tai {HOST}:{PORT}")
print(f"[Node {NODE_ID}] Toi la LEADER ban dau")

last_heartbeat = 0

while True:
    now = time.time()

    if now - last_heartbeat >= 2:
        hb = f"HEARTBEAT from Leader {NODE_ID}"
        sock.sendto(hb.encode(), NODE1_ADDR)
        sock.sendto(hb.encode(), NODE2_ADDR)
        print(f"[Node {NODE_ID}] Gui HEARTBEAT den Node 1 va Node 2")
        last_heartbeat = now

    try:
        data, addr = sock.recvfrom(1024)
        msg = data.decode()

        if msg.startswith("ELECTION"):
            print(f"[Node {NODE_ID}] Nhan {msg}")
            sock.sendto(b"OK", addr)
            print(f"[Node {NODE_ID}] Gui OK")
        else:
            print(f"[Node {NODE_ID}] Nhan: {msg}")

    except socket.timeout:
        pass