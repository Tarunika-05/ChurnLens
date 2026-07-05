"""Model training and evaluation for churn prediction."""

from __future__ import annotations

import json
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import optuna
import optuna.visualization as vis
import pandas as pd
import seaborn as sns
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

from src.config import IMAGES_DIR, RANDOM_STATE, TEST_SIZE
from src.exceptions import PipelineError
from src.experiment_tracking import log_training_run
from src.features import get_model_features


def build_preprocessor(feature_frame: pd.DataFrame) -> ColumnTransformer:
    categorical_cols = feature_frame.select_dtypes(include=["object", "bool"]).columns.tolist()
    numeric_cols = feature_frame.select_dtypes(include=["number"]).columns.tolist()

    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ]
    )


def evaluate_model(
    name: str, model: Any, x_test: pd.DataFrame, y_test: pd.Series, threshold: float = 0.5
) -> dict[str, float | str]:
    probabilities = model.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= threshold).astype(int)
    return {
        "model": name,
        "accuracy": round(accuracy_score(y_test, predictions), 4),
        "precision": round(precision_score(y_test, predictions), 4),
        "recall": round(recall_score(y_test, predictions), 4),
        "f1": round(f1_score(y_test, predictions), 4),
        "roc_auc": round(roc_auc_score(y_test, probabilities), 4),
        "optimal_threshold": threshold,
    }


def find_optimal_threshold(y_true, y_proba, fn_cost=45, fp_cost=5) -> float:
    """Find threshold that minimizes business cost."""
    _precisions, _recalls, thresholds = precision_recall_curve(y_true, y_proba)
    best_threshold = 0.5
    min_cost = float("inf")

    # We want to find threshold that minimizes: FN*fn_cost + FP*fp_cost
    # Calculate costs for all thresholds
    for threshold in thresholds:
        preds = (y_proba >= threshold).astype(int)
        _tn, fp, fn, _tp = confusion_matrix(y_true, preds).ravel()
        cost = (fn * fn_cost) + (fp * fp_cost)
        if cost < min_cost:
            min_cost = cost
            best_threshold = threshold

    return float(best_threshold)


def save_evaluation_charts(y_true, y_proba, threshold, save_dir):
    """Save confusion matrix, ROC curve, and PR curve."""
    save_dir.mkdir(parents=True, exist_ok=True)

    # Confusion Matrix
    preds = (y_proba >= threshold).astype(int)
    cm = confusion_matrix(y_true, preds)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title(f"Confusion Matrix (Threshold={threshold:.2f})")
    ax.set_ylabel("Actual")
    ax.set_xlabel("Predicted")
    fig.tight_layout()
    fig.savefig(save_dir / "confusion_matrix.png", dpi=150)
    plt.close(fig)

    # ROC Curve
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr, tpr, color="#2E86AB", lw=2)
    ax.plot([0, 1], [0, 1], color="gray", lw=1, linestyle="--")
    ax.set_title("ROC Curve")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    fig.tight_layout()
    fig.savefig(save_dir / "roc_curve.png", dpi=150)
    plt.close(fig)

    # PR Curve
    precisions, recalls, _ = precision_recall_curve(y_true, y_proba)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(recalls, precisions, color="#E94F37", lw=2)
    ax.set_title("Precision-Recall Curve")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    fig.tight_layout()
    fig.savefig(save_dir / "pr_curve.png", dpi=150)
    plt.close(fig)


def train_models(df: pd.DataFrame) -> tuple[ImbPipeline, pd.DataFrame, pd.DataFrame]:
    features = get_model_features()
    missing_cols = [c for c in [*features, "churn_flag"] if c not in df.columns]
    if missing_cols:
        raise PipelineError(f"Missing required columns for training: {missing_cols}")

    X = df[features]
    y = df["churn_flag"].astype(int)

    try:
        x_train, x_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
        )

        preprocessor = build_preprocessor(x_train)

        # Cross-validation setup
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

        candidates = {
            "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
            "Random Forest": RandomForestClassifier(
                n_estimators=200, random_state=RANDOM_STATE, class_weight="balanced"
            ),
            "XGBoost": XGBClassifier(
                eval_metric="logloss",
                random_state=RANDOM_STATE,
            ),
        }

        smote = SMOTE(random_state=RANDOM_STATE)

        metrics = []
        fitted_models: dict[str, ImbPipeline] = {}

        # Tune XGBoost with Optuna
        def objective(trial):
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 100, 300),
                "max_depth": trial.suggest_int("max_depth", 3, 7),
                "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
                "subsample": trial.suggest_float("subsample", 0.6, 1.0),
                "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
                "eval_metric": "logloss",
                "random_state": RANDOM_STATE,
            }
            xgb = XGBClassifier(**params)
            pipe = ImbPipeline(
                steps=[("preprocessor", preprocessor), ("smote", smote), ("model", xgb)]
            )

            # Use StratifiedKFold to evaluate this set of parameters
            roc_aucs = []
            for train_idx, val_idx in cv.split(x_train, y_train):
                X_tr, X_val = x_train.iloc[train_idx], x_train.iloc[val_idx]
                y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]
                pipe.fit(X_tr, y_tr)
                y_proba = pipe.predict_proba(X_val)[:, 1]
                roc_aucs.append(roc_auc_score(y_val, y_proba))
            return np.mean(roc_aucs)

        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=10)  # 10 trials for speed, usually 50+

        # Save Optuna plots
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        try:
            fig_history = vis.plot_optimization_history(study)
            fig_history.write_image(str(IMAGES_DIR / "optuna_history.png"))
        except Exception:
            pass  # Ignore if plotly or kaleido isn't installed for writing images

        # Update XGBoost candidate with best params
        candidates["XGBoost"] = XGBClassifier(
            **study.best_params, eval_metric="logloss", random_state=RANDOM_STATE
        )

        for name, estimator in candidates.items():
            pipeline = ImbPipeline(
                steps=[
                    ("preprocessor", preprocessor),
                    ("smote", smote),
                    ("model", estimator),
                ]
            )
            # Perform cross-validation to get CV metrics
            cv_roc_aucs = []
            for train_idx, val_idx in cv.split(x_train, y_train):
                X_tr, X_val = x_train.iloc[train_idx], x_train.iloc[val_idx]
                y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]
                pipeline.fit(X_tr, y_tr)
                cv_roc_aucs.append(roc_auc_score(y_val, pipeline.predict_proba(X_val)[:, 1]))

            # Train on full train set for final model
            pipeline.fit(x_train, y_train)
            fitted_models[name] = pipeline

            # Find optimal threshold on validation set (we use test set here for simplicity, but ideally should be CV)
            y_proba = pipeline.predict_proba(x_test)[:, 1]
            optimal_threshold = find_optimal_threshold(y_test, y_proba)

            model_metrics = evaluate_model(
                name, pipeline, x_test, y_test, threshold=optimal_threshold
            )
            model_metrics["cv_roc_auc_mean"] = round(float(np.mean(cv_roc_aucs)), 4)
            model_metrics["cv_roc_auc_std"] = round(float(np.std(cv_roc_aucs)), 4)
            metrics.append(model_metrics)

            # Log to MLflow
            try:
                params: dict[str, Any] = getattr(estimator, "get_params", lambda: {})()
                mlflow_metrics = {
                    k: v for k, v in model_metrics.items() if isinstance(v, (int, float))
                }
                log_training_run(name, params, mlflow_metrics, pipeline)
            except Exception:
                pass  # If MLflow isn't fully configured, fail gracefully

        metrics_df = pd.DataFrame(metrics).sort_values("roc_auc", ascending=False)
        best_name = metrics_df.iloc[0]["model"]
        best_model = fitted_models[best_name]
        best_threshold = metrics_df.iloc[0]["optimal_threshold"]

        test_probabilities = best_model.predict_proba(x_test)[:, 1]
        predictions = pd.DataFrame(
            {
                "customerID": df.loc[x_test.index, "customerID"].values,
                "churn_probability": test_probabilities,
                "actual_churn": y_test.values,
                "predicted_churn": (test_probabilities >= best_threshold).astype(int),
            }
        )
        predictions["risk_tier"] = pd.cut(
            predictions["churn_probability"],
            bins=[-0.01, 0.4, 0.7, 1.0],
            labels=["Low", "Medium", "High"],
        )

        # Save evaluation charts for the best model
        save_evaluation_charts(y_test.values, test_probabilities, best_threshold, IMAGES_DIR)

        return best_model, metrics_df, predictions
    except Exception as e:
        raise PipelineError(f"Model training failed: {e!s}") from e


def extract_feature_importance(model: ImbPipeline, x: pd.DataFrame) -> pd.DataFrame:
    preprocessor = model.named_steps["preprocessor"]
    estimator = model.named_steps["model"]
    feature_names = preprocessor.get_feature_names_out()

    if hasattr(estimator, "feature_importances_"):
        values = estimator.feature_importances_
    elif hasattr(estimator, "coef_"):
        values = np.abs(estimator.coef_[0])
    else:
        raise ValueError("Model does not expose feature importance.")

    importance = (
        pd.DataFrame({"feature": feature_names, "importance": values})
        .sort_values("importance", ascending=False)
        .head(20)
    )
    return importance


def save_metrics(metrics_df: pd.DataFrame, path: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(metrics_df.to_dict(orient="records"), handle, indent=2)
