"""Reports page: Excel / PDF / CSV export, chart export and database backup."""
from __future__ import annotations

from PySide6.QtWidgets import QFileDialog, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from .. import charts, exports, services
from .chart_canvas import ChartCanvas


class ReportsPage(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        layout = QVBoxLayout(self)
        title = QLabel("Reports & Backup")
        title.setObjectName("title")
        layout.addWidget(title)
        layout.addWidget(QLabel("Export your data or save a safety copy of the database."))
        for text, handler in (
            ("Export Excel (.xlsx)", lambda: self._export("Excel (*.xlsx)", "inventory.xlsx", exports.export_excel)),
            ("Export PDF report", lambda: self._export("PDF (*.pdf)", "stock_report.pdf", exports.export_pdf)),
            ("Export CSV", lambda: self._export("CSV (*.csv)", "products.csv", exports.export_csv)),
            ("Save stock chart as PNG", self._save_chart),
            ("Backup database", self._backup),
        ):
            button = QPushButton(text)
            button.clicked.connect(handler)
            layout.addWidget(button)
        self.canvas = ChartCanvas()
        layout.addWidget(self.canvas)

    def refresh(self):
        self.canvas.draw_with(charts.stock_by_category_chart)

    def _ask_path(self, flt, default):
        path, _ = QFileDialog.getSaveFileName(self, "Save as", default, flt)
        return path

    def _export(self, flt, default, function):
        path = self._ask_path(flt, default)
        if not path:
            return
        try:
            function(path)
        except Exception as exc:     # show a friendly alert instead of crashing (Q18 style)
            QMessageBox.critical(self, "Export failed", str(exc))
            return
        services.log_action(self.user.username, f"Exported {path}")
        QMessageBox.information(self, "Done", f"Saved to:\n{path}")

    def _save_chart(self):
        path = self._ask_path("PNG (*.png)", "stock_chart.png")
        if path:
            self.canvas.figure.savefig(path, dpi=150)
            QMessageBox.information(self, "Done", f"Saved to:\n{path}")

    def _backup(self):
        path = services.backup_db()
        services.log_action(self.user.username, "Database backup")
        QMessageBox.information(self, "Backup created", path)
