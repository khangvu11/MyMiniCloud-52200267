# Prometheus – Monitoring Server

Thu thập metrics từ Node Exporter, NGINX, Backend…

## ⚙️ Cấu hình trong `prometheus.yml`
scrape_configs:

job_name: 'node'
static_configs:

targets: ['node-exporter:9100']

job_name: 'web'
metrics_path: /metrics
static_configs:

targets: ['web-frontend-server:80']

shell
Copy code

## 🔗 UI giao diện
http://localhost:9090


