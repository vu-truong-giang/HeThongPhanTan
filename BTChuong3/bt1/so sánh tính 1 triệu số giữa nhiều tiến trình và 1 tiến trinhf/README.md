việc chạy code tính tổng 1 triệu số ta thấy singleProccess nhanh hơn multiProccess lý do: 

1.Chi phí tạo proccess (Proccess overhead)
    Khi bạn dùng ProcessPool, Python phải:

-Tạo process mới

-Copy dữ liệu sang process đó

-Gửi kết quả về lại process chính

Các bước này tốn thời gian.

Ví dụ:

Main process
   |
   | chia dữ liệu
   |
Process1  Process2  Process3  Process4

Nếu tác vụ quá nhỏ (ví dụ chỉ cộng số) thì:

thời gian tạo process > thời gian tính toán

2.Truyền dữ liệu quá lớn giữa các proccess

    Python phải copy hàng trăm nghìn số sang mỗi process.
    Chi phí này gọi là:

        IPC (Inter-Process Communication)

Rất tốn thời gian với nhưng bài toán đơn giản này 

3.Tổng 1 triểu phép tính là quá nhẹ 
CPU làm việc này cực nhanh (vài ms).

Do đó: tính toán rất nhỏ
→ overhead process lớn hơn
→ chậm hơn



Nhận xét:

Trong một số trường hợp, chạy nhiều tiến trình không nhanh hơn chạy đơn tiến trình. Điều này xảy ra khi chi phí tạo tiến trình và truyền dữ liệu giữa các tiến trình lớn hơn thời gian thực hiện tác vụ. Với các tác vụ tính toán nhỏ như tính tổng 1 triệu số, việc sử dụng Process Pool có thể không mang lại lợi ích về hiệu suất.