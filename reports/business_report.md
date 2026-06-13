# Customer Churn Analytics — Business Report

**Prepared for:** Telecom Executive Leadership  
**Dataset:** IBM Telco Customer Churn (7,043 customers)  
**Analysis period:** Portfolio project snapshot

---

## Executive Summary

The telecom business faces a **26.54% churn rate**, with **1,869 churned customers** representing an estimated **$139,131 in monthly revenue loss**. Contract structure, tenure, internet service type, and payment method are the strongest drivers of churn risk.

A machine learning model (Logistic Regression) achieved **84.25% ROC-AUC**, enabling proactive identification of high-risk customers for retention campaigns.

---

## Key Findings

### Customer base

| Metric | Value |
|--------|------:|
| Total customers | 7,043 |
| Active customers | 5,174 |
| Churned customers | 1,869 |
| Churn rate | 26.54% |
| Monthly revenue (active) | $316,986 |
| Revenue lost to churn | $139,131 |
| Average estimated CLV | $2,280 |

### Churn drivers

1. **Contract type** — Month-to-month subscribers churn at the highest rate; two-year contracts show the lowest risk.
2. **Tenure** — Customers in the first 12 months are the most likely to leave.
3. **Internet service** — Fiber optic customers show elevated churn, indicating potential price/value gaps.
4. **Payment method** — Electronic check users represent a high-risk payment segment.

### Model performance

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|-------|---------:|----------:|-------:|---:|--------:|
| Logistic Regression | 79.91% | 65.22% | 52.14% | 57.95% | **84.25%** |
| XGBoost | 79.13% | 63.42% | 50.53% | 56.25% | 83.68% |
| Random Forest | 78.28% | 61.56% | 48.40% | 54.19% | 82.50% |

**Selected model:** Logistic Regression — highest ROC-AUC with strong interpretability for stakeholder communication.

---

## Business Recommendations

### 1. Retention strategy (high-value, high-risk customers)

Target customers in the top spending tier with churn probability above 0.7.  
**Estimated impact:** Retaining 10% of high-risk high-value customers could recover approximately **$8,000–$12,000/month** in revenue.

### 2. Contract strategy

Offer migration incentives (e.g., 15% discount for first 6 months) to month-to-month customers with tenure greater than 6 months.  
**Rationale:** Longer contracts correlate with materially lower churn.

### 3. Payment strategy

Promote autopay and card-based billing for electronic check users.  
**Rationale:** Electronic check is consistently associated with higher churn across segments.

### 4. Onboarding program (0–12 month tenure)

Launch a 90-day engagement program for new customers: usage tips, support check-ins, and bundled service trials.  
**Rationale:** Early-tenure customers represent the largest churn concentration.

### 5. Fiber value proposition

Review fiber pricing and bundle fiber with support/streaming perks.  
**Rationale:** Fiber customers churn more than DSL despite higher ARPU.

---

## Next Steps

1. Deploy churn scores to CRM for weekly retention outreach.
2. Build Power BI executive dashboard for ongoing KPI monitoring.
3. A/B test contract migration offers on the top 3 risk segments.
4. Refresh model quarterly with new customer data.

---

*Export this report to PDF via your editor or `pandoc reports/business_report.md -o reports/business_report.pdf`*
