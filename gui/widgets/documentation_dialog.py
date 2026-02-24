"""
Tabbed Documentation Dialog for Mat Model Lab
Modern dialog with left navigation sidebar and scrollable content panes
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QFrame, QListWidget, QListWidgetItem,
                              QStackedWidget, QTextBrowser, QSplitter, QWidget)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
import os
import sys

from mml_utils.paths import resource_path


class DocumentationDialog(QDialog):
    """Modern Tabbed Documentation Dialog for Mat Model Lab"""
    
    def __init__(self, parent=None, is_dark=True):
        super().__init__(parent)
        self.is_dark = is_dark
        self.font_size = 14  # Base font size for zoom
        self.setWindowTitle("Mat Model Lab Documentation")
        self.resize(1000, 700)
        self.setMinimumSize(800, 500)
        # Enable maximize button
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | 
                           Qt.WindowType.WindowMaximizeButtonHint | Qt.WindowType.WindowMinimizeButtonHint)
        
        self.init_ui()
        self.apply_style()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left Navigation Panel
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(10, 15, 10, 15)
        nav_layout.setSpacing(5)
        
        # Navigation header
        nav_header = QLabel("Documentation")
        nav_header.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        nav_header.setObjectName("nav_header")
        nav_layout.addWidget(nav_header)
        nav_layout.addSpacing(10)
        
        # Navigation list
        self.nav_list = QListWidget()
        self.nav_list.setObjectName("nav_list")
        self.nav_list.setIconSize(QSize(20, 20))
        
        sections = [
            "Overview",
            "Elasticity Module",
            "Plasticity Module",
            "Hyperelasticity Module",
            "Material Database",
            "Crystal Systems",
            "Citation",
        ]
        
        for name in sections:
            item = QListWidgetItem(name)
            item.setSizeHint(QSize(200, 32))
            self.nav_list.addItem(item)
        
        self.nav_list.currentRowChanged.connect(self.on_section_changed)
        nav_layout.addWidget(self.nav_list)
        
        nav_widget.setFixedWidth(220)
        nav_widget.setObjectName("nav_panel")
        splitter.addWidget(nav_widget)
        
        # Content Stack
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_stack")
        
        # Add content pages
        self.add_content_pages()
        
        splitter.addWidget(self.content_stack)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
        
        # Button bar
        btn_bar = QWidget()
        btn_bar.setObjectName("btn_bar")
        btn_bar.setFixedHeight(50)
        btn_layout = QHBoxLayout(btn_bar)
        btn_layout.setContentsMargins(15, 8, 15, 8)
        
        # Font size controls - use text labels
        zoom_out_btn = QPushButton(" Aa- ")
        zoom_out_btn.setObjectName("zoom_btn")
        zoom_out_btn.setToolTip("Decrease font size")
        zoom_out_btn.clicked.connect(self.zoom_out)
        btn_layout.addWidget(zoom_out_btn)
        
        zoom_in_btn = QPushButton(" Aa+ ")
        zoom_in_btn.setObjectName("zoom_btn")
        zoom_in_btn.setToolTip("Increase font size")
        zoom_in_btn.clicked.connect(self.zoom_in)
        btn_layout.addWidget(zoom_in_btn)
        
        btn_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.setObjectName("close_btn")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addWidget(btn_bar)
        
        # Select first item
        self.nav_list.setCurrentRow(0)
        
    def add_content_pages(self):
        """Add all content pages to the stack"""
        pages = [
            self.get_overview_content(),
            self.get_elasticity_content(),
            self.get_plasticity_content(),
            self.get_hyperelasticity_content(),
            self.get_database_content(),
            self.get_crystal_content(),
            self.get_citation_content(),
        ]
        
        self.browsers = []
        for html_content in pages:
            browser = QTextBrowser()
            browser.setOpenExternalLinks(True)
            browser.setHtml(self.wrap_html(html_content))
            self.browsers.append(browser)
            self.content_stack.addWidget(browser)
    
    def on_section_changed(self, index):
        self.content_stack.setCurrentIndex(index)
    
    def zoom_in(self):
        """Increase font size"""
        if self.font_size < 24:
            self.font_size += 2
            self.refresh_content()
    
    def zoom_out(self):
        """Decrease font size"""
        if self.font_size > 10:
            self.font_size -= 2
            self.refresh_content()
    
    def refresh_content(self):
        """Refresh all content with new font size"""
        pages = [
            self.get_overview_content(),
            self.get_elasticity_content(),
            self.get_plasticity_content(),
            self.get_hyperelasticity_content(),
            self.get_database_content(),
            self.get_crystal_content(),
            self.get_citation_content(),
        ]
        for i, browser in enumerate(self.browsers):
            browser.setHtml(self.wrap_html(pages[i]))
    def wrap_html(self, content):
        """Wrap content with styled HTML"""
        if self.is_dark:
            bg_color = "#1e1e1e"
            text_color = "#e0e0e0"
            header_color = "#64b5f6"
            subheader_color = "#81c784"
            code_bg = "#3c3c3c"
            pre_bg = "#2d2d2d"
            pre_text = "#a5d6a7"
            border_color = "#444"
            note_bg = "#37474f"
            note_border = "#4fc3f7"
        else:
            bg_color = "#ffffff"
            text_color = "#333333"
            header_color = "#2c3e50"
            subheader_color = "#34495e"
            code_bg = "#f8f9fa"
            pre_bg = "#f0f0f0"
            pre_text = "#2c3e50"
            border_color = "#ddd"
            note_bg = "#e8f4f8"
            note_border = "#3498db"
            
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ 
                    font-family: 'Segoe UI', sans-serif; 
                    font-size: {self.font_size}px;
                    line-height: 1.6; 
                    color: {text_color}; 
                    background-color: {bg_color}; 
                    padding: 15px 25px;
                    margin: 0;
                }}
                h1 {{ color: {header_color}; font-size: 24px; margin-bottom: 15px; }}
                h2 {{ color: {subheader_color}; font-size: 18px; margin-top: 25px; border-bottom: 1px solid {border_color}; padding-bottom: 5px; }}
                h3 {{ color: {header_color}; font-size: 14px; margin-top: 20px; }}
                ul {{ margin: 10px 0; padding-left: 25px; }}
                li {{ margin-bottom: 8px; }}
                code {{ background-color: {code_bg}; padding: 2px 6px; border-radius: 3px; font-family: 'Consolas', monospace; }}
                pre {{ background-color: {pre_bg}; color: {pre_text}; padding: 15px; border-radius: 5px; overflow-x: auto; font-family: 'Consolas', monospace; font-size: 13px; border: 1px solid {border_color}; }}
                .note {{ background-color: {note_bg}; padding: 12px 15px; border-radius: 5px; border-left: 4px solid {note_border}; margin: 15px 0; }}
                .badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; }}
                .badge-active {{ background-color: #4CAF50; color: white; }}
                .badge-upcoming {{ background-color: transparent; color: #FF9800; border: 1px solid #FF9800; }}
                blockquote {{ border-left: 4px solid {border_color}; margin: 15px 0; padding-left: 15px; font-style: italic; color: {text_color}; opacity: 0.8; }}
            </style>
        </head>
        <body>
            {content}
        </body>
        </html>
        """
    
    def get_overview_content(self):
        return """
        <h1>Mat Model Lab</h1>
        <p>A comprehensive tool for material constitutive model analysis, visualization, and finite element code generation.</p>
        
        <h2>Modules</h2>
        <p>
            <span class="badge badge-active">Elasticity</span>
            <span class="badge badge-upcoming">Plasticity</span>
            <span class="badge badge-upcoming">Hyperelasticity</span>
        </p>
        
        <h2>Key Features</h2>
        <ul>
            <li><b>Elastic Properties:</b> Young's modulus, shear modulus, Poisson's ratio, bulk modulus, hardness</li>
            <li><b>Visualization:</b> 2D/3D directional property distribution</li>
            <li><b>Material Database:</b> Built-in library of common materials</li>
            <li><b>Export:</b> ABAQUS, COMSOL material cards</li>
            <li><b>Reports:</b> HTML, PDF, Word report generation</li>
        </ul>
        
        <h2>Quick Start</h2>
        <ol>
            <li>Select a crystal type or load material from database</li>
            <li>Input or load elastic constants (Cij matrix)</li>
            <li>Select properties to calculate</li>
            <li>Click <b>Calculate</b> to visualize</li>
            <li>Export model or generate report</li>
        </ol>
        """
    
    def get_elasticity_content(self):
        return """
        <h1>Elasticity Module</h1>
        <p>Post-processing and visualization of anisotropic elastic properties.</p>
        
        <h2>Core Calculations</h2>
        <ul>
            <li><b>Elastic Moduli:</b> Young's, Shear, Bulk modulus</li>
            <li><b>Poisson's Ratio:</b> Direction-dependent analysis</li>
            <li><b>Hardness:</b> Chen-Niu model (2011)</li>
            <li><b>VRH Average:</b> Voigt-Reuss-Hill polycrystalline averaging</li>
            <li><b>Stability Check:</b> Born mechanical stability criteria</li>
        </ul>
        
        <h2>Theory</h2>
        <h3>Elastic Moduli</h3>
        <p>Calculated from the compliance matrix <b>S</b> = <b>C</b><sup>-1</sup>:</p>
        <ul>
            <li>Young's Modulus: E = 1 / S'<sub>11</sub></li>
            <li>Shear Modulus: G = 1 / (4S'<sub>66</sub>)</li>
            <li>Poisson's Ratio: ν = -S'<sub>12</sub> / S'<sub>11</sub></li>
        </ul>
        
        <h3>VRH Averaging</h3>
        <ul>
            <li><b>Voigt:</b> Upper bound (uniform strain assumption)</li>
            <li><b>Reuss:</b> Lower bound (uniform stress assumption)</li>
            <li><b>Hill:</b> X<sub>Hill</sub> = (X<sub>Voigt</sub> + X<sub>Reuss</sub>) / 2</li>
        </ul>
        
        <h2>Usage</h2>
        <ol>
            <li>Select <b>Data Mode</b>: Manual Input, From File, or From Database</li>
            <li>Choose crystal type (affects Cij matrix constraints)</li>
            <li>Input non-zero Cij values</li>
            <li>Select properties and visualization type</li>
            <li>Click <b>Calculate</b></li>
        </ol>
        """
    
    def get_plasticity_content(self):
        return """
        <h1>Plasticity Module</h1>
        <p><span class="badge badge-upcoming">Coming Soon</span></p>
        
        <h2>Planned Features</h2>
        <ul>
            <li><b>Yield Criteria:</b> von Mises (J2), Tresca, Hill, Drucker-Prager</li>
            <li><b>Hardening Rules:</b> Isotropic, Kinematic, Combined</li>
            <li><b>Flow Rules:</b> Associated, Non-associated</li>
            <li><b>Parameter Fitting:</b> From experimental stress-strain data</li>
        </ul>
        
        <h2>Export Formats</h2>
        <ul>
            <li>ABAQUS *PLASTIC keyword</li>
            <li>COMSOL material expressions</li>
        </ul>
        
        <div class="note">
            This module is under development. Stay tuned for updates!
        </div>
        """
    
    def get_hyperelasticity_content(self):
        return """
        <h1>Hyperelasticity Module</h1>
        <p><span class="badge badge-upcoming">Coming Soon</span></p>
        
        <h2>Planned Features</h2>
        <ul>
            <li><b>Constitutive Models:</b>
                <ul>
                    <li>Neo-Hookean</li>
                    <li>Mooney-Rivlin</li>
                    <li>Ogden</li>
                    <li>Yeoh</li>
                    <li>Arruda-Boyce</li>
                </ul>
            </li>
            <li><b>Parameter Calibration:</b> Fit from uniaxial/biaxial test data</li>
            <li><b>UMAT/VUMAT Generation:</b> Auto-generate Fortran subroutines</li>
        </ul>
        
        <h2>Code Generation</h2>
        <ul>
            <li>ABAQUS UMAT/VUMAT (Fortran)</li>
            <li>COMSOL expressions</li>
            <li>Python implementation</li>
        </ul>
        
        <div class="note">
            This module is under development. UMAT generation will be a key feature!
        </div>
        """
    
    def get_database_content(self):
        return """
        <h1>Material Database</h1>
        <p>Built-in library of common material parameters for quick access.</p>
        
        <h2>Features</h2>
        <ul>
            <li><b>Browse Materials:</b> Search and filter by category</li>
            <li><b>Quick Load:</b> One-click load into active module</li>
            <li><b>Custom Materials:</b> Add your own materials (coming soon)</li>
        </ul>
        
        <h2>Access</h2>
        <ul>
            <li>Menu: <b>Database → Browse Materials...</b> (Ctrl+B)</li>
            <li>Data Mode: Select <b>From Database</b> in Elasticity module</li>
        </ul>
        
        <h2>Included Materials</h2>
        <h3>Elastic Materials</h3>
        <ul>
            <li>Steel (304 Stainless) - Cubic</li>
            <li>Aluminum 6061 - Cubic</li>
            <li>Copper (Pure) - Cubic</li>
            <li>Silicon - Cubic</li>
            <li>Quartz (Alpha) - Hexagonal</li>
            <li>Graphene - 2D Hexagonal</li>
            <li>MoS2 (Monolayer) - 2D Hexagonal</li>
        </ul>
        
        <div class="note">
            Material data is stored in <code>assets/database/materials.json</code>. 
            You can edit this file to add custom materials.
        </div>
        """
    
    def get_crystal_content(self):
        return """
        <h1>Crystal Systems</h1>
        <p>Mat Model Lab supports 10 crystal symmetry types with their specific Cij matrix forms.</p>
        
        <h2>Supported Crystal Types</h2>
        
        <h3>1. Triclinic</h3>
        <p>21 independent constants (full 6×6 symmetric matrix)</p>
        
        <h3>2-3. Monoclinic</h3>
        <p>13 independent constants. Two variants based on diad axis orientation.</p>
        
        <h3>4. Orthorhombic</h3>
        <p>9 independent constants: C11, C12, C13, C22, C23, C33, C44, C55, C66</p>
        
        <h3>5-6. Tetragonal</h3>
        <p>6-7 constants. Constraints: C22=C11, C23=C13, C55=C44</p>
        
        <h3>7-8. Trigonal</h3>
        <p>6-7 constants. Additional constraint: C66=(C11-C12)/2</p>
        
        <h3>9. Hexagonal</h3>
        <p>5 constants. Transverse isotropy: C66=(C11-C12)/2</p>
        <pre>
C11  C12  C13   .    .    .
C12  C11  C13   .    .    .
C13  C13  C33   .    .    .
 .    .    .   C44   .    .
 .    .    .    .   C44   .
 .    .    .    .    .   (C11-C12)/2
        </pre>
        
        <h3>10. Cubic</h3>
        <p>3 constants: C11, C12, C44</p>
        <pre>
C11  C12  C12   .    .    .
C12  C11  C12   .    .    .
C12  C12  C11   .    .    .
 .    .    .   C44   .    .
 .    .    .    .   C44   .
 .    .    .    .    .   C44
        </pre>
        """
    
    def get_citation_content(self):
        return """
        <h1>Citation</h1>
        
        <h2>Elasticity Module</h2>
        <p>If you use the Elasticity module in your research, please cite:</p>
        <blockquote>
            Mingqing Liao, Yong Liu, Nan Qu et al. ElasticPOST: A Matlab Toolbox for 
            Post-processing of Elastic Anisotropy with Graphic User Interface. 
            <i>Computer Physics Communications</i> (2019)
        </blockquote>
        
        <div class="note">
            The Elasticity module of Mat Model Lab is based on the original ElasticPOST MATLAB toolkit.
        </div>
        
        <h2>License</h2>
        <p>Mat Model Lab is released under the <b>GPL-3.0</b> license.</p>
        
        <h2>Contact</h2>
        <p>GitHub: <a href="https://github.com/seekzzh/mat-model-lab">github.com/seekzzh/mat-model-lab</a></p>
        """
    
    def apply_style(self):
        if self.is_dark:
            self.setStyleSheet("""
                QDialog { background-color: #1e1e1e; }
                #nav_panel { background-color: #252526; border-right: 1px solid #3d3d3d; }
                #nav_header { color: #ffffff; padding-left: 5px; }
                #nav_list {
                    background-color: transparent;
                    border: none;
                    color: #cccccc;
                    font-size: 10pt;
                    outline: none;
                }
                #nav_list::item {
                    padding: 6px 12px;
                    border-radius: 4px;
                    margin: 1px 0;
                }
                #nav_list::item:selected {
                    background-color: #094771;
                    color: #ffffff;
                }
                #nav_list::item:hover:!selected {
                    background-color: #2a2d2e;
                }
                #content_stack { background-color: #1e1e1e; }
                QTextBrowser { 
                    border: none; 
                    background-color: #1e1e1e;
                }
                QTextBrowser QScrollBar:vertical {
                    background-color: #1e1e1e;
                    width: 10px;
                    margin: 0;
                }
                QTextBrowser QScrollBar::handle:vertical {
                    background-color: #5a5a5a;
                    border-radius: 5px;
                    min-height: 30px;
                }
                QTextBrowser QScrollBar::handle:vertical:hover {
                    background-color: #787878;
                }
                QTextBrowser QScrollBar::add-line:vertical,
                QTextBrowser QScrollBar::sub-line:vertical {
                    height: 0;
                }
                #btn_bar { background-color: #252526; border-top: 1px solid #3d3d3d; }
                #close_btn {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 24px;
                    font-size: 10pt;
                }
                #close_btn:hover { background-color: #1084d8; }
                #zoom_btn {
                    background-color: #3c3c3c;
                    color: #ffffff;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    font-size: 11pt;
                    font-weight: bold;
                }
                #zoom_btn:hover { background-color: #505050; }
            """)
        else:
            self.setStyleSheet("""
                QDialog { background-color: #ffffff; }
                #nav_panel { background-color: #f8f8f8; border-right: 1px solid #e0e0e0; }
                #nav_header { color: #333333; padding-left: 5px; }
                #nav_list {
                    background-color: transparent;
                    border: none;
                    color: #333333;
                    font-size: 10pt;
                    outline: none;
                }
                #nav_list::item {
                    padding: 6px 12px;
                    border-radius: 4px;
                    margin: 1px 0;
                }
                #nav_list::item:selected {
                    background-color: #0078d4;
                    color: #ffffff;
                }
                #nav_list::item:hover:!selected {
                    background-color: #eeeeee;
                }
                #content_stack { background-color: #ffffff; }
                QTextBrowser { 
                    border: none;
                    background-color: #ffffff;
                }
                QTextBrowser QScrollBar:vertical {
                    background-color: #f0f0f0;
                    width: 10px;
                    margin: 0;
                }
                QTextBrowser QScrollBar::handle:vertical {
                    background-color: #c0c0c0;
                    border-radius: 5px;
                    min-height: 30px;
                }
                QTextBrowser QScrollBar::handle:vertical:hover {
                    background-color: #a0a0a0;
                }
                QTextBrowser QScrollBar::add-line:vertical,
                QTextBrowser QScrollBar::sub-line:vertical {
                    height: 0;
                }
                #btn_bar { background-color: #f8f8f8; border-top: 1px solid #e0e0e0; }
                #close_btn {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 24px;
                    font-size: 10pt;
                }
                #close_btn:hover { background-color: #1084d8; }
                #zoom_btn {
                    background-color: #e8e8e8;
                    color: #333333;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    font-size: 11pt;
                    font-weight: bold;
                }
                #zoom_btn:hover { background-color: #d0d0d0; }
            """)
