# Examples

## 10.1 LookML Complete Model

### models/orders.model.lkml
```lookml
connection: "postgres_warehouse"

include: "/views/*.view.lkml"
include: "/dashboards/*.dashboard.lookml"

explore: orders {
  label: "Order Analytics"
  
  join: customers {
    type: left_outer
    sql_on: ${orders.customer_id} = ${customers.id} ;;
  }
  
  join: order_items {
    type: left_outer
    sql_on: ${orders.id} = ${order_items.order_id} ;;
  }
  
  always_filter: {
    filters: [orders.status: "-Cancelled", orders.created_date: "90 days"]
  }
}
```

### views/orders.view.lkml
```lookml
view: orders {
  sql_table_name: public.orders ;;
  
  dimension: id { primary_key: yes type: number }
  dimension: customer_id { type: number }
  dimension: status { type: string }
  dimension: created_date { type: date }
  dimension: total_amount { type: number sql: ${TABLE}.total_amount ;; }
  
  measure: count { type: count }
  measure: total_revenue { type: sum sql: ${total_amount} ;; value_format_name: usd_0 }
  measure: avg_order_value { type: average sql: ${total_amount} ;; value_format_name: usd }
}
```

## 10.2 Metabase Dashboard with Filters

### Question 1: Daily Revenue Trend
```sql
SELECT DATE(created_at) AS date,
       SUM(amount) AS revenue
FROM orders
WHERE status = 'completed'
  AND created_at >= {{date_filter.start}}
  AND created_at <= {{date_filter.end}}
GROUP BY DATE(created_at)
ORDER BY date
```

### Question 2: Revenue by Category
```sql
SELECT p.category,
       SUM(o.amount) AS revenue,
       COUNT(DISTINCT o.id) AS order_count
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE {% filter date_filter %} AND {% filter category_filter %}
GROUP BY p.category
```

### Dashboard Filter Configuration
```json
{
  "filters": [
    {
      "id": "date_filter",
      "type": "date/range",
      "targets": [{"card_id": 1, "column": "date"}]
    },
    {
      "id": "category_filter", 
      "type": "string/=",
      "targets": [{"card_id": 2, "column": "category"}]
    }
  ]
}
```

## 10.3 Embedded Analytics Integration

### Looker Embed (React)
```jsx
import { LookerEmbedSDK } from '@looker/embed-sdk';

const EmbedDashboard = ({ dashboardId }) => {
  useEffect(() => {
    LookerEmbedSDK.init('https://myinstance.looker.com', '/auth');
    LookerEmbedSDK.createDashboardWithId(dashboardId)
      .withTheme('transparent')
      .withFilters({ status: 'active', region: 'west' })
      .appendTo('#dashboard-container')
      .build()
      .connect();
  }, []);
  
  return <div id="dashboard-container" />;
};
```

### Metabase Embed (Signed JWT)
```python
import jwt
import hashlib
import time

def create_metabase_token(dashboard_id, params, secret):
    payload = {
        "resource": {"dashboard": dashboard_id},
        "params": params,
        "exp": int(time.time()) + 3600  # 1 hour
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

# Frontend
const iframeUrl = `https://metabase.example.com/embed/dashboard/${token}#bordered=false&titled=false`;
```

## 10.4 Advanced LookML Patterns

### Conditional Formatting in LookML
```lookml
dimension: profit_ratio {
  type: number
  sql: ${profit} / NULLIF(${sales}, 0) ;;
  value_format: "0.00%"
  
  html:
    {% if value >= 0.3 %}
      <span style="color: green">{{ rendered_value }}</span>
    {% elsif value >= 0 %}
      <span style="color: orange">{{ rendered_value }}</span>
    {% else %}
      <span style="color: red">{{ rendered_value }}</span>
    {% endif %} ;;
}
```

### User-Specific Filtering
```lookml
dimension: customer_region {
  sql: ${TABLE}.region ;;
  
  user_attribute_filter: {
    user_attribute: region_access
    default: "All"
  }
}
```

## 10.5 Metabase SQL Snippets

### Running Total
```sql
SELECT order_date,
       daily_revenue,
       SUM(daily_revenue) OVER (ORDER BY order_date) AS running_total
FROM (
  SELECT DATE(created_at) AS order_date,
         SUM(amount) AS daily_revenue
  FROM orders
  GROUP BY DATE(created_at)
) t
```

### Percent of Total
```sql
SELECT category,
       revenue,
       revenue * 100.0 / SUM(revenue) OVER () AS pct_of_total
FROM (
  SELECT p.category,
         SUM(oi.sale_price) AS revenue
  FROM order_items oi
  JOIN products p ON oi.product_id = p.id
  GROUP BY p.category
) t
ORDER BY revenue DESC
```

### Period-over-Period Comparison
```sql
WITH current_period AS (
  SELECT DATE_TRUNC('month', created_at) AS month,
         SUM(amount) AS revenue
  FROM orders
  WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
  GROUP BY 1
),
previous_period AS (
  SELECT DATE_TRUNC('month', created_at - INTERVAL '1 month') AS month,
         SUM(amount) AS revenue
  FROM orders
  WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '2 month')
    AND created_at < DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
  GROUP BY 1
)
SELECT c.month, c.revenue, p.revenue AS prev_revenue,
       c.revenue - p.revenue AS change,
       ROUND(100.0 * (c.revenue - p.revenue) / NULLIF(p.revenue, 0), 1) AS pct_change
FROM current_period c
JOIN previous_period p ON c.month = p.month + INTERVAL '1 month'
```
