# Examples

## 10.1 Basic Model

```sql
-- models/staging/stg_orders.sql
{{ config(materialized='view') }}

SELECT 
    order_id,
    customer_id,
    order_date,
    status,
    total_amount
FROM {{ source('ecom', 'orders') }}
```

## 10.2 Staging Model with Transformations

```sql
-- models/staging/stg_customers.sql
WITH source AS (
    SELECT * FROM {{ source('ecom', 'customers') }}
),

renamed AS (
    SELECT
        customer_id AS id,
        first_name,
        last_name,
        email,
        created_at AS customer_created_at,
        CASE 
            WHEN status = 'active' THEN TRUE 
            ELSE FALSE 
        END AS is_active
    FROM source
)

SELECT * FROM renamed
```

## 10.3 Intermediate Model

```sql
-- models/intermediate/int_order_items.sql
{{ config(materialized='table') }}

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),

joined AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_date,
        i.product_id,
        i.quantity,
        i.unit_price,
        i.quantity * i.unit_price AS line_total
    FROM orders o
    JOIN items i ON o.order_id = i.order_id
)

SELECT * FROM joined
```

## 10.4 Fact Table

```sql
-- models/marts/fct_orders.sql
{{ config(
    materialization='incremental',
    unique_key='order_id'
) }}

WITH source AS (
    SELECT * FROM {{ ref('int_order_items') }}
    {% if is_incremental() %}
    WHERE order_date > (SELECT MAX(order_date) FROM {{ this }})
    {% endif %}
),

aggregated AS (
    SELECT
        order_id,
        MIN(order_date) AS order_date,
        customer_id,
        SUM(line_total) AS total_revenue,
        COUNT(DISTINCT product_id) AS unique_products,
        SUM(quantity) AS total_items
    FROM source
    GROUP BY order_id, customer_id
)

SELECT * FROM aggregated
```

## 10.5 Dimension Table

```sql
-- models/marts/dim_customers.sql
{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

with_history AS (
    SELECT
        id,
        first_name,
        last_name,
        email,
        customer_created_at,
        is_active,
        ROW_NUMBER() OVER (PARTITION BY id ORDER BY customer_created_at DESC) AS rn
    FROM source
)

SELECT * FROM with_history WHERE rn = 1
```

## 10.6 Schema YML with Tests

```yaml
version: 2

models:
  - name: fct_orders
    description: Order fact table
    columns:
      - name: order_id
        description: Primary key
        tests:
          - unique
          - not_null
      - name: customer_id
        description: Foreign key to customer
        tests:
          - not_null
          - relationships:
              field: id
              to: ref('dim_customers')
      - name: total_revenue
        description: Total order value
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: ">= 0"
```

## 10.7 Macro

```sql
-- macros/nullify_empty.sql
{% macro nullify_empty_columns(columns) %}
    {% for col in columns %}
        NULLIF({{ col }}, '') AS {{ col }}{% if not loop.last %},{% endif %}
    {% endfor %}
{% endmacro %}

-- Usage in model
SELECT 
    {{ nullify_empty_columns(['name', 'email', 'phone']) }}
FROM {{ source('data', 'table') }}
```

## 10.8 Snapshot

```sql
-- snapshots/snp_customers.sql
{% snapshot snap_customers %}

    {{
        config(
            strategy='timestamp',
            unique_key='customer_id',
            updated_at='updated_at'
        )
    }}

    SELECT
        customer_id,
        name,
        email,
        status,
        updated_at
    FROM {{ source('ecom', 'customers') }}

{% endsnapshot %}
```

## 10.9 Seed

```csv
-- seeds/countries.csv
country_code,country_name,region
US,United States,North America
UK,United Kingdom,Europe
DE,Germany,Europe
JP,Japan,Asia
AU,Australia,Oceania
```

```yaml
# dbt_project.yml
seeds:
  my_project:
    countries:
      +column_types:
        country_code: string
```

## 10.10 Package Usage

```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.0
  - package: dbt-labs/dbt_external_packages
    version: 0.2.0
```