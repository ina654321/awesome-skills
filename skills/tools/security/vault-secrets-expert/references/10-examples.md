# Examples

## 10.1 KV Secret

```bash
# Enable KV engine
vault secrets enable -path=secret kv

# Write secret
vault kv put secret/myapp db_password=supersecret

# Read secret
vault kv get secret/myapp

# Delete secret
vault kv delete secret/myapp
```

## 10.2 Kubernetes Auth

```bash
# Enable Kubernetes auth
vault auth enable kubernetes

# Configure
vault write auth/kubernetes/config \
    kubernetes_host=https://192.168.99.100:8443 \
    token_reviewer_jwt=@/var/run/secrets/kubernetes.io/serviceaccount/token
```

## 10.3 Policy

```path
# myapp-policy.hcl
path "secret/data/myapp/*" {
  capabilities = ["read", "write"]
}

path "secret/data/myapp/config" {
  capabilities = ["read"]
}
```

```bash
vault policy write myapp-policy myapp-policy.hcl
```

## 10.4 AppRole Auth

```bash
# Create role
vault write auth/approle/role/myapp-role \
    policies="myapp-policy" \
    token_ttl=1h

# Get role_id
vault read auth/approle/role/myapp-role/role-id

# Get secret_id
vault write -f auth/approle/role/myapp-role/secret-id
```