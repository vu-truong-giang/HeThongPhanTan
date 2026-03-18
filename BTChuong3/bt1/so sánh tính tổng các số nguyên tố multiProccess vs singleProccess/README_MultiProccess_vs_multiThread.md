#Nhận xét

Cả hai phương pháp đều cho kết quả chính xác giống nhau

Tuy nhiên:

Thread Pool chậm hơn rất nhiều

Process Pool nhanh vượt trội

#Giải thích sự khác biệt

1. GIL (Global Interpreter Lock)

Python có cơ chế:

Chỉ cho phép 1 thread thực thi mã Python tại một thời điểm

👉 Điều này dẫn đến:

Thread không chạy song song thực sự với tác vụ CPU

Các thread phải “chờ nhau”

2. Bản chất bài toán

Bài toán kiểm tra số nguyên tố là:

CPU-bound (tính toán nặng)

👉 Vì vậy:

Loại	Hiệu quả
Thread	❌ Không hiệu quả
Process	✅ Rất hiệu quả

3. Tại sao Process Pool nhanh hơn?

Mỗi process chạy trên core riêng

Không bị GIL

Tính toán song song thật sự

👉 Kết quả:

Process Pool nhanh hơn Thread Pool nhiều lần


#Khi nào nên dùng Thread
Thread phù hợp khi:

Tác vụ I/O (đọc file, gọi API, network)

Không phải tính toán nặng

Ví dụ:

Download file, chat server, web request


#Kết luận

Với bài toán tính tổng số nguyên tố:

Process Pool là lựa chọn tối ưu

Thread Pool không phù hợp do bị giới hạn bởi GIL

Việc lựa chọn đúng mô hình song song ảnh hưởng lớn đến hiệu năng hệ thống