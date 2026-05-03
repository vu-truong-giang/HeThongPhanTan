import time
from collections import OrderedDict


class DNSCache:
    def __init__(self, capacity=3):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.cache_hit = 0
        self.cache_miss = 0

    def get(self, domain):
        if domain not in self.cache:
            self.cache_miss += 1
            return None

        record = self.cache[domain]
        current_time = time.time()

        if current_time - record["created_at"] > record["ttl"]:
            print(f"[CACHE] {domain} đã hết TTL, xóa cache.")
            del self.cache[domain]
            self.cache_miss += 1
            return None

        self.cache.move_to_end(domain)
        self.cache_hit += 1
        print(f"[CACHE HIT] {domain} -> {record['ip']}")
        return record["ip"]

    def put(self, domain, ip, ttl):
        if domain in self.cache:
            self.cache.move_to_end(domain)

        self.cache[domain] = {
            "ip": ip,
            "ttl": ttl,
            "created_at": time.time()
        }

        if len(self.cache) > self.capacity:
            removed_domain, _ = self.cache.popitem(last=False)
            print(f"[LRU] Cache đầy, xóa domain ít dùng nhất: {removed_domain}")

    def flush(self):
        self.cache.clear()
        print("[CACHE] Đã xóa toàn bộ cache.")

    def show(self):
        if not self.cache:
            print("Cache đang trống.")
            return

        print("\n===== CACHE HIỆN TẠI =====")
        for domain, record in self.cache.items():
            remain = record["ttl"] - (time.time() - record["created_at"])
            print(f"{domain} -> {record['ip']} | TTL còn lại: {remain:.2f}s")

    def stats(self):
        print("\n===== THỐNG KÊ =====")
        print("Cache hit:", self.cache_hit)
        print("Cache miss:", self.cache_miss)


dns_database = {
    "www.example.com": "192.168.1.10",
    "mail.example.com": "192.168.1.11",
    "www.shop.com": "192.168.1.20",
    "shop.myorg.org": "10.0.0.6",
    "www.nsvien.vn": "172.16.0.10"
}


cache = DNSCache(capacity=3)


def real_dns_query(domain):
    print(f"[DNS QUERY] Truy vấn DNS thật cho {domain}")
    time.sleep(0.5)

    if domain in dns_database:
        return dns_database[domain]

    return None


def resolve(domain, ttl):
    print("\n========== PHÂN GIẢI DNS ==========")

    ip = cache.get(domain)

    if ip:
        print(f"Kết quả từ cache: {domain} -> {ip}")
        return

    print("[CACHE MISS] Không có trong cache hoặc đã hết hạn.")

    ip = real_dns_query(domain)

    if ip:
        print(f"Kết quả truy vấn mới: {domain} -> {ip}")
        cache.put(domain, ip, ttl)
    else:
        print("Không tìm thấy domain.")

    print("===================================")


while True:
    print("\n===== MENU DNS CACHE =====")
    print("1. Phân giải domain")
    print("2. Xem cache")
    print("3. Flush cache")
    print("4. Thống kê")
    print("0. Thoát")

    choice = input("Chọn: ")

    if choice == "1":
        domain = input("Nhập domain: ")
        ttl = int(input("Nhập TTL giây: "))
        resolve(domain, ttl)

    elif choice == "2":
        cache.show()

    elif choice == "3":
        cache.flush()

    elif choice == "4":
        cache.stats()

    elif choice == "0":
        break

    else:
        print("Lựa chọn không hợp lệ.")