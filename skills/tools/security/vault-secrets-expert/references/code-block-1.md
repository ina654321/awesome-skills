# bash Example

```
# Enable KV v2
vault secrets enable -path=secret kv-v2

# Write secret with multiple fields
vault kv put secret/myapp/database \
    username=admin \
    password=secret123 \
    connection_string="postgresql://..."

# Read secret
vault kv get secret/myapp/database

# Read specific version
vault kv get -version=2 secret/myapp/database

# Delete secret (soft delete)
vault kv delete secret/myapp/database

# Permanently delete
vault kv destroy -versions=2 secret/myapp/database

# Check metadata
vault kv metadata get secret/myapp/database

# Configure metadata settings
vault kv metadata put -max-versions=5 -delete-version-after=90d secret/myapp/database
```
