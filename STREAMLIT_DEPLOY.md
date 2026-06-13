# Streamlit Dashboard — Run & Deploy

## Local run

```powershell
cd "C:\Users\DELL\OneDrive\Desktop\Churn Analytics"
py -m pip install -r requirements.txt
py run_pipeline.py
py scripts/score_all_customers.py
py -m streamlit run app.py
```

Opens at `http://localhost:8501`

## Deploy to Streamlit Community Cloud (free live URL)

1. Push project to GitHub (see `GITHUB_SETUP.md`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. **New app** → select your repo
5. **Main file path:** `app.py`
6. **Deploy**

Your live URL will look like: `https://your-app-name.streamlit.app`

## Add link to README

```markdown
## Live Dashboard

[View interactive Streamlit dashboard](https://YOUR-APP.streamlit.app)
```

## Required files for deploy

- `app.py`
- `requirements.txt` (must include `streamlit`, `plotly`)
- `dashboard/dashboard_data.csv`
- `reports/feature_importance.csv`

Run the pipeline before committing so CSVs are up to date.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| File not found | Run `py scripts/score_all_customers.py` |
| Deploy fails on import | Check `requirements.txt` has all packages |
| Blank charts after filter | Select at least one value in each sidebar filter |
