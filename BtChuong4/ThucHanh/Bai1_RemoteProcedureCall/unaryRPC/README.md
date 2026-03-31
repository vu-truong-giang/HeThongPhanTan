Protocol Buffer là:

“Một định dạng nhị phân (binary) dùng để đóng gói dữ liệu có cấu trúc, giúp truyền dữ liệu hiệu quả hơn JSON/XML.”

Thay vì gửi dữ liệu dạng text như JSON:

{
  "name": "Alice",
  "age": 20
}

👉 Protobuf sẽ:

Định nghĩa trước cấu trúc
Encode thành dạng nhị phân nhỏ gọn

####Cách hoạt động#####

Bước 1: Định nghĩa dữ liệu (.proto)

syntax = "proto3";

message Student {
  string name = 1;
  int32 age = 2;
}

Bước 2:
Dùng compiler (protoc) → sinh code (Python, Java, C++...)

pip install protobuf
protoc --python_out=. student.proto


Bước 3:
Serialize (encode) → gửi qua mạng
Deserialize (decode) → đọc lại dữ liệu

#####4Đặc điểm
Dạng binary (không phải text)
Có schema rõ ràng
Tự sinh code nhiều ngôn ngữ
Rất nhanh và tối ưu



#python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. student.proto