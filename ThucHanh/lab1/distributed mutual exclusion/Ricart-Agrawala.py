import threading
import time
import random

N = 4  # số process

class Process:
    def __init__(self, pid):
        self.pid = pid
        self.timestamp = 0
        self.state = "RELEASED"
        self.reply_count = 0
        self.queue = []

    def request_cs(self):
        self.state = "WANTED"
        self.timestamp = time.time()

        print(f"P{self.pid} muốn vào CS")

        self.reply_count = 0

        # gửi request đến tất cả
        for p in processes:
            if p.pid != self.pid:
                p.receive_request(self.timestamp, self.pid)

        # chờ reply
        while self.reply_count < N - 1:
            time.sleep(0.1)

        self.enter_cs()

    def receive_request(self, ts, pid):
        if (self.state == "RELEASED" or
            (self.state == "WANTED" and (ts, pid) < (self.timestamp, self.pid))):

            processes[pid].receive_reply()
        else:
            self.queue.append(pid)

    def receive_reply(self):
        self.reply_count += 1

    def enter_cs(self):
        self.state = "HELD"
        print(f"🔥 P{self.pid} vào CS")
        time.sleep(random.uniform(1, 2))

        self.exit_cs()

    def exit_cs(self):
        print(f"✅ P{self.pid} rời CS")
        self.state = "RELEASED"

        # trả lời các thằng chờ
        for pid in self.queue:
            processes[pid].receive_reply()

        self.queue = []


# tạo process
processes = [Process(i) for i in range(N)]

# chạy thử
threads = []
for p in processes:
    t = threading.Thread(target=p.request_cs)
    threads.append(t)
    t.start()

for t in threads:
    t.join()