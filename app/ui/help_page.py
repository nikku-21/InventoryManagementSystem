"""Help screen (Q10 feature): searchable FAQ, in-app User Manual and shortcuts."""
from __future__ import annotations

from PySide6.QtWidgets import (QHBoxLayout, QLineEdit, QListWidget, QTabWidget, QTextBrowser,
                               QVBoxLayout, QWidget)

from ..db import BASE_DIR
from ..help_content import FAQS

SHORTCUTS_HTML = """
<h2>Keyboard shortcuts</h2>
<table cellpadding="6">
<tr><td><b>Ctrl+1 ... Ctrl+9</b></td><td>Switch between pages</td></tr>
<tr><td><b>F1</b></td><td>Open this Help screen</td></tr>
<tr><td><b>Ctrl+F</b></td><td>Jump to the search box of the current table</td></tr>
<tr><td><b>Double-click</b></td><td>Edit the selected row</td></tr>
<tr><td><b>Ctrl+Q</b></td><td>Quit</td></tr>
</table>
"""


class HelpPage(QWidget):
    def __init__(self, user=None):
        super().__init__()
        tabs = QTabWidget()

        # --- FAQ tab: search box + list of questions + answer viewer
        faq = QWidget()
        faq_layout = QVBoxLayout(faq)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search the FAQ...")
        self.search.textChanged.connect(self._filter)
        faq_layout.addWidget(self.search)
        row = QHBoxLayout()
        self.questions = QListWidget()
        self.answer = QTextBrowser()
        row.addWidget(self.questions, 2)
        row.addWidget(self.answer, 3)
        faq_layout.addLayout(row)
        for question, _ in FAQS:
            self.questions.addItem(question)
        self.questions.currentRowChanged.connect(self._show)
        self.questions.setCurrentRow(0)

        # --- Manual tab: renders docs/USER_MANUAL.md
        manual = QTextBrowser()
        manual_file = BASE_DIR / "docs" / "USER_MANUAL.md"
        if manual_file.exists():
            manual.setMarkdown(manual_file.read_text(encoding="utf-8"))
        else:
            manual.setPlainText("docs/USER_MANUAL.md was not found.")

        shortcuts = QTextBrowser()
        shortcuts.setHtml(SHORTCUTS_HTML)

        tabs.addTab(faq, "FAQ")
        tabs.addTab(manual, "User Manual")
        tabs.addTab(shortcuts, "Shortcuts")
        QVBoxLayout(self).addWidget(tabs)

    def _show(self, row):
        if 0 <= row < len(FAQS):
            self.answer.setHtml(f"<h3>{FAQS[row][0]}</h3><p>{FAQS[row][1]}</p>")

    def _filter(self, text):
        text = text.lower()
        for i, (q, a) in enumerate(FAQS):
            self.questions.item(i).setHidden(text not in (q + " " + a).lower())
