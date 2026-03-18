from multiprocessing import Process, Pipe

def child(conn, i):
    conn.send(f"Child {i} sending")
    conn.close()

if __name__ == "__main__":
    processes = []
    pipes = []

    for i in range(3):
        parent_conn, child_conn = Pipe()
        p = Process(target=child, args=(child_conn, i))
        processes.append(p)
        pipes.append(parent_conn)
        p.start()

    # Cha đọc
    for conn in pipes:
        print("Parent received:", conn.recv())
        conn.close()

    for p in processes:
        p.join()