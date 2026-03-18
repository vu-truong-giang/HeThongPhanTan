ý tưởng

Process A: giữ Resource 1 → đòi Resource 2

Process B: giữ Resource 2 → đòi Resource 1
→ nếu không xử lý → deadlock

👉 Giải pháp: dùng timeout khi acquire lock

Deadlock được tránh bằng timeout → chuyển từ chờ vô hạn sang chờ có giới hạn
#### timeout.py



Phát hiện và xử lý Deadlock
Nếu timeout xảy ra → coi như deadlock
Giải pháp:

giải phóng tài nguyên

hoặc kill process


