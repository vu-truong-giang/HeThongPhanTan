1. Ý tưởng thuật toán Bully Election

Giả sử có N tiến trình, mỗi tiến trình có một ID.

Leader thường là tiến trình có ID lớn nhất đang còn hoạt động.
Nếu một tiến trình phát hiện leader bị lỗi, nó sẽ:
Gửi thông điệp ELECTION cho tất cả tiến trình có ID lớn hơn nó.
Nếu có tiến trình lớn hơn trả lời OK, thì tiến trình đó sẽ tiếp tục tổ chức bầu cử.
Nếu không có ai trả lời, tiến trình hiện tại sẽ trở thành leader mới và gửi COORDINATOR cho mọi tiến trình khác.
Vì tiến trình có ID lớn nhất sẽ “bắt nạt” các tiến trình nhỏ hơn nên gọi là Bully.