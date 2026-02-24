# Path utilities for Mat Model Lab
# Provides resource path resolution for both development and PyInstaller environments.

import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to a resource file.

    Works in both development (running from source) and PyInstaller
    (frozen executable) environments.

    Parameters
    ----------
    relative_path : str
        Path relative to the project root (e.g. 'assets/icon.png').

    Returns
    -------
    str
        Absolute path to the resource.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running from source — resolve relative to this file's location
        # mml_utils/ is one level below the project root
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)
