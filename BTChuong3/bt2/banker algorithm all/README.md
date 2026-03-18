####Thuật toán dùng để:

Kiểm tra trước khi cấp tài nguyên để tránh deadlock

####Ý tưởng cốt lõi

👉 Chỉ cấp tài nguyên nếu:   Hệ thống vẫn ở trạng thái SAFE
Khi một process chạy xong, nó sẽ:

GIẢI PHÓNG tài nguyên nó đang giữ
💡 Vì thế:
Tài nguyên hệ thống lúc đó = tài nguyên còn lại + tài nguyên process vừa trả
Available + Allocation là: Mô phỏng việc process hoàn thành và trả tài nguyên


#######Các thành phần của hệ thống

Giả sử có:

n tiến trình

m loại tài nguyên

🔹 1. Available (tài nguyên còn lại)

👉 Số lượng tài nguyên mỗi loại đang rảnh

Available = [A1, A2, ..., Am]
🔹 2. Max (nhu cầu tối đa)

👉 Max[i][j]: tiến trình i cần tối đa bao nhiêu tài nguyên j

🔹 3. Allocation (đã cấp)

👉 Allocation[i][j]: tiến trình i đang giữ bao nhiêu tài nguyên j

🔹 4. Need (còn cần)

👉 Công thức:

Need[i][j] = Max[i][j] - Allocation[i][j]

#### Thuật toán kiểm tra trạng thái an toàn (Safety Algorithm)
✳️ Mục tiêu:

👉 Kiểm tra xem hệ thống có thể cho tất cả tiến trình hoàn thành không

🔹 Các bước:
Bước 1:
Work = Available
Finish[i] = False (với mọi i)
Bước 2:

Tìm tiến trình i sao cho:

Finish[i] == False
Need[i] <= Work
Bước 3:

Nếu tìm được:

Work = Work + Allocation[i]
Finish[i] = True

👉 quay lại bước 2

Bước 4:

Nếu tất cả Finish[i] = True → ✅ SAFE

Nếu không → ❌ UNSAFE (có nguy cơ deadlock)


luổng thuật toán: 
Request → check Need → check Available
→ giả lập cấp → chạy is_safe
    → SAFE → cấp thật
    → UNSAFE → rollback

Khi nào UNSAFE?

👉 Khi không tìm được thứ tự chạy:

P1 → P2 → P3 → ... (fail) -> có khả năng deadlock