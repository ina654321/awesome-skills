# Standards & Reference

## 7.1 Data Quality Framework

### Data Quality Dimensions
| Dimension | Definition | Measurement |
|-----------|-----------|-------------|
| Completeness | No missing values | % complete |
| Accuracy | Correct values | Error rate |
| Consistency | Uniform format | Validation pass rate |
| Timeliness | Current data | Time since update |
| Uniqueness | No duplicates | Duplicate count |

### Data Validation Rules
- Range checks (numerical bounds)
- Pattern matching (regex)
- Cross-field validation
- Referential integrity
- Uniqueness constraints

## 7.2 Statistical Methods

| Method | Use Case | Key Assumptions |
|--------|----------|----------------|
| t-test | Compare 2 means | Normal, independent |
| ANOVA | Compare 3+ means | Normal, equal variance |
| Chi-square | Categorical association | Expected counts > 5 |
| Regression | Prediction, relationships | Linearity, independence |
| Bootstrap | Robust inference | Large samples |

## 7.3 Data Visualization

| Chart Type | Use Case |
|------------|----------|
| Bar chart | Categorical comparisons |
| Line chart | Trends over time |
| Scatter plot | Relationships |
| Histogram | Distribution |
| Box plot | Distribution comparison |
