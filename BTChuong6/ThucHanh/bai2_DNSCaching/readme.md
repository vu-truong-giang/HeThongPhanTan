Ý tưởng:

👉 Lần 1: hỏi đầy đủ
👉 Lần 2: lấy từ cache → nhanh

Cấu trúc cache:
cache = {
    "www.example.com": {
        "ip": "192.168.1.1",
        "ttl": 10,
        "time": time.time()
    }
}
Logic:
Nếu có cache:
    Nếu chưa hết TTL → dùng cache
    Nếu hết TTL → query lại