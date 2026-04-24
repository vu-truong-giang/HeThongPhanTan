import threading
import time
import random

# =========================
# Cấu hình
# =========================
N = 5   # số tiến trình

# =========================
# Lớp Process mô phỏng 1 tiến trình
# =========================
class Process:
    def __init__(self, pid):
        self.pid = pid
        self.alive = True
        self.is_leader = False
        self.in_election = False

    def __str__(self):
        status = "ALIVE" if self.alive else "DOWN"
        leader = " (LEADER)" if self.is_leader else ""
        return f"P{self.pid} [{status}]{leader}"


# =========================
# Hệ thống mô phỏng
# =========================
class BullyElectionSystem:
    def __init__(self, n):
        self.processes = [Process(i) for i in range(1, n + 1)]
        self.lock = threading.Lock()
        self.current_leader = None
        self.initialize_leader()

    # -------------------------
    # Log
    # -------------------------
    def log(self, message):
        print(message)

    # -------------------------
    # Tìm tiến trình alive có ID lớn nhất
    # -------------------------
    def get_highest_alive_process(self):
        alive_processes = [p for p in self.processes if p.alive]
        if not alive_processes:
            return None
        return max(alive_processes, key=lambda p: p.pid)

    # -------------------------
    # Khởi tạo leader ban đầu
    # -------------------------
    def initialize_leader(self):
        leader = self.get_highest_alive_process()
        if leader:
            leader.is_leader = True
            self.current_leader = leader.pid
            self.log(f"[INIT] Leader ban đầu là P{leader.pid}")

    # -------------------------
    # Hiển thị trạng thái hệ thống
    # -------------------------
    def show_status(self):
        self.log("\n===== TRẠNG THÁI HỆ THỐNG =====")
        for p in self.processes:
            self.log(str(p))
        self.log(f"Leader hiện tại: P{self.current_leader}" if self.current_leader else "Không có leader")
        self.log("===============================\n")

    # -------------------------
    # Lấy tiến trình theo ID
    # -------------------------
    def get_process(self, pid):
        for p in self.processes:
            if p.pid == pid:
                return p
        return None

    # -------------------------
    # Giả lập gửi message
    # -------------------------
    def send_message(self, sender_pid, receiver_pid, msg_type):
        self.log(f"P{sender_pid} ---- {msg_type} ----> P{receiver_pid}")

    # -------------------------
    # Leader bị lỗi
    # -------------------------
    def fail_process(self, pid):
        with self.lock:
            p = self.get_process(pid)
            if p and p.alive:
                p.alive = False
                if p.is_leader:
                    p.is_leader = False
                    self.current_leader = None
                    self.log(f"\n[FAIL] Leader P{pid} đã bị lỗi!\n")
                else:
                    self.log(f"\n[FAIL] P{pid} đã bị lỗi!\n")

    # -------------------------
    # Khôi phục tiến trình
    # -------------------------
    def recover_process(self, pid):
        with self.lock:
            p = self.get_process(pid)
            if p and not p.alive:
                p.alive = True
                self.log(f"\n[RECOVER] P{pid} hoạt động trở lại.\n")

    # -------------------------
    # Công bố leader mới
    # -------------------------
    def announce_coordinator(self, leader_pid):
        with self.lock:
            for p in self.processes:
                p.is_leader = False

            leader = self.get_process(leader_pid)
            if leader and leader.alive:
                leader.is_leader = True
                self.current_leader = leader_pid

                self.log(f"\n[COORDINATOR] P{leader_pid} trở thành leader mới\n")
                for p in self.processes:
                    if p.alive and p.pid != leader_pid:
                        self.send_message(leader_pid, p.pid, "COORDINATOR")

    # -------------------------
    # Thuật toán Bully Election
    # -------------------------
    def start_election(self, initiator_pid):
        initiator = self.get_process(initiator_pid)

        if not initiator or not initiator.alive:
            self.log(f"P{initiator_pid} không thể bầu cử vì đã DOWN")
            return

        with self.lock:
            if initiator.in_election:
                return
            initiator.in_election = True

        self.log(f"\n[P{initiator_pid}] PHÁT HIỆN leader lỗi -> BẮT ĐẦU BẦU CỬ")

        higher_processes = [
            p for p in self.processes if p.pid > initiator_pid and p.alive
        ]

        got_ok = False

        # Gửi ELECTION đến các tiến trình có ID lớn hơn
        for p in higher_processes:
            self.send_message(initiator_pid, p.pid, "ELECTION")
            got_ok = True
            self.send_message(p.pid, initiator_pid, "OK")

            # Tiến trình lớn hơn sẽ khởi động bầu cử tiếp
            threading.Thread(target=self.start_election, args=(p.pid,)).start()

        time.sleep(1)

        # Nếu không có ai lớn hơn trả lời -> mình là leader
        if not got_ok:
            self.log(f"P{initiator_pid} không nhận được OK từ tiến trình nào lớn hơn")
            self.announce_coordinator(initiator_pid)

        with self.lock:
            initiator.in_election = False


# =========================
# Chạy mô phỏng
# =========================
def main():
    system = BullyElectionSystem(N)
    system.show_status()

    # -------------------------
    # Tình huống 1: leader hiện tại bị lỗi
    # -------------------------
    old_leader = system.current_leader
    system.fail_process(old_leader)
    system.show_status()

    # Tiến trình P2 phát hiện leader lỗi và bắt đầu election
    system.start_election(2)

    time.sleep(2)
    system.show_status()

    # -------------------------
    # Tình huống 2: leader mới lại bị lỗi
    # -------------------------
    new_leader = system.current_leader
    system.fail_process(new_leader)
    system.show_status()

    # Tiến trình P1 phát hiện leader lỗi
    system.start_election(1)

    time.sleep(2)
    system.show_status()

    # -------------------------
    # Tình huống 3: tiến trình lớn hơn quay lại
    # -------------------------
    system.recover_process(5)
    system.show_status()

    # P5 quay lại có thể tổ chức election để giành lại quyền leader
    system.start_election(5)

    time.sleep(2)
    system.show_status()


if __name__ == "__main__":
    main()