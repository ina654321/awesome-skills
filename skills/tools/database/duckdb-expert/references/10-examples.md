# Examples

## 10.1 Basic SQL Patterns

### Create and Populate Tables

```sql
-- Create table from Parquet file
CREATE TABLE sales AS SELECT * FROM read_parquet('s3://data/sales/*.parquet');

-- Create table with schema
CREATE TABLE customers (
    id BIGINT PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE,
    created_at DATE DEFAULT CURRENT_DATE
);

-- Insert data
INSERT INTO customers VALUES (1, 'John Doe', 'john@example.com', '2024-01-01');
INSERT INTO customers SELECT * FROM read_csv('new_customers.csv');

-- Copy from CSV
COPY customers TO 'export.csv' (HEADER, DELIMITER ',');
```

### Aggregations

```sql
-- Basic aggregation
SELECT 
    category,
    COUNT(*) as count,
    SUM(amount) as total,
    AVG(amount) as average,
    MIN(amount) as min_val,
    MAX(amount) as max_val
FROM sales
GROUP BY category
HAVING SUM(amount) > 10000
ORDER BY total DESC;
```

### Window Functions

```sql
-- Running total
SELECT 
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total
FROM sales;

-- Rank within group
SELECT 
    product,
    category,
    revenue,
    RANK() OVER (PARTITION BY category ORDER BY revenue DESC) as rank
FROM product_sales;
```

## 10.2 Data Analysis Patterns

### Time Series Analysis

```sql
-- Monthly aggregation
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as orders,
    SUM(amount) as revenue
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY 1
ORDER BY 1;

-- Moving average
SELECT 
    date,
    value,
    AVG(value) OVER (
        ORDER BY date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7d
FROM metrics;
```

### Complex JOINs

```sql
-- Multi-table join
SELECT 
    o.order_id,
    c.customer_name,
    p.product_name,
    oi.quantity,
    oi.price * oi.quantity as line_total
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.status = 'completed';
```

## 10.3 CLI Commands

```bash
# Start DuckDB CLI
duckdb

# Open database
duckdb mydb.duckdb

# Run SQL from file
duckdb -c "SELECT * FROM table;" mydb.duckdb

# Export to CSV
duckdb -csv -c "SELECT * FROM table;" mydb.duckdb

# Multiple queries
duckdb mydb.duckdb <<EOF
.mode csv
.headers on
SELECT COUNT(*) FROM users;
SELECT * FROM orders LIMIT 5;
EOF
```

## 10.4 Python Examples

```python
import duckdb

# Basic connection
con = duckdb.connect('analytics.db')

# Query DataFrame
df = con.sql("""
    SELECT category, SUM(amount) as total
    FROM read_parquet('data/*.parquet')
    GROUP BY category
""").df()

# Register DataFrame as table
import pandas as pd
df = pd.read_csv('data.csv')
con.register('my_data', df)
result = con.execute("SELECT * FROM my_data WHERE amount > 100").fetchdf()

# Read multiple files
result = con.execute("""
    SELECT * FROM read_parquet(['file1.parquet', 'file2.parquet'])
""").df()

# Export to Parquet
con.execute("COPY results TO 'output.parquet' (FORMAT PARQUET)")
```

## 10.5 Advanced Patterns

### Subqueries and CTEs

```sql
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as revenue
    FROM orders
    GROUP BY 1
),
avg_sales AS (
    SELECT AVG(revenue) as avg_revenue FROM monthly_sales
)
SELECT 
    month,
    revenue,
    revenue - avg_revenue as delta
FROM monthly_sales, avg_sales
ORDER BY month;
```

### Conditional Aggregation

```sql
SELECT 
    customer_id,
    SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) as completed,
    SUM(CASE WHEN status = 'pending' THEN amount ELSE 0 END) as pending,
    SUM(CASE WHEN status = 'cancelled' THEN amount ELSE 0 END) as cancelled,
    COUNT(*) as total_orders
FROM orders
GROUP BY customer_id;
```

### Percentile Calculations

```sql
SELECT 
    category,
    quantile(amount, 0.25) as q1,
    quantile(amount, 0.50) as median,
    quantile(amount, 0.75) as q3,
    quantile(amount, 0.95) as p95,
    quantile(amount, 0.99) as p99
FROM sales
GROUP BY category;
```
