# Examples

## 10.1 Data Cleaning Pipeline

```python
import pandas as pd
import numpy as np

def clean_sales_data(df):
    # 1. Remove duplicates
    df = df.drop_duplicates()
    
    # 2. Handle missing values
    df['revenue'] = df['revenue'].fillna(0)
    df['discount'] = df['discount'].fillna(df['discount'].median())
    df['customer_id'] = df['customer_id'].dropna()
    
    # 3. Fix types
    df['date'] = pd.to_datetime(df['date'])
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1)
    
    # 4. Remove outliers (IQR method)
    Q1 = df[['revenue', 'quantity']].quantile(0.25)
    Q3 = df[['revenue', 'quantity']].quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df[['revenue', 'quantity']] < (Q1 - 1.5 * IQR)) | 
              (df[['revenue', 'quantity']] > (Q3 + 1.5 * IQR))).any(axis=1)]
    
    # 5. Standardize text
    df['status'] = df['status'].str.strip().str.lower()
    df['category'] = df['category'].str.replace(r'\s+', ' ', regex=True)
    
    return df

df = pd.read_csv('sales.csv')
df_clean = clean_sales_data(df)
```

## 10.2 Complex Aggregation with Named Aggregations

```python
# Multi-level grouping with named outputs
sales_summary = df.groupby(['region', 'category', 'quarter']).agg(
    total_revenue=('revenue', 'sum'),
    avg_order_value=('order_value', 'mean'),
    transaction_count=('order_id', 'count'),
    unique_customers=('customer_id', 'nunique'),
    max_discount=('discount', 'max'),
    median_lead_time=('lead_time', 'median')
).round(2)

# Percentage of total within group
sales_summary['revenue_pct'] = sales_summary.groupby('region')['total_revenue'].transform(
    lambda x: x / x.sum() * 100
).round(2)
```

## 10.3 Time Series Analysis

```python
# Daily revenue with rolling statistics
daily = df.set_index('date').resample('D').agg({
    'revenue': 'sum',
    'orders': 'count'
}).reset_index()

# 7 and 30 day moving averages
daily['ma_7'] = daily['revenue'].rolling(7).mean()
daily['ma_30'] = daily['revenue'].rolling(30).mean()

# Year-over-year comparison
daily['revenue_ytd'] = daily.groupby(daily['date'].dt.year)['revenue'].cumsum()
daily['prev_year_revenue'] = daily['revenue'].shift(365)
daily['yoy_growth'] = (daily['revenue'] - daily['prev_year_revenue']) / daily['prev_year_revenue']

# Period-over-period
daily['prev_day'] = daily['revenue'].shift(1)
daily['prev_week'] = daily['revenue'].shift(7)
daily['wow_change'] = daily['revenue'] - daily['prev_week']
```

## 10.4 Advanced Merge Patterns

```python
# SCD Type 2: Historical tracking
def merge_scd_type2(current, history, key_cols=['customer_id']):
    # Find new/changed records
    merged = current.merge(history, on=key_cols, how='left', indicator=True)
    
    # Expire old records
    expired = merged[merged['_merge'] == 'both'].copy()
    expired['is_current'] = False
    
    # Add new records
    new_records = merged[merged['_merge'] == 'left_only'][key_cols + current.columns.difference(history.columns)]
    new_records['is_current'] = True
    
    return pd.concat([expired, new_records], ignore_index=True)

# Many-to-many merge with deduplication
order_products = orders.merge(
    order_items.groupby('order_id')['product_id'].apply(list).reset_index(),
    on='order_id'
)
```

## 10.5 Pivot and Unpivot

```python
# Wide to long (unpivot)
monthly_data = pd.read_csv('monthly_sales.csv')  # cols: region, jan, feb, mar, ...
long_data = monthly_data.melt(
    id_vars=['region', 'product'],
    value_vars=['jan', 'feb', 'mar', 'apr', 'may', 'jun'],
    var_name='month',
    value_name='sales'
)

# Long to wide (pivot)
summary = long_data.pivot_table(
    index=['region', 'product'],
    columns='month',
    values='sales',
    aggfunc='sum',
    fill_value=0
).reset_index()

# Multi-level unpivot
df.pipe(lambda d: d.set_index(['id', 'date'])
          .stack()
          .reset_index()
          .rename(columns={'level_2': 'metric', 0: 'value'}))
```

## 10.6 Efficient Chunked Processing

```python
import pandas as pd

def process_large_csv(input_file, output_file, chunk_size=50000):
    results = []
    
    for i, chunk in enumerate(pd.read_csv(input_file, chunksize=chunk_size)):
        # Process each chunk
        chunk['processed'] = chunk['value'] * 1.1
        chunk['category_group'] = chunk['category'].astype('category').cat.codes
        
        # Aggregate if needed
        agg = chunk.groupby('group').agg({
            'value': 'sum',
            'quantity': 'mean'
        }).assign(chunk_id=i)
        
        results.append(agg)
        
        # Progress indicator
        print(f"Processed chunk {i+1}: {len(chunk)} rows")
    
    # Combine results
    final = pd.concat(results, ignore_index=True)
    final.to_parquet(output_file, index=False)
    return final
```

## 10.7 Conditional Logic with NumPy

```python
# Vectorized if-else (faster than apply)
conditions = [
    df['score'] >= 90,
    df['score'] >= 70,
    df['score'] >= 50
]
choices = ['A', 'B', 'C']
df['grade'] = np.select(conditions, choices, default='F')

# Bin continuous variable
df['age_group'] = pd.cut(
    df['age'],
    bins=[0, 18, 35, 55, 100],
    labels=['0-17', '18-34', '35-54', '55+']
)

# Normalize within groups
df['normalized'] = df.groupby('category')['value'].transform(
    lambda x: (x - x.mean()) / x.std()
)
```
