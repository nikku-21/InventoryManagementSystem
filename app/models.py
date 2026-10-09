"""ORM models (tables) for the Inventory Management System."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .db import Base


class User(Base):
    """Application login. Passwords are stored only as bcrypt hashes."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    role = Column(String(20), default="staff")          # "admin" or "staff"


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)


class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    phone = Column(String(30), default="")
    email = Column(String(120), default="")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    sku = Column(String(40), unique=True, nullable=False)     # unique ID constraint (Poka-Yoke)
    name = Column(String(120), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    quantity = Column(Integer, default=0)
    reorder_level = Column(Integer, default=10)
    unit_price = Column(Float, default=0.0)
    category = relationship("Category")
    supplier = relationship("Supplier")
    movements = relationship("StockMovement", cascade="all, delete-orphan", back_populates="product")


class StockMovement(Base):
    """Every stock-in / stock-out is recorded here (traceability)."""
    __tablename__ = "stock_movements"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    kind = Column(String(3), nullable=False)                  # "IN" or "OUT"
    quantity = Column(Integer, nullable=False)
    note = Column(String(200), default="")
    user = Column(String(50), default="")
    timestamp = Column(DateTime, default=datetime.now)
    product = relationship("Product", back_populates="movements")


class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(Integer, primary_key=True)
    user = Column(String(50))
    action = Column(String(250))
    timestamp = Column(DateTime, default=datetime.now)


class Defect(Base):
    """Checksheet / defect log used for the Pareto analysis (Review 3 & 4)."""
    __tablename__ = "defects"
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    defect_type = Column(String(40), default="Validation")
    severity = Column(String(10), default="Medium")           # Low / Medium / High
    status = Column(String(10), default="Open")               # Open / Fixed
    logged_on = Column(DateTime, default=datetime.now)


class FmeaItem(Base):
    """One FMEA row. RPN = Severity x Occurrence x Detection."""
    __tablename__ = "fmea"
    id = Column(Integer, primary_key=True)
    failure_mode = Column(String(200), nullable=False)
    effect = Column(String(200), default="")
    severity = Column(Integer, default=1)
    occurrence = Column(Integer, default=1)
    detection = Column(Integer, default=1)
    mitigation = Column(Text, default="")

    @property
    def rpn(self) -> int:
        return (self.severity or 0) * (self.occurrence or 0) * (self.detection or 0)
