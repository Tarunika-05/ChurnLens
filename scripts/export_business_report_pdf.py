"""Export business report markdown to PDF."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "business_report.pdf"


def build_pdf() -> None:
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=18,
        spaceAfter=12,
        textColor=colors.HexColor("#2E86AB"),
    )
    heading_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=14,
        spaceAfter=8,
    )
    body_style = styles["BodyText"]

    story = []
    story.append(Paragraph("Customer Churn Analytics — Business Report", title_style))
    story.append(Paragraph("Prepared for: Telecom Executive Leadership", body_style))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Executive Summary", heading_style))
    story.append(
        Paragraph(
            "The telecom business faces a 26.54% churn rate, with 1,869 churned customers "
            "representing an estimated $139,131 in monthly revenue loss. Contract structure, "
            "tenure, internet service type, and payment method are the strongest churn drivers. "
            "Logistic Regression achieved 84.25% ROC-AUC for proactive retention targeting.",
            body_style,
        )
    )

    story.append(Paragraph("Key Metrics", heading_style))
    metrics = [
        ["Metric", "Value"],
        ["Total customers", "7,043"],
        ["Churn rate", "26.54%"],
        ["Monthly revenue (active)", "$316,986"],
        ["Revenue lost to churn", "$139,131"],
        ["Average CLV", "$2,280"],
    ]
    table = Table(metrics, colWidths=[3.2 * inch, 2.2 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E86AB")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F8FB")]),
            ]
        )
    )
    story.append(table)

    story.append(Paragraph("Model Comparison", heading_style))
    model_table = Table(
        [
            ["Model", "Accuracy", "Precision", "Recall", "ROC-AUC"],
            ["Logistic Regression", "79.91%", "65.22%", "52.14%", "84.25%"],
            ["XGBoost", "79.13%", "63.42%", "50.53%", "83.68%"],
            ["Random Forest", "78.28%", "61.56%", "48.40%", "82.50%"],
        ],
        colWidths=[1.6 * inch, 0.9 * inch, 0.9 * inch, 0.8 * inch, 0.9 * inch],
    )
    model_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E94F37")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )
    )
    story.append(model_table)

    recommendations = [
        "Target high-value customers with churn probability above 0.7 for retention offers.",
        "Promote annual/two-year contracts for month-to-month subscribers after 6 months.",
        "Migrate electronic check users to autopay or card billing.",
        "Launch a 90-day onboarding program for customers in their first year.",
        "Review fiber pricing and bundle support/streaming perks to reduce churn.",
    ]
    story.append(Paragraph("Business Recommendations", heading_style))
    for item in recommendations:
        story.append(Paragraph(f"• {item}", body_style))
        story.append(Spacer(1, 0.08 * inch))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    SimpleDocTemplate(str(OUTPUT), pagesize=letter, rightMargin=54, leftMargin=54).build(story)
    
    import logging
    from src.logger import setup_logging
    from src.config import settings
    logger = setup_logging(settings.log_level)
    logger.info(f"Saved {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
