"""Authentication: bcrypt password hashing, user creation and login checks.

Note: bcrypt is used directly (the library behind passlib's bcrypt scheme) because
passlib is unmaintained and breaks with recent bcrypt releases.
"""
from __future__ import annotations

import bcrypt
from sqlalchemy.exc import IntegrityError

from .db import SessionLocal
from .models import AuditLog, User

session = SessionLocal()   # shared long-lived session (single-user desktop app)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def log_action(user: str, action: str) -> None:
    """Write one line to the audit trail."""
    session.add(AuditLog(user=user, action=action))
    session.commit()


def create_user(username: str, password: str, role: str = "staff") -> User:
    username = username.strip()
    if not username:
        raise ValueError("Username is required.")
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters.")
    try:
        user = User(username=username, password_hash=hash_password(password), role=role)
        session.add(user)
        session.commit()
        return user
    except IntegrityError as exc:
        session.rollback()
        raise ValueError("That username already exists.") from exc


def authenticate(username: str, password: str) -> User | None:
    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        log_action(username, "Logged in")
        return user
    return None
