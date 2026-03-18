# Scenario Examples

## 9.1 Sample Size Determination

**User:** "How many participants do I need for my clinical trial?"

**Expert:**
> **Power Analysis:**
> 
> **Inputs:**
> - Expected effect size: d = 0.5 (medium)
> - Alpha (Type I error): 0.05
> - Power (1 - Type II): 0.80
> - Two-tailed test
> 
> **Calculation:**
> - Using G*Power or R: pwr.t.test()
> - Required sample: n = 64 per group
> - With 20% attrition: n = 80 per group
> 
> **Recommendation:**
> - Total N = 160 (80 treatment, 80 control)
> - Pre-register before data collection
