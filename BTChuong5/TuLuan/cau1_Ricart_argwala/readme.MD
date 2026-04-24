1. Ý tưởng thuật toán Ricart–Agrawala

Khi tiến trình Pi muốn vào critical section (CS):

Tăng logical clock
Gửi REQUEST(timestamp, i) đến tất cả tiến trình khác
Chờ nhận đủ REPLY từ tất cả tiến trình còn lại
Khi đủ reply thì vào CS

Khi tiến trình Pj nhận REQUEST từ Pi:

Nếu Pj không muốn vào CS và không ở trong CS
→ gửi REPLY ngay
Nếu Pj đang ở trong CS
→ trì hoãn (defer) reply
Nếu Pj cũng đang muốn vào CS
→ so sánh độ ưu tiên:
request nào có timestamp nhỏ hơn thì ưu tiên trước
nếu timestamp bằng nhau thì tiến trình có ID nhỏ hơn ưu tiên trước

Khi tiến trình thoát CS:

Gửi REPLY cho tất cả request bị trì hoãn