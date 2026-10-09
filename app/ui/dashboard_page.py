"""Dashboard: KPI tiles, low-stock list and a stock chart."""
from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QVBoxLayout, QWidget

from .. import charts, services
from .chart_canvas import ChartCanvas


class DashboardPage(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        layout = QVBoxLayout(self)
        heading = QLabel(f"Welcome, {user.username}")
        heading.setObjectName("title")
        layout.addWidget(heading)

        row = QHBoxLayout()
        self.kpis = {}
        for key in ("products", "units", "value", "low"):
            label = QLabel()
            label.setObjectName("kpi")
            self.kpis[key] = label
            row.addWidget(label)
        layout.addLayout(row)

        lower = QHBoxLayout()
        self.canvas = ChartCanvas()
        lower.addWidget(self.canvas, 3)
        side = QVBoxLayout()
        side.addWidget(QLabel("Items to re-order:"))
        self.low_list = QListWidget()
        side.addWidget(self.low_list)
        lower.addLayout(side, 1)
        layout.addLayout(lower)
        self.refresh()

    def refresh(self):
        stats = services.dashboard_stats()
        self.kpis["products"].setText(f"Products\n{stats['products']}")
        self.kpis["units"].setText(f"Units in stock\n{stats['units']}")
        self.kpis["value"].setText(f"Stock value\n{stats['value']:,.2f}")
        self.kpis["low"].setText(f"Low-stock items\n{stats['low']}")
        self.low_list.clear()
        for p in services.low_stock():
            self.low_list.addItem(f"{p.sku} - {p.name} ({p.quantity} left)")
        self.canvas.draw_with(charts.stock_by_category_chart)
