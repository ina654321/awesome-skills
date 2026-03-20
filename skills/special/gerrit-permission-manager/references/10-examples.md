# Gerrit Permission Management — Real-World Scenarios

## Scenario 1: Migrating from GitHub Pull Requests to Gerrit

**Context:** A 15-person engineering team has been using GitHub with a loose review culture. Management mandates stronger change control. You need to migrate to Gerrit with proper branch protection and permission structure.

**Steps:**

1. **Import repositories** into Gerrit and disable the GitHub pull request workflow.

2. **Define permission groups:**
```bash
ssh -p 29418 admin@host gerrit create-group engineers
ssh -p 29418 admin@host gerrit create-group leads
ssh -p 29418 admin@host gerrit create-group qa
ssh -p 29418 admin@host gerrit create-group release-managers

# Add members
ssh -p 29418 admin@host gerrit set-members --add alice@company.com engineers
ssh -p 29418 admin@host gerrit set-members --add bob@company.com leads
# ... etc
```

3. **Configure main branch protection:**
```bash
# Apply protected-branches template
./scripts/apply-permissions.sh --repo backend-api --template protected-branches

# Add label requirements for leads
ssh -p 29418 admin@host gerrit set-project-access \
  --project backend-api \
  --add 'refs/heads/main label-Code-Review -1..+1' leads
```

4. **Enforce CI verification before submit:**
```bash
./scripts/apply-permissions.sh --repo backend-api --template ci-cd
```

5. **Verify:**
```bash
./scripts/audit-permissions.sh --repo backend-api --strict
```

**Outcome:** All pushes now go through `refs/for/main` (code review). Direct push to `main` is blocked. At least 1 lead review +1 required for merge.

---

## Scenario 2: Managing Permissions Across 50 Repositories for a Product Line

**Context:** A company has 50 microservices, each in its own repository. You need to apply consistent permissions across all of them, grant the "payments-team" access only to payment-related repos, and enforce a 2-reviewer rule on production branches.

**Steps:**

1. **Create manifest repository:**
```bash
./scripts/create-manifest-repo.sh payments-platform repos.txt
# repos.txt contains: payments-api, payments-worker, payments-gateway, ...
```

2. **Define multi-team permission configuration:**
```json
{
  "refs/heads/main": {
    "read": ["Registered Users"],
    "submit": ["payments-leads", "release-managers"],
    "label-Code-Review": {
      "-2..+2": ["payments-leads"],
      "-1..+1": ["payments-team"]
    },
    "require-minimum-code-review-score": 2,
    "require-approval-count": 2,
    "block-force-push": true
  },
  "refs/heads/releases/*": {
    "submit": ["release-managers"],
    "label-Code-Review": {
      "-2..+2": ["release-managers"]
    }
  },
  "refs/heads/feature/*": {
    "read": ["payments-team"],
    "create": ["payments-team"],
    "push": ["payments-team"],
    "submit": ["payments-leads"]
  }
}
```

3. **Apply across all repos:**
```bash
./scripts/bulk-update.sh \
  --manifest payments-platform/default.xml \
  --permission-file payments-perms.json \
  --parallel 10

# Parallel execution speeds up bulk operations on large sets
```

4. **Grant team-specific access:**
```bash
./scripts/grant-team-access.sh \
  --manifest payments-platform/default.xml \
  --team payments-team \
  --access-level read
```

5. **Audit for compliance:**
```bash
./scripts/audit-permissions.sh \
  --manifest payments-platform/default.xml \
  --report payments-audit.json
```

**Outcome:** Consistent 2-reviewer protection across all 50 repos. payments-team can read but not submit to main. Release managers have exclusive release branch control.

---

## Scenario 3: Emergency Security Hotfix with Expedited Approval

**Context:** A critical CVE is discovered in production. The security team needs to push a hotfix within 30 minutes. Normal process requires 2 reviewers, but the hotfix must bypass this for emergency deployment.

**Steps:**

1. **Security lead creates hotfix branch:**
```bash
git checkout -b hotfix/CVE-2024-1234 master
# Make emergency fix
git commit -m "HOTFIX: Patch CVE-2024-1234 authentication bypass"
```

2. **Push with expedited review flag:**
```bash
git push origin HEAD:refs/for/master --opt "X-Should-Merge-If-Approved"

# Or use the hotfix template which has 1-reviewer requirement
./scripts/apply-permissions.sh --repo critical-service --template git-flow
```

3. **Release manager approves expedited:**
```bash
ssh -p 29418 admin@host gerrit review \
  --project critical-service \
  --message "Emergency CVE patch - expedited approval" \
  --label Code-Review=+2 \
  --label Verified=+1 \
  --submit Change-Id
```

4. **Post-emergency: run security audit:**
```bash
./scripts/audit-permissions.sh --repo critical-service --strict

# Update CODEOWNERS to prevent future delays
ssh -p 29418 admin@host gerrit set-project-access \
  --project critical-service \
  --add 'refs/heads/main label-Code-Review -2..+2 security-team'
```

**Outcome:** Hotfix merged in <30 minutes. Security team added as co-approvers for critical paths.

---

## Scenario 4: Setting Up Git Flow for a Continuous Delivery Pipeline

**Context:** A DevOps team adopts Git Flow with automated releases. Each merge to `main` triggers a production deployment. Release branches have a 1-week stabilization period. CI must verify before any merge.

**Setup:**

1. **Apply Git Flow template:**
```bash
./scripts/apply-permissions.sh --repo platform-service --template git-flow
```

2. **Configure CI bot permissions:**
```json
{
  "refs/heads/main": {
    "label-Verified": ["jenkins-ci-bot"]
  },
  "refs/heads/develop": {
    "label-Verified": ["jenkins-ci-bot"]
  },
  "refs/heads/release/*": {
    "label-Verified": ["jenkins-ci-bot"],
    "label-QA-Approved": ["qa-leads"]
  }
}
```

3. **Set up release automation:**
```bash
# Release Manager creates release branch
git checkout -b release/v2.1.0 develop
git push origin release/v2.1.0

# CI runs regression suite
# After 1 week, Release Manager merges
git checkout main
git merge --no-ff release/v2.1.0
git push origin HEAD:refs/for/main

# Approval requires: 2x Code-Review +2, 1x Verified +1, 1x QA-Approved +1
# Zuul/Jenkins enforces: all tests must pass before Verified +1
```

4. **Monitor the pipeline:**
```bash
./scripts/stats-permissions.sh --repo platform-service

# Output includes:
# - Permission counts per branch
# - Group references
# - Security coverage score
```

**Outcome:** Strict Git Flow with automated gates. Only Release Managers can create/merge release branches. All changes to main require full test suite + manual QA approval.

---

## Scenario 5: Detecting and Remediation Permission Drift

**Context:** After an organizational restructuring, you discover that several repositories have permission configurations that deviate from the corporate baseline. A developer may have accidentally granted broad permissions.

**Detection:**
```bash
# Run drift detection across all repos
./scripts/compare-permissions.sh --check-drift ALL --template standard --verbose

# Sample output:
# REPO: legacy-payment    STATUS: DRIFT DETECTED
#   - refs/heads/main: has "forge identity" for "All Users" (baseline: CI only)
#   - refs/heads/releases/*: missing "submit" for "Release Managers"
#   - SECURITY SCORE: 45/100
```

**Fix:**
```bash
# Review the drift report
cat drift-report.json

# For each drifted repo, re-apply template with force
./scripts/apply-permissions.sh --repo legacy-payment \
  --template standard \
  --force \
  --audit

# If specific permissions need to be preserved (e.g., special CI access),
# create a custom template that extends the standard
./scripts/apply-permissions.sh --repo legacy-payment \
  --template standard-with-ci \
  --force
```

**Root cause analysis:**
```bash
# Check refs/meta/config history for recent changes
ssh -p 29418 admin@host gerrit log project:legacy-payment refs/meta/config

# Identify who made the change
# Result: developer alice modified permissions during a sprint
# Fix: revoke forge identity from developers group
ssh -p 29418 admin@host gerrit set-project-access \
  --project legacy-payment \
  --remove 'refs/* forge identity' 'All Users' \
  --add 'refs/* forge identity' 'CI Service Account'
```

**Outcome:** All repositories return to baseline. Audit shows security score back to 90+/100.

---

## Scenario 6: Multi-Team Project with Path-Based Code Ownership

**Context:** A large monorepo has 4 teams (frontend, backend, infra, security). Each team owns specific directories. Only a code owner from the relevant team can approve changes to their directories.

**Setup:**
```bash
# Create code owner files per directory
# /frontend/OWNERS:
#   approvers:
#     - frontend-leads@company.com
#   reviewers:
#     - frontend-team@company.com

# /backend/OWNERS:
#   approvers:
#     - backend-leads@company.com

# /infra/OWNERS:
#   approvers:
#     - infra-leads@company.com

# /security/OWNERS:
#   approvers:
#     - security-leads@company.com
```

Configure submit rules to enforce code ownership:
```prolog
submit_rule(submit(X)) :-
  conditions,
  core:submit_rule(X),
  !.
```

Set label permissions per path:
```bash
ssh -p 29418 admin@host gerrit set-project-access \
  --project monorepo \
  --add 'refs/heads/main label-Code-Review -1..+1 frontend-team'

ssh -p 29418 admin@host gerrit set-project-access \
  --project monorepo \
  --add 'refs/heads/main label-Code-Review -2..+2 frontend-leads'
```

**Outcome:** A frontend developer can vote +1 on a backend change, but only a backend lead can give the blocking +2. Security-critical paths require security-team approval.

---

## Scenario 7: PCI-DSS Compliant Code Change Audit Trail

**Context:** A payment processing system must comply with PCI DSS 4.0. Auditors require documented evidence of who approved every change to the cardholder data environment.

**Implementation:**
```bash
# Use Gerrit's built-in audit trail
./scripts/audit-permissions.sh --repo payment-processor \
  --compliance pci-dss \
  --report pci-audit-2024-Q4.json
```

**Key compliance configurations:**
```json
{
  "refs/heads/*": {
    "read": ["Registered Users"],
    "block-anonymous": true
  },
  "refs/heads/main": {
    "submit": ["pci-change-board"],
    "label-Code-Review": {
      "-2..+2": ["pci-change-board"],
      "-1..+1": ["Registered Users"]
    },
    "require-minimum-code-review-score": 2,
    "require-approval-count": 2,
    "require-code-owner-approval": true
  },
  "refs/tags/*": {
    "pushTag": ["pci-change-board"],
    "pushSignedTag": ["pci-change-board"]
  }
}
```

**Audit evidence generation:**
```bash
# Export all changes merged to main in Q4
ssh -p 29418 admin@host gerrit query \
  --format=JSON \
  --patch-sets \
  --current-patch-set \
  --all-reviewers \
  'status:merged project:payment-processor \
   branch:main after:2024-10-01 before:2024-12-31' \
  > pci-changes-q4.json
```

**Outcome:** Complete audit trail showing every change, its reviewers, approval scores, and who clicked submit. Satisfies PCI DSS 6.2 requirements.

---

## Scenario 8: Graduated Developer Permissions with Automated Promotion

**Context:** New developers join with minimal permissions. As they gain experience (demonstrated by approved changes and passing CI), their permissions are gradually expanded.

**Stage 1 — Junior Developer (restricted):**
```bash
# New hires start in "onboarding" group
ssh -p 29418 admin@host gerrit set-members --add junior@company.com onboarding
```

**Stage 1 permissions:**
```json
{
  "refs/heads/main": { "read": ["onboarding"] },
  "refs/heads/feature/*": {
    "read": ["onboarding"],
    "create": ["onboarding"],
    "push": ["onboarding"],
    "submit": ["mentor-leads"]
  }
}
```

**Stage 2 — After 3 months, 20+ approved changes, all CI passing:**
```bash
# Promote to developers group
ssh -p 29418 admin@host gerrit set-members --remove junior@company.com onboarding
ssh -p 29418 admin@host gerrit set-members --add junior@company.com developers

# Now has broader permissions
./scripts/apply-permissions.sh --repo shared-lib --template multi-team
```

**Stage 3 — After becoming team lead:**
```bash
ssh -P 29418 admin@host gerrit set-members --add junior@company.com tech-leads
# Can now review and approve others' changes
```

**Outcome:** Permission escalation is tied to demonstrated competence, not just role assignment. Reduces insider threat risk.

---

## Scenario 9: Integrating Gerrit with External Identity Provider (LDAP)

**Context:** Gerrit must use the company's LDAP for authentication and group synchronization. Existing LDAP groups must map to Gerrit groups.

**Setup:**
```bash
# Configure gerrit.config for LDAP
cat >> $site_path/etc/gerrit.config << 'EOF'
[auth]
  type = LDAP
[ldap]
  server = ldap://ldap.company.com
  bindDN = cn=gerrit,ou=services,dc=company,dc=com
  bindPassword = ${env.LDAP_BIND_PASSWORD}
  accountBase = ou=people,dc=company,dc=com
  groupBase = ou=groups,dc=company,dc=com
  groupMemberPattern = (member=${dn})
  referral = follow
EOF

# Restart Gerrit
./bin/gerrit.sh restart
```

**Sync LDAP groups:**
```bash
# Manual sync
ssh -p 29418 admin@host gerrit gsql --format JSON -c \
  "SELECT group_name, owner_group_id FROM account_groups WHERE name LIKE '%Engineering%'"
```

**Create Gerrit groups mirroring LDAP:**
```bash
# LDAP group "cn=engineering,ou=groups" → Gerrit group "Engineering"
ssh -p 29418 admin@host gerrit create-group "Engineering" \
  --description "Synced from LDAP"

# Members are automatically added on next login
# Set permissions using the Gerrit group name
ssh -p 29418 admin@host gerrit set-project-access \
  --project backend \
  --add 'refs/heads/main submit' Engineering
```

**Outcome:** User permissions follow LDAP group membership. Adding/removing a user from LDAP LDAP group automatically updates their Gerrit access on next login.

---

## Scenario 10: Repository Migration with Permission Preservation

**Context:** Migrating 20 repositories from one Gerrit instance to another. Permissions must be preserved during migration.

**Steps:**

1. **Export permissions from source:**
```bash
for repo in $(cat repos-to-migrate.txt); do
  ./scripts/view-permissions.sh --repo "$repo" --format json \
    --export "migrations/$repo-permissions.json"
done

# Export group definitions
./scripts/gerrit-api.sh GET /groups/ > migrations/groups-export.json
```

2. **Import to target:**
```bash
# Create groups first
for group in $(jq -r '.[].name' migrations/groups-export.json); do
  ssh -p 29419 target-admin@new-host gerrit create-group "$group"
done

# Import project permissions
for perm_file in migrations/*-permissions.json; do
  repo=$(basename "$perm_file" | sed 's/-permissions.json//')
  ./scripts/gerrit-api.sh POST "/projects/$repo/access/" \
    --data @"$perm_file"
done
```

3. **Verify migration:**
```bash
# Compare source vs target
./scripts/compare-permissions.sh \
  --source-repo backend-api \
  --source-host old-gerrit.company.com \
  --target-repo backend-api \
  --target-host new-gerrit.company.com

# Should show 0 drift if migration was successful
```

**Outcome:** All 20 repositories migrated with identical permission structure. No service disruption.
