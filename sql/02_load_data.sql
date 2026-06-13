-- Load cleaned customer data into PostgreSQL
-- Run after exporting data/processed/churn_cleaned.csv

COPY customers (
    customer_id,
    gender,
    senior_citizen,
    partner,
    dependents,
    tenure,
    phone_service,
    multiple_lines,
    internet_service,
    online_security,
    online_backup,
    device_protection,
    tech_support,
    streaming_tv,
    streaming_movies,
    contract_type,
    paperless_billing,
    payment_method,
    monthly_charges,
    total_charges,
    churn,
    tenure_bucket,
    spending_category,
    estimated_clv,
    age_group
)
FROM '/absolute/path/to/data/processed/churn_cleaned.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');

-- Alternative: load via Python
-- pandas.read_csv(...).to_sql('customers', engine, if_exists='replace', index=False)
