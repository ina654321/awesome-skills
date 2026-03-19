# Scenario Examples

## 9.1 Basic Usage

**User:** "How do I rotate database passwords automatically every day?"

**Expert:**
> **Daily DB Credential Rotation with Vault:**
>
> 1. Configure database secrets engine with short TTL:
> ```bash
> vault write database/roles/app-role \
>   db_name=myapp-postgres \
>   creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
>   default_ttl=24h \
>   max_ttl=24h
> ```
>
> 2. App fetches credentials at startup:
> ```bash
> SECRET=$(vault read -format=json database/creds/app-role)
> USERNAME=$(echo $SECRET | jq -r .data.username)
> PASSWORD=$(echo $SECRET | jq -r .data.password)
> ```
>
> 3. Set up periodic rotation via Vault Agent or your app:
> ```bash
> # In cron or Vault Agent template
> vault lease renew -increment=true database/creds/app-role/<lease_id>
> # Or fetch new credentials periodically before lease expires
> ```
>
> 4. Verify: Check audit logs or `vault list sys/leases/lookup/database/creds/app-role`

---

**User:** "How do I authenticate a Kubernetes pod to Vault?"

**Expert:**
> **Kubernetes Auth Setup:**
>
> 1. Enable Kubernetes auth on Vault server:
> ```bash
> vault auth enable kubernetes
> ```
>
> 2. Configure Vault to talk to Kubernetes API:
> ```bash
> vault write auth/kubernetes/config \
>   token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
>   kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
>   kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
> ```
>
> 3. Create a Vault policy for your app:
> ```hcl
> path "secret/data/apps/myapp/*" {
>   capabilities = ["read"]
> }
> ```
>
> 4. Create a Kubernetes auth role:
> ```bash
> vault write auth/kubernetes/role/myapp \
>   bound_service_account_names=myapp-sa \
>   bound_service_account_namespaces=production \
>   policies=myapp-policy \
>   ttl=24h
> ```
>
> 5. App uses the service account token automatically:
> ```bash
> export VAULT_ADDR="https://vault.internal:8200"
> vault read secret/data/apps/myapp/config  # Uses mounted SA token automatically
> ```
>
> For Go:
> ```go
> client, _ := vault.NewClient(vault.DefaultConfig())
> client.SetKubernetesAuth()
> secret, err := client.Logical().Read("secret/data/apps/myapp/config")
> ```

---

**User:** "How do I manage secrets across multiple cloud providers?"

**Expert:**
> **Multi-Cloud Secrets with Vault:**
>
> ```bash
> # AWS
> vault secrets enable -path=aws aws
> vault write aws/config/root access_key=... secret_key=... region=us-east-1
> vault write aws/roles/app-ecs-role arn=arn:aws:iam::123:role/app-task ...
> vault read aws/creds/app-ecs-role
>
> # GCP
> vault secrets enable -path=gcp gcp
> vault write gcp/config/credentials=@gcp-creds.json
> vault write gcp/roleset/myapp-roleset \
>   project="my-project" \
>   secret_type="access_token" \
>   bindings=@gcp-bindings.hcl
> vault read gcp/token/myapp-roleset
>
> # Azure
> vault secrets enable -path=azure azure
> vault write azure/config subscription_id=... client_id=... tenant_id=...
> vault write azure/roles/myapp \
>   blob_permissions="Read,List" \
>   subscription_id=... \
>   tenant_id=... \
>   vm_name=myvm
> vault read azure/creds/myapp
> ```
>
> All accessed via a unified Vault API — your app only needs one secret store.

## 9.2 Disaster Recovery

**User:** "Our Vault cluster went down. How do I recover?"

**Expert:**
> **Recovery Procedures:**
>
> ### Single Node Failure (Raft)
> ```bash
> # If the node restarts, just unseal it
> vault operator unseal <unseal-key-1>
> vault operator unseal <unseal-key-2>
> vault operator unseal <unseal-key-3>
> # Verify: vault status shows "Sealed: false"
> ```
>
> ### Snapshot Recovery
> ```bash
> # On any remaining healthy node (or new node)
> vault operator raft snapshot restore backup_20240115_120000.snap
> ```
>
> ### Lost Unseal Keys (Shamir)
> ```bash
> # Only possible if you have an unseal key that was never used
> # After 3 successful unseals, threshold met
> vault operator unseal <key-a>
> vault operator unseal <key-b>
> vault operator unseal <key-c>
> # If threshold is 3, cluster is now unsealed
> ```
>
> ### Catastrophic Loss (all nodes gone)
> ```bash
> # Install fresh Vault on new node(s)
> # Restore from snapshot
> vault operator raft snapshot restore backup_latest.snap
> # Rejoin other nodes if needed
> vault operator raft join https://new-node:8200
> ```
>
> ### Best Practices for DR
> - Store snapshots in multiple regions/cloud providers
> - Schedule: `vault operator raft snapshot save` daily + before upgrades
> - Store unseal keys in separate secure locations (not same as Vault)
> - Test restores periodically

---

**User:** "How do I do a planned Vault upgrade with zero downtime?"

**Expert:**
> **Zero-Downtime Upgrade:**
>
> ```bash
> # 1. Take a snapshot before starting
> vault operator raft snapshot save pre_upgrade_$(date +%Y%m%d).snap
>
> # 2. Upgrade secondary nodes first (non-leader)
> # On each secondary node:
> systemctl stop vault
> # Replace binary
> systemctl start vault
>
> # 3. Verify secondary joined cluster
> vault status
> vault operator members
>
> # 4. Graceful leader handover
> # On current leader:
> vault step-down
> # Node will become standby
>
> # 5. Upgrade former leader
> systemctl stop vault
> # Replace binary
> systemctl start vault
>
> # 6. Verify all nodes on new version
> vault version
> # Check all members: vault operator members
>
> # 7. If rollback needed:
> vault operator raft snapshot restore pre_upgrade_$(date +%Y%m%d).snap
> ```

## 9.3 Audit Compliance

**User:** "Our security team needs to see who accessed what secrets and when."

**Expert:**
> **Vault Audit for Compliance:**
>
> ### Enable File Audit
> ```bash
> vault audit enable file \
>   file_path=/var/log/vault/audit.log \
>   log_raw=true \
>   hmac_accessor=false
>
> # Rotate logs
> vault audit enable file file_path=/var/log/vault/audit_$(date +%Y%m%d).log
> ```
>
> ### Enable Vault Telemetry (Prometheus)
> ```bash
> # In vault.hcl
> telemetry {
>   prometheus_retention_time = "30s"
>   disable_hostname = true
> }
>
> # Scrape metrics
> curl https://vault:8200/v1/sys/metrics?format=prometheus
> ```
>
> ### Key Audit Queries
> ```bash
> # Who accessed a specific secret?
> grep 'secret/data/apps/payment' /var/log/vault/audit.log | jq
>
> # All secrets read by a specific token
> grep '<token>' /var/log/vault/audit.log | grep request_path | jq '.data.path'
>
> # Failed authentication attempts
> grep '"error"' /var/log/vault/audit.log | jq
>
> # Certificates issued in last 24h
> grep 'pki/issue' /var/log/vault/audit.log | \
>   jq 'select(.time > (now - 86400))'
> ```
>
> ### Compliance Frameworks
> | Requirement | Vault Feature |
> |------------|---------------|
> | PCI-DSS | PKI certs, dynamic creds, audit log |
> | HIPAA | Encryption (Transit), audit, namespace isolation |
> | SOC 2 | Audit logging, TLS, MFA (OIDC) |
> | GDPR | Transit encryption, namespace per customer |

---

**User:** "Can I set up alerts when someone accesses the root token?"

**Expert:**
> **Alerting on Root Token Usage:**
>
> ```bash
> # Enable the syslog audit or file audit
> vault audit enable file file_path=/var/log/vault/secure_audit.log
>
> # Create a logstash/sidecar config to alert on:
> # - "auth/token/lookup-self" with policy contains "root"
> # - "secret/data/*" access from token with root policy
> # - Failed auth attempts > 5 in 10 minutes
> #
> # Or use Vault Enterprise Audit Broker + SIEM integration
> #
> # Prometheus alert rule example:
> # - alert: VaultRootTokenUsage
> #   expr: vault_audit_log_contains{match='root'} > 0
> #   for: 1m
> #   labels:
> #     severity: critical
> #   annotations:
> #     summary: "Root token used on {{ $labels.instance }}"
> ```
>
> Control Groups (Enterprise) can require approval before root operations:
> ```hcl
> path "auth/token/lookup-self" {
>   capabilities = ["update"]
>   control_group = {
>     max_authorizations = 1
>     authorized_entity_ids = ["security-team-entity-id"]
>   }
> }
> ```
