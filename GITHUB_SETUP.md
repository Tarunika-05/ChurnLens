# GitHub Setup

## 1. Initialize and commit locally

```powershell
cd "C:\Users\DELL\OneDrive\Desktop\Churn Analytics"
git init
git add .
git commit -m "Add customer churn prediction and analytics portfolio project"
```

## 2. Create GitHub repo

1. Go to [github.com/new](https://github.com/new)
2. Name: `customer-churn-analytics`
3. Do **not** add README (you already have one)
4. Create repository

## 3. Push

Replace `YOUR_USERNAME` with your GitHub username:

```powershell
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/customer-churn-analytics.git
git push -u origin main
```

## 4. README polish for portfolio

After building Power BI:

1. Save screenshots to `images/dashboard_screenshots/`
2. Add to README:

```markdown
## Dashboard Screenshots

![Executive Overview](images/dashboard_screenshots/executive_overview.png)
![Churn Analysis](images/dashboard_screenshots/churn_analysis.png)
```

## 5. Optional: GitHub Pages / profile pin

- Pin the repo on your GitHub profile
- Add live notebook badge linking to the repo
