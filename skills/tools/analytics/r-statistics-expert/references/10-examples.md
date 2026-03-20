# Examples

## 10.1 Complete Data Analysis Pipeline

```r
library(tidyverse)
library(lubridate)

# Import and clean
df <- read_csv("sales.csv") %>%
  mutate(
    date = mdy(date),
    category = fct_infreq(category)
  ) %>%
  filter(date >= "2024-01-01", status == "completed")

# Exploratory analysis
df %>%
  group_by(category) %>%
  summarize(
    n = n(),
    total = sum(amount),
    mean = mean(amount),
    median = median(amount),
    sd = sd(amount)
  ) %>%
  arrange(desc(total))

# Visualization
df %>%
  ggplot(aes(x = date, y = amount, color = category)) +
  geom_line(stat = "summary", fun = "sum") +
  facet_wrap(~category, scales = "free_y") +
  theme_minimal()
```

## 10.2 Complex Aggregations

```r
# Multi-level grouping with nested summary
sales_summary <- df %>%
  group_by(region, category, quarter = quarter(date)) %>%
  summarize(
    revenue = sum(amount),
    orders = n_distinct(order_id),
    customers = n_distinct(customer_id),
    aov = revenue / orders,
    .groups = "drop"
  ) %>%
  group_by(region) %>%
  mutate(
    region_share = revenue / sum(revenue),
    regional_rank = rank(desc(revenue))
  ) %>%
  ungroup()

# Conditional aggregation
df %>%
  group_by(category) %>%
  summarize(
    total = sum(amount),
    returns = sum(amount[status == "returned"]),
    return_rate = returns / total
  )
```

## 10.3 Time Series Analysis

```r
library(zoo)
library(forecast)

# Daily time series
ts_data <- df %>%
  complete(date = seq.Date(min(date), max(date), by = "day")) %>%
  mutate(revenue = coalesce(revenue, 0)) %>%
  arrange(date) %>%
  with_tsibble(index = date) %>%
  fill_gaps(.full = TRUE) %>%
  fill(revenue, .direction = "down")

# Rolling statistics
ts_data %>%
  mutate(
    ma_7 = rollmean(revenue, 7, fill = NA),
    ma_30 = rollmean(revenue, 30, fill = NA),
    yoy = revenue / lag(revenue, 365) - 1
  )

# Seasonal decomposition
ts_monthly <- ts_data %>%
  index_by(yearmonth) %>%
  summarize(revenue = sum(revenue)) %>%
  with_tsibble(index = yearmonth)

ts_monthly %>%
  model(STL(revenue ~ season())) %>%
  components() %>%
  autoplot()
```

## 10.4 Statistical Modeling

```r
library(broom)
library(modelr)

# Multiple regression with broom
model <- df %>%
  nest(data = -category) %>%
  mutate(
    fit = map(data, ~lm(revenue ~ age + tenure, data = .)),
    tidied = map(fit, tidy),
    glanced = map(fit, glance)
  )

# Extract coefficients
model %>%
  unnest(tidied) %>%
  filter(term != "(Intercept)") %>%
  select(category, term, estimate, p.value)

# Model quality
model %>%
  unnest(glanced) %>%
  select(category, r.squared, adj.r.squared, AIC)

# Predictions with confidence intervals
df %>%
  add_predictions(model, var = "pred") %>%
  add_residuals(model, var = "resid") %>%
  ggplot(aes(x = pred, y = resid)) +
  geom_point() +
  geom_hline(yintercept = 0)
```

## 10.5 Custom Functions

```r
# Function for repeated analysis
analyze_group <- function(df, group_var, outcome_var) {
  group_expr <- enquo(group_var)
  outcome_expr <- enquo(outcome_var)
  
  df %>%
    group_by(!!group_expr) %>%
    summarize(
      n = n(),
      mean = mean(!!outcome_expr, na.rm = TRUE),
      median = median(!!outcome_expr, na.rm = TRUE),
      sd = sd(!!outcome_expr, na.rm = TRUE),
      se = sd / sqrt(n)
    ) %>%
    mutate(
      ci_lower = mean - 1.96 * se,
      ci_upper = mean + 1.96 * se
    )
}

# Usage
analyze_group(df, category, revenue)
analyze_group(df, region, quantity)
```

## 10.6 Data Visualization Gallery

```r
library(patchwork)  # Combine plots

# Distribution
p1 <- df %>%
  ggplot(aes(x = revenue, fill = category)) +
  geom_histogram(bins = 30, alpha = 0.7) +
  facet_wrap(~category, scales = "free_y")

# Box plot
p2 <- df %>%
  ggplot(aes(x = category, y = revenue, fill = category)) +
  geom_boxplot() +
  coord_flip()

# Violin plot
p3 <- df %>%
  ggplot(aes(x = category, y = revenue)) +
  geom_violin() +
  stat_summary(fun = "median", geom = "point")

# Correlation heatmap
df %>%
  select_if(is.numeric) %>%
  cor() %>%
  as_tibble(rownames = "var1") %>%
  pivot_longer(-var1, names_to = "var2", values_to = "corr") %>%
  ggplot(aes(x = var1, y = var2, fill = corr)) +
  geom_tile() +
  scale_fill_gradient2()

# Combine with patchwork
(p1 + p2) / p3
```

## 10.7 Functional Programming with purrr

```r
library(purrr)

# Map over list
list_of_dfs <- map(c("train.csv", "test.csv"), read_csv)

# Map with index
map2(list_dfs, names(list_dfs), ~mutate(.x, source = .y))

# Safely handle errors
safe_read <- safely(read_csv, otherwise = tibble(error = TRUE))
map(c("good.csv", "bad.csv"), safe_read)

# Reduce to single output
list_dfs %>%
  reduce(full_join, by = c("id", "date", "amount"))

# Nested tibble iteration
df %>%
  group_by(category) %>%
  nest() %>%
  mutate(
    model = map(data, ~lm(revenue ~ date, data = .)),
    quality = map_dbl(model, ~glance(.)$r.squared)
  )
```

## 10.8 Database Operations

```r
library(DBI)
library(dbplyr)

con <- dbConnect(
  RPostgres::Postgres(),
  dbname = "analytics",
  host = "db.example.com",
  user = Sys.getenv("DB_USER"),
  password = Sys.getenv("DB_PASS")
)

# Use dplyr syntax with remote table
sales <- tbl(con, "sales")
recent_sales <- sales %>%
  filter(date >= "2024-01-01") %>%
  group_by(category) %>%
  summarize(total = sum(amount)) %>%
  arrange(desc(total)) %>%
  collect()  # Bring to R

# Generate SQL
sales %>%
  filter(status == "active") %>%
  mutate(revenue = amount * 0.8) %>%
  show_query()

dbDisconnect(con)
```
