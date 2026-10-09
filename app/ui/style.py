"""Qt style sheet (QSS) for a clean, modern look."""

STYLE = """
QWidget { font-family: "Segoe UI", "Helvetica Neue", Arial; font-size: 10.5pt; }
QMainWindow, QDialog { background: #f1f5f9; }
QListWidget#sidebar { background: #1e3a8a; color: #dbeafe; border: none; outline: 0; }
QListWidget#sidebar::item { padding: 12px 16px; }
QListWidget#sidebar::item:selected { background: #2563eb; color: white; }
QPushButton { background: #2563eb; color: white; border: none; border-radius: 6px; padding: 7px 16px; }
QPushButton:hover { background: #1d4ed8; }
QPushButton:disabled { background: #94a3b8; }
QPushButton#danger { background: #dc2626; }
QPushButton#danger:hover { background: #b91c1c; }
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QPlainTextEdit {
    background: white; border: 1px solid #cbd5e1; border-radius: 5px; padding: 5px; }
QTableWidget { background: white; alternate-background-color: #eff6ff; gridline-color: #e2e8f0; }
QHeaderView::section { background: #1e3a8a; color: white; padding: 6px; border: none; }
QLabel#kpi { background: white; border-radius: 10px; padding: 14px; font-size: 13pt; }
QLabel#title { font-size: 18pt; font-weight: bold; color: #1e3a8a; }
QTabWidget::pane { border: 1px solid #cbd5e1; background: white; }
QTextBrowser { background: white; border: 1px solid #cbd5e1; }
"""
