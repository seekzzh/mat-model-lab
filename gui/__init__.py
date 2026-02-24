# GUI module for Mat Model Lab

# Fix import path issues, allowing the script to run directly or be imported as a module
try:
    # Use this path when imported as a module
    from .main_window import MatModelLab_GUI
except ImportError:
    # Use this path when running the script directly
    import sys
    import os
    # Add the project root directory to the Python path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from gui.main_window import MatModelLab_GUI

__all__ = ['MatModelLab_GUI']