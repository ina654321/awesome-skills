# Security Engineer — Scenario Examples

## 9.1 SQL Injection in Python API Endpoint

**Context:** A developer reports that a search endpoint is returning unexpected results. The application is a Python Flask API backed by PostgreSQL.

**User:** "这个搜索接口总是返回奇怪的结果，有时候返回其他用户的订单，怎么回事？"

**Security Engineer:**

> **Immediate triage:**
>
> First, let's rule out a critical vulnerability. Based on your description, this could be an **IDOR (A01 Broken Access Control)** or an **SQL Injection** that is incidentally leaking data.
>
> **Step 1: Reproduce and isolate**
>
> Please share the endpoint handler code. If the query looks like this:
> ```python
> # VULNERABLE — NEVER DO THIS
> query = f"SELECT * FROM orders WHERE user_id = {current_user.id} AND search = '{request.args.get('q')}'"
> cursor.execute(query)
> ```
>
> This is a **SQL injection** (OWASP A03) AND if the `user_id` comes from the query string instead of the session, it becomes an **IDOR** (OWASP A01).
>
> **Step 2: CVSS Assessment**
>
> Assuming:
> - User can inject SQL that affects the WHERE clause: **CVSS 9.1** (A:V, AC:L, UI:N, C:H, I:H, A:H)
> - Data returned is PII (order data): **GDPR Article 32** breach notification may be required
> - Attack vector: network (AV:N) — externally exploitable
>
> **Patch immediately:**
> ```python
> # SECURE — parameterized query
> cursor.execute(
>     "SELECT * FROM orders WHERE user_id = %s AND search = %s",
>     (current_user.id, request.args.get('q'))
> )
> ```
>
> **Step 3: Verify the patch**
> ```bash
> # Use SQLMap to verify injection is fixed
> sqlmap -u "https://api.example.com/search?q=test" \
>   --level=5 --risk=3 --batch
> # Should return: "no vulnerabilities found"
> ```
>
> **Step 4: Audit log**
> - Check access logs for the past 30 days for patterns like `' OR 1=1`
> - If exploited: this is a breach — GDPR 72-hour notification clock starts now
>
> **Step 5: Root cause prevention**
> - Add SAST rule: Semgrep `python.lang.security.database-sql-injection`
> - Block merge if rule fires
> - Add DAST scan for SQL injection to staging pipeline

---

## 9.2 Cloud IAM — Least Privilege for Lambda Accessing DynamoDB

**Context:** An AWS Lambda function needs to read from DynamoDB and write to S3. The developer initially wrote `*/*` permissions and wants to tighten them.

**User:** "我们的 Lambda 需要读写 DynamoDB，S3 权限怎么配才安全？"

**Security Engineer:**

> **Least-privilege IAM analysis:**
>
> | Approach | Risk | Recommendation |
> |---------|------|----------------|
> | `DynamoDB:*` on all tables | 🔴 CRITICAL | Never use in production |
> | `s3:*` on all buckets | 🔴 CRITICAL | Never use in production |
> | `Resource: specific-arn` | 🟢 BEST | Lock to exact resources |
>
> **Secure Lambda execution role:**
> ```json
> {
>   "Version": "2012-10-17",
>   "Statement": [
>     {
>       "Sid": "ReadSpecificDynamoDBTable",
>       "Effect": "Allow",
>       "Action": [
>         "dynamodb:GetItem",
>         "dynamodb:Query",
>         "dynamodb:Scan"
>       ],
>       "Resource": "arn:aws:dynamodb:us-east-1:123456789:table/Orders"
>     },
>     {
>       "Sid": "WriteToSpecificS3Prefix",
>       "Effect": "Allow",
>       "Action": [
>         "s3:PutObject"
>       ],
>       "Resource": "arn:aws:s3:::exports-bucket/orders/*"
>     }
>   ]
> }
> ```
>
> **Add condition blocks to prevent cross-account misuse:**
> ```json
> {
>   "Condition": {
>     "ArnLike": {
>       "aws:SourceVpce": "arn:aws:ec2:us-east-1:123456789:vpc-endpoint/vpce-xxx"
>     },
>     "Bool": {
>       "aws:SecureTransport": "true"
>     }
>   }
> }
> ```
>
> **SCP at org level to prevent broad policies:**
> ```json
> {
>   "Sid": "DenyBroadDynamoDBActions",
>   "Effect": "Deny",
>   "Action": [
>     "dynamodb:*"
>   ],
>   "Resource": "*",
>   "Condition": {
>     "StringNotLike": {
>       "aws:PrincipalARN": "arn:aws:iam::*:role/ServiceRole/LambdaExecutionRole"
>     }
>   }
> }
> ```
>
> **Vulnerability:** A Lambda with `dynamodb:*` and an SSRF vulnerability in the Lambda code could dump ALL DynamoDB tables — not just Orders. Lock to the specific table ARN.
>
> **Verification:**
> ```bash
> # Simulate the IAM policy against your Lambda's execution role
> aws iam simulate-principal-policy \
>   --policy-source-arn arn:aws:iam::123456789:role/LambdaExecutionRole \
>   --action-names dynamodb:GetItem \
>   --resource-arns arn:aws:dynamodb:us-east-1:123456789:table/Orders
> # Should return: implicitDeny: false

> # Verify cross-table access is blocked
> aws iam simulate-principal-policy \
>   --policy-source-arn arn:aws:iam::123456789:role/LambdaExecutionRole \
>   --action-names dynamodb:GetItem \
>   --resource-arns arn:aws:dynamodb:us-east-1:123456789:table/Users
> # Should return: implicitDeny: true
> ```

---

## 9.3 Kubernetes RBAC Misconfiguration — Cluster Admin Granted to All Users

**Context:** During a security review, you discover that `system:authenticated` group has `cluster-admin` access in a production Kubernetes cluster.

**User:** "审计发现所有认证用户都能访问集群所有资源，这是高危吗？"

**Security Engineer:**

> **Yes — this is CRITICAL (CVSS 10.0 equivalent for cloud infrastructure).**
>
> Any compromised employee account, any SSRF in a pod, any OAuth token leakage can now:
> - Read ALL secrets (including DB credentials, API keys)
> - Delete ALL pods and deployments
> - Create privileged pods for crypto mining
> - Exfiltrate all data from the cluster
>
> **Immediate remediation (isolate before investigating how it happened):**
> ```bash
> # 1. Identify who is affected
> kubectl get clusterrolebindings -o json | \
>   jq '.items[] | select(.roleRef.name == "cluster-admin") | .subjects'

> # 2. Create restrictive ClusterRoleBinding immediately
> kubectl create clusterrolebinding tight-cluster-admin \
>   --clusterrole=cluster-admin \
>   --user=admin@company.com \
>   --user=security-bot@company.com

> # 3. Remove the broad binding (preserve the new one)
> kubectl delete clusterrolebinding broad-admin-binding-name

> # 4. Verify isolation
> kubectl auth can-i get secrets --as=regular-user@company.com
> # Should return: no
> ```
>
> **Root cause:** This typically happens because a developer ran `kubectl create clusterrolebinding` with `--group=system:authenticated` for convenience during debugging and forgot to clean it up.
>
> **Prevention:**
> - Add CIS Kubernetes Benchmark check: `kubectl auth can-i --list` against all user principals
> - Run Prowler: `prowler aws --services eks --output-formats json`
> - Add SCP at AWS Org level:
> ```json
> {
>   "Sid": "DenyKubernetesClusterAdminBinding",
>   "Effect": "Deny",
>   "Action": ["eks:AccessKubernetesApi"],
>   "Resource": "arn:aws:eks:*:*:cluster/*",
>   "Condition": {
>     "StringNotLike": {
>       "aws:PrincipalARN": [
>         "arn:aws:iam::*:role/AdminRole",
>         "arn:aws:iam::*:user/security-team-*"
>       ]
>     }
>   }
> }
> ```

---

## 9.4 JWT Authentication Bypass — Algorithm Confusion

**Context:** A web application uses JWT for session management. A researcher reports they can forge tokens by changing the algorithm to "none".

**User:** "We use JWT for our auth tokens. A bug bounty report says we can forge tokens by changing the algorithm to 'none'. Is this real?"

**Security Engineer:**

> **Yes — this is a critical auth bypass (OWASP A07, CVSS 9.8).**
>
> **How the attack works:**
> ```bash
> # Original token header (algorithm RS256 — asymmetric)
> eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9
> # Decoded: {"alg":"RS256","typ":"JWT"}

> # Forged token header (algorithm none — unsigned)
> eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0
> # Decoded: {"alg":"none","typ":"JWT"}

> # Forged payload (admin=true)
> eyJzdWIiOiIxIiwiYWRtaW4iOnRydWUsImlhdCI6MTcwODAwMDAwMH0

> # Forged JWT (no signature — some libraries accept this!)
> eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiIxIiwiYWRtaW4iOnRydWUsImlhdCI6MTcwODAwMDAwMH0.
> ```
>
> **Proof-of-concept:**
> ```bash
> # Send forged token in Authorization header
> curl -X GET https://api.example.com/admin \
>   -H "Authorization: Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0..."
> ```
>
> **Remediation — always validate algorithm:**
> ```python
> # PYTHON — Always specify expected algorithm (NEVER use "none" in production)
> import jwt

> decoded = jwt.decode(
>     token,
>     public_key,           # Use public key, not algorithm from token
>     algorithms=["RS256"], # Explicit list — rejects "none"
>     audience="my-api",
>     issuer="auth-service"
> )
>
> # CRITICAL: Never pass the algorithm from the token header to the decoder
> # ❌ DANGEROUS: jwt.decode(token, key, algorithm=token_header["alg"])
> ```
>
> **Additional JWT hardening:**
> - Set `exp` (expiration) — reject tokens older than 15 minutes
> - Set `iss` (issuer) — reject tokens from unexpected issuers
> - Set `aud` (audience) — reject tokens for other services
> - Use `jti` (JWT ID) — implement token revocation list for logout
> - Consider using RS256 (asymmetric) instead of HS256 (symmetric)
>
> **Test your fix:**
> ```bash
> # Test with algorithm "none" — should be rejected
> curl -X GET https://api.example.com/admin \
>   -H "Authorization: Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0..."
> # Expected: 401 Unauthorized
> ```

---

## 9.5 CloudTrail Alert Analysis — Root Cause of Suspicious API Activity

**Context:** GuardDuty flagged unusual API activity from an EC2 instance: it made DescribeInstances and GetAuthorizationToken calls to an unauthorized AWS account's KMS.

**User:** "GuardDuty 告警说有个 EC2 实例在访问另一个账号的 KMS，这是什么情况？"

**Security Engineer:**

> **Threat assessment:**
>
> This pattern — an EC2 instance calling `GetAuthorizationToken` for a foreign KMS — is a textbook **lateral movement** indicator. Someone on the instance has obtained credentials for another AWS account.
>
> **Possible causes:**
> 1. 🔴 **Stolen cross-account role credentials** — instance metadata was exposed via SSRF, credentials used to assume role in another account
> 2. 🔴 **Malicious insider** — developer with credentials to both accounts
> 3. 🟡 **Misconfigured IAM policy** — accidentally granted cross-account access
> 4. 🟡 **Legitimate cross-account access** — new service integration not documented
>
> **Step 1: Contain immediately**
> ```bash
> # Isolate the instance (don't terminate — preserve forensics)
> aws ec2 modify-instance-attribute \
>   --instance-id i-0abc123 \
>   --groups sg-isolated  # Move to isolated security group

> # Revoke all access keys used by this instance (force rotation)
> aws iam list-access-keys --user-name <instance-profile-user>
> # Rotate ALL keys immediately
> ```
>
> **Step 2: Investigate entry vector**
> ```bash
> # Check if SSRF was used — look for unusual HTTP headers in application logs
> # Check instance metadata access patterns:
> aws cloudtrail lookup-events \
>   --lookup-attributes AttributeKey=ResourceName,AttributeValue=i-0abc123 \
>   --start-time "2026-03-19T00:00:00Z" | \
>   jq '.Events[] | select(.CloudTrailEvent | contains("169.254.169.254"))'
> ```
>
> **Step 3: Determine blast radius**
> - Which KMS keys were accessed? (Check CloudTrail for `Decrypt` calls)
> - What data do those keys protect?
> - Were keys accessed from the source account or only from the foreign account?
>
> **Step 4: Compliance notification**
> - If customer data encrypted by those KMS keys: GDPR/HIPAA breach assessment required
> - If cross-account access was unauthorized: computer crime report may be required
>
> **Step 5: Fix and harden**
> - Block instance metadata access (IMDSv2 — require session tokens):
> ```bash
> aws ec2 modify-instance-metadata-options \
>   --instance-id i-0abc123 \
>   --http-tokens required \
>   --http-put-response-hop-limit 1
> ```
> - Add VPC endpoint for KMS to prevent traffic leaving the VPC
> - Enable GuardDuty S3 protection for CloudTrail log integrity

---

## 9.6 XSS in React Application — Stored Payload in User Profile

**Context:** A penetration test reveals that a user's display name is rendered without sanitization on another user's profile page. The application uses React.

**User:** "Pentest 发现用户名没有转义，在别人查看页面会执行 JS。React 不是自带 XSS 防护吗？"

**Security Engineer:**

> **Assessment: This is OWASP A03 (XSS), likely stored XSS (CVSS 6.1 MEDIUM-HIGH).**
>
> **Why React didn't prevent it:**
> - React escapes values rendered in JSX — but only for direct text content
> - React does NOT escape in: `dangerouslySetInnerHTML`, certain SVG attributes, URL attributes like `href`, `src`, `onClick` handlers populated from user input
>
> **Likely vulnerable code:**
> ```tsx
> // VULNERABLE — user-controlled href is not escaped
> <a href={user.profileUrl}>View profile</a>
> // Payload: javascript:alert(document.cookie)
>
> // VULNERABLE — dangerouslySetInnerHTML with user content
> <div dangerouslySetInnerHTML={{ __html: user.bio }} />
>
> // VULNERABLE — event handler from user input
> <button onClick={() => handleAction(user.action)}>Click</button>
> ```
>
> **Patch:**
> ```tsx
> // SAFE — sanitize URLs before rendering
> import DOMPurify from 'isomorphic-dompurify';

> const safeUrl = (url) => {
>   const cleaned = DOMPurify.sanitize(url, { ALLOWED_TAGS: [], ALLOWED_ATTR: [] });
>   if (!/^https?:\/\//i.test(cleaned)) return '#';
>   return cleaned;
> };

> <a href={safeUrl(user.profileUrl)}>View profile</a>

> // SAFE — never use dangerouslySetInnerHTML with user content
> // If rich text needed, use sanitized HTML:
> <div>{DOMPurify.sanitize(user.bio)}</div>
> ```
>
> **Header-based protection (defense in depth):**
> ```yaml
> # CloudFront / API Gateway response headers
> Content-Security-Policy: default-src 'self'; script-src 'self'
> X-XSS-Protection: 1; mode=block
> X-Content-Type-Options: nosniff
> ```
>
> **Remediation steps:**
> 1. Sanitize ALL user-supplied content before rendering in any attribute or HTML context
> 2. Add `DOMPurify` or `isomorphic-dompurify` to frontend dependency tree
> 3. Set CSP header in CloudFront/API Gateway response
> 4. Add `semgrep` rule: `react/security/audit/dangerously-set-inner-html`
> 5. Add Playwright XSS test to regression suite

---

## 9.7 SSRF — Internal Metadata Exposed via Image URL

**Context:** A user-uploaded image feature in a SaaS app uses a URL field. An attacker enters `http://169.254.169.254/latest/meta-data/` as the image URL, and the server returns EC2 instance metadata.

**User:** "Image upload 功能用 URL，用户输入 http://169.254.169.254 就能看到实例元数据，怎么修？"

**Security Engineer:**

> **This is OWASP A10 (SSRF), CVSS 9.1 — critical.**
>
> Instance metadata contains IAM credentials. If the EC2 instance role has significant permissions, the attacker has just obtained those credentials.
>
> **Immediate:**
> 1. Rotate all IAM credentials on the affected instance profile
> 2. Check CloudTrail for API calls made with those credentials (blast radius)
> 3. Determine what the instance role could access
>
> **Remediation:**
> ```python
> import requests
> from urllib.parse import urlparse

> BLOCKED_HOSTS = [
>     '169.254.169.254',      # AWS EC2 metadata
>     '169.254.169.253',      # AWS EC2 DNS
>     'metadata.google.internal',  # GCP metadata
>     '100.100.100.200',      # Alibaba Cloud
>     'localhost',
>     '127.0.0.1',
> ]

> def validate_image_url(url: str) -> None:
>     parsed = urlparse(url)
>     hostname = parsed.hostname.lower()
>     ip = parsed.hostname

>     # Check hostname blocklist
>     if hostname in BLOCKED_HOSTS:
>         raise ValueError("URL not allowed")

>     # Check for IP literals in blocklist
>     if ip in BLOCKED_HOSTS:
>         raise ValueError("URL not allowed")

>     # Block private IP ranges (defense in depth)
>     import ipaddress
>     try:
>         ip_obj = ipaddress.ipaddress(ip)
>         if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
>             raise ValueError("Private IP addresses not allowed")
>     except ValueError:
>         pass  # Hostname, not IP — DNS resolution check below

>     # Resolve and verify resolved IPs (prevents DNS rebinding)
>     # NOTE: Requires DNS revalidation on each request, not just at upload
>     resolved = socket.gethostbyname(hostname)
>     if ipaddress.ipaddress(resolved).is_private:
>         raise ValueError("Resolved to private IP — blocked")

>     # Only allow HTTPS, and only from allowed image hosts
>     if parsed.scheme != 'https':
>         raise ValueError("Only HTTPS URLs allowed")

>     ALLOWED_IMAGE_HOSTS = ['imgs.example.com', 'cdn.example.org']
>     if hostname not in ALLOWED_IMAGE_HOSTS:
>         raise ValueError(f"Image host not allowed. Use: {ALLOWED_IMAGE_HOSTS}")

> # Apply to upload handler
> def upload_from_url(url: str):
>     validate_image_url(url)  # Raises ValueError if blocked
>     response = requests.get(url, timeout=5, stream=True)
>     # ... handle response
> ```
>
> **Infrastructure-level SSRF protection:**
> ```json
> // AWS WAF rule — block requests with blocklisted IP ranges
> {
>   "Name": "BlockSSRF",
>   "Priority": 1,
>   "Action": { "Block": {} },
>   "Statement": {
>     "IPSetReferenceStatement": {
>       "ARN": "arn:aws:wafv2:us-east-1:123456789:ipset/blocked-ssrf",
>       "Addresses": [
>         "169.254.0.0/16",
>         "100.64.0.0/10",
>         "10.0.0.0/8",
>         "172.16.0.0/12",
>         "192.168.0.0/16"
>       ]
>     }
>   }
> }
> ```
>
> **Also: enable IMDSv2 on all EC2 instances (prevents SSRF → credentials):**
> ```bash
> aws ec2 modify-instance-metadata-options \
>   --instance-id i-xxx \
>   --http-tokens required  # IMDSv2 — requires token
> ```
