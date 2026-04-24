import threading
import queue
import time
import random

# =========================
# Cấu hình mô phỏng
# =========================
N = 5                   # số tiến trình
REQUEST_ROUNDS = 2      # mỗi tiến trình sẽ thử vào CS bao nhiêu lần

# =========================
# Biến toàn cục để kiểm tra an toàn
# =========================
cs_lock = threading.Lock()
current_in_cs = 0


class Message:
    def __init__(self, msg_type, sender_id, timestamp):
        self.msg_type = msg_type      # "REQUEST" hoặc "REPLY"
        self.sender_id = sender_id
        self.timestamp = timestamp


class Process(threading.Thread):
    def __init__(self, pid, all_queues):
        super().__init__()
        self.pid = pid
        self.all_queues = all_queues
        self.inbox = all_queues[pid]

        # Lamport clock
        self.clock = 0

        # Trạng thái Ricart-Agrawala
        self.requesting_cs = False
        self.in_cs = False
        self.request_timestamp = None

        # Tập tiến trình bị defer reply
        self.deferred_replies = set()

        # Đếm số reply đã nhận
        self.reply_count = 0

        # Đồng bộ nội bộ
        self.state_lock = threading.Lock()
        self.reply_event = threading.Event()
        self.running = True

    # -------------------------
    # Hàm log
    # -------------------------
    def log(self, message):
        print(f"[P{self.pid} | clock={self.clock}] {message}")

    # -------------------------
    # Lamport clock update
    # -------------------------
    def increment_clock(self):
        self.clock += 1

    def update_clock_on_receive(self, received_ts):
        self.clock = max(self.clock, received_ts) + 1

    # -------------------------
    # Gửi message
    # -------------------------
    def send_message(self, target_pid, msg_type):
        self.increment_clock()
        msg = Message(msg_type, self.pid, self.clock)
        self.all_queues[target_pid].put(msg)
        self.log(f"GỬI {msg_type} -> P{target_pid} (ts={msg.timestamp})")

    def broadcast_request(self):
        for pid in range(N):
            if pid != self.pid:
                self.send_message(pid, "REQUEST")

    # -------------------------
    # Xử lý REQUEST
    # -------------------------
    def handle_request(self, msg):
        with self.state_lock:
            self.update_clock_on_receive(msg.timestamp)
            self.log(f"NHẬN REQUEST từ P{msg.sender_id} (ts={msg.timestamp})")

            send_reply_now = False

            # Nếu không request CS và không ở CS -> reply ngay
            if not self.requesting_cs and not self.in_cs:
                send_reply_now = True

            # Nếu đang ở trong CS -> defer
            elif self.in_cs:
                self.deferred_replies.add(msg.sender_id)
                self.log(f"ĐANG ở CS -> HOÃN REPLY cho P{msg.sender_id}")

            # Nếu cũng đang request CS -> so sánh ưu tiên
            elif self.requesting_cs:
                my_request = (self.request_timestamp, self.pid)
                other_request = (msg.timestamp, msg.sender_id)

                if other_request < my_request:
                    send_reply_now = True
                else:
                    self.deferred_replies.add(msg.sender_id)
                    self.log(
                        f"ƯU TIÊN của mình cao hơn -> HOÃN REPLY cho P{msg.sender_id}"
                    )

        if send_reply_now:
            self.send_message(msg.sender_id, "REPLY")

    # -------------------------
    # Xử lý REPLY
    # -------------------------
    def handle_reply(self, msg):
        with self.state_lock:
            self.update_clock_on_receive(msg.timestamp)
            self.reply_count += 1
            self.log(
                f"NHẬN REPLY từ P{msg.sender_id} "
                f"({self.reply_count}/{N-1})"
            )

            if self.reply_count == N - 1:
                self.reply_event.set()

    # -------------------------
    # Xử lý các message đến
    # -------------------------
    def process_incoming_messages(self, timeout=0.1):
        try:
            msg = self.inbox.get(timeout=timeout)
            if msg.msg_type == "REQUEST":
                self.handle_request(msg)
            elif msg.msg_type == "REPLY":
                self.handle_reply(msg)
        except queue.Empty:
            pass

    # -------------------------
    # Yêu cầu vào critical section
    # -------------------------
    def request_critical_section(self):
        with self.state_lock:
            self.increment_clock()
            self.requesting_cs = True
            self.request_timestamp = self.clock
            self.reply_count = 0
            self.reply_event.clear()

            self.log(f"MUỐN vào CS với timestamp = {self.request_timestamp}")

        # Gửi REQUEST đến tất cả tiến trình khác
        for pid in range(N):
            if pid != self.pid:
                msg = Message("REQUEST", self.pid, self.request_timestamp)
                self.all_queues[pid].put(msg)
                self.log(f"GỬI REQUEST -> P{pid} (ts={self.request_timestamp})")

        # Chờ đủ reply
        while not self.reply_event.is_set():
            self.process_incoming_messages(timeout=0.1)

    # -------------------------
    # Vào critical section
    # -------------------------
    def enter_critical_section(self):
        global current_in_cs

        with self.state_lock:
            self.in_cs = True
            self.requesting_cs = False

        with cs_lock:
            current_in_cs += 1
            if current_in_cs > 1:
                print("\n*** LỖI: Có hơn 1 tiến trình trong critical section! ***\n")

        self.log(">>> VÀO CRITICAL SECTION")
        time.sleep(random.uniform(1, 2))
        self.log("<<< THOÁT CRITICAL SECTION")

        with cs_lock:
            current_in_cs -= 1

    # -------------------------
    # Rời critical section
    # -------------------------
    def release_critical_section(self):
        with self.state_lock:
            self.in_cs = False
            deferred_list = list(self.deferred_replies)
            self.deferred_replies.clear()

        for pid in deferred_list:
            self.send_message(pid, "REPLY")

    # -------------------------
    # Chạy thread tiến trình
    # -------------------------
    def run(self):
        for _ in range(REQUEST_ROUNDS):
            # Chờ ngẫu nhiên trước khi xin vào CS
            time.sleep(random.uniform(0.5, 2.0))

            self.request_critical_section()
            self.enter_critical_section()
            self.release_critical_section()

        # Sau khi xong các lượt, vẫn xử lý nốt message còn lại một lúc
        end_time = time.time() + 2
        while time.time() < end_time:
            self.process_incoming_messages(timeout=0.1)

        self.running = False
        self.log("KẾT THÚC")


def main():
    all_queues = [queue.Queue() for _ in range(N)]
    processes = [Process(pid=i, all_queues=all_queues) for i in range(N)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print("\nHoàn tất mô phỏng Ricart-Agrawala.")


if __name__ == "__main__":
    main()