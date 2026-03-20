# Examples

## 10.1 Advanced Calculated Fields

### Running Calculations
```tableau
// Running Sum (Table Down)
RUNNING_SUM(SUM([Sales]))

// Running Average (Table Across)
RUNNING_AVG(SUM([Sales]))

// Percent of Total
SUM([Sales]) / TOTAL(SUM([Sales]))

// Percent of Row Total
SUM([Sales]) / TOTAL(SUM([Sales]))

// Rank within Group
RANK(SUM([Sales]), 'desc')  -- Simple rank
RANK_UNIQUE(SUM([Sales]), 'asc')  -- Unique rank

// Index (row number)
INDEX()
```

### Date Calculations
```tableau
// Days Since Last Order
DATEDIFF('day', { FIXED [Customer ID] : MAX([Order Date]) }, TODAY())

// Order Month Number (fiscal year starting July)
(DATEDIFF('month', MAKEDATE(2000,7,1), [Order Date]) % 12) + 1

// Week Over Week Growth
(ZN(SUM([Sales])) - LOOKUP(SUM([Sales]), -1)) / ABS(LOOKUP(SUM([Sales]), -1))

// Same Period Last Year
DATEADD('year', -1, [Order Date])

// Fiscal Quarter
"Q" + STR(INT((MONTH([Date]) - 7) / 3) + 1)
```

### String Manipulation
```tableau
// Extract Domain from Email
REGEXP_EXTRACT([Email], '@(.+)', 1)

// Clean and Format
TRIM(LOWER(REPLACE([Name], ' ', '')))

// Conditional based on text
IF CONTAINS([Product], 'Pro') THEN 'Premium'
ELSEIF CONTAINS([Product], 'Basic') THEN 'Standard'
ELSE 'Other'
END

// Parse Number from String
FLOAT(REGEXP_EXTRACT([Revenue], '(\$[\d,.]+)'))

// First and Last Name
TRIM(LEFT([Name], FIND([Name], ' ') - 1))  -- First
TRIM(RIGHT([Name], LEN([Name]) - FIND([Name], ' ')))  -- Last
```

## 10.2 LOD Expression Patterns

### Customer Analysis
```tableau
// Count of Orders per Customer
{ FIXED [Customer ID] : COUNT([Order ID]) }

// Customer Lifetime Value
{ FIXED [Customer ID] : SUM([Sales]) }

// First Purchase Date
{ FIXED [Customer ID] : MIN([Order Date]) }

// Customer Cohort (first purchase month)
DATE(DATETRUNC('month', { FIXED [Customer ID] : MIN([Order Date]) }))

// Customer Retention - purchases in current vs prior period
SUM({ FIXED [Customer ID] : 
    MAX(IF [Period] = 'Current' THEN 1 ELSE 0 END) *
    MAX(IF [Period] = 'Prior' THEN 1 ELSE 0 END)
})
```

### Cohort Analysis
```tableau
// Cohort Period Number
DATEDIFF('month', [Cohort Month], DATETRUNC('month', [Order Date])) + 1

// Cohort Retention Rate
{ FIXED [Cohort Month], [Cohort Period] : 
    COUNTD([Customer ID]) } 
/ 
{ FIXED [Cohort Month] : COUNTD([Customer ID]) }
```

### Reference Lines with LOD
```tableau
// Average per Customer
{ FIXED : SUM([Sales]) / COUNTD([Customer ID]) }

// Percentage of Regional Sales
SUM([Sales]) / SUM({ FIXED [Region] : SUM([Sales]) })

// Top 10% Threshold
{ FIXED : PERCENTILE(SUM([Sales]), 0.9) }
```

### Nested LOD
```tableau
// Average Order Value per Customer
{ FIXED [Customer ID] : AVG({ FIXED [Customer ID], [Order ID] : SUM([Sales]) }) }

// Median Customer Value
{ FIXED : MEDIAN({ FIXED [Customer ID] : SUM([Sales]) }) }
```

## 10.3 Table Calculations

### Moving Average
```tableau
// 7-day Moving Average
WINDOW_AVG(SUM([Sales]), -6, 0)

// 12-Month Rolling Total
WINDOW_SUM(SUM([Sales]), -11, 0)

// Centered Moving Average
WINDOW_AVG(SUM([Sales]), -2, 2)
```

### Difference Calculations
```tableau
// Period Over Period
SUM([Sales]) - LOOKUP(SUM([Sales]), -1)

// Period Over Period Percent
(ZN(SUM([Sales])) - LOOKUP(SUM([Sales]), -1)) / ABS(LOOKUP(SUM([Sales]), -1))

// Moving Difference
SUM([Sales]) - LOOKUP(SUM([Sales]), -7)  -- 7 periods ago
```

### Z-Score Normalization
```tableau
// Z-Score
(SUM([Sales]) - WINDOW_AVG(SUM([Sales]))) / WINDOW_STDEV(SUM([Sales]))

// Percentile
PERCENTILE(SUM([Sales]), 0.75)  -- 75th percentile
```

## 10.4 Parameters and Dynamic Controls

### Parameter for Measure Selection
```tableau
// Create parameter: [Select Measure] with values: Sales, Profit, Quantity

// Calculation:
CASE [Select Measure]
    WHEN 'Sales' THEN SUM([Sales])
    WHEN 'Profit' THEN SUM([Profit])
    WHEN 'Quantity' THEN SUM([Quantity])
END
```

### Dynamic Top N
```tableau
// Create parameter: [Top N] (integer, default 10)
// Create parameter: [Dimension to Show] (list of dimensions)

{ INCLUDE [Dimension to Show] : 
    RANK(SUM({ INCLUDE : 
        CASE [Dimension to Show]
            WHEN 'Category' THEN [Category]
            WHEN 'Segment' THEN [Segment]
        END
    : SUM([Sales])})) <= [Top N]
}
```

### Dynamic Date Range
```tableau
// Parameters: [Date Range] (List: MTD, QTD, YTD, Last 30 Days, Custom)
// Parameter: [Custom End Date]

CASE [Date Range]
    WHEN 'MTD' THEN [Order Date] >= DATETRUNC('month', TODAY())
    WHEN 'QTD' THEN [Order Date] >= DATETRUNC('quarter', TODAY())
    WHEN 'YTD' THEN [Order Date] >= DATETRUNC('year', TODAY())
    WHEN 'Last 30 Days' THEN [Order Date] >= DATEADD('day', -30, TODAY())
    WHEN 'Custom' THEN [Order Date] <= [Custom End Date]
END
```

## 10.5 Set Actions

### Highlight on Selection
```tableau
// Create set: [Selected Customers]
// Dashboard > Actions > Set Action
// Source: Customer List
// Target: [Selected Customers]
// Aggregation: Use all values

// Visualization with highlight:
IF [Customer ID] IN [Selected Customers] THEN 'Selected'
ELSE 'Other'
END
```

### Dynamic Dimension Filter
```tableau
// Parameters for filter control
// Set for available values

// Calculation in filter:
{ FIXED : COUNTD([Category]) } = [Select N Categories]
```

## 10.6 Row-Level Security

### User-based Filtering
```tableau
// Create calculated field for security
// User filtering is typically done at data source or server level

// For live connections: use IS_MEMBER
IS_MEMBER('Sales Team')

// For published datasource: use USERNAME
USERNAME() = [Manager Name]
```

## 10.7 Dashboard Layout Examples

### Dynamic YTD vs LY Comparison
```tableau
// Create parameter: [Comparison Period]
// Values: YTD, QTD, MTD, Last 12 Months

// Current Period
CASE [Comparison Period]
    WHEN 'YTD' THEN [Order Date] >= DATETRUNC('year', TODAY())
    WHEN 'QTD' THEN [Order Date] >= DATETRUNC('quarter', TODAY())
    WHEN 'MTD' THEN [Order Date] >= DATETRUNC('month', TODAY())
    WHEN 'Last 12 Months' THEN [Order Date] >= DATEADD('year', -1, TODAY())
END

// Prior Period
DATEADD('year', -1, [Order Date])
```

### RFM Analysis (Recency, Frequency, Monetary)
```tableau
// Recency (days since last purchase)
DATEDIFF('day', { FIXED [Customer ID] : MAX([Order Date]) }, TODAY())

// Frequency (number of orders)
{ FIXED [Customer ID] : COUNTD([Order ID]) }

// Monetary (average order value)
{ FIXED [Customer ID] : AVG({ FIXED [Customer ID], [Order ID] : SUM([Sales]) }) }

// RFM Score
[Recency Score] + [Frequency Score] + [Monetary Score]

// Create bins for each
IF [Recency] <= 30 THEN 4
ELSEIF [Recency] <= 60 THEN 3
ELSEIF [Recency] <= 90 THEN 2
ELSE 1
END
```

## 10.8 SQL Optimization (Custom SQL)

```tableau
-- Use custom SQL to pre-aggregate in database

SELECT 
    DATE_TRUNC('month', "Order Date") AS "Order Month",
    "Category",
    "Region",
    SUM("Sales") AS "Total Sales",
    COUNT(DISTINCT "Customer ID") AS "Customer Count"
FROM "Orders"
WHERE "Order Date" >= DATE '2023-01-01'
GROUP BY 1, 2, 3
```
