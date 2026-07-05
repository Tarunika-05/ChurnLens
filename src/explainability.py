"""SHAP-based model explainability."""

from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import shap

from src.logger import setup_logging

logger = setup_logging()


def get_shap_explainer(model_pipeline: Any, X_background: pd.DataFrame):
    """Create a SHAP explainer from a trained sklearn pipeline."""
    try:
        # Get the actual model from the pipeline (assuming it's named 'classifier' or 'model')
        if hasattr(model_pipeline, "named_steps"):
            model = model_pipeline.named_steps.get(
                "classifier", model_pipeline.named_steps.get("model")
            )
            preprocessor = model_pipeline.named_steps.get("preprocessor")
        else:
            model = model_pipeline
            preprocessor = None

        if hasattr(model, "feature_importances_") and not isinstance(
            model, __import__("sklearn").linear_model.LogisticRegression
        ):
            # Tree-based model
            if preprocessor is not None:
                X_transformed = preprocessor.transform(X_background)
            else:
                X_transformed = X_background
            explainer = shap.TreeExplainer(model)
        else:
            # Linear model or other
            if preprocessor is not None:
                X_transformed = preprocessor.transform(X_background)
            else:
                X_transformed = X_background

            # Use LinearExplainer for Logistic Regression or KernelExplainer as fallback
            if isinstance(model, __import__("sklearn").linear_model.LogisticRegression):
                explainer = shap.LinearExplainer(model, X_transformed)
            else:
                # KernelExplainer is slow, use a summary of background data
                background_summary = shap.kmeans(X_transformed, 100)
                explainer = shap.KernelExplainer(model.predict_proba, background_summary)

        return explainer, preprocessor
    except Exception as e:
        logger.error(f"Error creating SHAP explainer: {e}")
        raise


def explain_prediction(
    explainer, preprocessor, instance: pd.DataFrame, feature_names: list[str]
) -> dict:
    """Get SHAP values for a single prediction."""
    try:
        X_transformed = preprocessor.transform(instance) if preprocessor is not None else instance

        shap_values = explainer.shap_values(X_transformed)

        # Depending on the model, shap_values might be a list (for classification) or an array
        vals = shap_values[1][0] if isinstance(shap_values, list) else shap_values[0]

        # Get transformed feature names if preprocessor exists
        if preprocessor is not None and hasattr(preprocessor, "get_feature_names_out"):
            actual_feature_names = preprocessor.get_feature_names_out()
        else:
            actual_feature_names = feature_names

        # Create a dictionary of feature -> importance
        # Ensure actual_feature_names length matches vals length
        if len(actual_feature_names) == len(vals):
            # Sort by absolute value to get top drivers
            importance_dict = {actual_feature_names[i]: float(vals[i]) for i in range(len(vals))}
            sorted_drivers = dict(
                sorted(importance_dict.items(), key=lambda item: abs(item[1]), reverse=True)
            )
            return sorted_drivers
        else:
            logger.warning(
                f"Feature names length ({len(actual_feature_names)}) doesn't match SHAP values length ({len(vals)}). Cannot map SHAP values to features."
            )
            return {}

    except Exception as e:
        logger.error(f"Error explaining prediction: {e}")
        return {}


def global_shap_summary(
    explainer, preprocessor, X: pd.DataFrame, feature_names: list[str], save_path: str | None = None
):
    """Compute and save global SHAP feature importance plot."""
    try:
        X_transformed = preprocessor.transform(X) if preprocessor is not None else X

        shap_values = explainer.shap_values(X_transformed)

        # Take positive class for classification if needed
        shap_values_to_plot = shap_values[1] if isinstance(shap_values, list) else shap_values

        # Get transformed feature names if preprocessor exists
        if preprocessor is not None and hasattr(preprocessor, "get_feature_names_out"):
            actual_feature_names = preprocessor.get_feature_names_out()
        else:
            actual_feature_names = feature_names

        # Create the plot
        plt.figure(figsize=(10, 8))

        if len(actual_feature_names) == shap_values_to_plot.shape[1]:
            shap.summary_plot(
                shap_values_to_plot, X_transformed, feature_names=actual_feature_names, show=False
            )

            if save_path:
                plt.tight_layout()
                plt.savefig(save_path, dpi=150, bbox_inches="tight")
                logger.info(f"Saved SHAP summary plot to {save_path}")

            plt.close()
        else:
            logger.warning(
                f"Feature names length ({len(actual_feature_names)}) doesn't match SHAP values shape ({shap_values_to_plot.shape[1]}). Skipping SHAP summary plot."
            )

    except Exception as e:
        logger.error(f"Error generating global SHAP summary: {e}")
