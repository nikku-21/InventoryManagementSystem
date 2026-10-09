"""Main window: sidebar navigation + stacked pages, shortcuts and role handling."""
from __future__ import annotations

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QHBoxLayout, QListWidget, QMainWindow, QStackedWidget, QWidget

from .. import config
from .about_page import AboutPage
from .dashboard_page import DashboardPage
from .help_page import HelpPage
from .login import LoginDialog          # re-exported for main.py
from .master_pages import audit_page, categories_page, history_page, suppliers_page
from .products_page import ProductsPage
from .quality_page import QualityPage
from .reports_page import ReportsPage
from .users_page import UsersPage

__all__ = ["MainWindow", "LoginDialog"]


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"{config.APP_NAME}  -  {user.username} ({user.role})")
        self.resize(1150, 700)

        # (sidebar label, page factory, admin-only?)
        pages = [
            ("Dashboard", DashboardPage, False), ("Products", ProductsPage, False),
            ("Categories", categories_page, False), ("Suppliers", suppliers_page, False),
            ("Stock History", history_page, False), ("Reports", ReportsPage, False),
            ("Quality (TQM)", QualityPage, False), ("Audit Log", audit_page, True),
            ("Users", UsersPage, True), ("Help & FAQ", HelpPage, False), ("About", AboutPage, False),
        ]
        self.sidebar = QListWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(190)
        self.stack = QStackedWidget()
        self.help_index = 0
        for label, factory, admin_only in pages:
            if admin_only and user.role != "admin":
                continue
            self.sidebar.addItem(label)
            self.stack.addWidget(factory(user))
            if label.startswith("Help"):
                self.help_index = self.stack.count() - 1

        root = QWidget()
        row = QHBoxLayout(root)
        row.setContentsMargins(0, 0, 0, 0)
        row.addWidget(self.sidebar)
        row.addWidget(self.stack, 1)
        self.setCentralWidget(root)

        self.sidebar.currentRowChanged.connect(self._switch)
        self.sidebar.setCurrentRow(0)
        for i in range(min(9, self.stack.count())):
            QShortcut(QKeySequence(f"Ctrl+{i + 1}"), self, activated=lambda i=i: self.sidebar.setCurrentRow(i))
        QShortcut(QKeySequence("F1"), self, activated=lambda: self.sidebar.setCurrentRow(self.help_index))
        QShortcut(QKeySequence("Ctrl+Q"), self, activated=self.close)
        self.statusBar().showMessage("F1 = Help   |   Ctrl+1..9 = switch pages   |   Ctrl+F = search")

    def _switch(self, row):
        self.stack.setCurrentIndex(row)
        page = self.stack.currentWidget()
        if hasattr(page, "refresh"):
            page.refresh()               # always show fresh data
