import time
import random


class DNSServer:
    def __init__(self, name, records, fail_rate=0.0, delay=0.2):
        self.name = name
        self.records = records
        self.fail_rate = fail_rate
        self.delay = delay

    def query(self, key):
        print(f"[{self.name}] Đang truy vấn: {key}")
        time.sleep(self.delay)

        if random.random() < self.fail_rate:
            raise TimeoutError(f"{self.name} bị timeout!")

        if key in self.records:
            print(f"[{self.name}] Tìm thấy: {self.records[key]}")
            return self.records[key]

        print(f"[{self.name}] Không tìm thấy {key}")
        return None


root_server = DNSServer("Root Server", {
    ".com": "TLD_COM",
    ".org": "TLD_ORG",
    ".vn": "TLD_VN"
})

tld_servers = {
    "TLD_COM": DNSServer("TLD .com", {
        "example.com": "AUTH_EXAMPLE",
        "shop.com": "AUTH_SHOP"
    }),

    "TLD_ORG": DNSServer("TLD .org", {
        "myorg.org": "AUTH_MYORG"
    }),

    "TLD_VN": DNSServer("TLD .vn", {
        "nsvien.vn": "AUTH_NSVIEN"
    })
}

auth_servers = {
    "AUTH_EXAMPLE": DNSServer("Authoritative example.com", {
        "www.example.com": "192.168.1.10",
        "mail.example.com": "192.168.1.11"
    }),

    "AUTH_SHOP": DNSServer("Authoritative shop.com", {
        "www.shop.com": "192.168.1.20"
    }),

    "AUTH_MYORG": DNSServer("Authoritative myorg.org", {
        "mail.myorg.org": "10.0.0.5",
        "shop.myorg.org": "10.0.0.6"
    }),

    "AUTH_NSVIEN": DNSServer("Authoritative nsvien.vn", {
        "www.nsvien.vn": "172.16.0.10"
    })
}


def get_tld(domain):
    parts = domain.split(".")
    return "." + parts[-1]


def get_second_level_domain(domain):
    parts = domain.split(".")
    return parts[-2] + "." + parts[-1]


def resolve(domain):
    print("\n========== BẮT ĐẦU PHÂN GIẢI ==========")
    start = time.time()

    try:
        tld = get_tld(domain)
        tld_server_name = root_server.query(tld)

        if not tld_server_name:
            print("Lỗi: Không tìm thấy TLD.")
            return

        tld_server = tld_servers[tld_server_name]

        sld = get_second_level_domain(domain)
        auth_server_name = tld_server.query(sld)

        if not auth_server_name:
            print("Lỗi: Không tìm thấy authoritative server.")
            return

        auth_server = auth_servers[auth_server_name]

        ip = auth_server.query(domain)

        if ip:
            print(f"\nKẾT QUẢ: {domain} -> {ip}")
        else:
            print("\nLỗi: Domain không tồn tại.")

    except TimeoutError as e:
        print("Lỗi timeout:", e)

    end = time.time()
    print(f"Thời gian truy vấn: {end - start:.3f} giây")
    print("========================================")


while True:
    domain = input("\nNhập domain cần phân giải hoặc 'exit': ")

    if domain == "exit":
        break

    resolve(domain)