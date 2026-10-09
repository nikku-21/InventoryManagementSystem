"""About page (Q10 feature): project, course and version information."""
from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from .. import config


class AboutPage(QWidget):
    def __init__(self, user=None):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel(config.APP_NAME)
        title.setObjectName("title")
        info = QLabel(
            f"<p><b>Version:</b> {config.VERSION}</p>"
            f"<p><b>Course:</b> {config.COURSE} (Session {config.SESSION})</p>"
            f"<p><b>Project code:</b> {config.PROJECT_CODE} &mdash; Quality goal: <i>{config.QUALITY_GOAL}</i></p>"
            f"<p><b>Developed by:</b> {config.AUTHOR} ({config.REG_NO})</p>"
            f"<p><b>Source code:</b> {config.GITHUB_URL}</p>"
            "<p><b>Built with:</b> Python 3, PySide6, SQLite, SQLAlchemy, Pandas, Matplotlib, "
            "ReportLab, OpenPyXL, bcrypt</p>"
            "<p><b>TQM principles applied:</b> Customer focus, Kaizen (PDCA), process-centric approach, "
            "fact-based decisions, Poka-Yoke error prevention.</p>")
        info.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(info)
        layout.addStretch()
