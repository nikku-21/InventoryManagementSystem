"""File exports: Excel (OpenPyXL via Pandas), PDF (ReportLab) and CSV."""
from __future__ import annotations

from datetime import datetime

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from . import config
from .dataframes import defects_df, fmea_df, movements_df, products_df


def export_excel(path: str) -> None:
    """One workbook, one sheet per dataset, with auto-sized columns."""
    sheets = {"Products": products_df(), "Movements": movements_df(),
              "FMEA": fmea_df(), "Defects": defects_df()}
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=name, index=False)
            for column in writer.sheets[name].columns:
                width = max(len(str(c.value)) if c.value is not None else 0 for c in column)
                writer.sheets[name].column_dimensions[column[0].column_letter].width = min(width + 2, 45)


def export_csv(path: str) -> None:
    products_df().to_csv(path, index=False)


def export_pdf(path: str) -> None:
    """Printable stock report."""
    styles = getSampleStyleSheet()
    df = products_df()
    story = [Paragraph(f"{config.APP_NAME} - Stock Report", styles["Title"]),
             Paragraph(f"Generated {datetime.now():%d %b %Y, %H:%M}", styles["Normal"]), Spacer(1, 12)]
    table = Table([list(df.columns)] + df.astype(str).values.tolist(), repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eff6ff")]),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    SimpleDocTemplate(path, pagesize=landscape(A4)).build(story)
