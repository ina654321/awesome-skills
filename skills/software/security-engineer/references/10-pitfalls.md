# Security Engineer — Common Pitfalls & Anti-Patterns

## 10.1 High-Severity Anti-Patterns

### 🔴 Anti-Pattern 1: Trusting Frontend Authentication Alone (IDOR)

```
❌ BAD: "User can only see their own data because the frontend hides other records"
✅ GOOD: Backend enforces authorization at the API layer (user_id from session, not request)
```

**Real-world consequence:** In 2019, a major bank's mobile app allowed account takeover via IDOR — changing `account_id=12345` to `account_id=12346` in the API request transferred funds without server-side authorization. $2.4M stolen. (Ref: OWASP IDOR)

**Correct fix:**
```python
# ❌ VULNERABLE — IDOR: user controls the lookup key
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    return db.query("SELECT * FROM orders WHERE id = ?", order_id)

# ✅ SECURE — authorization check from authenticated session
@app.get("/orders/{order_id}")
def get_order(order_id: int, user=Depends(get_current_user)):
    order = db.query(
        "SELECT * FROM orders WHERE id = ? AND user_id = ?",
        order_id, user.id
    )
    if not order:
        raise HTTPException(404, "Order not found")  # Don't reveal existence
    return order
```

**Why it matters:** Frontend filtering is UX, not security. Any API consumer (mobile app, curl, postman) bypasses frontend logic entirely.

---

### 🔴 Anti-Pattern 2: Storing Passwords with Insecure Hashing

```
❌ BAD: MD5("password"), SHA1("password"), or plain text in the database
✅ GOOD: Argon2id (preferred), bcrypt (≥ cost 12), PBKDF2 (≥ 310,000 iterations)
```

**Real-world consequence:** In 2012, LinkedIn stored 117M passwords with SHA1 (no salt). In 2016, the database was dumped and passwords were cracked in hours using rainbow tables.

**Correct implementation:**
```python
# Argon2id — memory-hard, resistant to GPU/ASIC attacks
import argon2

hash = argon2.PasswordHasher(
    time_cost=3,       # Number of iterations
    memory_cost=64 * 1024,  # 64 MiB
    parallelism=1,
    hash_len=32,
    salt_len=16,
)
stored_hash = hash.hash("user_password")
# Verify:
hash.verify(stored_hash, "user_password")
```

**Why it matters:** Breached password databases are cracked offline. MD5/SHA1 can be cracked at billions of hashes per second with commodity GPU. Argon2id requires significant memory per hash, making GPU cracking economically infeasible.

---

### 🔴 Anti-Pattern 3: Missing Rate Limiting on Auth Endpoints

```
❌ BAD: Login endpoint accepts unlimited attempts with no throttling
✅ GOOD: Exponential backoff, account lockout after 5 failures, CAPTCHA
```

**Real-world consequence:** Without rate limiting, credential stuffing attacks can try 100,000+ password combinations per hour against your API. Combined with breached password databases (HaveIBeenPwned: 15B+ credentials), attackers achieve 1-3% success rates on targeted services.

**Correct implementation:**
```python
# Rate limiting with Redis
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("5/minute")  # 5 attempts per minute per IP
def login(request: Request):
    # ... login logic
    pass

# Account lockout after 5 failures (24-hour window)
def check_login_attempts(user_id: int) -> bool:
    attempts = redis.zcount(f"login_attempts:{user_id}", "-inf", "+inf")
    return attempts < 5

def record_failed_attempt(user_id: int):
    now = time.time()
    pipe = redis.pipeline()
    pipe.zadd(f"login_attempts:{user_id}", {str(now): now})
    pipe.expire(f"login_attempts:{user_id}", 86400)  # 24 hours
    pipe.execute()
```

**Why it matters:** Credential stuffing is the #1 authentication attack vector for SaaS applications. NIST SP 800-63B §5.1.1 explicitly requires throttling as a primary countermeasure.

---

### 🔴 Anti-Pattern 4: Hardcoded Secrets in Code or Config

```
❌ BAD: AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE in Dockerfile, .env, docker-compose.yml
✅ GOOD: AWS Secrets Manager / HashiCorp Vault / Kubernetes External Secrets Operator
```

**Real-world consequence:** In 2021, Accenture left 4 cloud storage buckets publicly accessible due to misconfigured credentials in code that were committed to a public GitHub repo. Exposed data: 6TB of client data, API keys, private certificates.

**Correct implementation:**
```yaml
# Kubernetes — External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: database-credentials
  data:
    - secretKey: password
      remoteRef:
        key: prod/database
        property: password
---
# Pod uses Secret (not ConfigMap) — encrypted at rest by Kubernetes
```

```python
# Application reads from mounted Secret, not environment variable
from kubernetes.client import CoreV1Api
import os

api = CoreV1Api()
secret = api.read_namespaced_secret("database-credentials", "default")
db_password = secret.data["password"].decode("base64")
```

**Why it matters:** ENV vars are readable by any process in the container, visible in Kubernetes pod specs (`kubectl get pod -o yaml`), logged by many frameworks, and exposed in error messages. Secrets managers provide dynamic credentials with TTL, audit logging, and automatic rotation.

---

### 🔴 Anti-Pattern 5: Overly Permissive CORS Configuration

```
❌ BAD: Access-Control-Allow-Origin: *  (allows ANY origin on sensitive APIs)
✅ GOOD: Explicit origin allowlist; never use * for APIs handling auth or data
```

**Real-world consequence:** A misconfigured CORS policy on a banking API allowed any website to make authenticated AJAX requests to the bank on behalf of logged-in users. Attackers harvested account balances, transaction history, and personal details.

**Correct implementation:**
```python
# Python Flask — strict CORS
from flask_cors import CORS

CORS(
    app,
    origins=["https://app.example.com", "https://admin.example.com"],
    methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["X-Request-ID"],
    supports_credentials=True,  # Required for cookies/JWT
    max_age=600,  # Cache preflight for 10 minutes
)

# For GraphQL or API gateways, validate Origin explicitly:
@app.before_request
def check_origin():
    allowed = ["https://app.example.com"]
    if request.method == "OPTIONS":
        # Preflight — validate immediately
        if request.headers.get("Origin") not in allowed:
            abort(403)
```

**Why it matters:** CORS `*` means any malicious website can make authenticated requests to your API using the user's browser session. Session cookies and Bearer tokens are automatically sent with cross-origin requests.

---

## 10.2 Medium-Severity Anti-Patterns

### 🟡 Anti-Pattern 6: Insecure Deserialization

```
❌ BAD: pickle.loads(user_data) or eval(user_data) in Python
✅ GOOD: JSON (never pickle/eval), use cryptographically signed sessions
```

**Exploit example:**
```python
# ❌ DANGEROUS — arbitrary code execution via pickle
import pickle
class RCE:
    def __reduce__(self):
        import os
        return (os.system, ("whoami",))

pickle.loads(pickle.dumps(RCE()))  # Executes whoami on the server
```

**Correct fix:**
```python
# ✅ SAFE — JSON only; no code execution possible
import json
data = json.loads(user_data)  # Always safe

# If you need serialization (Redis sessions, etc.):
# Use itsdangerous.Serializer with a signing key
from itsdangerous import Serializer
s = Serializer(SECRET_KEY, serializer=json)
signed_data = s.dumps({"user_id": 123, "role": "admin"})
# Cookie value — tamper-evident but not a security boundary
```

**Why it matters:** Insecure deserialization is OWASP A08 (Deserialization). Python pickle, Java ObjectInputStream, Ruby Marshal can all execute arbitrary code when deserializing attacker-controlled data.

---

### 🟡 Anti-Pattern 7: Missing Security Headers on All Responses

```
❌ BAD: No security headers; XSS, clickjacking, and MIME-sniffing attacks possible
✅ GOOD: Comprehensive response header policy
```

**Required headers:**

| Header | Value | Protection |
|--------|-------|------------|
| `Content-Security-Policy` | `default-src 'self'` | XSS, injection |
| `X-Frame-Options` | `DENY` or `SAMEORIGIN` | Clickjacking |
| `X-Content-Type-Options` | `nosniff` | MIME sniffing |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | HTTPS downgrade |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Referer leakage |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` | Feature abuse |

**Implementation (nginx):**
```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self';";
add_header X-Frame-Options "DENY";
add_header X-Content-Type-Options "nosniff";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";
add_header Referrer-Policy "strict-origin-when-cross-origin";
add_header Permissions-Policy "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=()";
```

**Why it matters:** Security headers are a zero-code-change defense against XSS, clickjacking, and protocol downgrade attacks. They fail open (browsers degrade gracefully) but provide critical protection when present.

---

### 🟡 Anti-Pattern 8: Not Validating File Upload Type (Path Traversal)

```
❌ BAD: Save uploaded file as user-provided filename without sanitization
✅ GOOD: Generate server-side filename, validate MIME type and content
```

**Exploit — path traversal:**
```bash
# User uploads file with name: "../../../etc/passwd"
# Server saves to: /var/www/uploads/../../../etc/passwd → /etc/passwd
# Results in: arbitrary file write on the filesystem
```

**Correct implementation:**
```python
import hashlib
import magic

ALLOWED_EXTENSIONS = {".jpg", ".png", ".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
UPLOAD_DIR = "/var/www/uploads/"

def save_upload(file):
    # 1. Generate random server-side filename
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extension {ext} not allowed")
    
    server_filename = f"{uuid.uuid4().hex}{ext}"
    save_path = Path(UPLOAD_DIR) / server_filename
    
    # 2. Validate MIME type from file content (not extension)
    file_content = file.read(2048)  # Read first 2KB for magic bytes
    mime = magic.from_buffer(file_content, mime=True)
    allowed_mimes = {"image/jpeg", "image/png", "application/pdf"}
    if mime not in allowed_mimes:
        raise ValueError(f"MIME type {mime} not allowed")
    
    # 3. Write with controlled path
    with open(save_path, "wb") as f:
        f.write(file_content)
        f.write(file.read())  # Rest of file
    
    return server_filename
```

---

### 🟡 Anti-Pattern 9: Not Implementing Subresource Integrity (SRI)

```
❌ BAD: Loading third-party JS without integrity verification
✅ GOOD: Use SRI hashes for all external scripts and stylesheets
```

**Attack:** If a CDN serves a malicious JavaScript file (via compromise or DNS hijacking), and your page loads it via `<script src="https://cdn.example.com/lib.js">`, the malicious code runs with full page privileges.

**Correct implementation:**
```html
<!-- Compute SHA256 hash of the file content, embed in integrity attribute -->
<script
  src="https://cdn.example.com/app.js"
  integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxMi9s1K29qftfwQVZ"
  crossorigin="anonymous"
></script>
```

**Why it matters:** Supply chain attacks on JavaScript CDNs are increasing. SRI ensures that even if the CDN is compromised, the browser refuses to execute modified scripts.

---

## 10.3 Red Flags in Security Reviews

| Red Flag | Severity | What It Signals |
|----------|----------|-----------------|
| SQL query with string concatenation (`f"SELECT * FROM {table}")` | 🔴 CRITICAL | SQL injection |
| `eval()`, `exec()`, `pickle.loads()` on user data | 🔴 CRITICAL | Code injection |
| `*` in IAM policy Resource field | 🔴 CRITICAL | Over-privileged; privilege escalation path |
| `autoescape=False` in Jinja2 template engine | 🔴 CRITICAL | Stored/reflected XSS |
| No rate limiting on `/login`, `/reset-password` | 🔴 HIGH | Credential stuffing |
| Session tokens not rotated on login | 🔴 HIGH | Session fixation |
| `Access-Control-Allow-Origin: *` on auth endpoints | 🔴 HIGH | CSRF + data exfiltration |
| File uploads without extension/MIME validation | 🟡 MEDIUM | Path traversal, malware hosting |
| Error messages exposing stack traces in production | 🟡 MEDIUM | Information disclosure |
| `DEBUG=True` in Flask/Django in production | 🟡 MEDIUM | Full application internals exposed |
| Logs containing passwords, tokens, or PII | 🟡 MEDIUM | GDPR/HIPAA violation, insider threat |
| No CSP header on application responses | 🟡 MEDIUM | XSS exploitation easier |
| IMDSv1 enabled on EC2 instances | 🟡 MEDIUM | SSRF → credential theft |
| Secrets in GitHub Actions workflow logs | 🟡 MEDIUM | Secret exposure |
| No MFA on root AWS account | 🟡 MEDIUM | Complete AWS account compromise |
| TLS 1.0/1.1 enabled on payment endpoints | 🟡 MEDIUM | PCI DSS violation; protocol downgrade |
