Ý tưởng:
Mỗi server giữ một phần dữ liệu
Không có trung tâm
Ví dụ:
Root → biết .com
.com → biết example.com
example.com → biết www.example.com
Logic:
def resolve(domain):
    ask root
    ask tld
    ask authoritative
Đặc điểm:
Không central server ❌
Mỗi node độc lập ✔
Giao tiếp với nhau ✔