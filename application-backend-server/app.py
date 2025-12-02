from flask import Flask, jsonify, request
import time, requests, os, json
from jose import jwt
import pymysql

ISSUER = os.getenv("OIDC_ISSUER", "http://authentication-identity-server:8080/realms/realm_52200267")
AUDIENCE = os.getenv("OIDC_AUDIENCE", "account")
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"
_JWKS = None
_TS = 0


def get_jwks():
    global _JWKS, _TS
    now = time.time()
    if not _JWKS or now - _TS > 600:
        _JWKS = requests.get(JWKS_URL, timeout=5).json()
        _TS = now
    return _JWKS


def get_db_connection():
    """
    Tạo kết nối đến MariaDB dùng biến môi trường:
    DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
    (đã cấu hình trong docker-compose.yml)
    """
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "studentdb"),
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4"
    )


app = Flask(__name__)

# === Keycloak OIDC config (dùng lại realm_52200267) ===
OIDC_ISSUER = os.environ.get(
    "OIDC_ISSUER",
    "http://authentication-identity-server:8080/realms/realm_52200267"
)

TOKEN_URL = f"{OIDC_ISSUER}/protocol/openid-connect/token"

KEYCLOAK_CLIENT_ID = "flask-app"   # đúng tên client em đã tạo trong realm


@app.get("/hello")
def hello():
    return jsonify(message="Hello from App Server!")


# ===== MỞ RỘNG 2: /student đọc từ JSON =====
@app.get("/student")
def student():
    with open("students.json") as f:
        data = json.load(f)
    return jsonify(data)


# ===== MỞ RỘNG 3: /student_db đọc từ DB =====
@app.get("/student_db")
def student_db():
    """
    Đọc danh sách sinh viên từ bảng studentdb.students
    và trả về JSON.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, student_id, fullname, dob, major FROM students")
            rows = cur.fetchall()
        return jsonify(rows)
    except Exception as e:
        # Nếu có lỗi, trả về message để dễ debug
        return jsonify(error=str(e)), 500
    finally:
        conn.close()
# ==========================================


@app.get("/secure")
def secure():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify(error="Missing Bearer token"), 401
    token = auth.split(" ", 1)[1]
    try:
        payload = jwt.decode(
            token,
            get_jwks(),
            algorithms=["RS256"],
            audience=AUDIENCE
        )
        return jsonify(
            message="Secure resource OK",
            preferred_username=payload.get("preferred_username"),
        )
    except Exception as e:
        return jsonify(error=str(e)), 401

@app.route("/login", methods=["POST"])
def login():
    """
    Nhận username/password từ body JSON, gọi Keycloak để lấy access token.
    Dùng grant_type=password giống lệnh curl em đã test.
    """
    body = request.get_json(silent=True) or {}
    username = body.get("username")
    password = body.get("password")

    if not username or not password:
        return jsonify({"error": "missing_credentials"}), 400

    # Gọi tới token endpoint của Keycloak
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "password",
            "client_id": KEYCLOAK_CLIENT_ID,
            "username": username,
            "password": password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )

    if resp.status_code != 200:
        # Sai user/pass hoặc cấu hình client
        return jsonify({
            "error": "invalid_credentials",
            "details": resp.text,
        }), 401

    token_data = resp.json()

    # Trả về cho frontend: access_token + thêm chút info
    return jsonify({
        "access_token": token_data.get("access_token"),
        "token_type": token_data.get("token_type", "Bearer"),
        "expires_in": token_data.get("expires_in"),
        "refresh_expires_in": token_data.get("refresh_expires_in"),
        "id_token": token_data.get("id_token"),
        "scope": token_data.get("scope"),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
