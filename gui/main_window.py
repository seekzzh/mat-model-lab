# Main GUI window for Mat Model Lab (Shell)

import os
import sys
import datetime
try:
    import winreg
except ImportError:
    winreg = None

from mml_utils.paths import resource_path

from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
                             QFileDialog, QTabWidget, QGroupBox, QRadioButton,
                             QCheckBox, QSpinBox, QDoubleSpinBox, QMessageBox,
                             QLineEdit, QGridLayout, QFrame, QStackedWidget)
from PyQt6.QtGui import QIcon, QPixmap, QAction, QPalette, QColor, QPainter, QPen, QTextDocument
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtCore import Qt

from .widgets.help_dialog import HelpDialog
from .widgets.documentation_dialog import DocumentationDialog
from .widgets.about_dialog import AboutDialog
from .widgets.material_browser import MaterialBrowser
from .modules.elasticity.widget import ElasticityWidget
from .modules.plasticity.widget import PlasticityWidget
from .modules.hyperelasticity.widget import HyperelasticityWidget
from mml_utils.material_db import get_database
import matplotlib # For rcParams

class MatModelLab_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle('Mat Model Lab')
        self.resize(1200, 800)
        self.set_initial_position()
        
        # Icon
        icon_path = resource_path('assets/icon.png')
        self.setWindowIcon(QIcon(icon_path))
        
        # Central Stack
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Modules
        self.elasticity_widget = ElasticityWidget()
        self.plasticity_widget = PlasticityWidget()
        self.hyperelasticity_widget = HyperelasticityWidget()
        
        self.stack.addWidget(self.elasticity_widget)
        self.stack.addWidget(self.plasticity_widget)
        self.stack.addWidget(self.hyperelasticity_widget)
        
        # Menu Bar
        self.createMenuBar()
        
        # Apply modern theme (default: Auto)
        self.set_auto_theme()

    def set_initial_position(self):
        """Center the window horizontally and align to top vertically"""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        
        # Center horizontally
        x = (screen.width() - size.width()) // 2
        
        # Align to top (with small padding)
        y = screen.top() + 5 
        
        # Adjust for top-left position relative to screen if multiple screens
        x += screen.left()
        
        self.move(x, y)
        
    def createMenuBar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False) # Fix for invisible text on Windows
        menubar.clear()
        
        # File Menu
        file_menu = menubar.addMenu('File')
        
        # View Menu (moved before Modules)
        view_menu = menubar.addMenu('View')
        theme_menu = view_menu.addMenu('Theme')
        
        auto_action = QAction('Auto Mode (System/Time)', self)
        auto_action.triggered.connect(self.set_auto_theme)
        theme_menu.addAction(auto_action)
        theme_menu.addSeparator()
        
        dark_action = QAction('Dark Mode', self)
        dark_action.triggered.connect(lambda: self.apply_modern_theme('dark'))
        theme_menu.addAction(dark_action)
        
        light_action = QAction('Light Mode', self)
        light_action.triggered.connect(lambda: self.apply_modern_theme('light'))
        theme_menu.addAction(light_action)
        
        # Modules Menu
        modules_menu = menubar.addMenu('Modules')
        
        elasticity_action = QAction('Elasticity', self)
        elasticity_action.triggered.connect(lambda: self.switch_module(0))
        modules_menu.addAction(elasticity_action)
        
        # Placeholders for future
        plasticity_action = QAction('Plasticity', self)
        plasticity_action.triggered.connect(lambda: self.switch_module(1))
        modules_menu.addAction(plasticity_action)
        
        hyper_action = QAction('Hyperelasticity', self)
        hyper_action.triggered.connect(lambda: self.switch_module(2))
        modules_menu.addAction(hyper_action)
        
        # Database Menu
        database_menu = menubar.addMenu('Database')
        
        browse_action = QAction('Browse Materials...', self)
        browse_action.setShortcut('Ctrl+B')
        browse_action.triggered.connect(self.openMaterialBrowser)
        database_menu.addAction(browse_action)
        
        database_menu.addSeparator()
        
        reload_action = QAction('Reload Database', self)
        reload_action.triggered.connect(self.reloadDatabase)
        database_menu.addAction(reload_action)
        
        # Help Menu
        help_menu = menubar.addMenu('Help')
        
        # Documentation Action
        doc_action = QAction('Documentation', self)
        doc_action.setShortcut('F1')
        doc_action.setStatusTip('Show documentation')
        doc_action.triggered.connect(self.showDocumentation)
        help_menu.addAction(doc_action)
        
        # About Action
        about_action = QAction('About', self)
        about_action.setStatusTip('Show about information')
        about_action.triggered.connect(self.showAbout)
        help_menu.addAction(about_action)

        # Exit Action
        file_menu.addSeparator()
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def switch_module(self, index):
        self.stack.setCurrentIndex(index)
        # Maybe update title or status bar
        
    def showDocumentation(self):
        """Show the documentation dialog"""
        # Check if current_theme is dark
        is_dark = getattr(self, 'current_theme', 'dark') == 'dark'
        dialog = DocumentationDialog(self, is_dark=is_dark)
        dialog.exec()
        
    def showAbout(self):
        """Show about dialog"""
        is_dark = getattr(self, 'current_theme', 'dark') == 'dark'
        dialog = AboutDialog(self, is_dark=is_dark)
        dialog.exec()

    def detect_auto_theme(self):
        """Detect system theme or use time-based fallback"""
        # 1. Try Windows Registry
        if winreg:
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                value, _ = winreg.QueryValueEx(registry_key, "AppsUseLightTheme")
                winreg.CloseKey(registry_key)
                return 'light' if value == 1 else 'dark'
            except Exception:
                pass
        
        # 2. Fallback to Time (6 AM to 6 PM is light)
        current_hour = datetime.datetime.now().hour
        if 6 <= current_hour < 18:
            return 'light'
        else:
            return 'dark'
            
    def set_auto_theme(self):
        """Apply theme based on auto-detection"""
        theme = self.detect_auto_theme()
        self.apply_modern_theme(theme)
        self.statusBar().showMessage(f"Auto Mode: Applied {theme.capitalize()} Theme")

    def apply_modern_theme(self, theme='dark'):
        """Apply a modern, professional stylesheet to the application."""
        self.current_theme = theme
        
        # Configure Matplotlib style - Always use Default (Light) for plots as requested
        import matplotlib.pyplot as plt
        plt.style.use('default')
        
        # Configure Fonts and Colors for "Premium" Look
        matplotlib.rcParams.update({
            'font.family': 'sans-serif',
            'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans'],
            'font.size': 10,
            'axes.titlesize': 12,
            'axes.labelsize': 11,
            'axes.labelweight': 'bold',
            'axes.titleweight': 'bold',
            'xtick.labelsize': 9,
            'ytick.labelsize': 9,
            'legend.fontsize': 10,
            'figure.titlesize': 14,
            'figure.titleweight': 'bold',
            'text.color': '#333333',
            'axes.labelcolor': '#333333',
            'xtick.color': '#333333',
            'ytick.color': '#333333',
            'axes.edgecolor': '#cccccc',
            'grid.color': '#f0f0f0',
            'axes.grid': False, 
            'lines.linewidth': 1.5,
            'mathtext.fontset': 'cm',
        })
        
        # Plot Colors (Fixed to Light)
        plot_bg = "#ffffff"
        
        # Update Application Palette to guide Matplotlib Icon selection (and other native widgets)
        palette = QApplication.palette()
        
        if theme == 'dark':
            # Palette Definition - Dark
            bg_color = "#1e1e1e"        # VS Code-like Dark
            panel_bg = "#252526"        # Slightly lighter for panels
            text_color = "#f0f0f0"      # Off-white text
            muted_text = "#cccccc"
            border_color = "#454545"    
            input_bg = "#3c3c3c"
            input_disabled_bg = "#2d2d2d" # Darker grey for disabled
            accent_color = "#3498db"    # Blue
            primary_color = "#ffffff"   # Key headers
            
            # Apply Dark Palette
            palette.setColor(QPalette.ColorRole.Window, QColor(bg_color))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(text_color))
            palette.setColor(QPalette.ColorRole.Base, QColor(input_bg))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(panel_bg))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(bg_color))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(text_color))
            palette.setColor(QPalette.ColorRole.Text, QColor(text_color))
            palette.setColor(QPalette.ColorRole.Button, QColor(panel_bg))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(text_color))
            palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            palette.setColor(QPalette.ColorRole.Link, QColor(accent_color))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(accent_color))
            palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
            QApplication.instance().setPalette(palette)
            
            # Icons
            up_arrow_path = resource_path("assets/up_arrow_white.png").replace("\\", "/")
            down_arrow_path = resource_path("assets/down_arrow_white.png").replace("\\", "/")
            up_arrow = f"url({up_arrow_path})"
            down_arrow = f"url({down_arrow_path})"
            
        else:
            # Palette Definition - Light
            bg_color = "#f8f9fa"
            panel_bg = "#ffffff"
            text_color = "#333333"
            muted_text = "#555555"
            border_color = "#e0e0e0"
            input_bg = "#cfe2f3"        # Stronger Light Blue
            input_disabled_bg = "#f0f0f0" # Lighter Grey for disabled
            accent_color = "#3498db"
            primary_color = "#2c3e50"
            
            # Apply Light Palette
            palette.setColor(QPalette.ColorRole.Window, QColor(bg_color))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(text_color))
            palette.setColor(QPalette.ColorRole.Base, QColor(input_bg))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(panel_bg))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(bg_color))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(text_color))
            palette.setColor(QPalette.ColorRole.Text, QColor(text_color))
            palette.setColor(QPalette.ColorRole.Button, QColor(panel_bg))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(text_color))
            palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            palette.setColor(QPalette.ColorRole.Link, QColor(accent_color))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(accent_color))
            palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
            QApplication.instance().setPalette(palette)
            
            # Icons
            up_arrow_path = resource_path("assets/up_arrow.png").replace("\\", "/")
            down_arrow_path = resource_path("assets/down_arrow.png").replace("\\", "/")
            up_arrow = f"url({up_arrow_path})"
            down_arrow = f"url({down_arrow_path})"

        style_sheet = f"""
            QMainWindow {{
                background-color: {bg_color};
                color: {text_color};
            }}
            
            QWidget {{
                background-color: {bg_color};
                color: {text_color};
            }}
            
            QMenuBar {{
                background-color: {bg_color};
                border-bottom: 1px solid {border_color};
                color: {text_color};
            }}
            
            QMenuBar::item:selected {{
                background-color: {accent_color};
                color: white;
            }}
            
            QMenu {{
                background-color: {panel_bg};
                border: 1px solid {border_color};
                color: {text_color};
            }}
            
            QMenu::item {{
                padding: 6px 40px 6px 20px;
                background-color: transparent;
                margin: 0px;
            }}
            
            QMenu::item:selected {{
                background-color: {accent_color};
                color: white;
            }}
            
            QGroupBox {{
                border: 1px solid {border_color};
                border-radius: 5px;
                margin-top: 10px;
                background-color: {panel_bg};
                font-weight: bold;
                color: {primary_color};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
                background-color: {panel_bg};
            }}
            
            QLabel {{
                color: {text_color};
                background-color: transparent;
            }}
            
            QCheckBox, QRadioButton {{
                color: {text_color};
                background-color: transparent;
                spacing: 5px;
            }}
            
            QCheckBox::indicator, QRadioButton::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {border_color};
                border-radius: 3px;
                background-color: {input_bg};
            }}
            
            QRadioButton::indicator {{
                border-radius: 8px;
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {accent_color};
                border: 1px solid {accent_color};
                image: url({resource_path("assets/check.png").replace("\\", "/")}); 
            }}
            
            QRadioButton::indicator:checked {{
                background-color: {accent_color};
                border: 1px solid {accent_color};
            }}
            
            QPushButton {{
                background-color: {panel_bg};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                border: 1px solid {accent_color};
                color: {accent_color};
            }}
            
            QPushButton#calc_btn {{
                background-color: {accent_color};
                color: white;
                border: none;
                padding: 8px;
                font-size: 14px;
            }}
            
            QPushButton#calc_btn:hover {{
                background-color: #2980b9;
            }}
            
            QLineEdit, QSpinBox, QDoubleSpinBox {{
                background-color: {input_bg};
                color: {text_color};
                border: 1px solid {accent_color};
                border-radius: 3px;
                padding: 2px;
                min-height: 20px;
            }}
            
            QLineEdit:disabled, QDoubleSpinBox:disabled, QSpinBox:disabled {{
                background-color: {input_disabled_bg};
                color: {muted_text};
                border: 1px solid {border_color};
            }}

            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
                border: 1px solid {accent_color};
            }}
            
            /* Custom SpinBox Arrows using Images */
            QSpinBox::up-button, QDoubleSpinBox::up-button {{
                width: 16px;
                border: none;
                background-color: transparent; 
                image: {up_arrow};
            }}

            QSpinBox::down-button, QDoubleSpinBox::down-button {{
                width: 16px;
                border: none;
                background-color: transparent;
                image: {down_arrow};
            }}
            
            QScrollArea {{
                border: none;
                background-color: {bg_color};
            }}
            
            QWidget#scroll_content {{
                background-color: {bg_color};
            }}
            
            QComboBox {{
                background-color: {input_bg};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 3px;
                padding: 2px;
            }}
            
            QToolButton {{
                background-color: transparent;
                border: none;
                border-radius: 3px;
            }}
            
            QToolButton:hover {{
                background-color: {border_color};
            }}
        """
        self.setStyleSheet(style_sheet)
        
        # Propagate to active widget
        current_widget = self.stack.currentWidget()
        if hasattr(current_widget, 'update_theme'):
            current_widget.update_theme(theme)

    def openMaterialBrowser(self):
        """Open the Material Browser dialog."""
        dialog = MaterialBrowser(self)
        dialog.materialSelected.connect(self.applyMaterial)
        dialog.exec()
    
    def reloadDatabase(self):
        """Reload the material database from disk."""
        db = get_database()
        db.load()
        self.statusBar().showMessage(f"Database reloaded: {db.count_all()} materials")
    
    def applyMaterial(self, material, category):
        """Apply selected material to the currently active module.
        
        Parameters
        ----------
        material : dict
            Material data dictionary
        category : str
            Material category ('elastic', 'plastic', 'hyperelastic')
        """
        current_widget = self.stack.currentWidget()
        
        # Check if the widget can accept this material type
        if hasattr(current_widget, 'loadMaterialFromDatabase'):
            current_widget.loadMaterialFromDatabase(material)
            self.statusBar().showMessage(f"Applied material: {material.get('name', 'Unknown')}")
        else:
            QMessageBox.information(self, "Info", 
                f"The current module does not support loading {category} materials directly.\n"
                "Please switch to the appropriate module first.")
