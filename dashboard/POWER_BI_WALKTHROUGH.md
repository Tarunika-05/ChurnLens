# Power BI Dashboard — Step-by-Step (30 minutes)

Use **one file** for the fastest setup: `dashboard/dashboard_data.csv`  
(Includes all customers + churn scores. Generate with `py scripts/score_all_customers.py`.)

Also import `reports/feature_importance.csv` for Page 4.

---

## Step 1: Import data

1. Open **Power BI Desktop**
2. **Home → Get data → Text/CSV**
3. Select `dashboard/dashboard_data.csv`
4. Click **Transform Data** and confirm:
   - `churn_flag` is True/False
   - `churn_probability` is decimal
   - `risk_tier` is text
5. **Close & Apply**
6. Repeat for `reports/feature_importance.csv` (name table `FeatureImportance`)

---

## Step 2: Create measures

**Modeling → New measure** and paste from `dashboard/power_bi_measures.dax`, or create:

```dax
Total Customers = DISTINCTCOUNT(dashboard_data[customerID])

Churn Rate =
DIVIDE(
    CALCULATE(COUNTROWS(dashboard_data), dashboard_data[churn_flag] = TRUE()),
    COUNTROWS(dashboard_data)
)

Monthly Revenue =
SUMX(
    FILTER(dashboard_data, dashboard_data[churn_flag] = FALSE()),
    dashboard_data[MonthlyCharges]
)

Revenue Lost =
SUMX(
    FILTER(dashboard_data, dashboard_data[churn_flag] = TRUE()),
    dashboard_data[MonthlyCharges]
)

Avg CLV = AVERAGE(dashboard_data[estimated_clv])

High Risk Customers =
CALCULATE(
    COUNTROWS(dashboard_data),
    dashboard_data[risk_tier] = "High"
)
```

Format **Churn Rate** as percentage.

---

## Step 3: Page 1 — Executive Overview

| Visual | Field |
|--------|-------|
| Card | `Total Customers` |
| Card | `Churn Rate` |
| Card | `Monthly Revenue` |
| Card | `Revenue Lost` |
| Slicer | `Contract` |
| Slicer | `InternetService` |
| Slicer | `spending_category` |
| Donut | Legend: `Churn`, Values: count of `customerID` |

**Theme:** churn red `#E94F37`, retained teal `#2E86AB`

---

## Step 4: Page 2 — Churn Analysis

| Visual | Setup |
|--------|--------|
| Clustered bar | Axis: `Contract`, Values: `Churn Rate` (measure) |
| Stacked column | Axis: `tenure_bucket`, Values: count `customerID`, Legend: `Churn` |
| Donut | Legend: `PaymentMethod`, Values: count where `churn_flag` = true |
| Matrix | Rows: `InternetService`, Values: `Churn Rate`, count `customerID` |

---

## Step 5: Page 3 — Revenue Insights

| Visual | Setup |
|--------|--------|
| Bar chart | Axis: `spending_category`, Values: sum `MonthlyCharges` |
| Clustered bar | Axis: `Contract`, Values: `Revenue Lost` (filter churned) |
| Card | `Avg CLV` |
| Line chart | Axis: `tenure_bucket`, Values: average `MonthlyCharges` |

---

## Step 6: Page 4 — Churn Prediction

| Visual | Setup |
|--------|--------|
| Table | `customerID`, `Contract`, `MonthlyCharges`, `churn_probability`, `risk_tier` — sort by probability desc, Top N = 100 |
| Histogram | Values: `churn_probability` |
| Bar chart | From `FeatureImportance`: axis `feature`, values `importance` — top 10 |
| Card | `High Risk Customers` |

---

## Step 7: Finish

1. **View → Mobile layout** (optional)
2. Enable **cross-filtering** on all visuals
3. **File → Save as** `dashboard/churn_dashboard.pbix`
4. Export page screenshots to `images/dashboard_screenshots/`
5. Add a screenshot to `README.md` under Dashboard section

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `churn_flag` shows as text | Change type to True/False in Power Query |
| Churn rate looks wrong | Use the measure, not average of `churn_flag` |
| Risk tier blank | Re-run `py scripts/score_all_customers.py` |
