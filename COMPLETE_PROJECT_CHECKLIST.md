# Complete Project Checklist — Publish to Web

Use this list in order. Items marked **DONE** are already in your repo.

---

## Phase A — Local setup (15 min)

- [ ] **DONE** — Project files exist in `Churn Analytics` folder
- [ ] Install Python packages:
  ```powershell
  cd "C:\Users\DELL\OneDrive\Desktop\Churn Analytics"
  py -m pip install -r requirements.txt
  ```
- [ ] Run the full pipeline:
  ```powershell
  py run_pipeline.py
  py scripts/score_all_customers.py
  py scripts/export_business_report_pdf.py
  ```
- [ ] Confirm these files exist:
  - `dashboard/dashboard_data.csv`
  - `reports/feature_importance.csv`
  - `reports/business_report.pdf`
  - `models/best_model.pkl`
  - `images/*.png`

---

## Phase B — Review notebooks (optional, 30 min)

Open in Jupyter or VS Code and run top to bottom:

- [ ] `notebooks/01_data_cleaning.ipynb`
- [ ] `notebooks/02_eda.ipynb`
- [ ] `notebooks/03_ml_modeling.ipynb`

*(Skip if you trust the pipeline — outputs are already generated.)*

---

## Phase C — Streamlit dashboard (5 min local / 15 min deploy)

```powershell
py -m streamlit run app.py
```

Deploy live URL: `STREAMLIT_DEPLOY.md`

---

## Phase C (optional) — Build Power BI report (30–45 min)

**Requires:** [Power BI Desktop](https://www.microsoft.com/power-platform/products/power-bi/desktop) (free)

### C1. Import data

1. Open **Power BI Desktop**
2. **Home → Get data → Text/CSV**
3. Import:
   - `dashboard/dashboard_data.csv`
   - `reports/feature_importance.csv`
4. **Transform Data** → confirm types:
   - `churn_flag` → True/False
   - `churn_probability` → Decimal
   - `MonthlyCharges`, `estimated_clv` → Decimal
5. **Close & Apply**

### C2. Create measures

**Modeling → New measure** — paste each measure from `dashboard/power_bi_measures.dax`:

- `Total Customers`
- `Churn Rate` → format as **Percentage**
- `Monthly Revenue` → format as **Currency**
- `Revenue Lost` → format as **Currency**
- `Avg CLV`
- `High Risk Customers`

### C3. Build 4 pages

Follow `dashboard/POWER_BI_WALKTHROUGH.md`:

| Page | Visuals |
|------|---------|
| **Executive Overview** | 4 KPI cards, slicers (Contract, InternetService, spending_category), churn donut |
| **Churn Analysis** | Bar by Contract, stacked column by tenure_bucket, donut by PaymentMethod |
| **Revenue Insights** | Bar by spending_category, CLV card, avg charges by tenure |
| **Churn Prediction** | Top 100 table (sort by churn_probability), histogram, feature importance bar |

**Design:** Churn red `#E94F37`, retained teal `#2E86AB`

### C4. Save

- [ ] **File → Save as** → `dashboard/churn_dashboard.pbix`

---

## Phase D — Deploy Streamlit to web (10 min)

1. Push repo to GitHub
2. [share.streamlit.io](https://share.streamlit.io) → New app → `app.py`
3. Copy live URL → add to README

---

## Phase D (optional) — Power BI publish to web (10 min)

### D1. Sign in and publish

1. In Power BI Desktop: **Home → Sign in** (Microsoft account)
2. **Home → Publish**
3. Select **My workspace** (or a workspace you own)
4. Wait for “Success” → click **Open 'churn_dashboard.pbix' in Power BI**

### D2. Publish to web (public link)

1. On [app.powerbi.com](https://app.powerbi.com), open your report
2. **File** (top left) → **Embed report** → **Publish to web (public)**
3. Read the warning (data will be public) → **Create embed code**
4. Copy the **link** (starts with `https://app.powerbi.com/view?r=...`)

> If “Publish to web” is disabled, your org may block it. Use a personal Microsoft account or ask IT to enable it.

### D3. Test the link

- [ ] Open the link in an **Incognito/private** browser window
- [ ] Confirm all 4 pages load and filters work

---

## Phase E — Portfolio polish (20 min)

### E1. Screenshots

1. In Power BI Desktop or the published report, capture each page
2. Save to `images/dashboard_screenshots/`:
   - `executive_overview.png`
   - `churn_analysis.png`
   - `revenue_insights.png`
   - `churn_prediction.png`

### E2. Update README

Add your live link and screenshots to `README.md`:

```markdown
## Live Dashboard

**[View interactive dashboard on Power BI](YOUR_PUBLISH_TO_WEB_LINK)**

![Executive Overview](images/dashboard_screenshots/executive_overview.png)
```

Replace `YOUR_PUBLISH_TO_WEB_LINK` with the URL from Phase D2.

### E3. Push to GitHub

```powershell
cd "C:\Users\DELL\OneDrive\Desktop\Churn Analytics"
git add .
git commit -m "Complete churn analytics project with Power BI publish-to-web link"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/customer-churn-analytics.git
git push -u origin main
```

Create the empty repo on GitHub first: [github.com/new](https://github.com/new)

---

## Phase F — Optional extras

| Task | When |
|------|------|
| PostgreSQL + SQL queries | If you want to demo SQL in interviews |
| Scheduled refresh | Upload CSV to OneDrive, reconnect in Power BI, schedule daily refresh |
| Resume | Use bullets from README “Resume Bullets” section |

---

## You’re done when

- [ ] Pipeline runs without errors
- [ ] `churn_dashboard.pbix` saved locally
- [ ] Report published to Power BI Service
- [ ] **Publish to web** link works in incognito
- [ ] README has live link + screenshots
- [ ] Code pushed to GitHub

---

## Quick reference

| Guide | Purpose |
|-------|---------|
| `dashboard/POWER_BI_WALKTHROUGH.md` | Build each page |
| `dashboard/power_bi_measures.dax` | Copy-paste DAX |
| `dashboard/POWER_BI_DEPLOY.md` | Full deploy options |
| `GITHUB_SETUP.md` | Git commands |

**Estimated total time remaining:** ~1–2 hours (mostly Power BI build + publish)
