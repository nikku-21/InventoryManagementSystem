"""Quality (TQM) page: Defect Log checksheet, FMEA matrix, Pareto and Fishbone charts."""
from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QPushButton, QTabWidget, QVBoxLayout, QWidget

from .. import charts
from ..help_content import TOOLTIPS
from ..models import Defect, FmeaItem
from .chart_canvas import ChartCanvas
from .widgets import CrudPage, Field

DEFECT_TYPES = ["Validation", "UI/UX", "Database", "Calculation", "Crash", "Documentation"]


class FmeaPage(CrudPage):
    """FMEA table sorted by risk; RPN of 200 or more is highlighted."""

    def __init__(self, user):
        fields = [
            Field("failure_mode", "Failure mode", required=True),
            Field("effect", "Effect"),
            Field("severity", "Severity (1-10)", "int", minimum=1, maximum=10, tip=TOOLTIPS["severity"]),
            Field("occurrence", "Occurrence (1-10)", "int", minimum=1, maximum=10, tip=TOOLTIPS["occurrence"]),
            Field("detection", "Detection (1-10)", "int", minimum=1, maximum=10, tip=TOOLTIPS["detection"]),
            Field("mitigation", "Mitigation", "long"),
        ]
        cols = [("ID", lambda f: f.id), ("Failure mode", lambda f: f.failure_mode), ("Effect", lambda f: f.effect),
                ("S", lambda f: f.severity), ("O", lambda f: f.occurrence), ("D", lambda f: f.detection),
                ("RPN", lambda f: f.rpn), ("Mitigation", lambda f: f.mitigation)]
        super().__init__(user, FmeaItem, fields, cols, "FMEA row", sort_key=lambda f: -f.rpn,
                         hint="RPN = Severity x Occurrence x Detection. Fix the highest RPN first.")

    def row_color(self, item):
        return "#fee2e2" if item.rpn >= 200 else None


class QualityPage(QWidget):
    def __init__(self, user):
        super().__init__()
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        defect_fields = [
            Field("title", "Defect description", required=True),
            Field("defect_type", "Type", "choice", choices=DEFECT_TYPES),
            Field("severity", "Severity", "choice", choices=["Low", "Medium", "High"]),
            Field("status", "Status", "choice", choices=["Open", "Fixed"]),
        ]
        defect_cols = [("ID", lambda d: d.id), ("Defect", lambda d: d.title), ("Type", lambda d: d.defect_type),
                       ("Severity", lambda d: d.severity), ("Status", lambda d: d.status),
                       ("Logged", lambda d: d.logged_on.strftime("%Y-%m-%d"))]
        self.defects = CrudPage(user, Defect, defect_fields, defect_cols, "defect",
                                hint="Checksheet: log every bug you find. The Pareto chart is built from this list.")
        self.fmea = FmeaPage(user)

        charts_tab = QWidget()
        box = QVBoxLayout(charts_tab)
        row = QHBoxLayout()
        pareto, fishbone = QPushButton("Pareto chart"), QPushButton("Fishbone diagram")
        row.addWidget(pareto)
        row.addWidget(fishbone)
        row.addStretch()
        box.addLayout(row)
        self.canvas = ChartCanvas(7, 4.5)
        box.addWidget(self.canvas)
        pareto.clicked.connect(lambda: self.canvas.draw_with(charts.pareto_chart))
        fishbone.clicked.connect(lambda: self.canvas.draw_with(charts.fishbone_chart))

        self.tabs.addTab(self.defects, "Defect Log")
        self.tabs.addTab(self.fmea, "FMEA")
        self.tabs.addTab(charts_tab, "SQC Charts")
        layout.addWidget(self.tabs)

    def refresh(self):
        self.defects.refresh()
        self.fmea.refresh()
