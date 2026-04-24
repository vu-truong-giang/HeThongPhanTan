1. Ý tưởng đồng hồ Lamport

Trong hệ phân tán, mỗi tiến trình có một đồng hồ logic riêng, không cần đồng hồ vật lý giống nhau.

Quy tắc Lamport

Giả sử mỗi tiến trình có biến thời gian clock.

Quy tắc 1: Sự kiện nội bộ

Khi tiến trình thực hiện một sự kiện nội bộ:

clock = clock + 1
Quy tắc 2: Gửi tin nhắn

Khi tiến trình gửi tin nhắn:

clock = clock + 1

và đính kèm giá trị clock vào message.

Quy tắc 3: Nhận tin nhắn

Khi tiến trình nhận tin nhắn có timestamp t:

clock = max(clock, t) + 1

Mục đích là để đảm bảo:

nếu một sự kiện xảy ra trước sự kiện khác theo quan hệ nhân quả,
thì timestamp Lamport của nó cũng nhỏ hơn.