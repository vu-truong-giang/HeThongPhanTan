OAuth2 = cách lấy access token từ 1 bên thứ 3

Ví dụ quen thuộc:

Login with Google

####Flow OAuth2 (chuẩn)

Client → redirect user → Google login
      ↓
User login Google
      ↓
Google trả authorization code
      ↓
Client gửi code → lấy access_token
      ↓
Dùng access_token gọi API