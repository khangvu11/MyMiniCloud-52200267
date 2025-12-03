Nội dung:

# API Gateway / Reverse Proxy

Sử dụng **NGINX** để định tuyến request trong MyMiniCloud.

## 📌 Chức năng
- Định tuyến frontend → backend → keycloak
- Proxy `/api/`, `/student/`, `/auth/`
- Load balancing cho frontend (phần mở rộng)
- Redirect `/admin/` → `/auth/` (Keycloak UI)

## 🔧 Cấu hình NGINX (nginx.conf)
Ví dụ:


location / {
proxy_pass http://web-frontend-server:80
;
}
location /api/ {
proxy_pass http://application-backend-server:8081/
;
}
location /auth/ {
proxy_pass http://authentication-identity-server:8080/
;
}
location /admin/ {
return 302 /auth/;
}

## ⚙️ Load Balancing (phần mở rộng)

upstream frontend_pool {
server web-frontend-server1:80;
server web-frontend-server2:80;
}
upstream frontend_pool {
server web-frontend-server1:80;
server web-frontend-server2:80;
