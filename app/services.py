"""Business logic: validated CRUD, stock movements, backups and start-up seeding.

The GUI never talks to the database directly; it goes through this module and
app/auth.py, which keeps validation (Poka-Yoke) and audit logging in one place.
"""
from __future__ import annotations

import shutil
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from . import config
from .auth import create_user, log_action, session
from .db import DB_FILE, Base, engine
from .models import Category, FmeaItem, Product, StockMovement, Supplier, User


# ----------------------------------------------------------------- start-up ---
def init_db() -> None:
    """Create tables and seed first-run data (admin user, categories, FMEA examples)."""
    Base.metadata.create_all(engine)
    if not session.query(User).count():
        create_user(config.DEFAULT_ADMIN[0], config.DEFAULT_ADMIN[1], "admin")
    if not session.query(Category).count():
        session.add_all([Category(name=n) for n in ("Electronics", "Groceries", "Stationery", "Hardware")])
    if not session.query(FmeaItem).count():
        session.add_all([
            FmeaItem(failure_mode="Invalid data typed into product form", effect="Wrong stock values",
                     severity=7, occurrence=6, detection=3,
                     mitigation="Poka-Yoke: spin boxes, required-field checks, confirmation dialogs"),
            FmeaItem(failure_mode="Database file lost or corrupted", effect="Total data loss",
                     severity=10, occurrence=2, detection=4, mitigation="One-click backup in Reports page"),
            FmeaItem(failure_mode="Stock-out issued above available quantity", effect="Negative stock",
                     severity=8, occurrence=4, detection=2, mitigation="Block OUT movements above stock"),
            FmeaItem(failure_mode="Unauthorised user deletes records", effect="Data loss",
                     severity=9, occurrence=3, detection=3, mitigation="Role-based delete + audit log"),
            FmeaItem(failure_mode="User manual out of date", effect="Users operate system incorrectly",
                     severity=5, occurrence=5, detection=5,
                     mitigation="Update docs every release; in-app Help/FAQ is the single source of truth"),
        ])
    session.commit()


# --------------------------------------------------------------- generic CRUD ---
def list_all(model) -> list:
    return session.query(model).order_by(model.id).all()


def _validate(model, data: dict) -> dict:
    """Poka-Yoke: stop bad data before it reaches the database."""
    data = {k: (v.strip() if isinstance(v, str) else v) for k, v in data.items()}
    for key in ("name", "title", "failure_mode", "sku"):
        if key in data and not data[key]:
            raise ValueError(f"'{key.replace('_', ' ').title()}' is required.")
    if model is Product:
        data["sku"] = data["sku"].upper()
        for key in ("quantity", "reorder_level", "unit_price"):
            if data.get(key, 0) < 0:
                raise ValueError("Quantity, reorder level and price cannot be negative.")
    if model is FmeaItem:
        for key in ("severity", "occurrence", "detection"):
            if not 1 <= data.get(key, 1) <= 10:
                raise ValueError("Severity, Occurrence and Detection must be between 1 and 10.")
    return data


def save(model, data: dict, obj_id: int | None = None, user: str = "system"):
    """Create (obj_id=None) or update a record, with validation and audit logging."""
    data = _validate(model, data)
    try:
        obj = session.get(model, obj_id) if obj_id else model()
        for key, value in data.items():
            setattr(obj, key, value)
        session.add(obj)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ValueError("Duplicate value: a record with the same unique field already exists.") from exc
    log_action(user, f"{'Updated' if obj_id else 'Created'} {model.__name__} #{obj.id}")
    return obj


def delete(model, obj_id: int, user: str = "system") -> None:
    obj = session.get(model, obj_id)
    if obj is None:
        return
    if model is Category:       # keep products, just un-assign them
        session.query(Product).filter_by(category_id=obj_id).update({"category_id": None})
    if model is Supplier:
        session.query(Product).filter_by(supplier_id=obj_id).update({"supplier_id": None})
    session.delete(obj)
    session.commit()
    log_action(user, f"Deleted {model.__name__} #{obj_id}")


# ------------------------------------------------------------------ stock ---
def stock_move(product_id: int, kind: str, qty: int, note: str = "", user: str = "system") -> Product:
    """Record a stock IN/OUT. Refuses invalid quantities and overdrawn stock."""
    if kind not in ("IN", "OUT"):
        raise ValueError("Movement type must be IN or OUT.")
    if qty <= 0:
        raise ValueError("Quantity must be greater than zero.")
    product = session.get(Product, product_id)
    if product is None:
        raise ValueError("Product not found.")
    if kind == "OUT" and qty > product.quantity:
        raise ValueError(f"Only {product.quantity} units in stock - cannot issue {qty}.")
    product.quantity += qty if kind == "IN" else -qty
    session.add(StockMovement(product_id=product_id, kind=kind, quantity=qty, note=note, user=user))
    session.commit()
    log_action(user, f"Stock {kind} {qty} x {product.sku}")
    return product


def low_stock() -> list[Product]:
    return [p for p in list_all(Product) if p.quantity <= p.reorder_level]


def dashboard_stats() -> dict:
    products = list_all(Product)
    return {
        "products": len(products),
        "units": sum(p.quantity for p in products),
        "value": sum(p.quantity * p.unit_price for p in products),
        "low": len(low_stock()),
    }


def backup_db() -> str:
    """Copy the SQLite file into data/backups/ with a timestamp. Returns the new path."""
    session.commit()
    folder = DB_FILE.parent / "backups"
    folder.mkdir(exist_ok=True)
    target = folder / f"inventory_{datetime.now():%Y%m%d_%H%M%S}.db"
    shutil.copy2(DB_FILE, target)
    return str(target)
