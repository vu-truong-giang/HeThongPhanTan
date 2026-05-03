Ý tưởng

DNS thật hoạt động như cây:

Root
 ├── .com
 │     └── example.com
 │            └── www.example.com
Bạn cần làm:
1. Tạo 3 loại server:
Root Server
TLD Server (.com, .vn…)
Authoritative Server
2. Dữ liệu (dùng dict Python)
root = {
    ".com": "tld_com_server"
}

tld_com = {
    "example.com": "auth_example_server"
}

auth_example = {
    "www.example.com": "192.168.1.1"
}
3. Luồng query
Client → Root → TLD → Authoritative → IP