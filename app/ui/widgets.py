"""Reusable GUI building blocks: Field, FormDialog and the generic CrudPage."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QKeySequence, QShortcut
from PySide6.QtWidgets import (QAbstractItemView, QComboBox, QDialog, QDialogButtonBox,
                               QDoubleSpinBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMessageBox, QPlainTextEdit, QPushButton, QSpinBox, QTableWidget,
                               QTableWidgetItem, QVBoxLayout, QWidget)

from .. import services


class Field:
    """Describes one input in a form.

    kind: "text" | "int" | "float" | "choice" | "long" | "password"
    choices: list of (value, label) tuples or plain strings (for kind="choice").
    """

    def __init__(self, key, label, kind="text", required=False, choices=None,
                 minimum=0, maximum=1_000_000, tip=""):
        self.key, self.label, self.kind = key, label, kind
        self.required, self.choices = required, choices
        self.minimum, self.maximum, self.tip = minimum, maximum, tip

    def options(self):
        items = self.choices() if callable(self.choices) else (self.choices or [])
        return [(i, i) if isinstance(i, str) else i for i in items]


class FormDialog(QDialog):
    """Generic add/edit dialog built from a list of Field objects."""

    def __init__(self, title, fields, obj=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(400)
        self.fields, self.widgets = fields, {}
        form = QFormLayout(self)
        for f in fields:
            widget = self._make_widget(f)
            if f.tip:
                widget.setToolTip(f.tip)
            if obj is not None and f.kind != "password":
                self._set_value(widget, f, getattr(obj, f.key, None))
            self.widgets[f.key] = widget
            form.addRow(f.label + (" *" if f.required else ""), widget)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    @staticmethod
    def _make_widget(f):
        if f.kind == "int":
            w = QSpinBox()
            w.setRange(f.minimum, f.maximum)
        elif f.kind == "float":
            w = QDoubleSpinBox()
            w.setDecimals(2)
            w.setRange(f.minimum, f.maximum)
        elif f.kind == "choice":
            w = QComboBox()
            for value, label in f.options():
                w.addItem(label, value)
        elif f.kind == "long":
            w = QPlainTextEdit()
            w.setFixedHeight(70)
        else:
            w = QLineEdit()
            if f.kind == "password":
                w.setEchoMode(QLineEdit.EchoMode.Password)
        return w

    @staticmethod
    def _set_value(w, f, value):
        if f.kind in ("int", "float"):
            w.setValue(value or 0)
        elif f.kind == "choice":
            idx = w.findData(value)
            w.setCurrentIndex(idx if idx >= 0 else 0)
        elif f.kind == "long":
            w.setPlainText(value or "")
        else:
            w.setText(str(value or ""))

    def values(self) -> dict:
        out = {}
        for f in self.fields:
            w = self.widgets[f.key]
            if f.kind in ("int", "float"):
                out[f.key] = w.value()
            elif f.kind == "choice":
                out[f.key] = w.currentData()
            elif f.kind == "long":
                out[f.key] = w.toPlainText().strip()
            else:
                out[f.key] = w.text().strip()
        return out

    def accept(self):
        """Poka-Yoke: refuse to close while a required field is empty."""
        for f in self.fields:
            if f.required and f.kind in ("text", "password", "long") and not self.values()[f.key]:
                QMessageBox.warning(self, "Missing data", f"'{f.label}' is required.")
                return
        super().accept()


class CrudPage(QWidget):
    """A searchable table with Add / Edit / Delete buttons for any ORM model."""

    def __init__(self, user, model, fields, columns, noun, sort_key=None, read_only=False, hint=""):
        super().__init__()
        self.user, self.model, self.fields = user, model, fields
        self.columns, self.noun, self.sort_key = columns, noun, sort_key
        self.objs = []

        layout = QVBoxLayout(self)
        if hint:
            tip = QLabel(hint)
            tip.setWordWrap(True)
            layout.addWidget(tip)
        bar = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...  (Ctrl+F)")
        self.search.textChanged.connect(self._filter)
        bar.addWidget(self.search, 1)
        self.bar = bar
        self.btn_add, self.btn_edit, self.btn_del = QPushButton("Add"), QPushButton("Edit"), QPushButton("Delete")
        self.btn_del.setObjectName("danger")
        self.btn_add.clicked.connect(self.add)
        self.btn_edit.clicked.connect(self.edit)
        self.btn_del.clicked.connect(self.remove)
        if not read_only:
            for b in (self.btn_add, self.btn_edit, self.btn_del):
                bar.addWidget(b)
        layout.addLayout(bar)

        self.table = QTableWidget(0, len(columns))
        self.table.setHorizontalHeaderLabels([c[0] for c in columns])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.doubleClicked.connect(lambda: None if read_only else self.edit())
        layout.addWidget(self.table)
        QShortcut(QKeySequence("Ctrl+F"), self, activated=self.search.setFocus)
        self.refresh()

    # -- hooks subclasses may override ------------------------------------
    def row_color(self, obj):
        return None

    def save(self, data, obj_id):
        services.save(self.model, data, obj_id, self.user.username)

    # -- behaviour --------------------------------------------------------
    def refresh(self):
        self.objs = services.list_all(self.model)
        if self.sort_key:
            self.objs.sort(key=self.sort_key)
        self.table.setRowCount(len(self.objs))
        for r, obj in enumerate(self.objs):
            color = self.row_color(obj)
            for c, (_, getter) in enumerate(self.columns):
                item = QTableWidgetItem(str(getter(obj)))
                if c == 0:
                    item.setData(Qt.ItemDataRole.UserRole, obj.id)
                if color:
                    item.setBackground(QColor(color))
                    item.setForeground(QColor("#7f1d1d"))
                self.table.setItem(r, c, item)
        self._filter(self.search.text())

    def _filter(self, text):
        text = text.lower()
        for r in range(self.table.rowCount()):
            hit = any(text in (self.table.item(r, c).text().lower() if self.table.item(r, c) else "")
                      for c in range(self.table.columnCount()))
            self.table.setRowHidden(r, not hit)

    def selected_id(self):
        row = self.table.currentRow()
        if row < 0 or self.table.item(row, 0) is None:
            QMessageBox.information(self, "Select a row", f"Please select a {self.noun} first.")
            return None
        return self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)

    def _persist(self, data, obj_id):
        try:
            self.save(data, obj_id)
        except ValueError as exc:
            QMessageBox.warning(self, "Cannot save", str(exc))
            return
        self.refresh()

    def add(self):
        dlg = FormDialog(f"Add {self.noun}", self.fields, parent=self)
        if dlg.exec():
            self._persist(dlg.values(), None)

    def edit(self):
        obj_id = self.selected_id()
        if obj_id is None:
            return
        obj = services.session.get(self.model, obj_id)
        dlg = FormDialog(f"Edit {self.noun}", self.fields, obj=obj, parent=self)
        if dlg.exec():
            self._persist(dlg.values(), obj_id)

    def remove(self):
        if self.user.role != "admin":
            QMessageBox.warning(self, "Not allowed", "Only administrators can delete records.")
            return
        obj_id = self.selected_id()
        if obj_id is None:
            return
        answer = QMessageBox.question(self, "Confirm delete", f"Delete this {self.noun}? This cannot be undone.")
        if answer == QMessageBox.StandardButton.Yes:
            services.delete(self.model, obj_id, self.user.username)
            self.refresh()
