"""Pandas data frames built from the database. Used by exports and charts."""
from __future__ import annotations

import pandas as pd

from .models import Defect, FmeaItem, Product, StockMovement
from .services import list_all


def products_df() -> pd.DataFrame:
    cols = ["SKU", "Name", "Category", "Supplier", "Quantity", "Reorder Level", "Unit Price", "Stock Value"]
    rows = [[p.sku, p.name, p.category.name if p.category else "-", p.supplier.name if p.supplier else "-",
             p.quantity, p.reorder_level, p.unit_price, round(p.quantity * p.unit_price, 2)]
            for p in list_all(Product)]
    return pd.DataFrame(rows, columns=cols)


def movements_df() -> pd.DataFrame:
    cols = ["Date", "SKU", "Type", "Quantity", "Note", "User"]
    rows = [[m.timestamp.strftime("%Y-%m-%d %H:%M"), m.product.sku, m.kind, m.quantity, m.note, m.user]
            for m in list_all(StockMovement)]
    return pd.DataFrame(rows, columns=cols)


def defects_df() -> pd.DataFrame:
    cols = ["ID", "Title", "Type", "Severity", "Status", "Logged On"]
    rows = [[d.id, d.title, d.defect_type, d.severity, d.status, d.logged_on.strftime("%Y-%m-%d")]
            for d in list_all(Defect)]
    return pd.DataFrame(rows, columns=cols)


def fmea_df() -> pd.DataFrame:
    cols = ["ID", "Failure Mode", "Effect", "S", "O", "D", "RPN", "Mitigation"]
    rows = [[f.id, f.failure_mode, f.effect, f.severity, f.occurrence, f.detection, f.rpn, f.mitigation]
            for f in sorted(list_all(FmeaItem), key=lambda x: -x.rpn)]
    return pd.DataFrame(rows, columns=cols)
