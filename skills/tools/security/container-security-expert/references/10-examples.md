# Examples

## 10.1 Trivy Scan

```bash
# Scan image
trivy image myapp:latest

# Scan with severity filter
trivy image --severity HIGH,CRITICAL myapp:latest

# Scan in JSON
trivy image -f json myapp:latest

# Scan filesystem
trivy fs /path/to/project
```

## 10.2 Dockerfile Security

```dockerfile
# Use specific version
FROM node:20-alpine

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set ownership
COPY --chown=appuser:appgroup . /app

# Switch to non-root
USER appuser

# No secrets in image
```

## 10.3 Kubernetes Admission

```yaml
apiVersion: v1
kind: ValidatingWebhookConfiguration
metadata:
  name: check-privileged
webhooks:
- name: check-privileged.k8s.example.com
  rules:
  - apiGroups: [""]
    apiVersions: ["v1"]
    resources: ["pods"]
    operations: ["CREATE"]
  clientConfig:
    service:
      name: webhook-service
      namespace: default
    caBundle: LS0tLS1...
  admissionReviewVersions: ["v1"]
  sideEffects: None
  timeoutSeconds: 5
```