"""Entry point of the Inventory Management System (BBAT104 TQM project, Q10).

Run with:  python main.py
Default login (change it after the first start):  admin / Admin@123
"""
import sys

from PySide6.QtWidgets import QApplication, QDialog

from app import services
from app.ui.main_window import LoginDialog, MainWindow
from app.ui.style import STYLE


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)            # modern look & feel (see app/ui/style.py)
    services.init_db()                  # create tables + seed first-run data

    login = LoginDialog()
    if login.exec() != QDialog.DialogCode.Accepted:
        return 0                        # user closed the login window

    window = MainWindow(login.user)     # keep a reference so it is not garbage-collected
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
