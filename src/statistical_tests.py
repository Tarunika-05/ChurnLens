"""Statistical significance testing for churn drivers."""
import contextlib

import numpy as np
import pandas as pd
from scipy import stats


def chi_square_churn_test(df: pd.DataFrame, column: str) -> dict:
    """Chi-square test of independence for churn vs categorical variable."""
    contingency = pd.crosstab(df[column], df["churn_flag"])
    chi2, p_value, _dof, _expected = stats.chi2_contingency(contingency)
    n = len(df)
    cramers_v = np.sqrt(chi2 / (n * (min(contingency.shape) - 1)))
    return {
        "column": column,
        "test_type": "Chi-Square",
        "statistic": float(chi2),
        "p_value": float(p_value),
        "effect_size_metric": "Cramer's V",
        "effect_size": float(cramers_v),
        "significant": bool(p_value < 0.05)
    }

def mann_whitney_churn_test(df: pd.DataFrame, column: str) -> dict:
    """Mann-Whitney U test for churn vs continuous variable."""
    group1 = df[df["churn_flag"]][column].dropna()
    group2 = df[not df["churn_flag"]][column].dropna()

    stat, p_value = stats.mannwhitneyu(group1, group2, alternative='two-sided')

    # Rank-biserial correlation for effect size
    n1, n2 = len(group1), len(group2)
    n1 * n2 / 2
    r = 1 - (2 * stat) / (n1 * n2)  # Assuming stat is for group1

    return {
        "column": column,
        "test_type": "Mann-Whitney U",
        "statistic": float(stat),
        "p_value": float(p_value),
        "effect_size_metric": "Rank-biserial",
        "effect_size": float(abs(r)),
        "significant": bool(p_value < 0.05)
    }

def run_all_significance_tests(df: pd.DataFrame) -> pd.DataFrame:
    """Run all statistical tests and return summary table."""
    results = []

    # Identify categorical and continuous columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    cat_cols = [c for c in cat_cols if c not in ['customerID', 'Churn', 'churn_flag', 'risk_tier']]

    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    num_cols = [c for c in num_cols if c not in ['churn_probability', 'predicted_churn', 'actual_churn']]

    for col in cat_cols:
        if df[col].nunique() > 1:
            with contextlib.suppress(Exception):
                results.append(chi_square_churn_test(df, col))

    for col in num_cols:
        if df[col].nunique() > 1:
            with contextlib.suppress(Exception):
                results.append(mann_whitney_churn_test(df, col))

    return pd.DataFrame(results).sort_values('p_value')
