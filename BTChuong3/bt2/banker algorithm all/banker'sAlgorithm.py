import multiprocessing
import time

# 🔥 tính Need
def calculate_need(max_need, allocation):
    n = len(max_need)
    m = len(max_need[0])
    return [[max_need[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]


# 🔥 kiểm tra SAFE
def is_safe(available, max_need, allocation):
    n = len(max_need)
    m = len(available)

    need = calculate_need(max_need, allocation)

    work = available[:]
    finish = [False] * n

    while True:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                finish[i] = True
                found = True
        if not found:
            break

    return all(finish)


# 🔥 xin tài nguyên (có lock để tránh race condition)
def request_resources(pid, request, available, max_need, allocation, lock):
    with lock:
        print(f"\nP{pid} requesting {request}")

        n = len(max_need)
        m = len(available)

        need = calculate_need(max_need, allocation)

        # check Need
        if any(request[j] > need[pid][j] for j in range(m)):
            print(f"P{pid}: ❌ request > need")
            return

        # check Available
        if any(request[j] > available[j] for j in range(m)):
            print(f"P{pid}: ⏳ not enough resource")
            return

        # giả lập cấp phát
        for j in range(m):
            available[j] -= request[j]
            allocation[pid][j] += request[j]

        # check safe
        if is_safe(available, max_need, allocation):
            print(f"P{pid}: ✅ granted")
        else:
            # rollback
            for j in range(m):
                available[j] += request[j]
                allocation[pid][j] -= request[j]
            print(f"P{pid}: ❌ denied (unsafe)")


# 🔥 worker process
def worker(pid, request, available, max_need, allocation, lock):
    time.sleep(1)  # giả lập chạy đồng thời
    request_resources(pid, request, available, max_need, allocation, lock)


if __name__ == "__main__":

    manager = multiprocessing.Manager()

    # shared data
    available = manager.list([3, 3, 2])

    max_need = manager.list([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2]
    ])

    allocation = manager.list([
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2]
    ])

    lock = multiprocessing.Lock()

    # 🔥 3 process xin cùng lúc
    processes = [
        multiprocessing.Process(target=worker, args=(0, [0,1,0], available, max_need, allocation, lock)),
        multiprocessing.Process(target=worker, args=(1, [1,0,2], available, max_need, allocation, lock)),
        multiprocessing.Process(target=worker, args=(2, [3,0,0], available, max_need, allocation, lock)),
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print("\nFinal Available:", list(available))
    print("Final Allocation:", list(allocation))