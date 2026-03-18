from multiprocessing import Process, Pipe

def child(conn):
    msg = conn.recv()
    print("Child received:", msg)

    conn.send("Hello parent")
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()

    p = Process(target=child, args=(child_conn,))
    p.start()

    parent_conn.send("Hello child")
    reply = parent_conn.recv()

    print("Parent received:", reply)

    parent_conn.close()
    p.join()