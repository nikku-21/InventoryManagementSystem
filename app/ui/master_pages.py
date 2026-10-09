"""Small CRUD pages: Categories, Suppliers, Stock History and Audit Log."""
from __future__ import annotations

from ..models import AuditLog, Category, StockMovement, Supplier
from .widgets import CrudPage, Field


def categories_page(user):
    return CrudPage(user, Category, [Field("name", "Name", required=True)],
                    [("ID", lambda o: o.id), ("Name", lambda o: o.name)], "category")


def suppliers_page(user):
    fields = [Field("name", "Name", required=True), Field("phone", "Phone"), Field("email", "E-mail")]
    cols = [("ID", lambda o: o.id), ("Name", lambda o: o.name), ("Phone", lambda o: o.phone),
            ("E-mail", lambda o: o.email)]
    return CrudPage(user, Supplier, fields, cols, "supplier")


def history_page(user):
    cols = [("Date", lambda m: m.timestamp.strftime("%Y-%m-%d %H:%M")), ("SKU", lambda m: m.product.sku),
            ("Type", lambda m: m.kind), ("Qty", lambda m: m.quantity), ("Note", lambda m: m.note),
            ("User", lambda m: m.user)]
    return CrudPage(user, StockMovement, [], cols, "movement", sort_key=lambda m: -m.id, read_only=True)


def audit_page(user):
    cols = [("Time", lambda a: a.timestamp.strftime("%Y-%m-%d %H:%M:%S")), ("User", lambda a: a.user),
            ("Action", lambda a: a.action)]
    return CrudPage(user, AuditLog, [], cols, "log entry", sort_key=lambda a: -a.id, read_only=True)
