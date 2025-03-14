# Blog Platform Project

## Thông tin cá nhân
- **Họ và tên:** Phan Thành Đạt
- **MSSV:** 22641631
- **Lớp:** DHKHDL18A
- **Email:** Thanhdat2022cltv@gmail.com
- **GitHub:** https://github.com/PhanTDz

## Giới thiệu Project
Blog Platform là một ứng dụng web cho phép người dùng đọc, tạo và quản lý các bài blog. Hệ thống có hai loại người dùng:
- **Actor:** Có thể tạo, sửa, xóa bài viết và thực hiện tất cả chức năng của User thông thường
- **User:** Có thể đọc, lưu bài viết, theo dõi bài viết và bình luận

### Tính năng chính
1. **Quản lý người dùng**
   - Đăng ký tài khoản (Actor/User)
   - Đăng nhập/Đăng xuất
   - Phân quyền người dùng

2. **Quản lý bài viết**
   - Xem danh sách bài viết
   - Tạo bài viết mới (Actor)
   - Chỉnh sửa bài viết (Actor)
   - Xóa bài viết (Actor)
   - Hiển thị hình ảnh ngẫu nhiên cho bài viết

3. **Tương tác**
   - Bình luận bài viết
   - Lưu bài viết
   - Theo dõi bài viết
   - Xem danh sách bài viết đã lưu

## Yêu cầu hệ thống
- Python 3.7 trở lên
- Flask
- SQLite3
- Web browser hiện đại

## Hướng dẫn cài đặt

1. **Clone repository**
```bash
git clone [URL của repository của bạn]
cd blog-platform
```

2. **Tạo môi trường ảo Python**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Cài đặt các thư viện cần thiết**
```bash
pip install -r requirements.txt
```

4. **Khởi tạo database**
```bash
python init_db.py
```

5. **Chạy ứng dụng**
```bash
python app.py
```

6. **Truy cập ứng dụng**
- Mở trình duyệt web và truy cập: `http://localhost:5000`

## Tài khoản mẫu
1. **Tài khoản Actor**
   - Username: dat
   - Password: dat

2. **Tài khoản User thường**
   - Username: admin
   - Password: password123

## Cấu trúc thư mục
```
.
├── app.py              # File chính của ứng dụng
├── requirements.txt    # Các dependency cần thiết
├── static/            # Thư mục chứa file tĩnh (CSS, JS)
│   └── style.css      # File CSS
└── templates/         # Thư mục chứa các template
    ├── admin_dashboard.html
    ├── base.html
    ├── create_post.html
    ├── edit_post.html
    ├── home.html
    ├── login.html
    └── register.html
```

## Công nghệ sử dụng
- Flask: Web framework
- SQLAlchemy: ORM và quản lý database
- Flask-Login: Quản lý phiên đăng nhập
- SQLite: Database
- HTML/CSS: Frontend 

## Công nghệ sử dụng
- **Backend:** Python Flask
- **Database:** SQLite3
- **Frontend:** HTML, CSS
- **Icons:** Font Awesome
- **Fonts:** Google Fonts (Poppins)

## Lưu ý
- Database được lưu trong thư mục `instance/`
- Hình ảnh được lấy tự động từ [picsum.photos](https://picsum.photos/)
- Đảm bảo có kết nối internet để load fonts và icons

## Hỗ trợ
Nếu bạn gặp vấn đề hoặc có câu hỏi, vui lòng:
- Tạo issue trong repository
- Liên hệ qua email: thanhdat2022cltv@gmail.com

## License
[Loại license bạn sử dụng cho project]# ptud-gk-de-1
