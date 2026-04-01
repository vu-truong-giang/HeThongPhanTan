######## Hướng dẫn làm TLS########

BƯỚC 1. Chuẩn bị certificate (bắt buộc)
Bạn cần 3 file:

server.key → private key của server
server.crt → certificate của server
ca.crt → certificate của CA (dùng để verify)

👉 Có thể tạo nhanh bằng OpenSSL:

mở window vào folder TLS chứa server-client, dùng git bash lên : gó 3 lệnh sau 

1. Tạo private key

👉 Gõ lệnh này rồi Enter:

openssl genrsa -out server.key 2048

2. Tạo certificate (server.crt)

👉 Gõ:

openssl req -new -x509 -key server.key -out server.crt -days 365

👉 Sau đó terminal sẽ hỏi bạn nhiều dòng, bạn nhập như sau:

Country Name (2 letter code) [AU]: VN
State or Province Name (full name) []: HCM
Locality Name (eg, city) []: HCM
Organization Name (eg, company) []: MyCompany
Organizational Unit Name (eg, section) []: IT
Common Name (e.g. server FQDN or YOUR name) []: localhost
Email Address []: (Enter bỏ qua)

3. Tạo CA (demo nhanh)

cp server.crt ca.crt

==== sau khi xong vào kiểm tra lại xem đã có 3 file chưa

BƯỚC 2. Bật TLS cho gRPC Server

code python 

BƯỚC 3. Bật TLS cho Client

code python 

###### để làm mutual thì ngoài việc tạo 3 file server thì cần tạo 3 file client 