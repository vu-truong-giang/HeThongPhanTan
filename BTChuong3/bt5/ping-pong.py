from multiprocessing import Process, Pipe

def child(conn):
    for _ in range(3):
        msg = conn.recv()
        print("Child got:", msg)
        conn.send("pong")
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()

    p = Process(target=child, args=(child_conn,))
    p.start()

    for _ in range(3):
        parent_conn.send("ping")
        print("Parent got:", parent_conn.recv())

    parent_conn.close()
    p.join()