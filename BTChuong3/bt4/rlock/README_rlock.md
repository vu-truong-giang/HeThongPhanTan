RLock cho phép một thread khóa nhiều lần
RLock (Reentrant Lock) là một loại lock đặc biệt trong đa luồng cho phép cùng một thread có thể khóa (lock) nhiều lần mà không bị treo chương trình.


Ví dụ:

function A
   gọi function B

cả A và B đều dùng lock

Nếu dùng Lock thường → deadlock

Nhưng RLock → không bị


##Cách hoạt động của RLock

RLock lưu thêm 2 thông tin:

1️⃣ Thread nào đang giữ lock

2️⃣ Số lần đã lock

Ví dụ:

Thread A lock lần 1
count = 1

Thread A lock lần 2
count = 2

Thread A unlock
count = 1

Thread A unlock
count = 0 → lock mở



####Khi nào dùng RLock

Dùng khi:

Hàm gọi lồng nhau

Cùng tài nguyên được lock nhiều tầng

Tránh deadlock

Ví dụ:

function A
   -> function B
       -> function C

Cả 3 đều cần lock → RLock an toàn hơn