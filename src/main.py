"""Main.py

This module creates the Qt application and shows the main window.

Run instructions:
  Use the project's virtual environment to run this file so PySide6 is
  loaded from the project venv. 
  
"""

import sys
from PySide6.QtWidgets import QApplication

from gui import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


