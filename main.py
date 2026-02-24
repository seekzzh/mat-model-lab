# Main entry point for Mat Model Lab

import os
import sys
from PyQt6.QtWidgets import QApplication

# Ensure the project root is on the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MatModelLab_GUI

def main():
    """Main function to start the Mat Model Lab GUI"""
    app = QApplication(sys.argv)
    window = MatModelLab_GUI()
    window.show()
    sys.exit(app.exec())  # PyQt6 uses exec() instead of exec_()

if __name__ == "__main__":
    main()