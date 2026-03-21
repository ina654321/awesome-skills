# Logistics Algorithm Engineer — Scenarios & Anti-Patterns

This file contains detailed scenarios and anti-patterns referenced from SKILL.md §9 and §10.

---

## Scenario A: Last-Mile VRPTW — 500 Stops

**User:** "I have 500 delivery stops, 20 vans, 500kg capacity, 2-hour windows. How do I solve this efficiently?"

**Logistics Algorithm Engineer:**
> **Architecture**: OR-Tools with Guided Local Search (GLS) — achieves <5% gap in 60-120s
>
> **Step 1 — Build time matrix (OSRM):**
> ```python
> import requests, numpy as np
>
> def build_osrm_time_matrix(coordinates):
>     coords_str = ";".join(f"{lon},{lat}" for lon, lat in coordinates)
>     url = f"http://router.project-osrm.org/table/v1/driving/{coords_str}"
>     response = requests.get(url, params={"annotations": "duration"}).json()
>     matrix = np.array(response["durations"])
>     return np.round(matrix).astype(int)
> ```
>
> **Step 2 — Zone pre-clustering:**
> ```python
> from sklearn.cluster import KMeans
>
> def zone_cluster(customer_df, n_zones=20):
>     kmeans = KMeans(n_clusters=n_zones, random_state=42, n_init=10)
>     customer_df['zone'] = kmeans.fit_predict(customer_df[['lat', 'lon']].values)
>     return customer_df
> ```
>
> **Expected ROI**: 15-25% distance reduction, 1-3 fewer vehicles, 88%→95% on-time rate

---

## Scenario B: Warehouse Slotting — ABC Analysis + QAP

**User:** "Our warehouse pickers walk 12km per shift. How do I reduce this?"

**Logistics Algorithm Engineer:**
> **ABC Velocity Analysis:**
> ```python
> def abc_velocity_analysis(order_lines_df, cutoffs=(0.70, 0.90)):
>     freq = order_lines_df['sku_id'].value_counts().reset_index()
>     freq.columns = ['sku_id', 'pick_count']
>     freq['cum_pct'] = freq['pick_count'].cumsum() / freq['pick_count'].sum()
>
>     def classify(cum_pct):
>         if cum_pct <= cutoffs[0]: return 'A'
>         elif cum_pct <= cutoffs[1]: return 'B'
>         return 'C'
>
>     freq['abc_class'] = freq['cum_pct'].apply(classify)
>     return freq
> ```
>
> **Expected improvement**: 25-42% reduction in picker travel distance

---

## Scenario C: Multi-Depot Network Design Under Uncertainty

**User:** "50 candidate locations, select 5-8 to serve 200 zones with ±30% demand uncertainty"

**Logistics Algorithm Engineer:**
> **MILP Formulation:**
> ```
> min Σᵢ(fᵢ × yᵢ) + (1/|S|) × Σₛ Σᵢ Σⱼ(cᵢⱼ × xᵢⱼₛ × dⱼₛ)
>
> s.t. Σᵢ xᵢⱼₛ = 1           ∀ j,s  (demand satisfaction)
>     xᵢⱼₛ ≤ yᵢ              ∀ i,j,s (linking)
>     Σⱼ xᵢⱼₛ × dⱼₛ ≤ capᵢ × yᵢ  ∀ i,s (capacity)
> ```
>
> **Solution:**
> ```python
> import pulp
>
> prob = pulp.LpProblem("Stochastic_FLP", pulp.LpMinimize)
> y = {i: pulp.LpVariable(f"y_{i}", cat='Binary') for i in facilities}
> # ... (see full code in original)
> solver = pulp.HiGHS_CMD(msg=True, timeLimit=600)
> prob.solve(solver)
> ```

---

## Anti-Patterns (from §10)

| Severity | Anti-Pattern | Risk |
|----------|--------------|------|
| 🔴 High | **Over-optimizing on Historical Data** | 18% backtest → 8% production |
| 🔴 High | **Exact Solver on 1000+ Nodes** | 6h timeout, no solution |
| 🔴 High | **Ignoring Soft Constraints** | Zero operational adoption |
| 🔴 High | **No Sensitivity Analysis** | Wrong decision on uncertain inputs |
