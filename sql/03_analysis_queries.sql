-- ============================================================
-- KPI METRICS
-- ============================================================

-- Overall churn rate
SELECT
    ROUND(100.0 * AVG(CASE WHEN churn THEN 1.0 ELSE 0.0 END), 2) AS churn_rate_pct,
    COUNT(*) AS total_customers
FROM customers;

-- Monthly revenue from active customers
SELECT
    ROUND(SUM(monthly_charges), 2) AS monthly_revenue_active
FROM customers
WHERE churn = FALSE;

-- Customer retention rate
SELECT
    ROUND(100.0 * SUM(CASE WHEN churn = FALSE THEN 1 ELSE 0 END) / COUNT(*), 2) AS retention_rate_pct
FROM customers;

-- ============================================================
-- SEGMENT ANALYSIS
-- ============================================================

-- Churn by contract type
SELECT
    contract_type,
    COUNT(*) AS customers,
    SUM(CASE WHEN churn THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * AVG(CASE WHEN churn THEN 1.0 ELSE 0.0 END), 2) AS churn_rate_pct
FROM customers
GROUP BY contract_type
ORDER BY churn_rate_pct DESC;

-- Churn by age group
SELECT
    age_group,
    COUNT(*) AS customers,
    ROUND(100.0 * AVG(CASE WHEN churn THEN 1.0 ELSE 0.0 END), 2) AS churn_rate_pct
FROM customers
GROUP BY age_group
ORDER BY churn_rate_pct DESC;

-- Churn by payment method
SELECT
    payment_method,
    COUNT(*) AS customers,
    ROUND(100.0 * AVG(CASE WHEN churn THEN 1.0 ELSE 0.0 END), 2) AS churn_rate_pct
FROM customers
GROUP BY payment_method
ORDER BY churn_rate_pct DESC;

-- Churn by tenure bucket
SELECT
    tenure_bucket,
    COUNT(*) AS customers,
    ROUND(100.0 * AVG(CASE WHEN churn THEN 1.0 ELSE 0.0 END), 2) AS churn_rate_pct
FROM customers
GROUP BY tenure_bucket
ORDER BY churn_rate_pct DESC;

-- Churn by internet service
SELECT
    internet_service,
    COUNT(*) AS customers,
    ROUND(100.0 * AVG(CASE WHEN churn THEN 1.0 ELSE 0.0 END), 2) AS churn_rate_pct
FROM customers
GROUP BY internet_service
ORDER BY churn_rate_pct DESC;

-- ============================================================
-- REVENUE ANALYSIS
-- ============================================================

-- Revenue contribution by spending category
SELECT
    spending_category,
    COUNT(*) AS customers,
    ROUND(SUM(monthly_charges), 2) AS monthly_revenue,
    ROUND(100.0 * SUM(monthly_charges) / SUM(SUM(monthly_charges)) OVER (), 2) AS revenue_share_pct
FROM customers
GROUP BY spending_category
ORDER BY monthly_revenue DESC;

-- Revenue loss due to churn
SELECT
    ROUND(SUM(monthly_charges), 2) AS monthly_revenue_lost,
    COUNT(*) AS churned_customers
FROM customers
WHERE churn = TRUE;

-- Average customer lifetime value by contract
SELECT
    contract_type,
    ROUND(AVG(estimated_clv), 2) AS avg_estimated_clv,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
FROM customers
GROUP BY contract_type
ORDER BY avg_estimated_clv DESC;

-- ============================================================
-- TOP RISK SEGMENTS
-- ============================================================

SELECT
    contract_type,
    payment_method,
    tenure_bucket,
    COUNT(*) AS customers,
    ROUND(100.0 * AVG(CASE WHEN churn THEN 1.0 ELSE 0.0 END), 2) AS churn_rate_pct,
    ROUND(SUM(monthly_charges), 2) AS segment_monthly_revenue
FROM customers
GROUP BY contract_type, payment_method, tenure_bucket
HAVING COUNT(*) >= 50
ORDER BY churn_rate_pct DESC
LIMIT 15;
