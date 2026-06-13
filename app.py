"""Customer Churn Analytics — Streamlit executive dashboard."""

from __future__ import annotations

import joblib
from pathlib import Path
from src.features import add_engineered_features, get_model_features
from src.config import MODEL_PATH

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "dashboard" / "dashboard_data.csv"
IMPORTANCE_PATH = ROOT / "reports" / "feature_importance.csv"
SHAP_SUMMARY_PATH = ROOT / "images" / "shap_summary.png"

CHURN_RED = "#E94F37"
RETAINED_TEAL = "#2E86AB"
ACCENT = "#1B4965"
TENURE_ORDER = ["0-12 months", "12-24 months", "24-48 months", "48+ months"]
SPENDING_ORDER = ["Low Value", "Medium Value", "High Value"]


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    try:
        customers = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        st.error(f"Dashboard data file not found at {DATA_PATH}. Please run the pipeline first.")
        st.stop()
    except Exception as e:
        st.error(f"Failed to load dashboard data: {str(e)}")
        st.stop()
        
    customers["churn_flag"] = customers["churn_flag"].map(
        {"True": True, "False": False, True: True, False: False}
    )
    customers["risk_tier"] = customers["risk_tier"].fillna("Unknown").astype(str)
    importance = pd.read_csv(IMPORTANCE_PATH)
    importance["feature_label"] = importance["feature"].str.replace(
        r"^(num__|cat__)", "", regex=True
    )
    
    stats_path = ROOT / "reports" / "statistical_tests.csv"
    if stats_path.exists():
        stats = pd.read_csv(stats_path)
    else:
        stats = pd.DataFrame()
        
    return customers, importance, stats

@st.cache_resource
def get_trained_model():
    try:
        return joblib.load(MODEL_PATH)
    except Exception as e:
        return None

@st.cache_resource
def get_shap_components(_model):
    try:
        from src.explainability import get_shap_explainer
        df = pd.read_csv(DATA_PATH)
        features = get_model_features()
        X_bg = df[features].sample(min(100, len(df)), random_state=42)
        return get_shap_explainer(_model, X_bg)
    except Exception as e:
        return None, None


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()
    if st.session_state.get("filter_contract"):
        filtered = filtered[filtered["Contract"].isin(st.session_state["filter_contract"])]
    if st.session_state.get("filter_internet"):
        filtered = filtered[filtered["InternetService"].isin(st.session_state["filter_internet"])]
    if st.session_state.get("filter_spending"):
        filtered = filtered[filtered["spending_category"].isin(st.session_state["filter_spending"])]
    return filtered


def kpi_row(df: pd.DataFrame) -> None:
    total = len(df)
    churned = int(df["churn_flag"].sum())
    active = total - churned
    churn_rate = (churned / total * 100) if total else 0
    monthly_revenue = df.loc[~df["churn_flag"], "MonthlyCharges"].sum()
    revenue_lost = df.loc[df["churn_flag"], "MonthlyCharges"].sum()
    avg_clv = df["estimated_clv"].mean()
    high_risk = int((df["risk_tier"] == "High").sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Customers", f"{total:,}")
    c2.metric("Churn Rate", f"{churn_rate:.1f}%")
    c3.metric("Monthly Revenue", f"${monthly_revenue:,.0f}")
    c4.metric("Revenue Lost", f"${revenue_lost:,.0f}")

    c5, c6, c7 = st.columns(3)
    c5.metric("Active Customers", f"{active:,}")
    c6.metric("Avg CLV", f"${avg_clv:,.0f}")
    c7.metric("High Risk Customers", f"{high_risk:,}")


def page_executive(df: pd.DataFrame) -> None:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Executive Overview")
    with col2:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Export Filtered Data (CSV)",
            data=csv,
            file_name="telecom_churn_export.csv",
            mime="text/csv",
        )

    kpi_row(df)

    col1, col2 = st.columns(2)
    churn_counts = df["Churn"].value_counts().reset_index()
    churn_counts.columns = ["Churn", "Customers"]
    color_map = {"Yes": CHURN_RED, "No": RETAINED_TEAL}
    fig = px.pie(
        churn_counts,
        names="Churn",
        values="Customers",
        title="Customer Churn Distribution",
        color="Churn",
        color_discrete_map=color_map,
        hole=0.4,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    col1.plotly_chart(fig, use_container_width=True)

    contract = (
        df.groupby("Contract", as_index=False)
        .agg(churn_rate=("churn_flag", "mean"), customers=("customerID", "count"))
    )
    contract["churn_rate"] *= 100
    fig2 = px.bar(
        contract.sort_values("churn_rate", ascending=True),
        x="churn_rate",
        y="Contract",
        orientation="h",
        title="Churn Rate by Contract",
        labels={"churn_rate": "Churn Rate (%)", "Contract": ""},
        color="churn_rate",
        color_continuous_scale=["#FDECEA", CHURN_RED],
    )
    fig2.update_layout(coloraxis_showscale=False)
    col2.plotly_chart(fig2, use_container_width=True)


def get_significance_indicator(column: str, stats_df: pd.DataFrame) -> str:
    if stats_df.empty or "column" not in stats_df.columns:
        return ""
    
    match = stats_df[stats_df["column"] == column]
    if match.empty:
        return ""
        
    p_val = match.iloc[0]["p_value"]
    if p_val < 0.001:
        return " ✅"
    elif p_val < 0.05:
        return " ⚠️"
    return ""


def churn_rate_chart(df: pd.DataFrame, column: str, title: str, stats_df: pd.DataFrame) -> go.Figure:
    sig = get_significance_indicator(column, stats_df)
    
    summary = (
        df.groupby(column, as_index=False)
        .agg(churn_rate=("churn_flag", "mean"), customers=("customerID", "count"))
    )
    summary["churn_rate"] *= 100
    summary = summary.sort_values("churn_rate", ascending=False)
    fig = px.bar(
        summary,
        x=column,
        y="churn_rate",
        title=f"{title}{sig}",
        labels={"churn_rate": "Churn Rate (%)", column: ""},
        text=summary["churn_rate"].round(1),
        color="churn_rate",
        color_continuous_scale=["#FDEDEC", CHURN_RED],
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-20)
    return fig


def page_churn_analysis(df: pd.DataFrame, stats_df: pd.DataFrame) -> None:
    st.subheader("Churn Analysis")

    col1, col2 = st.columns(2)
    col1.plotly_chart(churn_rate_chart(df, "Contract", "Churn by Contract Type", stats_df), use_container_width=True)
    col2.plotly_chart(churn_rate_chart(df, "PaymentMethod", "Churn by Payment Method", stats_df), use_container_width=True)

    tenure_df = df.copy()
    tenure_df["tenure_bucket"] = pd.Categorical(
        tenure_df["tenure_bucket"], categories=TENURE_ORDER, ordered=True
    )
    tenure_churn = (
        tenure_df.groupby(["tenure_bucket", "Churn"], observed=False)
        .size()
        .reset_index(name="customers")
    )
    fig = px.bar(
        tenure_churn,
        x="tenure_bucket",
        y="customers",
        color="Churn",
        title="Customers by Tenure Group",
        barmode="stack",
        color_discrete_map={"Yes": CHURN_RED, "No": RETAINED_TEAL},
        category_orders={"tenure_bucket": TENURE_ORDER},
    )
    st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    col3.plotly_chart(
        churn_rate_chart(df, "InternetService", "Churn by Internet Service", stats_df),
        use_container_width=True,
    )

    matrix = (
        df.groupby(["Contract", "PaymentMethod"], as_index=False)
        .agg(churn_rate=("churn_flag", "mean"), customers=("customerID", "count"))
    )
    matrix["churn_rate"] *= 100
    heatmap = matrix.pivot(index="Contract", columns="PaymentMethod", values="churn_rate")
    fig_heat = px.imshow(
        heatmap,
        title="Churn Rate Heatmap: Contract × Payment Method",
        labels=dict(color="Churn Rate (%)"),
        color_continuous_scale=["#E8F4F8", CHURN_RED],
        aspect="auto",
    )
    col4.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("---")
    st.subheader("Statistical Validation")
    if not stats_df.empty:
        with st.expander("View Statistical Details"):
            st.markdown("This table proves which churn drivers are statistically significant (✅ p < 0.001, ⚠️ p < 0.05).")
            
            def format_p(val):
                if val < 0.001:
                    return f"{val:.4f} ✅"
                elif val < 0.05:
                    return f"{val:.4f} ⚠️"
                return f"{val:.4f} ❌"
                
            display_stats = stats_df.copy()
            display_stats["p_value"] = display_stats["p_value"].apply(format_p)
            display_stats["effect_size"] = display_stats["effect_size"].round(3)
            
            st.dataframe(display_stats, hide_index=True, use_container_width=True)
    else:
        st.info("Statistical tests not found. Run the pipeline to generate them.")


def page_revenue(df: pd.DataFrame) -> None:
    st.subheader("Revenue Insights")

    col1, col2 = st.columns(2)
    revenue_seg = (
        df.groupby("spending_category", as_index=False)
        .agg(monthly_revenue=("MonthlyCharges", "sum"))
    )
    revenue_seg["spending_category"] = pd.Categorical(
        revenue_seg["spending_category"], categories=SPENDING_ORDER, ordered=True
    )
    revenue_seg = revenue_seg.sort_values("spending_category")
    fig = px.bar(
        revenue_seg,
        x="spending_category",
        y="monthly_revenue",
        title="Monthly Revenue by Spending Category",
        labels={"monthly_revenue": "Revenue ($)", "spending_category": ""},
        color="spending_category",
        color_discrete_sequence=[RETAINED_TEAL, ACCENT, CHURN_RED],
    )
    fig.update_layout(showlegend=False)
    col1.plotly_chart(fig, use_container_width=True)

    loss = (
        df[df["churn_flag"]]
        .groupby("Contract", as_index=False)
        .agg(revenue_lost=("MonthlyCharges", "sum"))
        .sort_values("revenue_lost", ascending=False)
    )
    fig2 = px.bar(
        loss,
        x="Contract",
        y="revenue_lost",
        title="Revenue Lost to Churn by Contract",
        labels={"revenue_lost": "Lost Revenue ($)", "Contract": ""},
        color="revenue_lost",
        color_continuous_scale=["#FCEAE8", CHURN_RED],
    )
    fig2.update_layout(coloraxis_showscale=False)
    col2.plotly_chart(fig2, use_container_width=True)

    tenure_df = df.copy()
    tenure_df["tenure_bucket"] = pd.Categorical(
        tenure_df["tenure_bucket"], categories=TENURE_ORDER, ordered=True
    )
    clv_tenure = (
        tenure_df.groupby("tenure_bucket", observed=False)
        .agg(avg_monthly=("MonthlyCharges", "mean"), avg_clv=("estimated_clv", "mean"))
        .reset_index()
    )
    fig3 = px.line(
        clv_tenure,
        x="tenure_bucket",
        y="avg_monthly",
        markers=True,
        title="Average Monthly Charges by Tenure",
        labels={"avg_monthly": "Avg Monthly Charge ($)", "tenure_bucket": "Tenure"},
    )
    fig3.update_traces(line_color=ACCENT)
    st.plotly_chart(fig3, use_container_width=True)


def page_prediction(df: pd.DataFrame, importance: pd.DataFrame) -> None:
    st.subheader("Churn Prediction")

    col1, col2 = st.columns([2, 1])
    with col2:
        risk_filter = st.multiselect(
            "Risk tier",
            options=["Low", "Medium", "High"],
            default=["High", "Medium"],
        )
        min_prob = st.slider("Minimum churn probability", 0.0, 1.0, 0.5, 0.05)

    risk_df = df.copy()
    if risk_filter:
        risk_df = risk_df[risk_df["risk_tier"].isin(risk_filter)]
    risk_df = risk_df[risk_df["churn_probability"] >= min_prob]
    display_cols = [
        "customerID",
        "Contract",
        "tenure",
        "MonthlyCharges",
        "PaymentMethod",
        "churn_probability",
        "risk_tier",
        "Churn",
    ]
    with col1:
        st.markdown("**High-risk customers (Select a row for Deep Dive)**")
        table = (
            risk_df[display_cols]
            .sort_values("churn_probability", ascending=False)
            .head(100)
            .copy()
        )
        # We need raw values for selection to work well, so we format in pandas Styler or let Streamlit format
        # Actually, if we map strings, selection still works but we need to map back to original customerID.
        # customerID is unchanged.
        table_disp = table.copy()
        table_disp["churn_probability"] = table_disp["churn_probability"].map(lambda v: f"{v:.1%}")
        table_disp["MonthlyCharges"] = table_disp["MonthlyCharges"].map(lambda v: f"${v:,.2f}")
        
        event = st.dataframe(
            table_disp, 
            use_container_width=True, 
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row"
        )
        
        selected_rows = event.selection.rows
        
    if selected_rows:
        selected_idx = selected_rows[0]
        customer_id = table.iloc[selected_idx]["customerID"]
        st.markdown("---")
        st.subheader(f"Customer Deep Dive: {customer_id}")
        customer_data = df[df["customerID"] == customer_id].iloc[0]
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Risk Tier", customer_data["risk_tier"])
        c2.metric("Tenure", f"{customer_data['tenure']} months")
        c3.metric("Monthly Charge", f"${customer_data['MonthlyCharges']:.2f}")
        c4.metric("Contract", customer_data["Contract"])
        
        # SHAP Waterfall
        model = get_trained_model()
        if model:
            explainer, preprocessor = get_shap_components(model)
            if explainer:
                from src.explainability import explain_prediction
                features = get_model_features()
                drivers_dict = explain_prediction(explainer, preprocessor, df[df["customerID"] == customer_id][features], features)
                if drivers_dict:
                    st.markdown("**Why is this customer at risk? (Top Drivers)**")
                    driver_df = pd.DataFrame([
                        {"Feature": k, "Impact": v, "Direction": "Increased Risk" if v > 0 else "Decreased Risk"}
                        for k, v in list(drivers_dict.items())[:6]
                    ])
                    fig_shap = px.bar(
                        driver_df, 
                        x="Impact", 
                        y="Feature", 
                        color="Direction",
                        color_discrete_map={"Increased Risk": CHURN_RED, "Decreased Risk": RETAINED_TEAL},
                        orientation="h",
                    )
                    fig_shap.update_layout(yaxis={'categoryorder':'total ascending'}, height=300)
                    st.plotly_chart(fig_shap, use_container_width=True)
                    
                    if customer_data["churn_probability"] > 0.5:
                        st.warning("💡 **Retention Recommendation:** " + 
                            ("Offer a discounted 1-year contract." if customer_data["Contract"] == "Month-to-month" else "Review tech support experience."))
        
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    fig_hist = px.histogram(
        df,
        x="churn_probability",
        nbins=40,
        title="Churn Probability Distribution",
        labels={"churn_probability": "Churn Probability"},
        color_discrete_sequence=[ACCENT],
    )
    col3.plotly_chart(fig_hist, use_container_width=True)

    top_features = importance.head(12).sort_values("importance")
    fig_imp = px.bar(
        top_features,
        x="importance",
        y="feature_label",
        orientation="h",
        title="Top Churn Drivers (Standard Importance)",
        labels={"importance": "Importance", "feature_label": ""},
        color="importance",
        color_continuous_scale=["#E8F1F8", ACCENT],
    )
    fig_imp.update_layout(coloraxis_showscale=False, yaxis={"categoryorder": "total ascending"})
    col4.plotly_chart(fig_imp, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Global Feature Explainability (SHAP)")
    if SHAP_SUMMARY_PATH.exists():
        st.image(str(SHAP_SUMMARY_PATH), caption="SHAP Summary Plot (How features impact the model)")
    else:
        st.info("SHAP summary plot not found. Run the pipeline to generate it.")


def page_cohort_analysis(df: pd.DataFrame) -> None:
    st.subheader("Cohort Retention Analysis")
    try:
        from src.cohort_analysis import build_retention_heatmap_data, compute_cohort_metrics
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("**Retention by Tenure & Service**")
            pivot = build_retention_heatmap_data(df)
            fig_heat = px.imshow(
                pivot,
                title="Retention Rate",
                labels=dict(color="Retention Rate", x="Tenure Cohort", y="Internet Service"),
                color_continuous_scale=["#FCEAE8", RETAINED_TEAL],
                aspect="auto",
                text_auto=".1%"
            )
            st.plotly_chart(fig_heat, use_container_width=True)
        
        with col2:
            st.markdown("**Cohort Metrics**")
            metrics = compute_cohort_metrics(df)
            st.dataframe(metrics, hide_index=True, use_container_width=True)
    except ImportError:
        st.error("Cohort analysis module not found.")


def main() -> None:
    st.set_page_config(
        page_title="Customer Churn Analytics",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    customers, importance, stats = load_data()

    st.sidebar.title("Filters")
    st.session_state["filter_contract"] = st.sidebar.multiselect(
        "Contract",
        options=sorted(customers["Contract"].unique()),
        default=sorted(customers["Contract"].unique()),
    )
    st.session_state["filter_internet"] = st.sidebar.multiselect(
        "Internet Service",
        options=sorted(customers["InternetService"].unique()),
        default=sorted(customers["InternetService"].unique()),
    )
    st.session_state["filter_spending"] = st.sidebar.multiselect(
        "Spending Category",
        options=SPENDING_ORDER,
        default=SPENDING_ORDER,
    )

    def page_predict_single() -> None:
        st.subheader("🔮 Predict Customer Churn")
        st.caption("Enter customer details to get a real-time churn risk score")

        model = get_trained_model()
        explainer, preprocessor = None, None
        if model is not None:
            explainer, preprocessor = get_shap_components(model)

        with st.form("prediction_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                gender = st.selectbox("Gender", ["Male", "Female"])
                senior = st.selectbox("Senior Citizen", [0, 1])
                partner = st.selectbox("Partner", ["Yes", "No"])
                dependents = st.selectbox("Dependents", ["Yes", "No"])
                tenure = st.slider("Tenure (months)", 0, 72, 12)
            with col2:
                contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
                internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
                phone = st.selectbox("Phone Service", ["Yes", "No"])
                multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
                paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
                payment = st.selectbox("Payment Method", [
                    "Electronic check", "Mailed check",
                    "Bank transfer (automatic)", "Credit card (automatic)"
                ])
            with col3:
                monthly = st.slider("Monthly Charges ($)", 18.0, 120.0, 50.0, 0.5)
                total = monthly * tenure if tenure > 0 else monthly
                online_sec = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
                online_bak = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
                device_prot = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
                tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
                stream_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
                stream_mov = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

            submitted = st.form_submit_button("⚡ Predict Churn Risk", use_container_width=True)

        if submitted and model is not None:
            input_data = pd.DataFrame([{
                "customerID": "NEW",
                "gender": gender,
                "SeniorCitizen": senior,
                "Partner": partner,
                "Dependents": dependents,
                "tenure": tenure,
                "PhoneService": phone,
                "MultipleLines": multiple_lines,
                "InternetService": internet,
                "OnlineSecurity": online_sec,
                "OnlineBackup": online_bak,
                "DeviceProtection": device_prot,
                "TechSupport": tech_support,
                "StreamingTV": stream_tv,
                "StreamingMovies": stream_mov,
                "Contract": contract,
                "PaperlessBilling": paperless,
                "PaymentMethod": payment,
                "MonthlyCharges": monthly,
                "TotalCharges": total,
                "Churn": "No"
            }])

            try:
                # Add engineered features using our module
                enriched_data = add_engineered_features(input_data)
                features = get_model_features()
                
                # Predict
                prob = model.predict_proba(enriched_data[features])[0, 1]
                
                # Display results
                st.markdown("---")
                res_col1, res_col2 = st.columns([1, 2])
                
                with res_col1:
                    st.metric("Churn Probability", f"{prob*100:.1f}%")
                    if prob >= 0.7:
                        st.error("🚨 HIGH RISK")
                    elif prob >= 0.4:
                        st.warning("⚠️ MEDIUM RISK")
                    else:
                        st.success("✅ LOW RISK")
                
                with res_col2:
                    st.progress(float(prob), text="Risk Level")
                    if prob >= 0.5:
                        st.markdown("**Recommendation:** Immediate retention action required. Review plan pricing and tech support experience.")
                    else:
                        st.markdown("**Recommendation:** Customer is stable. Consider upsell opportunities based on current usage.")
                        
                # Explain with SHAP
                if explainer is not None:
                    from src.explainability import explain_prediction
                    drivers_dict = explain_prediction(explainer, preprocessor, enriched_data[features], features)
                    
                    if drivers_dict:
                        st.markdown("---")
                        st.markdown("##### Why did the model make this prediction?")
                        
                        # Convert to DataFrame for plotting
                        driver_df = pd.DataFrame([
                            {"Feature": k, "Impact": v, "Direction": "Increased Risk" if v > 0 else "Decreased Risk"}
                            for k, v in list(drivers_dict.items())[:6] # Top 6
                        ])
                        
                        fig_shap = px.bar(
                            driver_df, 
                            x="Impact", 
                            y="Feature", 
                            color="Direction",
                            color_discrete_map={"Increased Risk": CHURN_RED, "Decreased Risk": RETAINED_TEAL},
                            orientation="h",
                            title="Top Influencing Factors for this Customer"
                        )
                        fig_shap.update_layout(yaxis={'categoryorder':'total ascending'})
                        st.plotly_chart(fig_shap, use_container_width=True)
            except Exception as e:
                st.error(f"Error making prediction: {str(e)}")

    df = apply_filters(customers)

    st.title("Customer Churn Prediction & Analytics")
    st.caption("Telecom retention KPIs, segment analysis, revenue impact, and ML risk scoring")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Executive Overview", "Churn Analysis", "Revenue Insights", "Churn Prediction", "Cohort Analysis", "🔮 Predict Customer"]
    )
    with tab1:
        page_executive(df)
    with tab2:
        page_churn_analysis(df, stats)
    with tab3:
        page_revenue(df)
    with tab4:
        page_prediction(df, importance)
    with tab5:
        page_cohort_analysis(df)
    with tab6:
        page_predict_single()

    st.sidebar.divider()
    st.sidebar.markdown(
        "**Data:** IBM Telco Customer Churn  \n"
        f"**Records:** {len(df):,} (filtered)"
    )


if __name__ == "__main__":
    main()
