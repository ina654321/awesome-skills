# Examples

## 10.1 Advanced SQL Patterns

### UPSERT (ON CONFLICT)

```sql
INSERT INTO users (id, email, name)
VALUES (1, 'test@example.com', 'Test')
ON CONFLICT (id) DO UPDATE SET
    email = EXCLUDED.email,
    name = EXCLUDED.name;

-- UPSERT with unique constraint
INSERT INTO products (sku, name, price)
VALUES ('SKU-001', 'Widget', 19.99)
ON CONFLICT (sku) DO UPDATE SET
    price = EXCLUDED.price,
    updated_at = NOW();
```

### RETURNING

```sql
-- Return inserted rows
INSERT INTO orders (customer_id, total)
VALUES (1, 99.99)
RETURNING id, created_at;

-- Update and return
UPDATE inventory
SET stock = stock - 1
WHERE product_id = 5 AND stock > 0
RETURNING *;

-- Delete and return
DELETE FROM cart_items
WHERE cart_id = 123
RETURNING product_id, quantity;
```

### LATERAL JOIN

```sql
-- Get latest order per customer
SELECT c.name, latest.order_date, latest.total
FROM customers c
CROSS JOIN LATERAL (
    SELECT order_date, total
    FROM orders
    WHERE customer_id = c.id
    ORDER BY order_date DESC
    LIMIT 1
) AS latest;

-- Top N per group
SELECT category, product_name, sales
FROM products p
CROSS JOIN LATERAL (
    SELECT SUM(quantity) AS sales
    FROM sales s
    WHERE s.product_id = p.id
) AS sales_data
ORDER BY category, sales DESC;
```

## 10.2 JSONB Operations

```sql
-- Create with JSONB
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    payload JSONB NOT NULL
);

-- Insert
INSERT INTO events (payload) VALUES
('{"type": "click", "url": "/home", "user": "123"}'),
('{"type": "pageview", "url": "/about", "user": "456"}');

-- Query JSONB
SELECT * FROM events WHERE payload->>'type' = 'click';
SELECT * FROM events WHERE payload @> '{"user": "123"}';
SELECT * FROM events WHERE payload ? 'type';

-- GIN index for JSONB
CREATE INDEX idx_events_payload ON events USING GIN(payload);

-- Update JSONB
UPDATE events
SET payload = jsonb_set(payload, '{url}', '"https://example.com"')
WHERE id = 1;

-- Add to JSONB
UPDATE events
SET payload = payload || '{"source": "web"}'::jsonb
WHERE id = 1;

-- Remove key
UPDATE events
SET payload = payload - 'type'
WHERE id = 1;
```

## 10.3 Window Functions

```sql
-- Running total
SELECT 
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) AS running_total
FROM sales;

-- Partition by category
SELECT 
    category,
    product,
    sales,
    SUM(sales) OVER (PARTITION BY category) AS category_total,
    RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS rank,
    LAG(sales, 1) OVER (PARTITION BY category ORDER BY date) AS prev_sales,
    sales - LAG(sales, 1) OVER (PARTITION BY category ORDER BY date) AS sales_delta
FROM daily_sales;
```

## 10.4 Index Patterns

### Partial Index

```sql
-- Index only active users
CREATE INDEX idx_users_active ON users(last_login)
WHERE deleted_at IS NULL;

-- Index recent orders
CREATE INDEX idx_orders_recent ON orders(created_at DESC)
WHERE created_at > '2023-01-01';
```

### Expression Index

```sql
-- Index lowercased email
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Index on JSONB extraction
CREATE INDEX idx_data_name ON events((payload->>'name'));
```

### BRIN Index (Time Series)

```sql
-- Natural ordering, small index
CREATE INDEX idx_logs_created ON logs USING BRIN(created_at);

-- With page range
CREATE INDEX idx_logs_created ON logs USING BRIN(created_at) WITH (pages_per_range = 32);
```

### Covering Index

```sql
-- Include frequently accessed columns
CREATE INDEX idx_orders_covering 
ON orders(customer_id, created_at DESC)
INCLUDE (total, status);
```

## 10.5 Schema Patterns

### Soft Delete with Index

```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    deleted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_articles_active ON articles(created_at DESC)
WHERE deleted_at IS NULL;

-- Query: active articles only
SELECT * FROM articles WHERE deleted_at IS NULL ORDER BY created_at DESC;
```

### Audit Trail with Trigger

```sql
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name TEXT,
    action TEXT,
    row_id INTEGER,
    old_data JSONB,
    new_data JSONB,
    changed_by TEXT,
    changed_at TIMESTAMP DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log VALUES (
            TG_TABLE_NAME, TG_OP, NEW.id, NULL, to_jsonb(NEW), 
            current_user
        );
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log VALUES (
            TG_TABLE_NAME, TG_OP, OLD.id, to_jsonb(OLD), to_jsonb(NEW),
            current_user
        );
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log VALUES (
            TG_TABLE_NAME, TG_OP, OLD.id, to_jsonb(OLD), NULL,
            current_user
        );
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_users
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION audit_trigger();
```

## 10.6 Full Text Search

```sql
-- Add search vector column
ALTER TABLE articles ADD COLUMN search_vector tsvector;

-- Populate
UPDATE articles SET search_vector = 
    to_tsvector('english', coalesce(title, '') || ' ' || coalesce(content, ''));

-- Index
CREATE INDEX idx_articles_search ON articles USING GIN(search_vector);

-- Search
SELECT title, ts_rank(search_vector, query) AS rank
FROM articles, to_tsquery('english', 'postgresql & tutorial') query
WHERE search_vector @@ query
ORDER BY rank DESC;

-- With headline
SELECT title, ts_headline('english', content, query) AS snippet
FROM articles, to_tsquery('english', 'postgresql') query
WHERE search_vector @@ query;
```

## 10.7 Connection Pooling with pgBouncer

```ini
; pgbouncer.ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
listen_port = 6432
listen_addr = 127.0.0.1
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 3
```

## 10.8 CLI Commands

```bash
# psql
psql -U user -d db -h host -p 5432 -c "SELECT 1"
psql -U user -d db -f query.sql
psql -U user -d db --set=ON_ERROR_STOP=1 -f script.sql

# pg_dump
pg_dump -U postgres -Fc dbname > backup.dump
pg_dump -U postgres -Fd dbname -j 4 -f backup_dir

# pg_restore
pg_restore -U postgres -d dbname --jobs=4 backup.dump
pg_restore -U postgres -d dbname --create backup.dump

# psql meta
\dt+  -- tables with sizes
\di+  -- indexes with sizes
\dx   -- extensions
\df+  -- functions with source
```
