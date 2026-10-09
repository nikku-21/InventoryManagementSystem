"""Login window (Role-based login)."""
from __future__ import annotations

from PySide6.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QPushButton

from .. import auth, config


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.user = None
        self.setWindowTitle(f"{config.APP_NAME} - Login")
        self.setMinimumWidth(360)
        form = QFormLayout(self)
        title = QLabel(config.APP_NAME)
        title.setObjectName("title")
        form.addRow(title)
        self.username = QLineEdit()
        self.username.setPlaceholderText("admin")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.returnPressed.connect(self.attempt)
        self.error = QLabel("")
        self.error.setStyleSheet("color: #dc2626;")
        button = QPushButton("Log in")
        button.clicked.connect(self.attempt)
        form.addRow("Username", self.username)
        form.addRow("Password", self.password)
        form.addRow(self.error)
        form.addRow(button)

    def attempt(self):
        user = auth.authenticate(self.username.text().strip(), self.password.text())
        if user:
            self.user = user
            self.accept()
        else:
            self.error.setText("Invalid username or password.")
