import time

# =========================
# Cấu hình
# =========================
N = 5


# =========================
# Lớp Process
# =========================
class Process:
    def __init__(self, pid):
        self.pid = pid
        self.alive = True
        self.is_leader = False

    def __str__(self):
        status = "ALIVE" if self.alive else "DOWN"
        leader = " (LEADER)" if self.is_leader else ""
        return f"P{self.pid} [{status}]{leader}"


# =========================
# Hệ thống Ring Election
# =========================
class RingElectionSystem:
    def __init__(self, n):
        self.processes = [Process(i) for i in range(1, n + 1)]
        self.current_leader = None
        self.initialize_leader()

    # -------------------------
    # Log
    # -------------------------
    def log(self, message):
        print(message)

    # -------------------------
    # Khởi tạo leader ban đầu
    # -------------------------
    def initialize_leader(self):
        alive = [p for p in self.processes if p.alive]
        if alive:
            leader = max(alive, key=lambda p: p.pid)
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
        if self.current_leader:
            self.log(f"Leader hiện tại: P{self.current_leader}")
        else:
            self.log("Không có leader")
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
    # Tìm tiến trình kế tiếp còn sống trong vòng
    # -------------------------
    def get_next_alive(self, pid):
        n = len(self.processes)
        current_index = pid - 1

        for step in range(1, n + 1):
            next_index = (current_index + step) % n
            next_process = self.processes[next_index]
            if next_process.alive:
                return next_process.pid

        return None

    # -------------------------
    # Giả lập gửi tin nhắn
    # -------------------------
    def send_message(self, sender_pid, receiver_pid, msg_type, content=None):
        if content is not None:
            self.log(f"P{sender_pid} ---- {msg_type} {content} ----> P{receiver_pid}")
        else:
            self.log(f"P{sender_pid} ---- {msg_type} ----> P{receiver_pid}")

    # -------------------------
    # Làm tiến trình bị lỗi
    # -------------------------
    def fail_process(self, pid):
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
        p = self.get_process(pid)
        if p and not p.alive:
            p.alive = True
            self.log(f"\n[RECOVER] P{pid} hoạt động trở lại.\n")

    # -------------------------
    # Thông báo leader mới
    # -------------------------
    def announce_coordinator(self, initiator_pid, leader_pid):
        self.log(f"\n[RESULT] Leader mới được chọn là P{leader_pid}\n")

        for p in self.processes:
            p.is_leader = False

        leader = self.get_process(leader_pid)
        if leader and leader.alive:
            leader.is_leader = True
            self.current_leader = leader_pid

        current = initiator_pid
        next_pid = self.get_next_alive(current)

        while next_pid is not None and next_pid != initiator_pid:
            self.send_message(current, next_pid, "COORDINATOR", f"[leader = P{leader_pid}]")
            current = next_pid
            next_pid = self.get_next_alive(current)
            time.sleep(0.5)

        if next_pid == initiator_pid:
            self.send_message(current, initiator_pid, "COORDINATOR", f"[leader = P{leader_pid}]")

    # -------------------------
    # Bắt đầu Ring Election
    # -------------------------
    def start_election(self, initiator_pid):
        initiator = self.get_process(initiator_pid)

        if not initiator or not initiator.alive:
            self.log(f"P{initiator_pid} không thể khởi động bầu cử vì đã DOWN")
            return

        self.log(f"\n[P{initiator_pid}] PHÁT HIỆN LEADER LỖI -> BẮT ĐẦU RING ELECTION\n")

        election_message = [initiator_pid]

        current = initiator_pid
        next_pid = self.get_next_alive(current)

        # Nếu chỉ còn 1 tiến trình sống
        if next_pid == initiator_pid:
            self.log(f"Chỉ còn P{initiator_pid} hoạt động -> tự trở thành leader")
            self.announce_coordinator(initiator_pid, initiator_pid)
            return

        # Gửi vòng quanh ring
        while next_pid != initiator_pid:
            self.send_message(current, next_pid, "ELECTION", election_message)

            receiver = self.get_process(next_pid)
            if receiver.alive:
                if receiver.pid not in election_message:
                    election_message.append(receiver.pid)
                    self.log(f"P{receiver.pid} thêm ID của mình -> danh sách hiện tại: {election_message}")

            current = next_pid
            next_pid = self.get_next_alive(current)
            time.sleep(0.5)

        # Gửi quay về initiator để kết thúc vòng
        self.send_message(current, initiator_pid, "ELECTION", election_message)
        self.log(f"\n[P{initiator_pid}] nhận lại thông điệp ELECTION: {election_message}")

        # Chọn leader là ID lớn nhất
        new_leader = max(election_message)
        self.announce_coordinator(initiator_pid, new_leader)


# =========================
# Chạy mô phỏng
# =========================
def main():
    system = RingElectionSystem(N)
    system.show_status()

    # -------------------------
    # Tình huống 1: leader hiện tại bị lỗi
    # -------------------------
    old_leader = system.current_leader
    system.fail_process(old_leader)
    system.show_status()

    # P2 phát hiện leader lỗi và khởi động election
    system.start_election(2)
    system.show_status()

    # -------------------------
    # Tình huống 2: leader mới lại bị lỗi
    # -------------------------
    new_leader = system.current_leader
    system.fail_process(new_leader)
    system.show_status()

    # P1 phát hiện leader lỗi
    system.start_election(1)
    system.show_status()

    # -------------------------
    # Tình huống 3: một tiến trình lớn quay lại
    # -------------------------
    system.recover_process(5)
    system.show_status()

    # P3 khởi động election lại
    system.start_election(3)
    system.show_status()


if __name__ == "__main__":
    main()