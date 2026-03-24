## §3 · Domain Knowledge

### §3.1 · Oracle Cloud Infrastructure (OCI)

**Gen2 Cloud Differentiation:**

| Feature | OCI Approach | Competitor Approach |
|---------|--------------|---------------------|
| **Network** | Non-blocking, flat topology | Oversubscribed, tiered |
| **Storage** | NVMe local + block, no noisy neighbors | Shared storage pools |
| **Compute** | Bare metal standard, no hypervisor tax | Virtualization-heavy |
| **Pricing** | Simple, predictable, no egress surprise | Complex, variable |
| **Performance** | Consistent, HPC-optimized | Burstable, general-purpose |

**OCI Global Footprint (2025):**
- **75+ Public Cloud Regions** live, 14+ planned
- **72+ Cloud@Customer deployments**
- **60+ countries** with hybrid cloud presence
- **Multi-Cloud**: Database@Azure (28 regions), Database@AWS (2+ regions, 20 planned), Database@Google Cloud (8+ regions, 17 planned)

**Key OCI Services:**

```yaml
Compute:
  - Bare Metal: No virtualization overhead
  - VM: Consistent performance
  - Container Engine (OKE): Kubernetes workloads
  - Functions: Serverless (60 min runtime)

Storage:
  - Object Storage: 11 9s durability
  - Block Volume: Sub-ms latency
  - File Storage: Shared filesystems
  - Archive Storage: Cold data, compliance

Database:
  - Autonomous Database: Self-driving
  - Exadata Database Service: Extreme performance
  - Base Database: Full DBA access
  - NoSQL Database: Document, key-value
  - MySQL HeatWave: Analytics + OLTP

AI/ML:
  - OCI Generative AI: LLM inference
  - OCI AI Agent Platform: Agent development
  - Oracle AI Data Platform: OpenAI/xAI/Meta integration
```

### §3.2 · Oracle Database 23ai

**The Converged Database:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Oracle Database 23ai                         │
├───────────┬───────────┬───────────┬───────────┬─────────────────┤
│Relational │   JSON    │   Graph   │  Spatial  │  Vector / ML    │
│   SQL     │ Document  │ Property  │   Maps    │  AI Search      │
├───────────┴───────────┴───────────┴───────────┴─────────────────┤
│              Unified Storage & Processing Layer                  │
├─────────────────────────────────────────────────────────────────┤
│              Autonomous Capabilities (Optional)                  │
│         Auto-Tuning • Auto-Patching • Auto-Scaling              │
└─────────────────────────────────────────────────────────────────┘
```

**Key 23ai Innovations:**

| Feature | Description | Use Case |
|---------|-------------|----------|
| **AI Vector Search** | Native VECTOR datatype, similarity search | RAG, semantic search, recommendations |
| **JSON Relational Duality** | Dual access patterns (SQL + JSON) | Modern apps with relational consistency |
| **Property Graph Views** | SQL/PGQ standard graph queries | Fraud detection, network analysis |
| **SQL Firewall** | In-database attack protection | SQL injection prevention |
| **True Cache** | Disk-less Oracle cache instance | Application acceleration |
| **Priority Transactions** | Auto-prioritize critical transactions | Mission-critical workloads |

**Autonomous Database:**

| Capability | Implementation | Benefit |
|------------|----------------|---------|
| **Self-Driving** | AI-based optimization | Zero tuning effort |
| **Self-Securing** | Auto-patching, threat detection | Always secure |
| **Self-Repairing** | Auto backup, failover | 99.995% uptime |
| **Auto-Scaling** | Compute/storage independent | Cost optimization |

### §3.3 · Enterprise Applications

**Oracle Fusion Cloud:**

| Application | Function | FY2025 Revenue |
|-------------|----------|----------------|
| **Fusion ERP** | Financial management | $0.9B (up 16%) |
| **Fusion HCM** | Human capital | Core HR, Payroll, Talent |
| **Fusion SCM** | Supply chain | Inventory, Manufacturing |
| **Fusion CX** | Customer experience | Sales, Service, Marketing |
| **NetSuite** | Mid-market ERP | $0.9B (up 16%) |

**Oracle Health (Cerner):**
- $28.3B acquisition (2022) — Oracle's largest
- Millenium EHR + Oracle Cloud infrastructure
- AI-powered healthcare analytics
- Population health management

---
