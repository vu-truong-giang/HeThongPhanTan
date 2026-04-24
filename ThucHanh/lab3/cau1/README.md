Remote Procedure Call (RPC) là mô hình giao tiếp trong hệ thống phân tán cho phép một chương trình gọi hàm (procedure) trên máy khác như gọi hàm cục bộ.

👉 Mục tiêu:

Ẩn đi chi tiết truyền thông mạng
Làm cho lập trình phân tán giống lập trình thông thường

####Nguyên lý hoạt động

1.Client gọi hàm (procedure call)
2.Client stub:
    Đóng gói dữ liệu (marshalling)
3.Gửi request qua mạng
4.Server nhận request
5.Server stub:
    Giải mã dữ liệu (unmarshalling)
6.Server thực thi hàm
7.Kết quả được gửi ngược lại cho client

👉 Tóm lại:
Call → Đóng gói → Gửi → Thực thi → Trả kết quả

Client: bên gọi hàm
Client Stub: đại diện phía client
Server Stub: đại diện phía server
Server: nơi chứa hàm thực
Stub đóng vai trò “cầu nối” giữa chương trình và mạng

####Đặc điểm của RPC

Giao tiếp theo kiểu client-server
Thường là đồng bộ (synchronous)
Ẩn chi tiết truyền thông mạng
Sử dụng cơ chế:
Marshalling: đóng gói dữ liệu
Unmarshalling: giải mã dữ liệu

###Khi nào sử dụng RPC#

👉 Dùng khi:

Hệ thống client-server
Cần gọi dịch vụ từ xa như gọi hàm
Microservices giao tiếp trực tiếp

👉 Không phù hợp khi:

Cần bất đồng bộ cao
Hệ thống yêu cầu chịu lỗi tốt, loosely coupled