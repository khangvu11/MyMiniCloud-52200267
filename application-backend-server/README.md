Nội dung:

# Keycloak – Identity Server

Cung cấp chức năng xác thực & phân quyền cho MyMiniCloud.

## 📌 Thành phần
- Realm: `realm_52200267`
- User:
  - sv01 → role `student`
  - sv02 → không có role (dùng để test chặn truy cập)
- Role: `student`
- Client: `backend-client`

## 🔄 Flow đăng nhập
1. Frontend gửi /api/login
2. Backend gửi request tới Keycloak để lấy Token
3. Backend trả về JWT
4. Frontend lưu JWT và gọi `/student/`
5. Backend xác thực token + role

## 🔧 Docker Volume
Keycloak có database persistent:
- `keycloak-db-trace.db`
- export file realm: `realm-export.json`

## 🧪 Test token bằng curl


curl -X POST http://localhost:8080/realms/.../token
 ...
