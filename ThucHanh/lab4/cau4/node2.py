import socket
import threading
import time

NODE_ID = 2
HOST = "127.0.0.1"
PORT = 5002

NODE1_ADDR = ("127.0.0.1", 5001)
NODE3_ADDR = ("127.0.0.1", 5003)

HEARTBEAT_TIMEOUT = 5
leader_id = 3
last_heartbeat_time = time.time()
is_leader = False

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.settimeout(1)

print(f"[Node {NODE_ID}] Dang chay tai {HOST}:{PORT}")

def send_message(message, target):
    sock.sendto(message.encode(), target)

def become_leader():
    global leader_id, is_leader
    leader_id = NODE_ID
    is_leader = True
    print(f"[Node {NODE_ID}] Toi tro thanh LEADER moi")

    coordinator_msg = f"COORDINATOR Node {NODE_ID} la leader moi"
    send_message(coordinator_msg, NODE1_ADDR)
    print(f"[Node {NODE_ID}] Gui COORDINATOR den Node 1")

def election():
    print(f"[Node {NODE_ID}] Bat dau bau chon")
    print(f"[Node {NODE_ID}] Gui ELECTION den Node 3")
    send_message(f"ELECTION from Node {NODE_ID}", NODE3_ADDR)

    wait_start = time.time()
    got_ok = False

    while time.time() - wait_start < 3:
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode()

            if msg == "OK":
                print(f"[Node {NODE_ID}] Nhan OK tu Node 3")
                got_ok = True
                break
            elif msg.startswith("HEARTBEAT"):
                print(f"[Node {NODE_ID}] Nhan {msg}")
            elif msg.startswith("COORDINATOR"):
                print(f"[Node {NODE_ID}] Nhan {msg}")

        except socket.timeout:
            pass

        except ConnectionResetError:
            print(f"[Node {NODE_ID}] Node 3 khong phan hoi (WinError 10054)")
            break

    if not got_ok:
        print(f"[Node {NODE_ID}] Khong nhan phan hoi tu Node 3")
        become_leader()
def monitor_leader():
    global last_heartbeat_time

    while True:
        time.sleep(1)
        if not is_leader and time.time() - last_heartbeat_time > HEARTBEAT_TIMEOUT:
            print(f"[Node {NODE_ID}] Khong nhan duoc heartbeat tu Leader {leader_id}")
            election()
            break

threading.Thread(target=monitor_leader, daemon=True).start()

while True:
    try:
        data, addr = sock.recvfrom(1024)
        msg = data.decode()

        if msg.startswith("HEARTBEAT"):
            last_heartbeat_time = time.time()
            print(f"[Node {NODE_ID}] Nhan {msg}")
        elif msg.startswith("COORDINATOR"):
            print(f"[Node {NODE_ID}] Nhan thong bao: {msg}")
        elif msg.startswith("ELECTION"):
            print(f"[Node {NODE_ID}] Nhan ELECTION: {msg}")
        elif msg == "OK":
            print(f"[Node {NODE_ID}] Nhan OK")
        else:
            print(f"[Node {NODE_ID}] Nhan: {msg}")

    except socket.timeout:
        pass
    except ConnectionResetError:
        print(f"[Node {NODE_ID}] Bo qua WinError 10054 do leader da tat")
        pass