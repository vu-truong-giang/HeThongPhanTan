#Nhận xét
    Multi-process nhanh hơn rất nhiều (≈ 20 lần trong thử nghiệm).

Lý do:

Các tiến trình chạy song song trên nhiều lõi CPU

Giảm thời gian xử lý tổng thể



#Giải thích sự khác biệt hiệu năng
1.Tại sao Multi-Process nhanh hơn?
Bài toán kiểm tra số nguyên tố là CPU-bound (tính toán nặng)

Python bị giới hạn bởi GIL (Global Interpreter Lock) nên:

Thread không tận dụng được nhiều lõi

Process thì có thể

Vì vậy:

Process Pool → tận dụng đa lõi → nhanh hơn

2. Khi nào Multi-Process không hiệu quả?

Khi dữ liệu nhỏ

Khi chi phí tạo process lớn hơn thời gian tính toán

Khi số process > số core CPU