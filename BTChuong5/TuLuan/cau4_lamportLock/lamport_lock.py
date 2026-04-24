import time
import queue
import threading


# =========================
# Message
# =========================
class Message:
    def __init__(self, sender, receiver, timestamp, content):
        self.sender = sender
        self.receiver = receiver
        self.timestamp = timestamp
        self.content = content


# =========================
# Process
# =========================
class Process:
    def __init__(self, pid):
        self.pid = pid
        self.clock = 0
        self.inbox = queue.Queue()
        self.lock = threading.Lock()

    def log(self, message):
        print(f"[P{self.pid} | clock={self.clock}] {message}")

    # -------------------------
    # Sự kiện nội bộ
    # -------------------------
    def internal_event(self, event_name):
        with self.lock:
            self.clock += 1
            self.log(f"SỰ KIỆN NỘI BỘ: {event_name}")

    # -------------------------
    # Gửi message
    # -------------------------
    def send_message(self, receiver_process, content):
        with self.lock:
            self.clock += 1
            msg = Message(
                sender=self.pid,
                receiver=receiver_process.pid,
                timestamp=self.clock,
                content=content
            )
            self.log(
                f"GỬI message -> P{receiver_process.pid} | "
                f"content='{content}', send_ts={msg.timestamp}"
            )

        receiver_process.inbox.put(msg)

    # -------------------------
    # Nhận message
    # -------------------------
    def receive_message(self):
        try:
            msg = self.inbox.get_nowait()
            with self.lock:
                old_clock = self.clock
                self.clock = max(self.clock, msg.timestamp) + 1
                self.log(
                    f"NHẬN message từ P{msg.sender} | "
                    f"content='{msg.content}', msg_ts={msg.timestamp} | "
                    f"clock cập nhật: max({old_clock}, {msg.timestamp}) + 1 = {self.clock}"
                )
        except queue.Empty:
            self.log("Không có message nào để nhận")


# =========================
# Mô phỏng
# =========================
def main():
    # Tạo 3 tiến trình
    p1 = Process(1)
    p2 = Process(2)
    p3 = Process(3)

    print("\n===== BẮT ĐẦU MÔ PHỎNG ĐỒNG HỒ LAMPORT =====\n")

    # Bước 1: Sự kiện nội bộ ở P1
    p1.internal_event("Tính toán dữ liệu cục bộ")
    time.sleep(0.5)

    # Bước 2: P1 gửi message cho P2
    p1.send_message(p2, "Hello từ P1 đến P2")
    time.sleep(0.5)

    # Bước 3: P2 có sự kiện nội bộ trước khi nhận
    p2.internal_event("Kiểm tra hàng đợi")
    time.sleep(0.5)

    # Bước 4: P2 nhận message từ P1
    p2.receive_message()
    time.sleep(0.5)

    # Bước 5: P2 gửi message cho P3
    p2.send_message(p3, "Forward dữ liệu từ P2 đến P3")
    time.sleep(0.5)

    # Bước 6: P3 có 2 sự kiện nội bộ
    p3.internal_event("Xử lý bước 1")
    time.sleep(0.5)
    p3.internal_event("Xử lý bước 2")
    time.sleep(0.5)

    # Bước 7: P3 nhận message từ P2
    p3.receive_message()
    time.sleep(0.5)

    # Bước 8: P3 gửi message về P1
    p3.send_message(p1, "Phản hồi từ P3 về P1")
    time.sleep(0.5)

    # Bước 9: P1 có thêm sự kiện nội bộ
    p1.internal_event("Ghi log hệ thống")
    time.sleep(0.5)

    # Bước 10: P1 nhận message từ P3
    p1.receive_message()
    time.sleep(0.5)

    print("\n===== KẾT THÚC MÔ PHỎNG =====\n")

    print("Giá trị clock cuối cùng:")
    print(f"P1 = {p1.clock}")
    print(f"P2 = {p2.clock}")
    print(f"P3 = {p3.clock}")


if __name__ == "__main__":
    main()