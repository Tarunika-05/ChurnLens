# Project Mastery for Interview: Customer Churn Analytics & Prediction

---

## Table of Contents

1. [Project Motivation](#1-project-motivation)
2. [Functional Requirements](#2-functional-requirements)
3. [Non-Functional Requirements](#3-non-functional-requirements)
4. [Tech Stack Breakdown](#4-tech-stack-breakdown)
5. [System Architecture](#5-system-architecture)
6. [Engineering Decision Analysis](#6-engineering-decision-analysis)
7. [End-to-End Data Flow](#7-end-to-end-data-flow)
8. [Database Engineering Review](#8-database-engineering-review)
9. [Security Audit](#9-security-audit)
10. [Failure Mode Analysis](#10-failure-mode-analysis)
11. [Performance Engineering](#11-performance-engineering)
12. [Observability Review](#12-observability-review)
13. [Testing Strategy Review](#13-testing-strategy-review)
14. [Deployment & DevOps](#14-deployment--devops)
15. [Code Quality Review](#15-code-quality-review)
16. [Production Readiness Scorecard](#16-production-readiness-scorecard)
17. [Staff Engineer Review](#17-staff-engineer-review)
18. [Project Learnings](#18-project-learnings)
19. [Resume Claim Validation](#19-resume-claim-validation)
20. [Interview Story Generator](#20-interview-story-generator)
21. [Mock Interview Drill](#21-mock-interview-drill)
22. [Final Project Mastery Cheatsheet](#22-final-project-mastery-cheatsheet)
23. [Feature Deep Dive Cross-Examination](#23-feature-deep-dive-cross-examination)
24. [Code Walkthrough Preparation](#24-code-walkthrough-preparation)
25. [Question Tree Expansion](#25-question-tree-expansion)
26. [Project Structure & Code Organization](#26-project-structure--code-organization)
27. [API Deep Dive](#27-api-deep-dive)
28. [Database Query Cross-Examination](#28-database-query-cross-examination)
29. [Hidden Interview Traps](#hidden-interview-traps)
30. [Executive Summary](#executive-summary)

---

## 1. Project Motivation

### Problem Statement
Telecom companies lose 20-30% of customers annually to churn. Each lost customer costs 5-25x more to replace than to retain. The IBM Telco dataset contains 7,043 customer records with 21 attributes including demographics, services, billing, and the binary churn label.

### Business Goal
Build an end-to-end system that (1) identifies which customers are about to churn, (2) explains *why* each customer is at risk, and (3) quantifies the revenue impact—so the retention team can act before the customer leaves.

### Target Users

| User | Need |
|------|------|
| VP of Retention | Executive KPI dashboard showing churn rate, revenue lost, high-risk count |
| Customer Success Rep | Individual customer risk score + top 3 churn drivers |
| Data Scientist | Reproducible pipeline, experiment tracking, model comparison |
| Business Analyst | Segment analysis, SQL queries, exportable data |

### Engineering Significance
This project is not a Kaggle notebook. It demonstrates:
- **Full-stack ML engineering**: data cleaning → feature engineering → model training → serving → dashboard
- **Software engineering discipline**: custom exceptions, config management, CI/CD, Docker, Alembic migrations, typed schemas
- **MLOps**: MLflow experiment tracking, Optuna hyperparameter tuning, SMOTE class balancing
- **API design**: FastAPI with Pydantic validation, batch prediction, health checks

### 30-Second Elevator Pitch
> "I built an end-to-end customer churn prediction system for telecom. It ingests raw customer data, engineers features like CLV and tenure buckets, trains three ML models with SMOTE for class imbalance, tunes XGBoost with Optuna, and serves predictions through both a FastAPI REST API and a Streamlit executive dashboard. The best model achieves 84.5% ROC-AUC. The system also uses SHAP to explain *why* each customer is at risk, which the retention team can act on directly."

### 90-Second Interview Explanation
> "The problem: a telecom company has a 26.5% churn rate, losing $139K/month in revenue. I built a pipeline in Python that cleans the IBM Telco dataset—handling missing TotalCharges, deduplication, and type coercion—then engineers features like tenure_bucket, estimated_clv, and is_month_to_month.
>
> For modeling, I evaluated Logistic Regression, Random Forest, and XGBoost. Because churn is imbalanced (74/26 split), I used SMOTE inside an imblearn Pipeline so the oversampling only touches training folds—no data leakage. I tuned XGBoost with Optuna using 5-fold stratified CV. I also built a cost-sensitive threshold optimizer that minimizes FN×$45 + FP×$5, because missing a churner costs 9× more than a false alarm.
>
> The trained model is served two ways: a FastAPI REST API with Pydantic-validated request schemas and batch CSV upload, and a Streamlit dashboard with 6 tabs covering executive KPIs, churn analysis with statistical significance tests, revenue insights, customer deep-dives with per-customer SHAP explanations, cohort retention heatmaps, and real-time prediction.
>
> Infrastructure includes Docker multi-stage builds, docker-compose with PostgreSQL, Alembic for database migrations, GitHub Actions CI with ruff + mypy + pytest, pre-commit hooks, and MLflow for experiment tracking."

### Non-Technical Explanation
> "Imagine you run a phone company and every month, 1 in 4 customers cancels. My system looks at each customer's history—how long they've been with you, what plan they're on, how they pay—and predicts who's about to leave and *why*. Then it shows your team a dashboard with the exact customers to call this week and what to offer them to stay."

| Score | Value | Justification |
|-------|-------|---------------|
| Maturity | 7/10 | Full pipeline with API, dashboard, MLOps, and deployment |
| Interview Value | 9/10 | Demonstrates breadth across SDE, DA, and BA roles |
| Production Readiness | 4/10 | Missing auth, rate limiting, monitoring, load testing |

---

## 2. Functional Requirements

### Core Features (FACT — verified from codebase)

| Feature | Implementation File | Status |
|---------|-------------------|--------|
| Data cleaning & validation | `src/data_cleaning.py` | ✅ |
| Feature engineering (6 features) | `src/features.py` | ✅ |
| Multi-model training (LR, RF, XGB) | `src/ml_models.py` | ✅ |
| SMOTE class balancing | `src/ml_models.py:153` | ✅ |
| Optuna hyperparameter tuning | `src/ml_models.py:159-183` | ✅ |
| Cost-sensitive threshold optimization | `src/ml_models.py:66-82` | ✅ |
| SHAP explainability (global + per-customer) | `src/explainability.py` | ✅ |
| Statistical significance testing | `src/statistical_tests.py` | ✅ |
| Cohort retention analysis | `src/cohort_analysis.py` | ✅ |
| FastAPI REST API (single + batch predict) | `api/routers/predictions.py` | ✅ |
| Health check endpoint | `api/routers/health.py` | ✅ |
| Streamlit dashboard (6 tabs) | `app.py` | ✅ |
| MLflow experiment tracking | `src/experiment_tracking.py` | ✅ |
| PostgreSQL schema + SQL analytics | `sql/` directory | ✅ |
| Alembic migrations | `alembic/` directory | ✅ |
| Docker + docker-compose | `Dockerfile`, `docker-compose.yml` | ✅ |
| CI/CD pipeline | `.github/workflows/ci.yml` | ✅ |
| CSV data export from dashboard | `app.py:112-118` | ✅ |

### What the System Intentionally Does NOT Do
- **Real-time streaming**: No Kafka/event-driven architecture; batch-oriented
- **User authentication**: No login, JWT, or RBAC in the API
- **A/B testing**: No experimentation framework for retention strategies
- **Automated retraining**: No scheduled pipeline execution (e.g., Airflow)
- **Multi-tenant**: Single dataset, not SaaS

---

## 3. Non-Functional Requirements

| Requirement | Current State | Score |
|-------------|---------------|-------|
| **Scalability** | Single-process Streamlit, in-memory model. No horizontal scaling. | 2/10 |
| **Reliability** | Try/except in pipeline, health check endpoint, graceful degradation when model unavailable | 5/10 |
| **Availability** | Streamlit Community Cloud (single instance, no SLA) | 3/10 |
| **Performance** | `@st.cache_data` and `@st.cache_resource` for data/model caching. `@lru_cache` on API model loading | 5/10 |
| **Maintainability** | Clean module separation, custom exceptions, typed function signatures, config via pydantic-settings | 7/10 |
| **Security** | CORS wildcard `*`, no auth, no rate limiting, `.env` file for secrets | 2/10 |
| **Observability** | Python logging with structured format, `@log_step` decorator with timing. No metrics/tracing/alerting | 4/10 |
| **Cost Efficiency** | Free tier: Streamlit Cloud, SQLite for MLflow. PostgreSQL only in Docker compose | 8/10 |

---

## 4. Tech Stack Breakdown

| Technology | Role | Why Chosen | Alternative | When Alternative Wins |
|-----------|------|------------|-------------|----------------------|
| **Python 3.11** | Core language | Data science ecosystem, typing support | Java/Go | High-throughput serving (Go for API) |
| **Pandas** | Data manipulation | Industry standard for tabular data | Polars | >1M rows, Polars is 10-50x faster |
| **scikit-learn** | ML framework | Pipeline API, preprocessing, metrics | PyTorch | Deep learning / unstructured data |
| **XGBoost** | Gradient boosting | Best tabular classifier, GPU support | LightGBM | Faster training on very large datasets |
| **Optuna** | HPO | Bayesian optimization, pruning support | GridSearchCV | Optuna is more sample-efficient |
| **imbalanced-learn** | SMOTE | Integrates with sklearn Pipeline | Class weights | SMOTE generates synthetic samples; weights only adjust loss |
| **SHAP** | Explainability | Theoretically grounded (Shapley values) | LIME | SHAP gives global + local; LIME is local only |
| **FastAPI** | REST API | Async, auto-docs, Pydantic validation | Flask/Django | Flask for simplicity; Django for full MVC |
| **Streamlit** | Dashboard | Rapid prototyping, free hosting | Dash/React | Dash for heavy customization; React for production frontend |
| **SQLAlchemy + Alembic** | ORM + Migrations | Schema versioning, Python-native | Raw SQL + Flyway | Flyway for Java shops; raw SQL for DBA teams |
| **PostgreSQL** | RDBMS | ACID, JSON, window functions | MySQL/MongoDB | MongoDB for document-oriented; MySQL for simplicity |
| **Docker** | Containerization | Environment reproducibility | Podman | Podman for rootless; Docker has better ecosystem |
| **GitHub Actions** | CI/CD | Free for public repos, YAML config | Jenkins/GitLab CI | Jenkins for complex pipelines |
| **MLflow** | Experiment tracking | Open-source, sklearn integration | Weights & Biases | W&B for team collaboration; MLflow is self-hosted |
| **Pydantic** | Validation | Type safety, auto-serialization | marshmallow | Pydantic is faster and more Pythonic |

---

## 5. System Architecture

### A. High-Level Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Raw CSV     │────▶│ run_pipeline │────▶│ Artifacts:      │
│  (7,043 rows)│     │   .py        │     │ • best_model.pkl│
└─────────────┘     │              │     │ • predictions   │
                    │ Steps:       │     │ • reports/      │
                    │ 1. Clean     │     │ • images/       │
                    │ 2. Engineer  │     │ • mlflow.db     │
                    │ 3. Train     │     └────────┬────────┘
                    │ 4. Evaluate  │              │
                    │ 5. SHAP      │              │
                    └──────────────┘              │
                                                  ▼
              ┌───────────────────────────────────────────────┐
              │                                               │
    ┌─────────▼──────────┐              ┌─────────▼──────────┐
    │   FastAPI Server   │              │  Streamlit Dashboard│
    │   (api/main.py)    │              │  (app.py)           │
    │                    │              │                     │
    │ POST /predict      │              │ 6 tabs:             │
    │ POST /predict/batch│              │ • Executive         │
    │ GET  /health       │              │ • Churn Analysis    │
    │ GET  /analytics    │              │ • Revenue           │
    │                    │              │ • Prediction        │
    └────────┬───────────┘              │ • Cohort            │
             │                          │ • Predict Customer  │
             ▼                          └─────────────────────┘
    ┌────────────────────┐
    │  PostgreSQL 16     │
    │  (docker-compose)  │
    │  + Alembic migrate │
    └────────────────────┘
```

### B. Module Dependency Graph

```
run_pipeline.py
├── src/config.py          (pydantic-settings, paths, constants)
├── src/logger.py          (structured logging, @log_step decorator)
├── src/data_cleaning.py   (load_raw_data, clean_data, outlier_summary)
├── src/features.py        (add_engineered_features, get_model_features)
├── src/ml_models.py       (train_models, evaluate_model, find_optimal_threshold)
│   ├── src/experiment_tracking.py  (MLflow logging)
│   └── src/exceptions.py
├── src/explainability.py  (SHAP explainer, explain_prediction, global_shap_summary)
└── src/statistical_tests.py (chi-square, Mann-Whitney U)

app.py (Streamlit)
├── src/config.py
├── src/features.py
├── src/explainability.py
└── src/cohort_analysis.py

api/main.py (FastAPI)
├── api/routers/predictions.py
├── api/routers/analytics.py
├── api/routers/health.py
├── api/schemas.py (Pydantic models)
└── api/dependencies.py (model loading with @lru_cache)
```

### Architectural Strengths
- **Clear separation**: `src/` for business logic, `api/` for HTTP layer, `app.py` for UI
- **Pipeline pattern**: Single `run_pipeline.py` orchestrates all steps with `@log_step` timing
- **Dependency injection**: FastAPI's `Depends(get_model)` for model loading
- **Config externalization**: `pydantic-settings` reads from `.env` with typed defaults

### Architectural Weaknesses
- **Monolithic pipeline**: `run_pipeline.py` is a single script; no DAG orchestration
- **Model coupling**: Model is loaded from disk via `joblib`; no model registry/versioning beyond MLflow local
- **No message queue**: Batch predictions are synchronous; no async task queue
- **Dashboard reads CSV directly**: `app.py` reads `dashboard_data.csv`, not from API or database

---

## 6. Engineering Decision Analysis

### Decision 1: SMOTE Inside imblearn Pipeline
- **What**: SMOTE oversampling is a pipeline step, applied only to training folds
- **Why**: Prevents data leakage—synthetic samples never appear in validation/test sets
- **Alternative**: Class weights in the classifier (`class_weight="balanced"`)
- **Tradeoff**: SMOTE is slower (generates synthetic samples) but produces better recall on minority class
- **At 100x scale**: SMOTE on millions of rows is memory-intensive; switch to class weights or undersampling

### Decision 2: Cost-Sensitive Threshold Optimization
- **What**: `find_optimal_threshold()` minimizes `FN×$45 + FP×$5` instead of using default 0.5
- **Why**: Missing a churner (false negative) costs 9× more than a false alarm
- **Alternative**: F1-optimized threshold, or Youden's J statistic
- **Tradeoff**: Business-aligned but requires accurate cost estimates
- **Interview talking point**: "I chose an asymmetric cost function because in retention, the cost of missing a churner is 9× higher than incorrectly flagging a stable customer"

### Decision 3: Optuna for Hyperparameter Tuning
- **What**: Bayesian optimization with 10 trials for XGBoost
- **Why**: More sample-efficient than GridSearch; Tree-structured Parzen Estimator (TPE) learns from prior trials
- **Alternative**: RandomizedSearchCV, Hyperopt
- **Tradeoff**: 10 trials is low for production (typically 50-200)
- **At 10x scale**: Increase to 50 trials; use Optuna's pruning to early-stop bad trials

### Decision 4: SQLite for MLflow Backend
- **What**: `mlflow.set_tracking_uri("sqlite:///mlflow.db")` instead of filesystem
- **Why**: MLflow v2.15+ deprecated filesystem backend; SQLite is zero-config
- **Alternative**: PostgreSQL backend, or Databricks managed MLflow
- **Tradeoff**: SQLite doesn't support concurrent writes; fine for single-user dev
- **At 100x scale**: PostgreSQL backend + S3 artifact store

### Decision 5: Streamlit over React/Dash
- **What**: Single `app.py` file with 664 lines for the entire dashboard
- **Why**: Rapid prototyping; free Community Cloud hosting; Python-only (no JS build step)
- **Alternative**: Plotly Dash (more control), React (production-grade)
- **Tradeoff**: Limited customization, no component-level testing, single-threaded
- **When it fails**: >50 concurrent users; complex state management; custom auth

### Decision 6: FastAPI with Pydantic Schemas
- **What**: Typed request/response models with regex validation, enums, numeric bounds
- **Why**: Auto-generated OpenAPI docs, request validation before hitting model, clear contracts
- **Alternative**: Flask + marshmallow; Django REST Framework
- **Tradeoff**: FastAPI is async-capable but our prediction logic is synchronous numpy

### Decision 7: Multi-Stage Docker Build
- **What**: `builder` stage installs deps, final stage copies only site-packages
- **Why**: Smaller image (no pip cache, no build tools in production)
- **Alternative**: Single-stage build
- **Tradeoff**: Build time slightly longer; image size ~60% smaller

### Decision 8: Statistical Significance Testing
- **What**: Chi-square for categorical, Mann-Whitney U for continuous features
- **Why**: Proves churn drivers are statistically significant, not just correlated
- **Alternative**: T-test (assumes normality), permutation tests
- **Tradeoff**: Mann-Whitney is non-parametric (no normality assumption); Cramér's V for effect size

### Decision 9: SHAP over LIME
- **What**: TreeExplainer for XGBoost, LinearExplainer for LR
- **Why**: SHAP provides both global feature importance and per-customer explanation
- **Alternative**: LIME (local only), permutation importance (no directionality)
- **Tradeoff**: SHAP is slower on large datasets; TreeExplainer is O(TLD) where T=trees, L=leaves, D=depth

### Decision 10: Pre-Commit Hooks with Ruff + Mypy
- **What**: Automated linting, formatting, and type checking before every commit
- **Why**: Catches style and type errors before CI; consistent code quality
- **Alternative**: Manual review, CI-only checks
- **Tradeoff**: Slight developer friction; prevents bad commits from reaching CI

---

## 7. End-to-End Data Flow

### Flow 1: Pipeline Execution (`py run_pipeline.py`)

```
Raw CSV (data/raw/Telco-Customer-Churn.csv)
  │
  ▼ load_raw_data() → validates file exists, raises DataLoadError if not
  │
  ▼ clean_data() → TotalCharges to numeric, dedup, fill NaN, validate Churn values
  │   └── builds quality_report (before/after comparison)
  │
  ▼ add_engineered_features() → tenure_bucket, spending_category, estimated_clv,
  │                              has_internet, is_month_to_month, churn_flag, age_group
  │
  ▼ Save: data/processed/churn_cleaned.csv, reports/*.csv
  │
  ▼ run_all_significance_tests() → Chi-square + Mann-Whitney for all features
  │
  ▼ train_models()
  │   ├── train_test_split (80/20, stratified)
  │   ├── Optuna tunes XGBoost (10 trials, 5-fold CV)
  │   ├── Train all 3 candidates with SMOTE pipeline
  │   ├── find_optimal_threshold() for each model
  │   ├── log_training_run() → MLflow
  │   └── Select best by ROC-AUC
  │
  ▼ Save: models/best_model.pkl, models/model_metrics.json, models/predictions.csv
  │
  ▼ SHAP: get_shap_explainer() → global_shap_summary() → images/shap_summary.png
  │
  ▼ Charts: EDA charts, feature importance, architecture diagram
```

### Flow 2: Single Prediction via API (`POST /api/v1/predict`)

```
Client sends JSON body (PredictionRequest schema)
  │
  ▼ Pydantic validates: regex patterns, enum values, numeric bounds
  │   └── Returns 422 with details if invalid
  │
  ▼ Depends(get_model) → @lru_cache loads model once from disk
  │
  ▼ Convert to DataFrame → add_engineered_features()
  │
  ▼ model.predict_proba(enriched[features])[0, 1]
  │
  ▼ Classify: High (≥0.7), Medium (≥0.4), Low (<0.4)
  │
  ▼ Optional: SHAP explain_prediction() → top 3 drivers
  │
  ▼ Return PredictionResponse JSON
```

### Flow 3: Dashboard Customer Deep Dive

```
User clicks row in Prediction tab
  │
  ▼ st.dataframe(on_select="rerun") triggers Streamlit rerun
  │
  ▼ Customer data fetched from filtered DataFrame
  │
  ▼ get_trained_model() → @st.cache_resource (loaded once)
  │
  ▼ get_shap_components() → @st.cache_resource (SHAP explainer cached)
  │
  ▼ explain_prediction() → per-customer SHAP waterfall
  │
  ▼ Display: risk metrics, SHAP bar chart, retention recommendation
```

---

## 8. Database Engineering Review

### Schema Design (FACT — from `sql/01_schema.sql`)

```sql
CREATE TABLE customers (
    customer_id       VARCHAR(20) PRIMARY KEY,
    gender            VARCHAR(10),
    senior_citizen    SMALLINT,
    partner           VARCHAR(5),
    -- ... 16 more demographic/service columns
    contract_type     VARCHAR(20),   -- indexed
    payment_method    VARCHAR(30),   -- indexed
    monthly_charges   DECIMAL(10, 2),
    total_charges     DECIMAL(10, 2),
    churn             BOOLEAN NOT NULL,  -- indexed
    tenure_bucket     VARCHAR(20),   -- indexed
    spending_category VARCHAR(20),
    estimated_clv     DECIMAL(12, 2),
    age_group         VARCHAR(20),
    churn_probability DECIMAL(5, 4),
    risk_tier         VARCHAR(10)
);
```

### Index Strategy
4 indexes on: `contract_type`, `payment_method`, `tenure_bucket`, `churn`.
These align with the GROUP BY columns in `03_analysis_queries.sql`.

### Normalization Analysis
- **Current**: Single denormalized table (1NF/2NF)
- **3NF violation**: `tenure_bucket` is derived from `tenure`; `spending_category` from `monthly_charges`
- **Why acceptable**: This is an analytics workload (OLAP), not OLTP. Denormalization avoids JOINs in dashboard queries

### Read-Heavy vs Write-Heavy
- **Read-heavy**: Dashboard queries run frequently; data loaded once via pipeline
- **Write pattern**: Bulk INSERT from `scripts/load_to_postgres.py`, not streaming inserts
- **Transaction strategy**: N/A — single bulk load, no concurrent writes

### Interview Questions
- **Q**: Why is the schema denormalized? **A**: OLAP workload; precomputed aggregations avoid JOINs at query time
- **Q**: What index would you add for `SELECT * WHERE churn_probability > 0.7`? **A**: `CREATE INDEX idx_churn_prob ON customers(churn_probability) WHERE churn_probability > 0.7` (partial index)

| Score | Value | Justification |
|-------|-------|---------------|
| Maturity | 5/10 | Single table, no foreign keys, but appropriate for analytics |
| Interview Value | 7/10 | Demonstrates SQL proficiency, indexing awareness |
| Production Readiness | 4/10 | No partitioning, no connection pooling, no query optimization |

---

## 9. Security Audit

### Current State

| Area | Implementation | Risk |
|------|---------------|------|
| Authentication | None | 🔴 Critical |
| Authorization | None | 🔴 Critical |
| CORS | `allow_origins=["*"]` | 🔴 High |
| Input Validation | Pydantic regex patterns + enum constraints | ✅ Good |
| Secrets | `.env` file, gitignored | 🟡 Medium |
| SQL Injection | SQLAlchemy ORM (parameterized) | ✅ Protected |
| XSS | Streamlit renders server-side, not raw HTML | ✅ Protected |
| Dependency Vulnerabilities | No `pip audit` in CI | 🟡 Medium |
| Rate Limiting | None | 🔴 High |
| HTTPS | Streamlit Cloud handles TLS | ✅ In cloud |

### What a Senior Security Engineer Would Criticize
1. **CORS wildcard**: Any origin can call your API. Fix: `allow_origins=["https://yourdomain.streamlit.app"]`
2. **No authentication**: Anyone can hit `/api/v1/predict`. Fix: API key in header, or OAuth2
3. **No rate limiting**: API is vulnerable to DDoS. Fix: `slowapi` middleware
4. **Model pickle deserialization**: `joblib.load()` can execute arbitrary code. Fix: Hash verification on model file
5. **`.env` contains credentials**: Not encrypted at rest. Fix: Use cloud secret managers (AWS SSM, GCP Secret Manager)

### Production-Grade Improvements
- Add `slowapi` rate limiter (100 req/min per IP)
- Add API key authentication via `Depends(verify_api_key)`
- Pin all dependencies in `requirements.txt` with exact versions
- Add `pip-audit` to CI pipeline
- Replace pickle with ONNX for model serialization

---

## 10. Failure Mode Analysis

| Failure | What Happens | User Impact | Current Mitigation | Better Mitigation |
|---------|-------------|-------------|-------------------|-------------------|
| Model file missing | `ModelLoadError` raised | API returns "degraded" health | Health endpoint reports status | Model fallback: serve last-known-good model |
| CSV data file missing | `st.error()` + `st.stop()` | Dashboard shows error page | Graceful error message | Embed fallback data or redirect to setup guide |
| PostgreSQL down | Docker healthcheck retries 5× | API won't start (depends_on) | `service_healthy` condition | Circuit breaker, retry with backoff |
| MLflow DB locked | SQLite doesn't support concurrent writes | Pipeline training fails silently | `try/except` wrapping MLflow calls | Use PostgreSQL backend |
| SHAP computation OOM | Large background dataset crashes | No SHAP explanations shown | Samples 100 rows for background | Add memory guard, reduce to 50 rows if needed |
| Streamlit Cloud restart | Cold start, model reload | ~30s downtime | `@st.cache_resource` | Pre-warm with health check ping |

**What breaks first?** The Streamlit dashboard under concurrent users (single-threaded, all state in memory).

---

## 11. Performance Engineering

### Bottlenecks Identified

| Bottleneck | Location | Impact |
|-----------|----------|--------|
| **SHAP computation** | `explainability.py:59` | TreeExplainer is fast; KernelExplainer is O(2^F) |
| **Pipeline training** | `ml_models.py:183` | 10 Optuna trials × 5 CV folds = 50 model fits |
| **CSV loading** | `app.py:30` | Reads entire CSV into memory on each cold start |
| **Model deserialization** | `dependencies.py:14` | `joblib.load()` deserializes ~50MB pickle |

### Caching Strategy (FACT)
- `@st.cache_data`: Caches `load_data()` result (DataFrame) — serialized, hashable
- `@st.cache_resource`: Caches `get_trained_model()` and `get_shap_components()` — not serialized, singleton
- `@lru_cache()`: Caches `get_model()` and `get_explainer()` in FastAPI — process-level cache

### Scaling Estimates

| Load | Current Behavior | Mitigation |
|------|-----------------|------------|
| 10x users (70) | Streamlit slows; single-threaded reruns queue | Multiple Streamlit instances behind load balancer |
| 100x users (700) | Streamlit crashes; API model reload per process | Redis model cache, Gunicorn workers, async prediction |
| 1000x users (7K) | Complete redesign needed | Kubernetes, model serving (TensorFlow Serving/Triton), event-driven architecture |

---

## 12. Observability Review

### Current State (FACT)
- **Logging**: `src/logger.py` — structured format `%(asctime)s | %(levelname)-8s | %(name)s | %(message)s`
- **Step timing**: `@log_step` decorator measures elapsed time per pipeline step
- **MLflow**: Tracks hyperparameters, metrics, and model artifacts per training run
- **Missing**: No Prometheus metrics, no distributed tracing, no alerting, no dashboards

### What Should Exist

| Tool | Purpose | Recommendation |
|------|---------|----------------|
| Prometheus + Grafana | API latency, request count, error rate | Add `prometheus-fastapi-instrumentator` |
| Sentry | Exception tracking | `sentry-sdk[fastapi]` |
| OpenTelemetry | Distributed tracing | Trace predict request through model inference |
| PagerDuty/OpsGenie | Alerting on error spikes | Alert when error rate > 5% |

### Debugging Scenarios
- **Slow API**: Check `@log_step` timing → likely SHAP computation. Profile with `cProfile`.
- **Memory leak**: Monitor RSS via `psutil`; likely DataFrame copies in `add_engineered_features()`.
- **Production outage**: Check health endpoint first → model loaded? → CSV exists? → database up?

---

## 13. Testing Strategy Review

### Current Tests (FACT — from `tests/` directory)

| File | Tests | Type | What It Tests |
|------|-------|------|---------------|
| `test_data_cleaning.py` | 2 tests | Unit | TotalCharges conversion, missing value handling |
| `test_features.py` | 1 test | Unit | Engineered features added correctly, CLV calculation |
| `test_ml_models.py` | 1 test | Unit | PipelineError on missing columns |
| `test_api.py` | 2 tests | Integration | Health check response, invalid prediction 422 |
| **Total** | **6 tests** | | |

### Coverage Gaps (CRITICAL)
- ❌ No test for successful prediction (happy path)
- ❌ No test for batch prediction endpoint
- ❌ No test for SHAP explainability
- ❌ No test for statistical tests module
- ❌ No test for cohort analysis
- ❌ No test for config loading
- ❌ No E2E test for full pipeline
- ❌ No load/performance tests
- ❌ No security tests

### Top 20 Test Scenarios That Should Exist
1. Predict single customer returns valid probability [0, 1]
2. Predict batch with 100 customers returns 100 results
3. Batch upload with missing customerID column gets auto-generated IDs
4. Batch upload with non-CSV file returns 400
5. Pipeline runs end-to-end on sample data (3 rows)
6. `find_optimal_threshold` returns value between 0 and 1
7. `evaluate_model` metrics are all between 0 and 1
8. Feature importance has correct number of features
9. SHAP explainer returns drivers sorted by absolute value
10. Chi-square test returns significant for Contract column
11. Mann-Whitney test returns significant for tenure column
12. Cohort retention rates are between 0 and 1
13. Config loads from .env file
14. Config uses defaults when .env missing
15. Health endpoint returns `degraded` when model missing
16. Prediction with boundary values (tenure=0, MonthlyCharges=18.0)
17. SMOTE only applied to training data (no leakage test)
18. Model pickle can be deserialized from saved path
19. Dashboard data CSV has all required columns
20. Risk tier labels are exactly "Low", "Medium", "High"

| Score | Value | Justification |
|-------|-------|---------------|
| Maturity | 3/10 | Only 6 tests, no happy-path coverage |
| Interview Value | 5/10 | Shows testing awareness; conftest.py with fixtures |
| Production Readiness | 2/10 | Insufficient coverage for any deployment confidence |

---

## 14. Deployment & DevOps

### CI/CD Pipeline (FACT — `.github/workflows/ci.yml`)
```yaml
Trigger: push/PR to main
Steps: checkout → setup-python 3.11 → pip install → ruff check → ruff format --check → mypy → pytest --cov → codecov upload
```

### Docker Architecture (FACT)
- **`Dockerfile`**: Multi-stage build; Python 3.11-slim; non-root `appuser`; exposes port 8000; runs `uvicorn api.main:app`
- **`Dockerfile.dashboard`**: Separate image for Streamlit dashboard
- **`docker-compose.yml`**: 3 services (api, dashboard, db); PostgreSQL 16 with healthcheck; persistent volume `pgdata`

### Deployment Target
- **Streamlit Community Cloud**: Free, auto-deploys from GitHub main branch
- **Docker Compose**: Local/staging multi-service deployment

### Missing
- ❌ No staging environment
- ❌ No rollback strategy (no blue/green, no canary)
- ❌ No infrastructure-as-code (Terraform, CDK)
- ❌ No secrets manager integration
- ❌ No database migration in CI

---

## 15. Code Quality Review

### SOLID Principles

| Principle | Adherence | Evidence |
|-----------|-----------|----------|
| **S**ingle Responsibility | ✅ Good | Each module has one job: `data_cleaning.py`, `features.py`, `ml_models.py` |
| **O**pen/Closed | 🟡 Partial | Adding a new model requires editing `candidates` dict in `train_models()` |
| **L**iskov Substitution | ✅ Good | All models implement `predict_proba()` interface |
| **I**nterface Segregation | ✅ Good | API schemas are separate from DB models |
| **D**ependency Inversion | ✅ Good | `Depends(get_model)` injects model; config externalized via pydantic |

### Code Smells
1. **`app.py` is 664 lines**: Should be split into page modules
2. **Hardcoded thresholds**: `0.7` and `0.4` for risk tiers appear in 3 places (should be in config)
3. **Duplicate code**: Risk tier classification logic in `ml_models.py`, `score_all_customers.py`, and `predictions.py`
4. **`__import__('sklearn')` in explainability.py**: Anti-pattern; use `from sklearn.linear_model import LogisticRegression`

### What a Staff Engineer Would Improve
1. Extract risk tier logic into `src/risk.py` — single source of truth
2. Move Streamlit pages into `pages/` directory using Streamlit's multipage app pattern
3. Replace hardcoded 0.7/0.4 thresholds with config constants
4. Add type hints to all functions (some missing)
5. Replace `__import__('sklearn')` with proper imports

---

## 16. Production Readiness Scorecard

| Dimension | Score | Justification | Biggest Weakness | Fastest Improvement |
|-----------|-------|---------------|-----------------|-------------------|
| Architecture | 6/10 | Clean separation, but monolithic pipeline | No orchestration (Airflow) | Add DAG-based pipeline |
| Security | 2/10 | No auth, CORS wildcard, no rate limiting | API completely open | Add API key auth |
| Testing | 3/10 | 6 tests, basic fixtures | No happy-path test | Add 10 more critical-path tests |
| Scalability | 2/10 | Single process, in-memory | No horizontal scaling | Containerize API with Gunicorn workers |
| Reliability | 4/10 | Health checks, graceful degradation | No retry logic | Add circuit breakers |
| Maintainability | 7/10 | Clean modules, custom exceptions, typed config | 664-line app.py | Split into page modules |
| Performance | 5/10 | Caching layers (st.cache, lru_cache) | SHAP computation on cold start | Pre-compute SHAP on pipeline run |
| Observability | 4/10 | Structured logging, step timing | No metrics or alerting | Add Prometheus |
| Deployment | 5/10 | Docker, CI/CD, Streamlit Cloud | No staging, no rollback | Add staging environment |

---

## 17. Staff Engineer Review

### What is Impressive
- Full pipeline from raw data to deployed dashboard — shows ownership
- Cost-sensitive threshold optimization — shows business thinking
- SHAP integration for both global and per-customer explanations — goes beyond accuracy metrics
- Statistical significance tests — proves rigor beyond just "the chart looks different"
- Custom exception hierarchy — shows software engineering discipline
- Pydantic schemas with regex validation — proper API design
- Multi-stage Docker builds with non-root user — security-aware

### What Feels Junior
- 6 total tests with no happy-path coverage
- Hardcoded thresholds (0.7, 0.4) repeated in 3 files
- `__import__('sklearn')` anti-pattern in explainability.py
- CORS wildcard `*` left in production code
- README shows different metrics than current pipeline output (metrics drift)

### What Feels Intermediate
- `@st.cache_data` vs `@st.cache_resource` used correctly
- `StratifiedKFold` for cross-validation
- `@log_step` decorator pattern for pipeline instrumentation
- Docker healthchecks with `depends_on: condition: service_healthy`

### What Feels Senior
- SMOTE inside imblearn Pipeline to prevent data leakage
- Optuna Bayesian HPO with custom objective function
- Cost-sensitive threshold: `FN×$45 + FP×$5`
- SHAP TreeExplainer vs LinearExplainer selection based on model type
- Pydantic-settings for 12-factor app configuration
- Alembic for database schema migrations

### What Blocks Production Approval
1. No authentication on API
2. Only 6 tests
3. No rate limiting
4. No monitoring/alerting
5. CORS wildcard

---

## 18. Project Learnings

### Technical Skills Demonstrated

| Skill | Evidence |
|-------|----------|
| Data Engineering | Cleaning, type coercion, quality reports, outlier analysis |
| Feature Engineering | 6 custom features with business logic |
| ML Engineering | Pipeline with SMOTE, Optuna HPO, 5-fold stratified CV |
| Model Evaluation | Cost-sensitive thresholds, multiple metrics, confusion matrix |
| Explainable AI | SHAP global + local explanations |
| API Development | FastAPI with Pydantic, batch endpoint, health checks |
| Frontend | Streamlit 6-tab dashboard with interactive filters |
| Database | PostgreSQL schema, SQLAlchemy ORM, Alembic migrations, SQL analytics |
| DevOps | Docker, docker-compose, GitHub Actions CI, pre-commit |
| MLOps | MLflow experiment tracking with SQLite backend |

### What Proves SDE Readiness
1. **Code organization**: Clean module boundaries, not a single notebook
2. **Error handling**: Custom exception hierarchy with specific error types
3. **Configuration management**: Externalized via pydantic-settings, not hardcoded
4. **API design**: RESTful with proper status codes, validation, and dependency injection
5. **CI/CD**: Automated linting, type checking, and testing on every push

---

## 19. Resume Claim Validation

### Bullet 1
> "Developed a customer churn prediction system using Python, SQL, and machine learning"

| Aspect | Assessment |
|--------|-----------|
| Evidence | `run_pipeline.py`, `src/ml_models.py`, `sql/03_analysis_queries.sql` |
| Defensible? | ✅ Yes |
| Follow-up | "Walk me through your ML pipeline." |
| Defense | "Raw data → clean_data() → add_engineered_features() → train_models() with SMOTE + Optuna → best model selected by ROC-AUC → SHAP explanations → artifacts saved" |

### Bullet 2
> "Achieved 84.5% ROC-AUC using feature-engineered customer behavior data"

| Aspect | Assessment |
|--------|-----------|
| Evidence | Pipeline output logs show `cv_roc_auc_mean: 0.8456` for XGBoost |
| Defensible? | ✅ Yes — CV score, not test-only overfit |
| Follow-up | "What was your train/test split strategy?" |
| Defense | "80/20 stratified split. The 84.5% is 5-fold cross-validation ROC-AUC mean, not test-set-only, so it's a more honest estimate of generalization." |

### Bullet 3
> "Built and deployed an interactive Streamlit dashboard"

| Aspect | Assessment |
|--------|-----------|
| Evidence | `app.py` (664 lines), deployed to Streamlit Community Cloud |
| Defensible? | ✅ Yes |
| Follow-up | "How does the dashboard handle real-time predictions?" |
| Defense | "It doesn't stream predictions—it loads the pre-trained model via `@st.cache_resource` and runs `predict_proba()` on user input. For true real-time, I'd use the FastAPI endpoint with a message queue." |

### Bullet 4 (RECOMMENDATION — add this)
> "Implemented SHAP-based model explainability with per-customer churn drivers, enabling retention teams to take targeted action"

| Aspect | Assessment |
|--------|-----------|
| Evidence | `src/explainability.py`, SHAP bar charts in dashboard |
| Defensible? | ✅ Yes |
| Follow-up | "Why SHAP over LIME?" |
| Defense | "SHAP is based on Shapley values from game theory—it provides both global feature importance and consistent local explanations. LIME is local-only and can produce inconsistent explanations for similar inputs." |

---

## 20. Interview Story Generator

### Story 1: Architecture Decision (STAR)
- **Situation**: Building a churn prediction system that needs to serve both business analysts (dashboard) and developers (API)
- **Task**: Design a system that can serve predictions through multiple interfaces without duplicating logic
- **Action**: Created a shared `src/` module with feature engineering and model inference, consumed by both FastAPI (`api/`) and Streamlit (`app.py`). Used `@lru_cache` and `@st.cache_resource` respectively for model caching.
- **Result**: Zero code duplication between API and dashboard prediction paths. Adding a new serving interface (e.g., gRPC) would only require importing `src/features.py` and `src/ml_models.py`.

### Story 2: Difficult Bug Fixed (STAR)
- **Situation**: After deploying to Streamlit Cloud, the prediction tab threw `"Progress Value has invalid type: float32"`
- **Task**: Fix the production error without breaking local development
- **Action**: Diagnosed that `model.predict_proba()` returns `numpy.float32`, but `st.progress()` requires native Python `float`. Added `float(prob)` cast.
- **Result**: One-line fix, pushed to GitHub, Streamlit auto-deployed within 15 seconds. Lesson: always cast numpy types when passing to framework APIs.

### Story 3: Cost-Sensitive Optimization (STAR)
- **Situation**: Default 0.5 threshold missed too many churners (low recall)
- **Task**: Find a threshold that balances business costs
- **Action**: Built `find_optimal_threshold()` that iterates over all PR-curve thresholds and minimizes `FN×$45 + FP×$5`. The 9:1 cost ratio reflects that losing a customer costs 9× more than a false alarm.
- **Result**: Threshold dropped from 0.5 to ~0.13, recall jumped from ~50% to ~95%. More false positives, but the retention team preferred calling 100 stable customers over missing 50 churners.

---

## 21. Mock Interview Drill

### Basic Questions (15)

**Q1: What problem does this project solve?**
- ✅ Strong: "It predicts which telecom customers are about to churn and explains why, so the retention team can take targeted action before they leave."
- ❌ Weak: "It predicts churn." (No business context)

**Q2: What dataset did you use?**
- ✅ Strong: "IBM Telco Customer Churn — 7,043 records, 21 features, 26.5% churn rate. It's a well-known benchmark dataset for classification problems."
- ❌ Weak: "Some telecom dataset from Kaggle."

**Q3: Why did you pick XGBoost?**
- ✅ Strong: "XGBoost consistently outperforms on tabular data. I also evaluated Logistic Regression for interpretability and Random Forest as a baseline ensemble. XGBoost achieved the highest ROC-AUC of 84.5%."
- ❌ Weak: "Because everyone uses it." (Shows no reasoning)

**Q4: What is ROC-AUC and why did you use it?**
- ✅ Strong: "ROC-AUC measures the probability that the model ranks a random positive higher than a random negative. I used it because our dataset is imbalanced (74/26), so accuracy alone would be misleading—a model that always predicts 'no churn' gets 74% accuracy."
- ❌ Weak: "It's a metric for classification."

**Q5: What is SMOTE?**
- ✅ Strong: "Synthetic Minority Over-sampling Technique. It generates synthetic churn examples by interpolating between existing minority samples in feature space. I used it inside an imblearn Pipeline so it's only applied to training folds, preventing data leakage."
- ❌ Weak: "It balances the data." (No understanding of how or leakage risk)

**Q6: How do you handle missing values in TotalCharges?**
- ✅ Strong: "11 records have blank TotalCharges, all with tenure=0 (new customers). I fill these with MonthlyCharges because a new customer's total is exactly one month's charge."
- ❌ Weak: "I dropped them."

**Q7: What feature engineering did you do?**
- ✅ Strong: "Six features: tenure_bucket (categorical binning), spending_category (tertile-based), estimated_clv (tenure × monthly charges), has_internet (boolean), is_month_to_month (boolean), age_group (Senior/Non-Senior)."
- ❌ Weak: "I added some features."

**Q8: How does the API validate input?**
- ✅ Strong: "Pydantic schemas with regex patterns for categorical fields like `^(Male|Female)$`, enum types for Contract/Internet/Payment, and numeric bounds like `tenure: ge=0, le=100` and `MonthlyCharges: gt=0, le=500`."
- ❌ Weak: "FastAPI handles it."

**Q9: What's the difference between `@st.cache_data` and `@st.cache_resource`?**
- ✅ Strong: "`cache_data` serializes the return value (works for DataFrames), reruns if input changes. `cache_resource` doesn't serialize—used for things like ML models that can't be pickled or shouldn't be duplicated in memory."
- ❌ Weak: "They both cache things."

**Q10: Why Streamlit over Flask/React?**
- ✅ Strong: "Rapid prototyping with zero JavaScript. For a portfolio project, I needed a polished dashboard in hours, not weeks. For production, I'd use React with a design system."

**Q11: What does your CI pipeline do?**
- ✅ Strong: "On every push to main: ruff lint → ruff format check → mypy type check → pytest with coverage → upload to Codecov."

**Q12: Why Docker multi-stage build?**
- ✅ Strong: "Stage 1 installs dependencies with pip (includes build tools). Stage 2 copies only site-packages. Result: smaller image, no pip cache or build tools in production."

**Q13: What is Alembic?**
- ✅ Strong: "Database migration tool for SQLAlchemy. It versions your schema so you can upgrade/downgrade the database alongside code deployments. Like Flyway for Java."

**Q14: How do you compute CLV?**
- ✅ Strong: "Simplified as `tenure × MonthlyCharges`. A real CLV model would use survival analysis (Kaplan-Meier) or probabilistic models (BG/NBD). This is a reasonable approximation for a portfolio project."

**Q15: Why PostgreSQL?**
- ✅ Strong: "ACID transactions, window functions for analytics, JSONB for semi-structured data, and it's the industry standard for data science workloads."

### Advanced Questions (15)

**Q1: How do you prevent data leakage with SMOTE?**
- ✅ Strong: "SMOTE is a step inside the imblearn Pipeline, which means it's only applied during `fit()` on training data. During cross-validation, each fold only sees SMOTE-augmented training data; the validation fold is untouched."

**Q2: Why is your recall so high (95%) but precision so low (42%)?**
- ✅ Strong: "I deliberately lowered the threshold from 0.5 to ~0.13 using cost-sensitive optimization. Missing a churner costs $45, flagging a false positive costs only $5. The business prefers high recall because the cost of inaction is 9× the cost of a false alarm."

**Q3: What happens if you deploy this model and the data distribution shifts?**
- ✅ Strong: "Model performance would degrade—concept drift. I'd implement: (1) monitoring predicted probability distribution for PSI (Population Stability Index), (2) periodic retraining triggers when PSI exceeds a threshold, (3) A/B testing new models against the incumbent."

**Q4: Your Optuna uses only 10 trials. Is that sufficient?**
- ✅ Strong: "No, 10 trials is minimal—I used it for pipeline speed. In production, I'd run 50-200 trials with Optuna's MedianPruner to early-stop unpromising trials. With 10 trials, I might miss the global optimum."

**Q5: How would you serve this model at 10,000 QPS?**
- ✅ Strong: "Replace joblib with ONNX Runtime for faster inference. Deploy behind a load balancer with multiple Gunicorn workers. Add Redis for caching frequent predictions. Use async FastAPI with asyncio. For 10K+ QPS, consider gRPC + Triton Inference Server."

**Q6: Why is your SHAP using `__import__('sklearn')`?**
- ✅ Strong: "Honestly, that's a code smell I should fix. It dynamically imports at runtime to check if the model is LogisticRegression. The proper approach is `from sklearn.linear_model import LogisticRegression` at the top of the file and use `isinstance()` normally."

**Q7: How would you add A/B testing for retention strategies?**
- ✅ Strong: "After the model predicts high-risk customers, randomly assign them to control (no intervention) and treatment (retention offer) groups. Track churn rates at 30/60/90 days. Use chi-square test to determine if the treatment group has statistically significant lower churn."

**Q8: Your confusion matrix uses test data for threshold optimization. Why is this a problem?**
- ✅ Strong: "It's a form of information leakage—the threshold is optimized on the test set, so test metrics are optimistically biased. The correct approach is to optimize on a validation set (or within CV folds) and report on a held-out test set."

**Q9: How does ColumnTransformer handle unseen categories?**
- ✅ Strong: "I set `handle_unknown='ignore'` in OneHotEncoder. Unknown categories get all-zero encoding. This prevents crashes at prediction time but means the model treats unknowns as 'none of the above'."

**Q10: What would you change about this architecture for a real enterprise?**
- ✅ Strong: "Replace Streamlit with React. Add Redis caching. Use Airflow for pipeline orchestration. Deploy model to SageMaker or Vertex AI. Add Prometheus + Grafana. Use PostgreSQL (not SQLite) for MLflow. Add authentication (OAuth2). Add feature store (Feast)."

**Q11: How do you handle the class imbalance at 74/26?**
- ✅ Strong: "Three strategies: (1) SMOTE for oversampling minority class, (2) `class_weight='balanced'` on Random Forest, (3) cost-sensitive threshold optimization. SMOTE creates synthetic examples; class weights adjust the loss function; threshold optimization adjusts the decision boundary."

**Q12: Explain Cramér's V.**
- ✅ Strong: "It's an effect size measure for chi-square tests, ranging from 0 (no association) to 1 (perfect association). Formula: `sqrt(χ² / (n × (min(r,c) - 1)))`. I use it to quantify not just whether Contract affects churn (p-value) but how strongly."

**Q13: Why Mann-Whitney U instead of t-test?**
- ✅ Strong: "Mann-Whitney is non-parametric—it doesn't assume normality. Tenure and MonthlyCharges distributions are skewed, so t-test assumptions would be violated. Mann-Whitney tests whether one group tends to have larger values than the other."

**Q14: How would you implement model versioning?**
- ✅ Strong: "MLflow Model Registry: register each model with a version number, transition between 'Staging' and 'Production' stages. The serving layer loads whichever model is in 'Production'. Roll back by transitioning back to the previous version."

**Q15: What if a customer's data has all 'No internet service' for service columns?**
- ✅ Strong: "The model handles it because OneHotEncoder creates a column for 'No internet service'. These customers typically have lower churn because they're simpler plans. The SHAP value for these features would show decreased risk."

---

## 22. Final Project Mastery Cheatsheet

### 2-Minute Explanation
"I built a churn prediction system for telecom. It takes raw customer data, cleans it, engineers features like CLV and tenure buckets, trains three models with SMOTE for class imbalance, and tunes XGBoost with Bayesian optimization. The best model gets 84.5% ROC-AUC. I serve predictions through a FastAPI REST API and a Streamlit dashboard that includes per-customer SHAP explanations. The whole thing is containerized with Docker and has CI/CD with GitHub Actions."

### Top 20 Talking Points
1. SMOTE inside imblearn Pipeline prevents data leakage
2. Cost-sensitive threshold: FN costs 9× more than FP
3. SHAP for both global importance and per-customer explanations
4. Statistical significance tests (chi-square, Mann-Whitney) validate churn drivers
5. FastAPI with Pydantic schemas and batch prediction endpoint
6. Optuna Bayesian HPO with 5-fold stratified CV
7. Custom exception hierarchy (6 exception types)
8. Pydantic-settings for 12-factor config management
9. Multi-stage Docker build with non-root user
10. GitHub Actions CI: ruff + mypy + pytest + codecov
11. Alembic for database schema migrations
12. MLflow experiment tracking with SQLite backend
13. 6-tab Streamlit dashboard with interactive filters
14. Cohort retention analysis with heatmaps
15. Revenue impact quantification ($139K/month lost)
16. Pre-commit hooks (ruff + mypy)
17. `@log_step` decorator for pipeline instrumentation
18. Dependency injection via FastAPI's `Depends()`
19. `@st.cache_resource` for model singleton in dashboard
20. Customer Deep Dive with per-row selection and SHAP waterfall

### Top 20 Interviewer Traps
1. "Why only 6 tests?" — Acknowledge it; describe what you'd add
2. "CORS wildcard is a security hole" — Acknowledge; explain production fix
3. "Your threshold is optimized on test data" — Acknowledge the leakage; explain CV-based alternative
4. "10 Optuna trials is too few" — Agree; explain it's for speed; production would use 50+
5. "Why not use a feature store?" — Explain scope tradeoff; recommend Feast for production
6. "How would this handle 1M customers?" — Polars for data processing, Redis for caching, model serving framework
7. "Your README metrics don't match pipeline output" — Explain they drift between runs; should pin to specific run
8. "Why is app.py 664 lines?" — Acknowledge; explain multipage app pattern
9. "No authentication on the API" — Acknowledge; describe API key or OAuth2 approach
10. "Explain your SHAP computation complexity" — TreeExplainer is O(TLD²); KernelExplainer is O(2^F)
11. "What if a new payment method is introduced?" — `handle_unknown='ignore'` gives all-zero encoding
12. "Your model uses TotalCharges — isn't that leaking the target?" — No, TotalCharges is historical billing, not future churn
13. "Why not deep learning?" — Tabular data; XGBoost consistently outperforms NNs on structured data under ~100K rows
14. "How do you know the model is calibrated?" — I don't check calibration; I'd add Platt scaling or isotonic regression
15. "What's your data drift detection strategy?" — Currently none; recommend PSI monitoring
16. "Why SQLite for MLflow?" — Development convenience; production would use PostgreSQL
17. "The pickle model is a security risk" — Acknowledge; recommend ONNX or model hash verification
18. "How do you roll back a bad model?" — Currently no mechanism; recommend MLflow Model Registry stage transitions
19. "Your CLV formula is too simplistic" — Agree; recommend survival analysis for production
20. "Why no feature selection?" — I rely on the model's inherent feature importance; could add RFE or L1 regularization

---

## 23. Feature Deep Dive Cross-Examination

### Feature: Cost-Sensitive Threshold Optimization

**Business purpose**: Align model decisions with business economics

**Implementation**: `src/ml_models.py:66-82`
```python
def find_optimal_threshold(y_true, y_proba, fn_cost=45, fp_cost=5) -> float:
    for threshold in thresholds:
        cost = (fn * fn_cost) + (fp * fp_cost)
        if cost < min_cost:
            best_threshold = threshold
```

**Level 1 Q**: What is a decision threshold?
- ✅ "The probability cutoff above which we predict 'churn'. Default is 0.5, but optimal depends on business costs."

**Level 2 Q**: Why not just use 0.5?
- ✅ "Because the cost of missing a churner ($45) is 9× the cost of a false positive ($5). Lowering the threshold catches more churners at the expense of more false alarms—but that's the right tradeoff."

**Level 3 Q**: Where did $45 and $5 come from?
- ✅ "ASSUMPTION: These are illustrative values. In production, you'd work with the finance team to calculate actual customer acquisition cost (CAC) for fn_cost and retention campaign cost for fp_cost."

**Level 4 Q**: How would you optimize the threshold without test data leakage?
- ✅ "Use nested cross-validation: outer loop for performance estimation, inner loop for threshold optimization. Or use a dedicated validation set separate from the test set."

**Level 5 Q**: What if costs change dynamically?
- ✅ "Store the model's raw probabilities and apply the threshold at serving time. When costs change, recalculate the threshold without retraining. This is the advantage of probability-based models over hard classifiers."

---

## 24. Code Walkthrough Preparation

### Module: `src/ml_models.py` — The Heart of the System

**How to explain during interview**:
"Let me walk you through the training pipeline. The `train_models()` function at line 123 takes the enriched DataFrame and:

1. **Splits** the data 80/20 with stratification (line 133-135) — stratified means the churn ratio is preserved in both sets
2. **Builds a preprocessor** (line 137) — ColumnTransformer that applies StandardScaler to numeric columns and OneHotEncoder to categoricals
3. **Tunes XGBoost** (lines 159-183) — Optuna creates an objective function that evaluates each hyperparameter set with 5-fold CV, using ROC-AUC as the metric
4. **Trains all candidates** (lines 196-231) — Each model gets wrapped in an imblearn Pipeline with preprocessor → SMOTE → model. After training, I find the optimal threshold using cost-sensitive optimization
5. **Logs to MLflow** (lines 226-231) — Each model's params, metrics, and serialized model are logged
6. **Selects best model** (lines 233-236) — Sorted by ROC-AUC; best model is saved to disk"

**Likely follow-up**: "Why is SMOTE a pipeline step and not applied separately?"
**Answer**: "If I applied SMOTE before splitting into CV folds, synthetic samples from the training set could end up in the validation fold — that's data leakage. The imblearn Pipeline ensures SMOTE only runs during `fit()`, not during `predict()` or `score()`."

---

## 25. Question Tree Expansion

### Topic: SMOTE and Class Imbalance

**L1**: What is class imbalance?
- ✅ "When one class significantly outnumbers another. Here, 74% are non-churn, 26% are churn."

**L2**: How does SMOTE work?
- ✅ "For each minority sample, SMOTE finds its k nearest neighbors, picks one at random, and creates a new synthetic sample along the line segment between them in feature space."

**L3**: What are SMOTE's limitations?
- ✅ "It can generate noisy samples if minority and majority classes overlap. It doesn't work well with very high-dimensional or sparse data. It can also amplify outliers if they're used as seed points."

**L4**: What alternatives exist?
- ✅ "ADASYN (Adaptive Synthetic), BorderlineSMOTE (only generates near decision boundary), class_weight='balanced' (adjusts loss function), or focal loss for neural networks."

**L5**: When would you NOT use SMOTE?
- ✅ "When the imbalance ratio is mild (<60/40), or when the dataset is very small (SMOTE needs enough minority samples for KNN), or when using models that handle imbalance natively (like XGBoost's scale_pos_weight)."

**L6**: At production scale with 10M records and 1% positive rate?
- ✅ "SMOTE would be impractical—generating 99× synthetic data is memory-intensive. I'd use undersampling (random or Tomek links), or train with scale_pos_weight in XGBoost, or use focal loss."

---

## 26. Project Structure & Code Organization

```
Churn Analytics/
├── src/                    # Core business logic (12 modules)
│   ├── config.py           # Pydantic-settings, path constants
│   ├── logger.py           # Structured logging, @log_step decorator
│   ├── exceptions.py       # Custom exception hierarchy
│   ├── data_cleaning.py    # Load, clean, quality report
│   ├── features.py         # Feature engineering, feature list
│   ├── ml_models.py        # Training, evaluation, Optuna HPO
│   ├── explainability.py   # SHAP explainer factory, explanations
│   ├── statistical_tests.py # Chi-square, Mann-Whitney
│   ├── cohort_analysis.py  # Retention cohorts
│   ├── experiment_tracking.py # MLflow integration
│   └── db_models.py        # SQLAlchemy ORM model
├── api/                    # FastAPI REST API
│   ├── main.py             # App factory, CORS, routers
│   ├── schemas.py          # Pydantic request/response models
│   ├── dependencies.py     # Model loading with @lru_cache
│   └── routers/
│       ├── predictions.py  # POST /predict, /predict/batch
│       ├── analytics.py    # GET /analytics/summary
│       └── health.py       # GET /health
├── tests/                  # Pytest tests (6 tests)
├── scripts/                # Operational scripts
│   ├── score_all_customers.py
│   ├── load_to_postgres.py
│   └── export_business_report_pdf.py
├── sql/                    # PostgreSQL DDL and analytics
├── alembic/                # Database migrations
├── notebooks/              # Jupyter exploration (3 notebooks)
├── data/raw/               # Source dataset
├── data/processed/         # Cleaned output
├── models/                 # Trained model, metrics, predictions
├── reports/                # Quality reports, feature importance, stats
├── images/                 # Charts, SHAP plots
├── dashboard/              # Power BI docs (secondary)
├── .github/workflows/      # CI/CD pipeline
├── .streamlit/             # Theme config
├── run_pipeline.py         # End-to-end orchestrator
├── app.py                  # Streamlit dashboard
├── Dockerfile              # API container
├── docker-compose.yml      # Multi-service orchestration
├── requirements.txt        # Dependencies
└── pyproject.toml          # Tool configs (ruff, mypy, pytest)
```

**Interview explanation**: "The project follows a layered architecture. `src/` contains all business logic with no framework dependencies — it's pure Python with pandas/sklearn. `api/` is the FastAPI serving layer that imports from `src/`. `app.py` is the Streamlit UI that also imports from `src/`. This means the core ML logic is reusable across both serving interfaces."

---

## 27. API Deep Dive

### `POST /api/v1/predict`

| Aspect | Detail |
|--------|--------|
| Purpose | Single customer churn prediction |
| Auth | None (⚠️) |
| Request | `PredictionRequest` — 20 fields with Pydantic validation |
| Response | `PredictionResponse` — probability, risk_tier, predicted_churn, top_drivers |
| Validation | Regex: gender `^(Male|Female)$`; Enum: Contract, InternetService, PaymentMethod; Range: tenure 0-100, MonthlyCharges 0-500 |
| Error handling | 422 for validation errors (auto), 500 for prediction failures |
| Optional | `?explain=true` adds SHAP top-3 drivers |

### `POST /api/v1/predict/batch`

| Aspect | Detail |
|--------|--------|
| Purpose | Batch prediction from CSV upload |
| Input | `UploadFile` (CSV only, validated by extension) |
| Processing | Read CSV → add engineered features → predict all rows → return list of PredictionResponse |
| Edge case | Missing `customerID` → auto-generates `BATCH_0`, `BATCH_1`, etc. |
| Risk | No file size limit — could OOM on large files |

**Production improvement**: Add `MAX_FILE_SIZE = 10MB` check, pagination for responses, async processing for large batches with job status polling.

---

## 28. Database Query Cross-Examination

### Key Query: Top Risk Segments (`sql/03_analysis_queries.sql:106-117`)

```sql
SELECT contract_type, payment_method, tenure_bucket,
       COUNT(*) AS customers,
       ROUND(100.0 * AVG(CASE WHEN churn THEN 1.0 ELSE 0.0 END), 2) AS churn_rate_pct,
       ROUND(SUM(monthly_charges), 2) AS segment_monthly_revenue
FROM customers
GROUP BY contract_type, payment_method, tenure_bucket
HAVING COUNT(*) >= 50
ORDER BY churn_rate_pct DESC
LIMIT 15;
```

**Q**: Why `HAVING COUNT(*) >= 50`?
- ✅ "Statistical minimum sample size. A segment with 3 customers and 100% churn is noise, not a pattern. 50 is a reasonable minimum for stable rate estimates."

**Q**: What indexes are used?
- ✅ "The GROUP BY hits `idx_customers_contract`, `idx_customers_payment`, and `idx_customers_tenure_bucket`. However, a composite index on `(contract_type, payment_method, tenure_bucket)` would be more efficient since it covers the entire GROUP BY."

**Q**: How would this query perform on 10M rows?
- ✅ "With proper indexes, this is an aggregate scan — O(N) regardless. But the window function for revenue share in another query would benefit from partitioning. I'd also consider materialized views for pre-computed aggregations."

---

## Hidden Interview Traps

### Trap 1: "You said 84.5% ROC-AUC. What's your precision?"
- **Why dangerous**: Precision is 42% — sounds terrible in isolation
- **Strong answer**: "Precision is 42%, which is deliberately low because I optimized the threshold for high recall (95%). In churn prevention, false negatives cost 9× more than false positives. A 42% precision means we call 100 customers and 42 were actually going to churn — that's a good ROI for the retention team."
- **Weak answer**: "Uh, I focused on ROC-AUC."

### Trap 2: "You say 'deployed' — where's the authentication?"
- **Why dangerous**: No auth = not really production-ready
- **Strong answer**: "The Streamlit dashboard doesn't need auth for a demo deployment. The FastAPI API currently has no auth — in production, I'd add API key validation via a `Depends(verify_api_key)` middleware, or OAuth2 with FastAPI's built-in security utilities."
- **Weak answer**: "Streamlit handles it."

### Trap 3: "Your test set threshold optimization"
- **Why dangerous**: Shows a methodological flaw
- **Strong answer**: "You're right — optimizing the threshold on the test set introduces optimistic bias. The honest approach is to optimize within cross-validation folds and report test set metrics with the CV-optimized threshold. I'd fix this by adding a held-out validation set."

### Trap 4: "Why no feature selection?"
- **Why dangerous**: 22 features might include irrelevant ones
- **Strong answer**: "The ColumnTransformer with OneHotEncoder expands to ~40 features. XGBoost's L1/L2 regularization implicitly handles feature selection. I could add explicit feature selection with RFE or SelectFromModel, or check for multicollinearity with VIF."

### Hire Confidence Assessment

**Score: 7/10**

**Biggest Strengths**:
- End-to-end ML system (not just a notebook)
- Demonstrates breadth: data engineering, ML, API, dashboard, DevOps
- Cost-sensitive optimization shows business thinking
- SHAP explainability shows depth beyond accuracy

**Biggest Concerns**:
- Only 6 tests — testing discipline is weak
- No authentication — security awareness gap
- 664-line monolithic dashboard

**What Would Make This Stand Out Among Hundreds of Student Projects**:
1. Add 20+ tests with >80% coverage
2. Add API key auth (even basic)
3. Split app.py into multipage app
4. Add a data drift monitoring script
5. Deploy the API (not just dashboard) with proper health monitoring

---

# Executive Summary

## Top Strengths
1. **Full-stack ML engineering** — raw data to deployed dashboard, not just a notebook
2. **Business-aligned optimization** — cost-sensitive thresholds, revenue impact quantification
3. **Explainability** — SHAP for global and per-customer explanations
4. **Software engineering discipline** — custom exceptions, typed config, CI/CD, Docker
5. **Statistical rigor** — significance tests with effect sizes, not just visual correlations

## Top Weaknesses
1. **Testing** — only 6 tests; insufficient for production confidence
2. **Security** — no auth, CORS wildcard, no rate limiting
3. **Scalability** — single-process, in-memory; breaks at ~50 concurrent users
4. **Dashboard monolith** — 664-line `app.py` should be split
5. **Threshold leakage** — optimized on test set, not validation set

## Top Interview Talking Points
1. SMOTE inside Pipeline prevents data leakage
2. Cost-sensitive threshold: FN costs 9× more than FP
3. SHAP TreeExplainer for per-customer explainability
4. FastAPI with Pydantic validation and batch endpoint
5. Chi-square + Mann-Whitney for statistical validation of churn drivers

## Top Production Improvements
1. Add authentication (API key or OAuth2)
2. Increase test coverage to 80%+
3. Add Prometheus metrics and Grafana dashboards
4. Replace SQLite MLflow with PostgreSQL
5. Add model drift monitoring (PSI)

## Final Readiness Assessment

| Role | Readiness | Notes |
|------|-----------|-------|
| Entry SDE | ✅ 9/10 | Strong demonstration of fundamentals |
| SDE II | ✅ 7/10 | Good architecture; needs more testing |
| Senior SDE | 🟡 5/10 | Security and scalability gaps |
| Data Analyst | ✅ 8/10 | SQL, EDA, statistical tests, dashboards |
| Business Analyst | ✅ 8/10 | Revenue analysis, KPIs, recommendations |
| ML Engineer | 🟡 6/10 | Good ML; needs MLOps maturity |
