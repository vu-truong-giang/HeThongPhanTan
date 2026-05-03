import random
import time


class DNSServer:
    def __init__(self, name, records, fail_rate=0.0, enabled=True, delay=0.3):
        self.name = name
        self.records = records
        self.fail_rate = fail_rate
        self.enabled = enabled
        self.delay = delay

    def query(self, domain):
        print(f"[{self.name}] Đang truy vấn {domain}")
        time.sleep(self.delay)

        if not self.enabled:
            raise ConnectionError(f"{self.name} đang bị tắt.")

        if random.random() < self.fail_rate:
            raise TimeoutError(f"{self.name} bị lỗi timeout.")

        if domain in self.records:
            return self.records[domain]

        return None


primary_dns = DNSServer(
    name="DNS_PRIMARY",
    records={
        "www.example.com": "192.168.1.10",
        "mail.example.com": "192.168.1.11",
        "www.nsvien.vn": "172.16.0.10"
    },
    fail_rate=0.3
)

backup_dns_list = [
    DNSServer("DNS_BACKUP_1", {
        "www.example.com": "192.168.1.10",
        "mail.example.com": "192.168.1.11",
        "shop.myorg.org": "10.0.0.6"
    }),

    DNSServer("DNS_BACKUP_2", {
        "www.shop.com": "192.168.1.20",
        "www.nsvien.vn": "172.16.0.10"
    })
]

stats = {
    "total_queries": 0,
    "primary_fail": 0,
    "fallback_count": 0
}


def resolve(domain):
    stats["total_queries"] += 1

    print("\n========== BẮT ĐẦU TRUY VẤN ==========")

    try:
        ip = primary_dns.query(domain)

        if ip:
            print(f"[THÀNH CÔNG] Primary trả về: {domain} -> {ip}")
            return

        print("[PRIMARY] Không có domain này.")

    except Exception as e:
        stats["primary_fail"] += 1
        stats["fallback_count"] += 1
        print(f"[LỖI PRIMARY] {e}")
        print("[FALLBACK] Chuyển sang DNS phụ...")

    for backup in backup_dns_list:
        try:
            ip = backup.query(domain)

            if ip:
                print(f"[THÀNH CÔNG] {backup.name} trả về: {domain} -> {ip}")
                return
            else:
                print(f"[{backup.name}] Không có domain.")

        except Exception as e:
            print(f"[LỖI BACKUP] {e}")

    print("[THẤT BẠI] Không tìm thấy domain ở tất cả server.")


def show_stats():
    print("\n===== THỐNG KÊ =====")
    print("Tổng số truy vấn:", stats["total_queries"])
    print("Số lần primary lỗi:", stats["primary_fail"])
    print("Số lần fallback:", stats["fallback_count"])

    if stats["total_queries"] > 0:
        rate = stats["primary_fail"] / stats["total_queries"] * 100
        print(f"Tỷ lệ lỗi primary: {rate:.2f}%")


while True:
    print("\n===== MENU DNS FALLBACK =====")
    print("1. Truy vấn domain")
    print("2. Bật primary")
    print("3. Tắt primary")
    print("4. Xem thống kê")
    print("0. Thoát")

    choice = input("Chọn: ")

    if choice == "1":
        domain = input("Nhập domain: ")
        resolve(domain)

    elif choice == "2":
        primary_dns.enabled = True
        print("Đã bật DNS_PRIMARY.")

    elif choice == "3":
        primary_dns.enabled = False
        print("Đã tắt DNS_PRIMARY.")

    elif choice == "4":
        show_stats()

    elif choice == "0":
        break

    else:
        print("Lựa chọn không hợp lệ.")