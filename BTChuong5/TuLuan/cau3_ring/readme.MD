1. Ý tưởng thuật toán Ring Election

Trong Ring Election, các tiến trình được tổ chức theo vòng tròn logic.

Ví dụ:

P1 -> P2 -> P3 -> P4 -> P5 -> quay lại P1

Khi leader bị lỗi:

Một tiến trình phát hiện lỗi sẽ khởi động bầu cử
Nó gửi thông điệp ELECTION cho tiến trình kế tiếp trong vòng
Mỗi tiến trình nhận được thông điệp sẽ:
thêm ID của mình vào danh sách
chuyển tiếp cho tiến trình kế tiếp còn sống
Khi thông điệp quay lại tiến trình khởi tạo:
nó chọn ID lớn nhất trong danh sách
leader mới là tiến trình có ID lớn nhất đó
Sau đó gửi thông điệp COORDINATOR đi quanh vòng để thông báo cho tất cả