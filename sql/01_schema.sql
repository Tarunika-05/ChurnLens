-- PostgreSQL schema for telecom customer churn analytics

DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id       VARCHAR(20) PRIMARY KEY,
    gender            VARCHAR(10),
    senior_citizen    SMALLINT,
    partner           VARCHAR(5),
    dependents        VARCHAR(5),
    tenure            INTEGER NOT NULL,
    phone_service     VARCHAR(5),
    multiple_lines    VARCHAR(20),
    internet_service  VARCHAR(20),
    online_security   VARCHAR(20),
    online_backup     VARCHAR(20),
    device_protection VARCHAR(20),
    tech_support      VARCHAR(20),
    streaming_tv      VARCHAR(20),
    streaming_movies  VARCHAR(20),
    contract_type     VARCHAR(20),
    paperless_billing VARCHAR(5),
    payment_method    VARCHAR(30),
    monthly_charges   DECIMAL(10, 2),
    total_charges     DECIMAL(10, 2),
    churn             BOOLEAN NOT NULL,
    tenure_bucket     VARCHAR(20),
    spending_category VARCHAR(20),
    estimated_clv     DECIMAL(12, 2),
    age_group         VARCHAR(20)
);

CREATE INDEX idx_customers_contract ON customers(contract_type);
CREATE INDEX idx_customers_payment ON customers(payment_method);
CREATE INDEX idx_customers_tenure_bucket ON customers(tenure_bucket);
CREATE INDEX idx_customers_churn ON customers(churn);
