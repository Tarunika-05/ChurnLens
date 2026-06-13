"""Cohort retention analysis for churn analytics."""
import pandas as pd
import numpy as np

def build_tenure_cohorts(df: pd.DataFrame) -> pd.DataFrame:
    """Build retention matrix by tenure cohort and service tier."""
    df_cohort = df.copy()
    
    # We use tenure_bucket as the cohort and InternetService as the segment
    # A customer is retained if they haven't churned
    df_cohort['retained'] = (df_cohort['Churn'] == 'No').astype(int)
    
    cohort_data = df_cohort.groupby(['tenure_bucket', 'InternetService']).agg(
        total_customers=('customerID', 'count'),
        retained_customers=('retained', 'sum')
    ).reset_index()
    
    cohort_data['retention_rate'] = cohort_data['retained_customers'] / cohort_data['total_customers']
    return cohort_data

def build_retention_heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    """Create pivot table for retention heatmap."""
    cohort_data = build_tenure_cohorts(df)
    pivot = cohort_data.pivot(index='InternetService', columns='tenure_bucket', values='retention_rate')
    
    # Reorder columns to ensure logical progression if they exist
    expected_cols = ["0-12 months", "12-24 months", "24-48 months", "48+ months"]
    available_cols = [c for c in expected_cols if c in pivot.columns]
    pivot = pivot[available_cols]
    
    return pivot

def compute_cohort_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute churn rate, avg CLV, avg monthly by cohort."""
    df_cohort = df.copy()
    df_cohort['churned'] = (df_cohort['Churn'] == 'Yes').astype(int)
    
    metrics = df_cohort.groupby('tenure_bucket').agg(
        total_customers=('customerID', 'count'),
        churn_rate=('churned', 'mean'),
        avg_monthly_revenue=('MonthlyCharges', 'mean'),
        total_monthly_revenue=('MonthlyCharges', 'sum')
    ).reset_index()
    
    # Format
    metrics['churn_rate'] = (metrics['churn_rate'] * 100).round(1).astype(str) + '%'
    metrics['avg_monthly_revenue'] = metrics['avg_monthly_revenue'].round(2)
    metrics['total_monthly_revenue'] = metrics['total_monthly_revenue'].round(2)
    
    return metrics
