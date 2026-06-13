# Deploy Power BI for Live Users

This project uses **Power BI only** for the live dashboard. GitHub hosts the code and data pipeline; **Power BI Service** (cloud) is where users open the interactive report.

```text
Python pipeline  →  CSV files  →  Power BI Desktop (.pbix)  →  Publish  →  app.powerbi.com  →  Users
```

---

## Prerequisites

| Requirement | Notes |
|-------------|--------|
| **Power BI Desktop** | Free — build the report locally |
| **Microsoft account** | Work or school account recommended |
| **Power BI Pro license** | Required to **share** with other users (~$10/user/month). Free license = only you can view published reports |
| **Power BI Premium / Fabric** | Optional — for large orgs or “Publish to web” at scale |

Build the report first: `POWER_BI_WALKTHROUGH.md`

---

## Step 1 — Prepare data for the cloud

Before publishing, refresh local data:

```powershell
cd "C:\Users\DELL\OneDrive\Desktop\Churn Analytics"
py run_pipeline.py
py scripts/score_all_customers.py
```

Files Power BI will use:

| File | Purpose |
|------|---------|
| `dashboard/dashboard_data.csv` | Main dataset (customers + churn scores) |
| `reports/feature_importance.csv` | Feature importance page |

---

## Step 2 — Build and publish

1. Open **Power BI Desktop**
2. **Get data → Text/CSV** → import both files above
3. Build all 4 pages (`POWER_BI_WALKTHROUGH.md`)
4. **File → Save as** → `dashboard/churn_dashboard.pbix`
5. **Home → Publish** → sign in → select a **workspace**

After publish, open [app.powerbi.com](https://app.powerbi.com) → your workspace → confirm **Churn Dashboard** appears under **Reports**.

---

## Step 3 — How users see the dashboard (pick one)

### Option A — Share report (team / internal users) — recommended

Best for colleagues, managers, or stakeholders with Microsoft accounts.

1. On app.powerbi.com, open the report
2. Click **Share**
3. Enter user emails → set **Allow recipients to view** (or build permission)
4. Users get an email link → opens live, interactive Power BI in the browser

**Requires:** Power BI Pro for you and each viewer (or Premium capacity in your org).

---

### Option B — Power BI App (polished distribution)

Best when many users need one entry point (e.g. “Executive Analytics” app).

1. In the workspace: **Create app**
2. Add your churn report + optional description
3. **Publish app** → share app link with users
4. Users install/open the app from app.powerbi.com or mobile

Users see a branded app tile, not raw workspace files.

---

### Option C — Publish to web (public, no login)

Best for **portfolio demos** where anyone with the link can view (read-only).

1. Open report on app.powerbi.com
2. **File → Embed report → Publish to web (public)**
3. Copy the **embed link** or iframe
4. Add link to your README, LinkedIn, or company intranet

**Warning:** Data is public. Fine for sample IBM data; **do not use for real customer PII.**

---

## Step 4 — Keep the dashboard live (scheduled refresh)

Published reports go stale unless data refreshes. Choose one source:

### A. OneDrive / SharePoint (simplest for CSV)

1. Upload `dashboard/dashboard_data.csv` and `feature_importance.csv` to **OneDrive** or **SharePoint**
2. In Power BI Desktop: **Transform data → Data source settings** → point to cloud path
3. Re-publish the report
4. On app.powerbi.com: **Dataset → Schedule refresh** (e.g. daily at 6 AM)

Each time your Python pipeline runs, overwrite the OneDrive CSV → Power BI refreshes on schedule.

### B. PostgreSQL (production-style)

1. Run `py scripts/load_to_postgres.py` after each pipeline run
2. In Power BI Desktop: **Get data → PostgreSQL**
3. Install **On-premises data gateway** if DB is not public cloud
4. Schedule refresh in Power BI Service

Use this when data lives in a company database, not local files.

### C. Manual refresh (portfolio / demo)

1. Re-run `py run_pipeline.py` and `py scripts/score_all_customers.py`
2. In Power BI Desktop: **Refresh** → **Publish** again

Fine for interviews; not ideal for daily business users.

---

## End-to-end deployment flow

```text
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  run_pipeline   │────▶│ dashboard_data   │────▶│ Power BI Desktop│
│  (scheduled job)│     │ .csv on OneDrive │     │ churn_dashboard │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │ Publish
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Users (browser)│◀────│ Share / App /    │◀────│ Power BI Service│
│  app.powerbi.com│     │ Publish to web   │     │ Scheduled refresh│
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

**GitHub** = code + documentation  
**Power BI Service** = live dashboard for users

---

## What to put in your README (portfolio)

After Option C (publish to web):

```markdown
## Live Dashboard

[View interactive Power BI dashboard](https://app.powerbi.com/view?r=YOUR_EMBED_ID)
```

After Option A/B (internal):

```markdown
## Dashboard

Interactive Power BI report published to [Company] workspace. Available to authorized stakeholders via Power BI App.
```

Add screenshots in `images/dashboard_screenshots/` for GitHub visitors who don’t have access.

---

## Licensing quick reference

| Scenario | License |
|----------|---------|
| Only you view the published report | Free (My workspace) |
| Share with other users | **Power BI Pro** (each user) or org **Premium** |
| Public portfolio link | Free + Publish to web |
| Embed in your website | Pro or Premium + embed token setup |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Publish button grayed out | Sign in to Power BI Desktop with work/school account |
| Users can’t open shared report | They need Pro, or move report to Premium workspace |
| Scheduled refresh fails | CSV must be on OneDrive/SharePoint, not local `C:\` path |
| Stale churn scores | Re-run pipeline, update cloud CSV, trigger refresh |
| Gateway required | PostgreSQL/on-prem sources need [data gateway](https://learn.microsoft.com/power-bi/connect-data/service-gateway-onprem) |

---

## Checklist — live for users

- [ ] Build report in Power BI Desktop (`POWER_BI_WALKTHROUGH.md`)
- [ ] Save `dashboard/churn_dashboard.pbix`
- [ ] Publish to a workspace on app.powerbi.com
- [ ] Configure data source on cloud (OneDrive/SharePoint or PostgreSQL)
- [ ] Enable scheduled refresh
- [ ] Share via **Share**, **App**, or **Publish to web**
- [ ] Add live link + screenshots to README

Power BI is the only live dashboard surface for this project — no separate web app required.
