"""Users page (admin only): create accounts with hashed passwords."""
from __future__ import annotations

from .. import auth
from ..models import User
from .widgets import CrudPage, Field


class UsersPage(CrudPage):
    def __init__(self, user):
        fields = [
            Field("username", "Username", required=True),
            Field("password", "Password (min 6 chars)", "password", required=True),
            Field("role", "Role", "choice", choices=["staff", "admin"]),
        ]
        cols = [("ID", lambda u: u.id), ("Username", lambda u: u.username), ("Role", lambda u: u.role)]
        super().__init__(user, User, fields, cols, "user")
        self.btn_edit.hide()          # passwords are only set when an account is created

    def save(self, data, obj_id):
        auth.create_user(data["username"], data["password"], data["role"])
        auth.log_action(self.user.username, f"Created user {data['username']}")
