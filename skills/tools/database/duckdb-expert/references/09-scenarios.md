# Scenario Examples

## 9.1 Local Analytics

**Scenario:** Analyzing local CSV/Parquet files on a laptop without a database server.

### Single-File Analysis

```sql
-- Load and analyze a single file
SELECT 
    date_trunc('week', timestamp) AS week,
    category,
    count(*) AS transactions,
    sum(amount) AS total_sales,
    avg(amount) AS avg_sale
FROM 'sales_2024.csv'
WHERE status = 'completed'
GROUP BY 1, 2
ORDER BY 1, 3 DESC;

-- Multi-file analysis with glob
SELECT *
FROM 'data/2024/*.parquet'
WHERE region = 'US'
ORDER BY date;
```

### Local Database Workflow

```python
import duckdb
import pandas as pd

# Create local analytics database
con = duckdb.connect('analytics.duckdb')

# Load data from files
con.execute("""
    CREATE TABLE sales AS 
    SELECT * FROM 'sales_2024.csv'
""")

con.execute("""
    CREATE TABLE customers AS 
    SELECT * FROM 'customers.parquet'
""")

# Analytics queries
monthly = con.execute("""
    SELECT 
        strftime(order_date, '%Y-%m') AS month,
        c.segment,
        SUM(s.amount) AS revenue,
        COUNT(*) AS orders
    FROM sales s
    JOIN customers c ON s.customer_id = c.id
    GROUP BY 1, 2
    ORDER BY 1, 2
""").df()

print(monthly.head())

# Export results
con.execute("""
    COPY ({monthly_query}) TO 'monthly_report.csv' (HEADER, DELIMITER ',')
""".format(monthly_query="SELECT * FROM monthly_sales"))
```

### Cohort Analysis

```sql
-- Customer cohort retention analysis
WITH first_purchase AS (
    SELECT 
        customer_id,
        min(order_date) AS cohort_date,
        date_trunc('month', min(order_date)) AS cohort_month
    FROM orders
    GROUP BY customer_id
),
customer_activity AS (
    SELECT 
        o.customer_id,
        f.cohort_month,
        date_trunc('month', o.order_date) AS activity_month,
        date_diff('month', f.cohort_month, date_trunc('month', o.order_date)) AS months_since_first
    FROM orders o
    JOIN first_purchase f ON o.customer_id = f.customer_id
)
SELECT 
    cohort_month,
    months_since_first,
    count(DISTINCT customer_id) AS customers,
    count(*) AS orders
FROM customer_activity
GROUP BY 1, 2
ORDER BY 1, 2;
```

## 9.2 Data Pipeline

**Scenario:** Reading from S3, transforming data, writing to another location.

### S3 Data Pipeline

```sql
-- Enable S3 support
INSTALL httpfs;
LOAD httpfs;

-- Configure S3
SET s3_access_key_id = 'AKIAIOSFODNN7EXAMPLE';
SET s3_secret_access_key = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY';
SET s3_region = 'us-east-1';

-- Read from S3
SELECT * FROM 's3://my-bucket/raw/*.parquet' LIMIT 100;

-- ETL: Transform and write
CREATE TABLE cleaned_data AS
SELECT
    id,
    lower(trim(name)) AS name,
    date,
    round(amount, 2) AS amount,
    lower(category) AS category,
    year(date) AS year,
    month(date) AS month
FROM 's3://my-bucket/raw/transactions.parquet'
WHERE status = 'active'
  AND amount > 0;

-- Write to S3
COPY cleaned_data TO 's3://my-bucket/processed/transactions.parquet' (FORMAT PARQUET);

-- Partitioned write
COPY cleaned_data TO 's3://my-bucket/processed/' (
    FORMAT PARQUET,
    PARTITION_BY (year, month),
    OVERWRITE_OR_IGNORE true
);
```

### Python Pipeline

```python
import duckdb

con = duckdb.connect()

# Define pipeline stages
stages = [
    {
        'source': 's3://bucket/raw/events_*.parquet',
        'transform': """
            SELECT 
                event_id,
                user_id,
                event_type,
                timestamp,
                properties:page AS page,
                properties:duration AS duration
            FROM read_parquet(?)
        """,
        'dest': 'events_cleaned'
    },
    {
        'source': 's3://bucket/raw/users.parquet',
        'transform': "SELECT * FROM read_parquet(?) WHERE active = true",
        'dest': 'users_active'
    }
]

for stage in stages:
    df = con.execute(stage['transform'], [stage['source']]).df()
    con.execute(f"CREATE TABLE {stage['dest']} AS SELECT * FROM df")
    print(f"Processed {stage['dest']}: {len(df)} rows")

# Join and aggregate
result = con.execute("""
    SELECT 
        e.event_type,
        u.segment,
        count(*) AS events,
        avg(e.duration) AS avg_duration
    FROM events_cleaned e
    JOIN users_active u ON e.user_id = u.id
    GROUP BY 1, 2
    ORDER BY 3 DESC
""").df()

# Write output
result.to_parquet('s3://bucket/analytics/segment_events.parquet')
```

## 9.3 ML Integration

### Python with Pandas/Scikit-learn

```python
import duckdb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load data via DuckDB
con = duckdb.connect()

df = con.execute("""
    SELECT 
        feature1,
        feature2,
        feature3,
        target
    FROM 'training_data.parquet'
    WHERE target IS NOT NULL
""").df()

# Split for ML
X = df[['feature1', 'feature2', 'feature3']]
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Score and log
score = model.score(X_test, y_test)
print(f"R² Score: {score:.3f}")

# Batch prediction on new data
new_data = con.execute("""
    SELECT feature1, feature2, feature3
    FROM 'prediction_candidates.parquet'
""").df()

predictions = model.predict(new_data)

# Store predictions back
result_df = new_data.copy()
result_df['predicted_target'] = predictions
con.execute("""
    COPY (SELECT * FROM result_df) TO 'predictions.parquet' (FORMAT PARQUET)
""")
```

### DuckDB ML Extension (v1.1+)

```sql
-- Install ML extension
INSTALL sml;
LOAD sml;

-- Create model
CREATE MODEL price_predictor USING
    regressor (
        SELECT feature1, feature2, feature3 FROM training_data
    );

-- Predict
SELECT 
    id,
    PREDICT(price_predictor USING feature1, feature2, feature3) AS predicted_price
FROM new_products;
```

### R Integration

```r
library(duckdb)
library(dplyr)

con <- dbConnect(duckdb())

# Load data
sales <- tbl(con, "sales_parquet") 

# Preprocess with dplyr syntax
summary <- sales %>%
    filter(year >= 2023) %>%
    group_by(category, month) %>%
    summarize(
        total_revenue = sum(revenue),
        avg_order = mean(order_value),
        n_orders = n()
    ) %>%
    collect()

# Run R model
model <- lm(total_revenue ~ avg_order, data = summary)

# Write predictions back
predictions <- data.frame(
    category = summary$category,
    predicted = predict(model, summary)
)

dbWriteTable(con, "predictions", predictions, overwrite = TRUE)
```

### Feature Engineering with DuckDB

```sql
-- Create features for ML training
CREATE TABLE feature_table AS
WITH user_stats AS (
    SELECT 
        user_id,
        count(*) AS total_events,
        avg(session_duration) AS avg_session,
        count(DISTINCT date) AS active_days
    FROM events
    GROUP BY user_id
),
purchase_stats AS (
    SELECT 
        user_id,
        sum(amount) AS lifetime_value,
        count(*) AS total_purchases,
        max(date) AS last_purchase_date
    FROM purchases
    GROUP BY user_id
)
SELECT
    u.user_id,
    u.total_events,
    u.avg_session,
    u.active_days,
    p.lifetime_value,
    p.total_purchases,
    date_diff('day', p.last_purchase_date, current_date) AS days_since_purchase,
    p.total_purchases::FLOAT / NULLIF(u.active_days, 0) AS purchase_rate,
    p.lifetime_value / NULLIF(u.total_events, 0) AS value_per_event
FROM user_stats u
LEFT JOIN purchase_stats p ON u.user_id = p.user_id;

-- Export for ML
COPY feature_table TO '/tmp/features.parquet' (FORMAT PARQUET);
```
