import time
import random


class NameServer:
    def __init__(self, name, zone, records=None, children=None, fail_rate=0.0):
        self.name = name
        self.zone = zone
        self.records = records if records else {}
        self.children = children if children else {}
        self.cache = {}
        self.fail_rate = fail_rate

    def query(self, domain):
        print(f"\n[{self.name}] Nhận truy vấn: {domain}")
        time.sleep(0.3)

        if random.random() < self.fail_rate:
            raise TimeoutError(f"{self.name} bị timeout!")

        if domain in self.cache:
            print(f"[{self.name}] Cache hit: {domain} -> {self.cache[domain]}")
            return self.cache[domain]

        if domain in self.records:
            ip = self.records[domain]
            print(f"[{self.name}] Tìm thấy trong records: {domain} -> {ip}")
            self.cache[domain] = ip
            return ip

        next_server = self.find_child_server(domain)

        if next_server:
            print(f"[{self.name}] Chuyển tiếp sang server con: {next_server.name}")
            ip = next_server.query(domain)

            if ip:
                self.cache[domain] = ip

            return ip

        print(f"[{self.name}] Không biết chuyển tiếp đến đâu.")
        return None

    def find_child_server(self, domain):
        for suffix, server in self.children.items():
            if domain.endswith(suffix):
                return server

        return None

    def show_cache(self):
        print(f"\n===== CACHE CỦA {self.name} =====")
        if not self.cache:
            print("Cache trống.")
        else:
            for domain, ip in self.cache.items():
                print(f"{domain} -> {ip}")


example_server = NameServer(
    name="SERVER_example.com",
    zone="example.com",
    records={
        "www.example.com": "192.168.1.10",
        "mail.example.com": "192.168.1.11"
    }
)

test_server = NameServer(
    name="SERVER_test.com",
    zone="test.com",
    records={
        "www.test.com": "192.168.2.10",
        "api.test.com": "192.168.2.11"
    }
)

com_server = NameServer(
    name="SERVER_com",
    zone="com",
    children={
        "example.com": example_server,
        "test.com": test_server
    }
)

vn_server = NameServer(
    name="SERVER_vn",
    zone="vn",
    records={
        "www.nsvien.vn": "172.16.0.10"
    }
)

root_server = NameServer(
    name="SERVER_root",
    zone="root",
    children={
        ".com": com_server,
        ".vn": vn_server
    }
)


def resolve(domain):
    print("\n========== DISTRIBUTED NAME RESOLUTION ==========")

    try:
        ip = root_server.query(domain)

        if ip:
            print(f"\nKẾT QUẢ CUỐI: {domain} -> {ip}")
        else:
            print("\nKhông phân giải được domain.")

    except TimeoutError as e:
        print("Lỗi:", e)

    print("=================================================")


def show_all_cache():
    root_server.show_cache()
    com_server.show_cache()
    example_server.show_cache()
    test_server.show_cache()
    vn_server.show_cache()


while True:
    print("\n===== MENU DISTRIBUTED NAMING =====")
    print("1. Phân giải domain")
    print("2. Xem cache các server")
    print("3. Tăng lỗi timeout cho root server")
    print("4. Tắt lỗi timeout root server")
    print("0. Thoát")

    choice = input("Chọn: ")

    if choice == "1":
        domain = input("Nhập domain: ")
        resolve(domain)

    elif choice == "2":
        show_all_cache()

    elif choice == "3":
        root_server.fail_rate = 0.5
        print("Đã đặt root server có 50% lỗi timeout.")

    elif choice == "4":
        root_server.fail_rate = 0.0
        print("Đã tắt lỗi timeout root server.")

    elif choice == "0":
        break

    else:
        print("Lựa chọn không hợp lệ.")