# Power BI Dashboard Setup Guide

## Data Sources

Import these files into Power BI Desktop:

1. `data/processed/churn_cleaned.csv` — customer attributes and engineered features
2. `models/predictions.csv` — churn probabilities and risk tiers (test set)
3. `reports/feature_importance.csv` — top model drivers

Create a relationship on `customerID` between the customer table and predictions table.

## Recommended Pages

### Page 1: Executive Overview

**KPI cards**
- Total Customers = `DISTINCTCOUNT(customers[customerID])`
- Churn Rate = `DIVIDE(CALCULATE(COUNTROWS(customers), customers[churn_flag] = TRUE()), COUNTROWS(customers))`
- Monthly Revenue = `SUMX(FILTER(customers, customers[churn_flag] = FALSE()), customers[MonthlyCharges])`
- Revenue Lost = `SUMX(FILTER(customers, customers[churn_flag] = TRUE()), customers[MonthlyCharges])`

**Slicers:** `Contract`, `InternetService`, `spending_category`

### Page 2: Churn Analysis

- Clustered bar: churn rate by `Contract`
- Stacked column: churn count by `tenure_bucket`
- Donut chart: churn by `PaymentMethod`
- Matrix: `InternetService` vs churn rate

### Page 3: Revenue Insights

- Bar chart: monthly revenue by `spending_category`
- Waterfall: revenue lost by `contract_type`
- Card: average `estimated_clv`
- Line chart: average monthly charges by tenure bucket

### Page 4: Churn Prediction

- Table: top 100 customers by `churn_probability`
- Histogram: distribution of `churn_probability`
- Bar chart: feature importance from `feature_importance.csv`

## Design Tips

- Use churn red `#E94F37` and retained teal `#2E86AB`
- Add tooltips defining churn rate, CLV, and risk tiers
- Enable cross-filtering across all pages
- Export screenshots to `images/dashboard_screenshots/` for the README

## Save Location

Save the dashboard as `dashboard/churn_dashboard.pbix` after building in Power BI Desktop.

## Deploy for live users

See **`POWER_BI_DEPLOY.md`** — publish to Power BI Service, share with users, and set up scheduled refresh.
