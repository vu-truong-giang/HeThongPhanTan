from multiprocessing import Process, Pipe

def child(conn):
    msg = conn.recv()   # nhận từ cha
    print("Child received:", msg)
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()

    p = Process(target=child, args=(child_conn,))
    p.start()

    parent_conn.send("Hello from parent")
    parent_conn.close()

    p.join()