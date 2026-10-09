"""Products page: CRUD plus Stock In / Stock Out buttons and low-stock highlighting."""
from __future__ import annotations

from PySide6.QtWidgets import QInputDialog, QMessageBox, QPushButton

from .. import services
from ..help_content import TOOLTIPS
from ..models import Category, Product, Supplier
from .widgets import CrudPage, Field


def _choices(model):
    """Dropdown list (Poka-Yoke: pick from a list instead of typing)."""
    return lambda: [(None, "- none -")] + [(o.id, o.name) for o in services.list_all(model)]


class ProductsPage(CrudPage):
    def __init__(self, user):
        fields = [
            Field("sku", "SKU", required=True, tip=TOOLTIPS["sku"]),
            Field("name", "Name", required=True),
            Field("category_id", "Category", "choice", choices=_choices(Category)),
            Field("supplier_id", "Supplier", "choice", choices=_choices(Supplier)),
            Field("quantity", "Quantity", "int"),
            Field("reorder_level", "Reorder level", "int", tip=TOOLTIPS["reorder"]),
            Field("unit_price", "Unit price", "float"),
        ]
        columns = [
            ("SKU", lambda p: p.sku), ("Name", lambda p: p.name),
            ("Category", lambda p: p.category.name if p.category else "-"),
            ("Supplier", lambda p: p.supplier.name if p.supplier else "-"),
            ("Qty", lambda p: p.quantity), ("Reorder", lambda p: p.reorder_level),
            ("Price", lambda p: f"{p.unit_price:.2f}"),
        ]
        super().__init__(user, Product, fields, columns, "product",
                         hint="Red rows are at or below their reorder level.")
        self.btn_in, self.btn_out = QPushButton("Stock In"), QPushButton("Stock Out")
        self.btn_in.clicked.connect(lambda: self.move("IN"))
        self.btn_out.clicked.connect(lambda: self.move("OUT"))
        self.bar.addWidget(self.btn_in)
        self.bar.addWidget(self.btn_out)

    def row_color(self, p):
        return "#fee2e2" if p.quantity <= p.reorder_level else None

    def move(self, kind):
        obj_id = self.selected_id()
        if obj_id is None:
            return
        qty, ok = QInputDialog.getInt(self, f"Stock {kind}", "Quantity:", 1, 1, 1_000_000)
        if not ok:
            return
        try:
            services.stock_move(obj_id, kind, qty, user=self.user.username)
        except ValueError as exc:
            QMessageBox.warning(self, "Cannot move stock", str(exc))
            return
        self.refresh()
