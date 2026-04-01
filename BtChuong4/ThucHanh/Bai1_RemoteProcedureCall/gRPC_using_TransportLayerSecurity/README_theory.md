TLS (Transport Layer Security) là giao thức dùng để:

Mã hóa dữ liệu khi truyền giữa Client và Server


Không dùng TLS:

Client  ----(plain text)---->  Server

👉 Hacker có thể đọc:

username=admin&password=123456 ❌

Dùng TLS:

Client  ----(encrypted)---->  Server

👉 Hacker chỉ thấy:

asjdh1238asdhakjsdhkasd 🔒

🔥 TLS làm được 3 việc cực quan trọng

1. 🔐 Encryption (Mã hóa)

👉 Biến dữ liệu thành dạng không đọc được

✔ Bảo vệ:

    password
    token
    dữ liệu API

2. 🧾 Authentication (Xác thực)

👉 Đảm bảo:

“Bạn đang nói chuyện với server thật, không phải fake”

✔ thông qua certificate (chứng chỉ)

3. 🛡 Integrity (Toàn vẹn dữ liệu)

👉 Đảm bảo:

“Dữ liệu không bị sửa giữa đường”


###TLS trong gRPC hoạt động như nào?
TLS trong gRPC hoạt động như nào?

Bước 1: Client kết nối
Client → Server: "Hello"

Bước 2: Server gửi certificate
Server → Client: "Đây là chứng chỉ của tao"

Bước 3: Client verify

👉 kiểm tra:

    có đúng CA không
    có hợp lệ không

Bước 4: Tạo key mã hóa

👉 2 bên thống nhất key bí mật

Bước 5: Giao tiếp an toàn
Client ⇄ Server (encrypted)


######TLS vs Mutual TLS

🔹 TLS (1 chiều)

👉 chỉ server có cert

Client → verify Server
🔸 Mutual TLS (2 chiều)

👉 cả 2 đều có cert

Client ⇄ Server verify nhau

👉 dùng trong:

    hệ thống nội bộ
    microservices