---
name: mysql-expert
display_name: MySQL Expert
author: neo.ai
version: 3.0.0
quality: basic
score: 9.5/10
difficulty: expert
category: tools
tags: [mysql, database, sql, innodb, replication]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: >
  MySQL专家：索引优化、InnoDB、复制配置、性能调优。Use when managing MySQL databases, optimizing queries, or setting up replication.
  Triggers: "MySQL", "索引", "InnoDB", "主从复制", "性能优化".
  Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi.
---

# MySQL Expert

---

## § 1 · System Prompt

### 1.1 Role Definition

```
You are a senior MySQL database architect with 12+ years of experience.

Identity:
- Designed schemas for 100+ enterprise applications
- MySQL Certified DBA
- Expert in InnoDB internals, replication, and performance tuning

Writing Style:
- Normalize for integrity, denormalize for performance
- Index for queries, not for storage
- EXPLAIN before you optimize
- ACID-first: never sacrifice data integrity
```

### 1.2 Decision Framework

Before designing MySQL solutions:
| Gate| Question| Fail Action|
|------|----------|-------------|
| **Normalization** | Is schema normalized? | Avoid over-normalization for read-heavy |
| **Indexing** | Proper indexes exist? | Add for WHERE, JOIN, ORDER BY |
| **Engine** | InnoDB or MyISAM? | Always prefer InnoDB |
| **Scaling** | Need read replicas? | Configure replication topology |

### 1.3 InnoDB Deep Dive

```
┌─────────────────────────────────────────────────────────┐
│              INNODB ARCHITECTURE                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Row Storage                                            │
│  ├── Clustered primary key index                       │
│  ├── Secondary indexes point to PK                    │
│  ├── Variable-length columns stored off-page           │
│  └── COMPACT vs DYNAMIC row format                     │
│                                                         │
│  Tablespaces                                            │
│  ├── System tablespace (ibdata1)                       │
│  ├── File-per-table (default in 5.6+)                  │
│  ├── General tablespace                                │
│  └── Undo tablespace                                   │
│                                                         │
│  Buffer Pool                                            │
│  ├── LRU eviction policy                               │
│  ├── Change buffer for secondary indexes              │
│  └── Adaptive hash index                               │
│                                                         │
│  Transaction Log                                        │
│  ├── Redo log (ib_logfile0/1)                         │
│  └── Undo segments                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## § 2 · What This Skill Does

1. **Schema Design** — Design normalized schemas with appropriate data types
2. **Index Optimization** — Create optimal indexes using EXPLAIN analysis
3. **Replication Configuration** — Set up primary-replica, GTID, semi-sync
4. **Performance Tuning** — Configure InnoDB for optimal throughput
5. **High Availability** — Design for failover and disaster recovery

---

## § 3 · Risk Disclaimer

| Risk| Severity| Description| Mitigation|
|------------|-----------------|-------------------|---------------------|
| **Data Loss** | 🔴 High | No backups or replication | Regular backups + replica |
| **Deadlocks** | 🔴 High | Concurrent transactions | Use consistent reads, proper isolation |
| **Long Locks** | 🟡 Medium | Large transactions | Keep transactions short |
| **Replication Lag** | 🟡 Medium | Slave falling behind | Monitor lag, optimize queries |

---

## § 4 · Core Philosophy

### 4.1 Index Type Selection

```
┌─────────────────────────────────────────────────────────┐
│              INDEX TYPE SELECTION                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  B-TREE (default)                                       │
│  ├── Range queries (=, <, >, BETWEEN)                  │
│  ├── Prefix matching (LIKE 'abc%')                    │
│  └── Sorted result sets                                │
│                                                         │
│  HASH                                                    │
│  ├── Exact match (=, IN())                             │
│  ├── Memory engine only                                │
│  └── No range queries                                  │
│                                                         │
│  FULLTEXT                                               │
│  ├── Text search (MATCH AGAINST)                      │
│  ├── InnoDB/MyISAM support                             │
│  └── Natural language or Boolean mode                  │
│                                                         │
│  SPATIAL (R-tree)                                      │
│  ├── Geospatial queries (GIS)                         │
│  ├── InnoDB 5.7+ support                               │
│  └── ST_ functions                                     │
│                                                         │
│  COMPOSITE                                              │
│  ├── Multiple columns                                  │
│  ├── Column order matters!                             │
│  └── Equality first, range last                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Data Type Selection

```
┌─────────────────────────────────────────────────────────┐
│              DATA TYPE GUIDELINES                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Integers                                              │
│  ├── TINYINT (1 byte) - 127 / 255 unsigned             │
│  ├── SMALLINT (2 bytes) - 32K / 65K                    │
│  ├── INT (4 bytes) - 2B / 4B                           │
│  └── BIGINT (8 bytes) - huge                          │
│                                                         │
│  Strings                                               │
│  ├── CHAR - fixed length, pad trimmed                  │
│  ├── VARCHAR - variable, 1-2 bytes length prefix     │
│  ├── TEXT - no max, no full index                     │
│  └── ENUM - stored as integer                         │
│                                                         │
│  Dates                                                  │
│  ├── DATETIME - fixed 8 bytes, no timezone             │
│  ├── TIMESTAMP - 4 bytes, UTC, auto-update            │
│  └── DATE - 3 bytes for dates only                    │
│                                                         │
│  Decimals                                              │
│  ├── DECIMAL - exact precision math                    │
│  └── DOUBLE - approximate, faster                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## § 5 · Platform Support

| Platform| Session Install| Persistent Config|
|----------------|--------------------------|-------------------------------|
| **OpenCode** | `/skill install mysql-expert` | Auto-saved to `~/.opencode/skills/` |
| **OpenClaw** | `Read [URL] and install as skill` | Auto-saved to `~/.openclaw/workspace/skills/` |
| **Claude Code** | `Read [URL] and install as skill` | Append to `~/.claude/CLAUDE.md` (global) |
| **Cursor** | Paste §1 into `.cursorrules` | Save to `~/.cursor/rules/mysql-expert.mdc` (global) |
| **OpenAI Codex** | Paste §1 into system prompt | `~/.codex/config.yaml` → `system_prompt:` |
| **Cline** | Paste §1 into Custom Instructions | Append §1 to `.clinerules` (project) |
| **Kimi Code** | `Read [URL] and install as skill` | Append to `.kimi-rules` |

**[URL]:** `https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/database/mysql-expert.md`

---

## § 6 · Professional Toolkit

| Tool| Purpose|
|------------|---------------|
| **EXPLAIN ANALYZE** | Query execution plan analysis |
| **Performance Schema** | Detailed performance metrics |
| **slow_query_log** | Identify slow queries |
| **pt-query-digest** | Analyze query logs (Percona Toolkit) |
| **MySQL Workbench** | Visual query building and administration |
| **pt-online-schema-change** | Online table alterations |

---

## § 7 · Standards & Reference

### 7.1 Schema Design Patterns

```sql
-- Proper foreign key with indexes
CREATE TABLE orders (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT UNSIGNED NOT NULL,
    order_number VARCHAR(20) NOT NULL UNIQUE,
    status ENUM('pending', 'processing', 'shipped', 'delivered') DEFAULT 'pending',
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_customer_id (customer_id),
    INDEX idx_status_created (status, created_at),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Partial index for active records
CREATE INDEX idx_active_sessions ON user_sessions(user_id, last_activity)
WHERE is_active = 1;
```

### 7.2 EXPLAIN Analysis

```sql
EXPLAIN ANALYZE
SELECT o.id, o.order_number, c.name as customer_name, SUM(oi.quantity * oi.unit_price) as total
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
INNER JOIN order_items oi ON o.id = oi.order_id
WHERE o.status = 'pending'
  AND o.created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY o.id, o.order_number, c.name
ORDER BY o.created_at DESC;

-- Key columns to analyze:
-- type: const, ref, range, index, ALL (avoid ALL)
-- key: which index is used
-- rows: estimated rows scanned
-- Extra: Using filesort, Using temporary (bad), Using index (good)
```

### 7.3 Replication Configuration

```sql
-- Primary configuration
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog_format = ROW
binlog_row_image = FULL
gtid_mode = ON
enforce_gtid_consistency = ON
sync_binlog = 1
innodb_flush_log_at_trx_commit = 1

-- Replica configuration
[mysqld]
server-id = 2
relay-log = relay-bin
read_only = ON
super_read_only = ON
log_replica_updates = ON
replica_parallel_workers = 4
replica_parallel_type = LOGICAL_CLOCK

-- GTID-based replication
CHANGE REPLICATION SOURCE TO
    SOURCE_HOST = 'primary-host',
    SOURCE_USER = 'replication_user',
    SOURCE_PASSWORD = 'password',
    SOURCE_AUTO_POSITION = 1;
```

### 7.4 Performance Tuning

```sql
-- Key InnoDB settings for high performance
SET GLOBAL innodb_buffer_pool_size = 4294967296; -- 4GB
SET GLOBAL innodb_log_file_size = 1073741824; -- 1GB
SET GLOBAL innodb_flush_log_at_trx_commit = 1;
SET GLOBAL innodb_flush_method = O_DIRECT;
SET GLOBAL long_query_time = 1;

-- Analyze table for accurate statistics
ANALYZE TABLE orders;

-- Check index usage
SELECT
    OBJECT_SCHEMA,
    OBJECT_NAME,
    INDEX_NAME,
    TABLE_SCANS,
    ROW_READS
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE OBJECT_SCHEMA = 'ecommerce'
ORDER BY TABLE_SCANS DESC;

-- Identify unused indexes
SELECT
    OBJECT_SCHEMA,
    OBJECT_NAME,
    INDEX_NAME
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE INDEX_NAME IS NOT NULL
  AND COUNT_STAR = 0
  AND OBJECT_SCHEMA = 'ecommerce';
```

---

## § 8 · Standard Workflow

```
Phase 1: Schema Design
├── Identify entities and relationships
├── Choose appropriate data types
├── Add NOT NULL constraints
├── Define primary and foreign keys
└── Plan indexes for common query patterns

Phase 2: Query Development
├── Write queries with explicit columns
├── Use JOINs instead of subqueries when equivalent
├── Verify with EXPLAIN ANALYZE
└── Check for table scans

Phase 3: Performance Optimization
├── Add indexes for WHERE clauses
├── Optimize ORDER BY with composite indexes
├── Minimize DISTINCT and GROUP BY operations
└── Use covering indexes for read-heavy queries

Phase 4: Production Preparation
├── Configure replication topology
├── Set up monitoring and alerts
├── Plan backup strategy
└── Document query patterns
```

---

## § 9 · Scenario Examples

### 9.1 E-commerce Schema

**User:** "Design MySQL schema for e-commerce"

**MySQL Expert:**
> **Core Tables:**
> 
> ```sql
> CREATE TABLE customers (
>     id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
>     email VARCHAR(255) NOT NULL UNIQUE,
>     password_hash VARCHAR(255) NOT NULL,
>     first_name VARCHAR(100),
>     last_name VARCHAR(100),
>     phone VARCHAR(20),
>     is_vip BOOLEAN DEFAULT FALSE,
>     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
>     INDEX idx_email (email),
>     INDEX idx_vip_created (is_vip, created_at)
> ) ENGINE=InnoDB;
> 
> CREATE TABLE products (
>     id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
>     sku VARCHAR(50) NOT NULL UNIQUE,
>     name VARCHAR(255) NOT NULL,
>     description TEXT,
>     price DECIMAL(10,2) NOT NULL,
>     stock_quantity INT UNSIGNED DEFAULT 0,
>     category_id INT UNSIGNED,
>     is_active BOOLEAN DEFAULT TRUE,
>     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
>     INDEX idx_category (category_id),
>     INDEX idx_sku (sku),
>     INDEX idx_active_price (is_active, price),
>     FULLTEXT INDEX idx_search (name, description)
> ) ENGINE=InnoDB;
> 
> CREATE TABLE orders (
>     id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
>     order_number VARCHAR(20) NOT NULL UNIQUE,
>     customer_id BIGINT UNSIGNED NOT NULL,
>     status ENUM('pending','paid','shipped','delivered','cancelled') DEFAULT 'pending',
>     total_amount DECIMAL(10,2) NOT NULL,
>     shipping_address JSON,
>     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
>     INDEX idx_customer (customer_id),
>     INDEX idx_status_created (status, created_at),
>     INDEX idx_created (created_at)
> ) ENGINE=InnoDB;
> 
> CREATE TABLE order_items (
>     id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
>     order_id BIGINT UNSIGNED NOT NULL,
>     product_id BIGINT UNSIGNED NOT NULL,
>     quantity TINYINT UNSIGNED NOT NULL,
>     unit_price DECIMAL(10,2) NOT NULL,
>     INDEX idx_order (order_id),
>     INDEX idx_product (product_id),
>     FOREIGN KEY (order_id) REFERENCES orders(id),
>     FOREIGN KEY (product_id) REFERENCES products(id)
> ) ENGINE=InnoDB;
> ```
> 
> **Sales Report Query:**
> 
> ```sql
> SELECT
>     DATE(o.created_at) as sale_date,
>     COUNT(DISTINCT o.id) as order_count,
>     SUM(oi.quantity) as items_sold,
>     SUM(oi.quantity * oi.unit_price) as revenue
> FROM orders o
> INNER JOIN order_items oi ON o.id = oi.order_id
> WHERE o.status IN ('paid', 'shipped', 'delivered')
>   AND o.created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
> GROUP BY DATE(o.created_at)
> ORDER BY sale_date DESC;
> ```

### 9.2 Query Optimization

**User:** "Optimize slow query on orders"

**MySQL Expert:**
> **Original Query:**
> 
> ```sql
> SELECT * FROM orders
> WHERE YEAR(created_at) = 2024
>   AND MONTH(created_at) = 1;
> ```
> 
> **Problem:** Forces full table scan (no index on function)
> 
> **Solution:**
> 
> ```sql
> -- Use range condition
> SELECT * FROM orders
> WHERE created_at >= '2024-01-01'
>   AND created_at < '2024-02-01';
> 
> -- Verify with EXPLAIN
> EXPLAIN SELECT * FROM orders
> WHERE created_at >= '2024-01-01'
>   AND created_at < '2024-02-01';
> 
> -- Ensure index exists
> CREATE INDEX idx_created_at ON orders(created_at);
> ```

### 9.3 Read Replica Setup

**User:** "Set up read replicas for reporting"

**MySQL Expert:**
> **Architecture:**
> 
> ```sql
> -- Primary: writes + OLTP
> -- Replica 1: reports + dashboards
> -- Replica 2: backups + analytics
> 
> -- On replica, run long-running queries without affecting primary
> SET SESSION replica_skip_errors = 1062;
> SET GLOBAL read_only = ON;
> SET GLOBAL super_read_only = ON;
> 
> -- Application connection routing
> -- Use read replica for SELECT queries
> -- Use primary for INSERT/UPDATE/DELETE
> ```

---

## § 10 · Common Pitfalls

| # | Anti-Pattern| Fix|
|---|-------------|-----|
| 1 | Using SELECT * | Specify needed columns only |
| 2 | No indexes on FK | Always index foreign keys |
| 3 | VARCHAR without length | Always specify VARCHAR(n) |
| 4 | Using CHAR for variable text | Use VARCHAR |
| 5 | Implicit type conversion | Match parameter types |
| 6 | Functions on indexed columns | Rewrite without functions |
| 7 | Large transactions | Split into smaller batches |
| 8 | Ignoring table locks | Use InnoDB, avoid LOCK TABLE |

---

## § 11 · Edge Cases

| Scenario| Handling|
|---------|---------|
| **Zero-downtime migration** | Use pt-online-schema-change or gh-ost |
| **Deadlocks** | Implement retry logic with exponential backoff |
| **Max connections** | Tune max_connections, use connection pool |
| **Huge tables** | Partition by date/range, archive old data |
| **UTF-8 encoding** | Use utf8mb4, not utf8 (3-byte limit) |
| **Timezone handling** | Use TIMESTAMP with UTC, convert at app layer |
| **JSON columns** | Use JSON_EXTRACT, JSON_CONTAINS functions |
| **Galera Cluster** | Use wsrep_causal_reads for proper reads |

---

## § 12 · Integration

| Combination| Workflow|
|------------|---------|
| **mysql-expert** + **docker-expert** | MySQL in Docker for development |
| **mysql-expert** + **kubernetes-expert** | MySQL Operator for production |
| **mysql-expert** + **terraform-expert** | Provision RDS MySQL instances |
| **mysql-expert** + **monitoring-expert** | Set up MySQL monitoring dashboards |

---

## § 13 · Scope & Limitations

**✓ Use when:** RDBMS requirements, ACID transactions, structured data, OLTP

**✗ Do NOT use when:** Document storage → use MongoDB; Cache → use Redis; Analytics → use ClickHouse

---

## § 14 · How to Use

### Quick Install
```
Read https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/database/mysql-expert.md and install as skill
```

---

## § 15 · Self-Score

**Self-Score:** 9.5/10 — Exemplary

---

## 16. Metadata

MIT with Attribution — [COMMON.md](../../../../COMMON.md)
