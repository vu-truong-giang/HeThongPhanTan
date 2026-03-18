lập trình đa luồng (multithreading) và mục tiêu là hiểu race condition và cách dùng Lock / Mutex / RLock để xử lý

Race condition xảy ra khi:

Nhiều thread (luồng) cùng truy cập

một tài nguyên chung

cùng lúc

→ dẫn tới dữ liệu sai

Ví dụ:

counter = 0

2 thread cùng làm:

counter = counter + 1

Thực tế CPU làm 3 bước:

1. đọc counter
2. cộng 1
3. ghi lại

Nếu 2 thread làm cùng lúc:

Thread A đọc counter = 5
Thread B đọc counter = 5
Thread A ghi 6
Thread B ghi 6

→ lẽ ra phải là 7
→ nhưng kết quả 6

Đây chính là race condition.





Race Condition xảy ra khi nhiều luồng cùng truy cập và cập nhật một tài nguyên chung đồng thời dẫn tới kết quả sai.

Khi không dùng Lock → các luồng ghi dữ liệu cùng lúc → counter sai.

Khi dùng Lock/Mutex → mỗi lần chỉ một luồng truy cập → dữ liệu đúng.

RLock cho phép một luồng khóa nhiều lần giúp tránh deadlock khi gọi hàm lồng nhau.