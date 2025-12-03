
# Web Frontend Server

Thư mục này chứa mã nguồn giao diện người dùng (Student Portal) của hệ thống **MyMiniCloud**.

## 📌 Chức năng chính
- Trang **Login** (login.html)
- Trang **Student Portal** hiển thị thông tin sinh viên (student.html)
- Tích hợp **Keycloak** để xác thực và nhận JWT Token
- Kiểm tra **role** trong JWT: chỉ user có role `student` mới truy cập được
- Gọi API qua **API Gateway** (nginx reverse proxy)
- Dùng fetch() gọi backend và truyền Bearer Token

## 📁 Cấu trúc


web-frontend-server/
│ Dockerfile
│ index.html
│ login.html
│ student.html
└ script.js (tùy dự án)


## 🐳 Dockerfile
Dockerfile build ra image:


levukhang/myminicloud-web:1.0


## 🚀 Chạy frontend local


docker build -t mymini-web .
docker run -p 8080:80 mymini-web


## 🔗 Các route quan trọng qua API Gateway
- `/api/login`
- `/student/`
- `/auth/` → Keycloak

## 🔐 JWT & phân quyền
- Lấy JWT từ Keycloak
- Lưu vào localStorage
- Kiểm tra:
```js
if (!roles.includes("student")) redirect_to_home();


---

# 🟧 2) README cho **application-backend-server/**

Tạo:



application-backend-server/README.md


Nội dung:

```markdown
# Application Backend Server

Backend API cung cấp dữ liệu cho Student Portal, xử lý đăng nhập, kết nối MariaDB và xác thực bằng Keycloak.

## 📌 Chức năng chính
- API `/api/login` → gọi Keycloak để lấy JWT
- API `/student/` → trả danh sách sinh viên
- API `/secure` → yêu cầu Bearer Token hợp lệ
- Kết nối MariaDB
- Validate token bằng thư viện Keycloak Adapter / JWT

## 📁 Cấu trúc


application-backend-server/
│ Dockerfile
│ index.js / server.js
├── controllers/
├── routes/
└── db/


## 🐳 Docker
Dockerfile build backend server:


docker build -t mini-backend .


## 🔗 API quan trọng
| API | Mô tả |
|-----|-------|
| `POST /api/login` | Login user qua Keycloak |
| `GET /student/` | Lấy danh sách sinh viên |
| `GET /secure` | Test JWT Token |

## 🔐 Keycloak Integration
- Realm: `realm_52200267`
- Client: `backend-client`
- Role: `student`
