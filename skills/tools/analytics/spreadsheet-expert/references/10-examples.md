# Examples

## 10.1 Advanced Lookup Patterns

### XLOOKUP with Multiple Criteria
```excel
=XLOOKUP(1, (A:A=A2)*(B:B=B2), C:C, "Not Found")

=XLOOKUP(A2&B2, Products[Category]&Products[SKU], Products[Price])
```

### INDEX/MATCH with Multiple Criteria
```excel
=INDEX(C:C, MATCH(1, (A:A=F2)*(B:B=G2), 0))

-- Array formula in older Excel (Ctrl+Shift+Enter)
{=INDEX(C2:C100, MATCH(1, (A2:A100=F2)*(B2:B100=G2), 0))}
```

### Fuzzy Lookup (Google Sheets)
```excel
=INDEX(B:B, MATCH(MAX(ArrayFormula(SIMILARITY(A2, A:A))), ArrayFormula(SIMILARITY(A2, A:A)), 0))
```

## 10.2 Dynamic Arrays (Excel 365/Sheets)

### Unique Values with Aggregation
```excel
=SUM(UNIQUE(FILTER(B:B, A:A=E2)))

=DROP(REDUCE(0, UNIQUE(A:A), LAMBDA(a,b, VSTACK(a, SUMIF(A:A,b,B:B)))), 1)
```

### Ranking Within Groups
```excel
=SUMPRODUCT((A:A=A2)*(B:B>B2))+1

-- Dynamic version
=SUMPRODUCT((A$2:A$100=A2)*(B$2:B$100>B2))+1
```

### Cross-reference Two Lists
```excel
=FILTER(A:A, COUNTIF(B:B, A:A))
=FILTER(B:B, COUNTIF(A:A, B:B)=0)
```

## 10.3 Financial Modeling

### NPV with Variable Discount Rate
```excel
=NPV(rate, cashflow1, cashflow2, ...)

=NPV(B1, -B2, B3/(1+B1)^2, B4/(1+B1)^3)
```

### IRR with Guessed Rate
```excel
=IRR(cashflows, guess)
=IRR({-1000, 300, 400, 500, 200}, 0.1)
```

### Loan Amortization Schedule
```excel
-- Monthly Payment
=PMT(rate/12, years*12, -principal)

-- Interest portion
=IPMT(rate/12, period, years*12, -principal)

-- Principal portion
=PPMT(rate/12, period, years*12, -principal)

-- Running balance
=principal + CUMPRINC(rate/12, years*12, -principal, 1, period, 0)
```

### EBITDA Calculation
```excel
=Revenue - COGS  -- Gross Profit
=Gross Profit - Operating Expenses  -- EBIT
=EBIT + Depreciation + Amortization  -- EBITDA
```

## 10.4 Date Calculations

### Fiscal Year Calculations
```excel
=FY = IF(MONTH(A2)<=6, YEAR(A2), YEAR(A2)+1)

=FiscalQuarter = "Q"&CEILING(MONTH(A2)/3, 1)

=FiscalYear = YEAR(A2) - IF(MONTH(A2)<7, 1, 0)  -- Jul-Jun FY
```

### Business Days Calculations
```excel
=WORKDAY(start_date, days, [holidays])

=NETWORKDAYS(start_date, end_date, [holidays])

=NETWORKDAYS.INTL(start_date, days, weekend, [holidays])
```

### Age and Tenure
```excel
=DATEDIF(birth_date, TODAY(), "Y")  -- Full years

=DATEDIF(start_date, TODAY(), "Y")&" years, "&DATEDIF(start_date, TODAY(), "YM")&" months"
```

## 10.5 Statistical Analysis

### Descriptive Statistics
```excel
=MEAN(A:A)      -- Average
=MEDIAN(A:A)    -- Middle value
=STDEV(A:A)     -- Standard deviation
=SKEW(A:A)      -- Skewness
=KURT(A:A)      -- Kurtosis

=QUARTILE(A:A, 1)  -- Q1
=QUARTILE(A:A, 3)  -- Q3
=PERCENTILE(A:A, 0.95)  -- 95th percentile
```

### Regression Analysis
```excel
=SLOPE(Y_range, X_range)    -- Beta/gradient
=INTERCEPT(Y_range, X_range)  -- Alpha
=CORREL(X_range, Y_range)   -- Correlation coefficient
=RSQ(X_range, Y_range)      -- R-squared
=STEYX(Y_range, X_range)   -- Standard error
```

### Normal Distribution
```excel
=NORM.DIST(x, mean, stdev, TRUE)     -- CDF
=NORM.INV(probability, mean, stdev) -- Inverse CDF
=Z.SCORE = (x - MEAN(range)) / STDEV(range)
```

## 10.6 Text Manipulation

### Extract Patterns
```excel
=LEFT(A2, FIND(" ", A2)-1)           -- First word
=RIGHT(A2, LEN(A2)-FIND(" ", A2))    -- After first space
=MID(A2, FIND("@", A2)+1, 100)       -- Domain from email

=REGEXEXTRACT(A2, "(\d{3})-(\d{3})-(\d{4})")  -- Extract phone
=REGEXEXTRACT(A2, "@(.+)")                     -- Extract domain
```

### Clean and Transform
```excel
=TRIM(A2)                    -- Remove extra spaces
=CLEAN(A2)                   -- Remove non-printable
=UPPER/LOWER/PROPER(A2)     -- Change case
=SUBSTITUTE(A2, "old", "new", n)  -- Replace nth occurrence

=CONCATENATE(A2, " ", B2)    -- Join with delimiter
=TEXTJOIN(", ", TRUE, A:A)   -- Join with filter
```

## 10.7 Google Sheets: Advanced QUERY

### Complex Filtering
```excel
=QUERY(A:D, 
  "SELECT A, SUM(B), AVG(C) 
   WHERE A IS NOT NULL 
   AND B > 1000 
   AND C > DATE '2024-01-01'
   GROUP BY A 
   ORDER BY SUM(B) DESC 
   LIMIT 20
   LABEL SUM(B) 'Total Sales', AVG(C) 'Avg Rate'")
```

### Pivot with QUERY
```excel
=QUERY(A:C, 
  "SELECT A, SUM(B) 
   WHERE A IS NOT NULL 
   GROUP BY A 
   PIVOT C")
```

### Subqueries
```excel
=QUERY({A:A, IF(B:B>1000, "High", "Low")},
  "SELECT Col1, COUNT(Col1) 
   GROUP BY Col1 
   LABEL COUNT(Col1) 'Count'")
```

## 10.8 VBA/Apps Script Automation

### Excel VBA: Loop Through Rows
```vba
Sub ProcessRows()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Data")
    
    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    
    Dim i As Long
    For i = 2 To lastRow
        If ws.Cells(i, "B").Value > 1000 Then
            ws.Cells(i, "C").Value = "High"
        Else
            ws.Cells(i, "C").Value = "Low"
        End If
    Next i
End Sub
```

### Google Apps Script: On Edit Trigger
```javascript
function onEdit(e) {
  const sheet = e.source.getActiveSheet();
  const range = e.range;
  
  // Auto-timestamp on column B edit
  if (range.getColumn() === 2 && range.getValue()) {
    sheet.getRange(range.getRow(), 3).setValue(new Date());
  }
  
  // Uppercase in column A
  if (range.getColumn() === 1) {
    range.setValue(range.getValue().toUpperCase());
  }
}
```

### Apps Script: Custom Function
```javascript
/**
 * Calculate weighted average
 * @param {range} values The values
 * @param {range} weights The weights
 * @return {number} Weighted average
 */
function WEIGHTED_AVERAGE(values, weights) {
  const sum = values.reduce((acc, val, i) => acc + val * weights[i], 0);
  const totalWeight = weights.reduce((acc, w) => acc + w, 0);
  return sum / totalWeight;
}
```
