
```markdown
# MyMiniCloud-52200267

**MyMiniCloud** là một hệ thống “cloud mini” được thiết kế để mô phỏng một môi trường cloud với nhiều dịch vụ (web frontend, backend API, database, object storage, DNS, identity, monitoring, …) chạy trên Docker Compose.  

Mục tiêu của dự án:  
- Triển khai 9+ dịch vụ containerized bằng Docker Compose, chạy local và sẵn sàng deploy lên môi trường thật (như EC2).  
- Hỗ trợ giao diện frontend (Student Portal), backend API + DB, xác thực/ phân quyền với Keycloak, object storage, DNS nội bộ, API Gateway/ Reverse Proxy + Load Balancer, hệ thống monitoring (Prometheus, Grafana, Node Exporter).  
- Push ít nhất 1 image tùy chỉnh lên Docker Hub và cấu hình docker-compose sử dụng image đó.  

---

## 📂 Cấu trúc thư mục

```

(MyMiniCloud-52200267 root)
│  docker-compose.yml
│
├─ web-frontend-server/            # source + Dockerfile frontend
├─ application-backend-server/     # source + backend API + DB logic
├─ relational-database-server/     # DB init scripts (MariaDB)
├─ authentication-identity-server/ # config cho Keycloak
├─ internal-dns-server/            # cấu hình BIND9 DNS nội bộ
├─ object-storage-server/          # MinIO config
├─ monitoring-prometheus-server/   # Prometheus config
├─ monitoring-grafana-dashboard-server/ # Grafana + dashboard config
├─ monitoring-node-exporter-server/ # Node Exporter config
└─ [các folder khác theo dịch vụ mở rộng nếu có]

````

---

## ✅ Yêu cầu & chuẩn bị trước khi chạy

- Cài đặt Docker & Docker Compose (phiên bản hỗ trợ `docker compose up`).  
- (Nếu deploy lên server/VPS) Cổng mạng cần mở (SSH, 80, 443, cổng dịch vụ monitoring nếu sử dụng).  
- (Local) Máy có đủ tài nguyên để chạy ~9–10 container đồng thời (CPU, RAM, disk).  

---

## 🚀 Cách chạy local (development / demo)

Từ thư mục root của project:

```bash
docker compose up -d
````

Lệnh này sẽ build (nếu cần) và khởi động toàn bộ stack MyMiniCloud.

Kiểm tra trạng thái:

```bash
docker compose ps
```

Truy cập dịch vụ qua browser / curl theo port mà bạn đã map (có thể cấu hình trong `docker-compose.yml`).

---

## 🌐 Docker Hub – Pull image tùy chỉnh

Project đã gồm image frontend được build & push lên Docker Hub:

* Repository: `levukhang/myminicloud-web`
* Tags: `1.0`, `latest`

Nếu bạn muốn skip build frontend, docker-compose đã có cấu hình để pull image này:

```yaml
web-frontend-server:
  image: levukhang/myminicloud-web:1.0
  ...
```

---

## 🔧 Cấu hình & triển khai nâng cao

* Bạn có thể thay đổi cấu hình dịch vụ (ports, volumes, environment vars…) trong `docker-compose.yml`.
* Nếu muốn đảm bảo hiệu năng/ổn định hơn, nên dùng external volume cho DB / MinIO / Keycloak data để dữ liệu không mất sau restart.
* Bạn có thể deploy stack lên máy chủ (VPS/EC2), cấu hình firewall / security group để mở các port cần thiết, và dùng domain + reverse proxy nếu muốn.

---

## 📚 Giới thiệu chức năng chính

| Thành phần                           | Mô tả / Chức năng                                                                        |
| ------------------------------------ | ---------------------------------------------------------------------------------------- |
| Web Frontend                         | Giao diện Student Portal + login / logout / JWT                                          |
| Backend API + DB                     | Logic xử lý, API cho frontend, truy xuất MariaDB                                         |
| Identity Server (Keycloak)           | Xác thực / phân quyền OIDC, quản lý user/role                                            |
| API Gateway / Reverse Proxy          | Định tuyến route + load balancing (nếu có nhiều frontend)                                |
| DNS nội bộ                           | BIND9 — phục vụ DNS nội bộ giữa các container                                            |
| Object Storage                       | MinIO dùng object storage như S3 (chứa file, dữ liệu tĩnh…)                              |
| Monitoring Stack                     | Node Exporter + Prometheus + Grafana — đo metric + dashboard “System Health of 52200267” |
| Load Balancer (nếu cấu hình mở rộng) | Cân tải giữa nhiều frontend                                                              |

---

## 📦 Yêu cầu Docker Hub & cài đặt image đã build sẵn

Nếu bạn không muốn build frontend (tiết kiệm thời gian), docker-compose mặc định dùng image đã build sẵn từ Docker Hub. Bạn chỉ cần `docker compose up -d`.

Nếu muốn rebuild từ source — hoặc thay đổi frontend — bạn có thể:

```bash
cd web-frontend-server
docker build -t levukhang/myminicloud-web:1.0 .
docker tag levukhang/myminicloud-web:latest
# rồi docker compose up -d
```

---

## 📖 README phụ / tài liệu bổ sung

Bạn nên chuẩn bị thêm các file sau để báo cáo/ triển khai dễ hơn:

* `README-LOCAL.md`: hướng dẫn chạy local & demo nhanh
* `README-EC2.md`: hướng dẫn deploy trên AWS EC2 (mở port, security group, pull image, run docker compose…)
* `README-SCREENSHOTS.md` hoặc folder `screenshots/`: chứa ảnh screenshot state của dashboard, service list, login portal… để làm báo cáo PDF / slide

---

## 📝 Một số lưu ý & best practices

* Sử dụng file `.env` (nếu có thông tin nhạy cảm: password DB, secret key…) — tránh hardcode credentials.
* Đảm bảo volume persistent cho DB, MinIO, Keycloak data để tránh mất dữ liệu sau recreate container.
* Nếu triển khai thực tế — cân nhắc security: HTTPS, firewall, backup dữ liệu, cấu hình mạng riêng (VPC / subnet / security group).

---

## 👥 Tác giả & Liên hệ

* Repository của bạn: **[https://github.com/levukhang/MyMiniCloud-52200267](https://github.com/levukhang/MyMiniCloud-52200267)**
* Docker Hub image: **[https://hub.docker.com/r/levukhang/myminicloud-web](https://hub.docker.com/r/levukhang/myminicloud-web)**
* Người thực hiện: Khang Vu (mssv: 52200267)

---

## 🎯 Tóm tắt lý do viết README này

README này giúp người dùng — hoặc giảng viên đánh giá — nhanh chóng:

* Hiểu mục tiêu & kiến trúc của MyMiniCloud
* Biết cách khởi chạy local hoặc dùng image đã build sẵn
* Có link dẫn đến Docker Hub (image custom) → chứng minh đã push
* Có cái nhìn tổng quan về thành phần, cấu trúc và cách mở rộng/deploy


