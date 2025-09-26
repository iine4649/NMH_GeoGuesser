"""Main.py

This module creates the Qt application and shows the main window.

Run instructions:
  Use the project's virtual environment to run this file so PySide6 is
  loaded from the project venv. 
  
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Change working directory to project root for proper file paths
os.chdir(project_root)

from src.gui import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


