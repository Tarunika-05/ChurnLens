"""Tests for feature engineering."""

from src.features import add_engineered_features


def test_add_engineered_features(sample_clean_data):
    """Test that all engineered features are added correctly."""
    df = add_engineered_features(sample_clean_data)

    assert "tenure_bucket" in df.columns
    assert "spending_category" in df.columns
    assert "estimated_clv" in df.columns

    # Check specific logic
    assert df.loc[df["tenure"] == 1, "tenure_bucket"].iloc[0] == "0-12 months"
    assert df.loc[df["tenure"] == 34, "tenure_bucket"].iloc[0] == "24-48 months"

    # Check CLV calculation
    # CLV = tenure * MonthlyCharges
    expected_clv_001 = 1 * 29.85
    assert df.loc[df["customerID"] == "001", "estimated_clv"].iloc[0] == expected_clv_001
