# Examples

## 10.1 SQL Patterns

### Common Table Expressions (CTE)

```sql
WITH monthly_sales AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS month,
        customer_id,
        SUM(total) AS revenue
    FROM orders
    GROUP BY DATE_FORMAT(order_date, '%Y-%m'), customer_id
),
ranked_customers AS (
    SELECT 
        month,
        customer_id,
        revenue,
        RANK() OVER (PARTITION BY month ORDER BY revenue DESC) AS rnk
    FROM monthly_sales
)
SELECT * FROM ranked_customers WHERE rnk <= 5;
```

### Window Functions

```sql
-- Running total
SELECT 
    order_date,
    amount,
    SUM(amount) OVER (ORDER BY order_date) AS running_total
FROM orders;

-- Partition by category
SELECT 
    category,
    product_name,
    sales,
    SUM(sales) OVER (PARTITION BY category) AS category_total,
    ROUND(sales * 100.0 / SUM(sales) OVER (PARTITION BY category), 2) AS pct
FROM products;
```

### Recursive CTE

```sql
WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 1 AS level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, ot.level + 1
    FROM employees e
    JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT * FROM org_tree ORDER BY level, name;
```

## 10.2 Index Patterns

### Partial/Covering Index

```sql
-- Covering index for specific query
CREATE INDEX idx_order_status_date 
ON orders(status, order_date DESC)
INCLUDE (customer_id, total);

-- Index for JSON extraction
CREATE INDEX idx_data_email 
ON users((CAST(data->>'$.email' AS CHAR(255))));
```

### Invisible Index

```sql
-- Test index impact without dropping
CREATE INDEX idx_test ON users(email);
ALTER INDEX idx_test INVISIBLE;

-- Verify query uses different index or not
EXPLAIN SELECT * FROM users WHERE email LIKE 'a%';

-- Make visible or drop
ALTER INDEX idx_test VISIBLE;
DROP INDEX idx_test ON users;
```

## 10.3 JSON Operations

```sql
-- Create JSON column
CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    attributes JSON
);

-- Insert JSON
INSERT INTO products VALUES (1, 'Widget', '{"color": "red", "sizes": ["S", "M"]}');

-- Query JSON
SELECT * FROM products WHERE attributes->>'$.color' = 'red';

-- Update JSON
UPDATE products 
SET attributes = JSON_SET(attributes, '$.color', 'blue')
WHERE id = 1;

-- Search in JSON array
SELECT * FROM products WHERE JSON_CONTAINS(attributes->>'$.sizes', '"M"');
```

## 10.4 Schema Patterns

### E-commerce Schema

```sql
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    INDEX idx_category (category_id)
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    status ENUM('pending', 'processing', 'shipped', 'delivered') DEFAULT 'pending',
    total DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    INDEX idx_customer (customer_id),
    INDEX idx_status_date (status, created_at)
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Soft Delete Pattern

```sql
CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    deleted_at TIMESTAMP NULL,
    INDEX idx_active (deleted_at)
);

-- Query active only
SELECT * FROM articles WHERE deleted_at IS NULL;

-- Soft delete
UPDATE articles SET deleted_at = NOW() WHERE id = 1;
```

## 10.5 CLI Commands

```bash
# Connect
mysql -u root -p database_name
mysql -h hostname -u user -p database_name

# Execute from file
mysql -u root -p < schema.sql
mysql -u root -p -e "SELECT * FROM table" database

# Import/Export
mysqldump -u root -p database > backup.sql
mysql -u root -p database < backup.sql

# Multi-table dump
mysqldump -u root -p --databases db1 db2 > multi.sql

# Copy database
mysqldump -u root -p source_db | mysql -u root -p target_db

# Check table
mysqlcheck -u root -p --optimize database
mysqlcheck -u root -p --analyze database

# Process list
SHOW PROCESSLIST;
KILL 123;
```

## 10.6 Performance Patterns

### Pagination

```sql
-- Keyset pagination (faster than OFFSET)
SELECT * FROM orders 
WHERE id > 1000 
ORDER BY id 
LIMIT 20;

-- Cursor-based
SELECT * FROM posts 
WHERE created_at < '2024-01-01' 
ORDER BY created_at DESC 
LIMIT 10;
```

### Upsert

```sql
-- MySQL 8.0+
INSERT INTO users (id, email, name) 
VALUES (1, 'test@example.com', 'Test')
ON DUPLICATE KEY UPDATE 
    name = VALUES(name),
    updated_at = CURRENT_TIMESTAMP;

-- MySQL 8.0+ REPLACE
REPLACE INTO users (id, email, name) VALUES (1, 'test@example.com', 'Test');
```

### Row Number

```sql
-- Deduplicate
DELETE FROM orders
WHERE id NOT IN (
    SELECT id FROM (
        SELECT MIN(id) FROM orders
        GROUP BY customer_id, order_date
    ) AS kept
);
```
