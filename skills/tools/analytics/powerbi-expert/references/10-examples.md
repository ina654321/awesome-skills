# Examples

## 10.1 Complete Data Model with DAX

### Dimension Tables (Power Query)
```m
// DimCustomer
let
    Source = Sql.Database("server", "dw"),
    dbo_Customer = Source{[Schema="dbo",Item="DimCustomer"]}[Data],
    RenamedColumns = Table.RenameColumns(dbo_Customer,
        {{"CustomerID", "CustomerKey"}, {"CustomerName", "Customer"}),
    RemovedColumns = Table.RemoveColumns(RenamedColumns,{"Phone", "Fax"}),
    ChangedType = Table.TransformColumnTypes(RemovedColumns,
        {{"CustomerKey", Int64.Type}, {"Customer", type text}})
in
    ChangedType
```

### Fact Table with Incremental Refresh
```m
let
    Source = Sql.Database("server", "dw"),
    dbo_FactSales = Source{[Schema="dbo",Item="FactSales"]}[Data],
    FilteredRows = Table.SelectRows(dbo_FactSales, 
        each [OrderDate] > RangeStart and [OrderDate] <= RangeEnd),
    ChangedType = Table.TransformColumnTypes(FilteredRows,
        {{"OrderDate", type date}, {"Quantity", Int64.Type}, {"Amount", type number}})
in
    ChangedType
```

### Date Table DAX
```dax
Date = 
VAR StartDate = DATE(2020,1,1)
VAR EndDate = DATE(2025,12,31)
VAR DateTable =
    CALENDAR(StartDate, EndDate)
RETURN
    ADDCOLUMNS(DateTable,
        "Year", YEAR([Date]),
        "Month", FORMAT([Date], "MMM"),
        "Month Number", MONTH([Date]),
        "Quarter", "Q" & QUARTER([Date]),
        "Year Quarter", YEAR([Date]) & "-Q" & QUARTER([Date]),
        "Day of Week", FORMAT([Date], "ddd"),
        "Is Weekend", IF(WEEKDAY([Date]) IN {1,7}, TRUE, FALSE),
        "Is Today", [Date] = TODAY()
    )
```

## 10.2 Advanced DAX Measures

### Budget vs Actual
```dax
Total Budget := SUM(Budget[BudgetAmount])

Actual :=
SUM(Sales[SalesAmount])

Variance := [Actual] - [Total Budget]

Variance % :=
DIVIDE([Variance], [Total Budget], 0)

Budget Status :=
VAR BudgetPct = [Actual] / [Total Budget]
RETURN
    SWITCH(
        TRUE(),
        BudgetPct >= 1.1, "Over Budget",
        BudgetPct >= 0.9, "On Target",
        "Under Budget"
    )
```

### Customer Segmentation
```dax
Customer Segment :=
VAR TotalRevenue = [Total Sales]
VAR Segment =
    SWITCH(
        TRUE(),
        TotalRevenue >= 100000, "Platinum",
        TotalRevenue >= 50000, "Gold",
        TotalRevenue >= 10000, "Silver",
        "Bronze"
    )
RETURN Segment

New Customers :=
VAR MaxDate = MAX(Sales[OrderDate])
VAR CustomerFirstPurchase =
    ADDCOLUMNS(
        VALUES(Sales[CustomerKey]),
        "FirstPurchase", MINX(RELATEDTABLE(Sales), Sales[OrderDate])
    )
RETURN
    COUNTROWS(
        FILTER(CustomerFirstPurchase, [FirstPurchase] = MaxDate)
    )
```

### Time Intelligence
```dax
MTD Sales :=
VAR MaxDate = MAX('Date'[Date])
VAR StartOfMonth = STARTOFMONTH('Date'[Date])
RETURN
    CALCULATE(
        [Total Sales],
        DATESMTD('Date'[Date]),
        'Date'[Date] <= MaxDate
    )

QTD Sales :=
CALCULATE(
    [Total Sales],
    DATESQTD('Date'[Date])
)

YTD Sales :=
CALCULATE(
    [Total Sales],
    DATESYTD('Date'[Date])
)

Rolling 12 Months :=
CALCULATE(
    [Total Sales],
    DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -12, MONTH)
)
```

## 10.3 Row-Level Security Implementation

### Role Definition
```dax
// Role: SalesRep
[Email] = USERPRINCIPALNAME()

// Role: Manager
VAR ManagerID = LOOKUPVALUE(
    Employees[EmployeeID],
    Employees[Email], USERPRINCIPALNAME()
)
RETURN
[ManagerID] IN VALUES(Employees[ManagerID])

// Role: Department
VAR UserDepartment = LOOKUPVALUE(
    UserDepartments[Department],
    UserDepartments[Email], USERPRINCIPALNAME()
)
RETURN
'Financials'[Department] = UserDepartment
```

### Testing RLS
```dax
// Debug measure to verify user context
Current User := USERPRINCIPALNAME()

User Region := 
CALCULATE(
    VALUES(UserRegion[Region]),
    UserRegion[Email] = USERPRINCIPALNAME()
)

// Row count by role
Visible Rows :=
CALCULATE(
    COUNTROWS(Sales),
    ALLSELECTED()
)
```

## 10.4 Power Query Advanced Patterns

### Combine Multiple CSV Files
```m
let
    Source = Folder.Files("C:\Data\Sales"),
    FilteredRows = Table.SelectRows(Source, 
        each [Extension] = ".csv"),
    AddedCustom = Table.AddColumn(FilteredRows, "Content",
        each Csv.Document([Content], [Delimiter=",", Encoding=65001])),
    ExpandedData = Table.ExpandTableColumn(AddedCustom, "Content",
        {"Column1", "Column2", "Column3"}, {"Date", "Amount", "Category"})
in
    ExpandedData
```

### Parameterized Query
```m
let
    ServerParam = Text.From(Parameters){[Name="Server", Value="."]}[Value],
    DatabaseParam = Text.From(Parameters){[Name="Database", Value="Sales"]}[Value],
    Source = Sql.Database(ServerParam, DatabaseParam),
    QueryResult = Value.NativeQuery(
        Source,
        "SELECT * FROM Sales WHERE Year = @Year",
        [Year = Parameters]{[Name="Year", Value=2024]}[Value]
    )
in
    QueryResult
```

## 10.5 Composite Model with Aggregations

### Table Storage Mode
| Table | Storage Mode | Description |
|-------|-------------|-------------|
| FactSales | DirectQuery | 100M+ rows, live connection |
| DimDate | Import | Date dimension |
| DimCustomer | Import | Customer attributes |
| DimProduct | Import | Product catalog |
| DailySalesAgg | Import | Pre-aggregated daily data |

### Aggregation Table
```m
let
    Source = Sql.Database("server", "dw"),
    Aggregation = Sql.Database("server", "dw"){[Schema="dbo",Item="DailySalesAgg"]}[Data]
in
    Table.TransformColumnTypes(Aggregation,
        {{"Date", type date}, {"Amount", type number}})
```

### GroupByColumn Properties
```json
// In Model.bim
{
  "name": "DailySalesAgg",
  "isAggregation": true,
  "groupByColumns": ["DateKey"],
  "sourceColumnGroupByColumns": ["DateKey"]
}
```

## 10.6 Calculation Groups

### Time Intelligence Calculation Group
```dax
// Create via Tabular Editor or XMLA

// ItemSelection: Time Intelligence
CALCITEM(
    SWITCH(
        SELECTEDMEASURE(),
        [Total Sales], [Total Sales],
        [Total Cost], [Total Cost],
        [Total Margin], [Total Margin]
    ),
    SWITCH(
        VALUES('Time Intelligence'[Index]),
        1, CALCULATE(SELECTEDMEASURE(), DATESYTD('Date'[Date])),
        2, CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date])),
        3, CALCULATE(SELECTEDMEASURE(), PARALLELPERIOD('Date'[Date], -1, YEAR)),
        SELECTEDMEASURE()
    )
)
```
