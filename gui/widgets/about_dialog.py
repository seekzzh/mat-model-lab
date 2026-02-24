"""
Custom About Dialog for Mat Model Lab
Modern, styled dialog with logo, animations, and theme support
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QFrame, QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QUrl
from PyQt6.QtGui import QPixmap, QFont, QDesktopServices
import os
import sys

from mml_utils.paths import resource_path


class AboutDialog(QDialog):
    """Modern About Dialog for Mat Model Lab"""
    
    def __init__(self, parent=None, is_dark=True):
        super().__init__(parent)
        self.is_dark = is_dark
        self.setWindowTitle("About Mat Model Lab")
        self.setFixedSize(480, 360)  # Adjusted height for logo
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        
        self.init_ui()
        self.apply_style()
        self.animate_in()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 25, 30, 25)
        
        # Header with logo and title
        header = QHBoxLayout()
        header.setSpacing(20)
        
        # Logo
        logo_label = QLabel()
        icon_path = resource_path('assets/icon.png')
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path).scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, 
                                                Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("🔬")
            logo_label.setFont(QFont("Segoe UI Emoji", 48))
        header.addWidget(logo_label)
        
        # Title and tagline
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)
        
        title = QLabel("Mat Model Lab")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setObjectName("title")
        title_layout.addWidget(title)
        
        tagline = QLabel("Material Constitutive Model Laboratory")
        tagline.setFont(QFont("Segoe UI", 10))
        tagline.setObjectName("tagline")
        title_layout.addWidget(tagline)
        
        header.addLayout(title_layout)
        header.addStretch()
        layout.addLayout(header)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("separator")
        layout.addWidget(separator)
        
        # Description
        desc = QLabel(
            "A comprehensive tool for material constitutive model analysis, "
            "visualization, and finite element code generation."
        )
        desc.setWordWrap(True)
        desc.setFont(QFont("Segoe UI", 10))
        desc.setObjectName("description")
        layout.addWidget(desc)
        
        # Modules badges
        modules_layout = QHBoxLayout()
        modules_layout.setSpacing(6)  # Compact spacing
        
        modules = [
            ("Elasticity", "#4CAF50", True),
            ("Plasticity", "#FF9800", False),
            ("Hyperelasticity", "#2196F3", False)
        ]
        
        for name, color, active in modules:
            badge = QLabel(name)
            badge.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge.setFixedHeight(26)
            badge.setMinimumWidth(90)
            if active:
                badge.setStyleSheet(f"""
                    background-color: {color};
                    color: white;
                    border-radius: 14px;
                    padding: 4px 12px;
                """)
            else:
                badge.setStyleSheet(f"""
                    background-color: transparent;
                    color: {color};
                    border: 2px solid {color};
                    border-radius: 14px;
                    padding: 4px 12px;
                """)
            modules_layout.addWidget(badge)
        
        modules_layout.addStretch()
        layout.addLayout(modules_layout)
        
        layout.addSpacing(10)  # Small spacing instead of stretch
        
        # Version, author, and license
        version_layout = QVBoxLayout()
        version_layout.setSpacing(2)
        
        version = QLabel("Version 1.0.0")
        version.setFont(QFont("Segoe UI", 9))
        version.setObjectName("version")
        version_layout.addWidget(version)
        
        author_label = QLabel("Author: Zhaohang Zhang")
        author_label.setFont(QFont("Segoe UI", 9))
        author_label.setObjectName("copyright")
        version_layout.addWidget(author_label)
        
        copyright_label = QLabel("© 2026 Mat Model Lab  ·  GPL-3.0 License")
        copyright_label.setFont(QFont("Segoe UI", 9))
        copyright_label.setObjectName("copyright")
        version_layout.addWidget(copyright_label)
        
        layout.addLayout(version_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        github_btn = QPushButton("GitHub")
        github_btn.setObjectName("link_btn")
        github_btn.clicked.connect(lambda: QDesktopServices.openUrl(
            QUrl("https://github.com/seekzzh/mat-model-lab")))
        button_layout.addWidget(github_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.setObjectName("close_btn")
        close_btn.setDefault(True)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
    def apply_style(self):
        if self.is_dark:
            self.setStyleSheet("""
                QDialog {
                    background-color: #1e1e1e;
                }
                #title {
                    color: #ffffff;
                }
                #tagline {
                    color: #888888;
                }
                #separator {
                    background-color: #3d3d3d;
                    border: none;
                    height: 1px;
                }
                #description {
                    color: #cccccc;
                }
                #version, #copyright {
                    color: #666666;
                }
                #link_btn {
                    background-color: transparent;
                    color: #4a9eff;
                    border: 1px solid #4a9eff;
                    border-radius: 4px;
                    padding: 6px 16px;
                    font-size: 10pt;
                }
                #link_btn:hover {
                    background-color: #4a9eff;
                    color: white;
                }
                #close_btn {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 6px 20px;
                    font-size: 10pt;
                }
                #close_btn:hover {
                    background-color: #1084d8;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background-color: #ffffff;
                }
                #title {
                    color: #1a1a1a;
                }
                #tagline {
                    color: #666666;
                }
                #separator {
                    background-color: #e0e0e0;
                    border: none;
                    height: 1px;
                }
                #description {
                    color: #333333;
                }
                #version, #copyright {
                    color: #999999;
                }
                #link_btn {
                    background-color: transparent;
                    color: #0066cc;
                    border: 1px solid #0066cc;
                    border-radius: 4px;
                    padding: 6px 16px;
                    font-size: 10pt;
                }
                #link_btn:hover {
                    background-color: #0066cc;
                    color: white;
                }
                #close_btn {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 6px 20px;
                    font-size: 10pt;
                }
                #close_btn:hover {
                    background-color: #1084d8;
                }
            """)
    
    def animate_in(self):
        """Fade-in animation on open"""
        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)
        
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
