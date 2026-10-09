"""Database layer: SQLAlchemy engine and session factory (SQLite).

The ORM models live in app/models.py.
"""
from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
# INVENTORY_DB lets the unit tests use a throw-away database.
DB_FILE = Path(os.environ.get("INVENTORY_DB", BASE_DIR / "data" / "inventory.db"))
DB_FILE.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_FILE}", future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()
