import time


nodes = {
    1: True,
    2: True,
    3: True
}

leader = 3

def send_heartbeat():
    if nodes[leader]:
        print(f"[Node {leader}] (LEADER) gui HEARTBEAT den Node 1, Node 2")
    else:
        print(f"[Node {leader}] da bi tat, khong gui heartbeat")

def detect_failure(node_id):
    print(f"\n[Node {node_id}] Khong nhan duoc heartbeat tu Leader {leader}")
    start_election(node_id)

def start_election(node_id):
    global leader
    print(f"[Node {node_id}] Bat dau ELECTION")

    higher_nodes = [nid for nid in nodes if nid > node_id]

    responded = False

    for nid in higher_nodes:
        print(f"[Node {node_id}] Gui ELECTION den Node {nid}")
        if nodes[nid]:
            print(f"[Node {nid}] Tra loi OK")
            responded = True
        else:
            print(f"[Node {node_id}] Node {nid} KHONG phan hoi")

    if not responded:
        leader = node_id
        print(f"[Node {node_id}] Toi tro thanh LEADER moi")
        announce_coordinator(node_id)

def announce_coordinator(node_id):
    for nid in nodes:
        if nid != node_id and nodes[nid]:
            print(f"[Node {node_id}] Gui COORDINATOR den Node {nid}")
            print(f"[Node {nid}] Cap nhat: Node {node_id} la LEADER moi")



print("=== HE THONG BAT DAU ===")
send_heartbeat()

time.sleep(1)

print("\n=== Node 3 (LEADER) BI TAT ===")
nodes[3] = False

time.sleep(1)


detect_failure(2)