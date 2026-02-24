# Result Display Widgets for Mat Model Lab GUI
# Shows calculated elastic properties and VRH averages

import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QGroupBox, QFrame, QTableWidget,
                             QTableWidgetItem, QHeaderView, QPushButton,
                             QTextEdit, QApplication)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


class VRHResultsWidget(QWidget):
    """
    Widget to display Voigt-Reuss-Hill averaged elastic properties.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(['Property', 'Voigt', 'Reuss', 'Hill'])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.results_table.setAlternatingRowColors(True)
        
        # Set rows
        properties = [
            "Young's Modulus (GPa)",
            "Shear Modulus (GPa)",
            "Bulk Modulus (GPa)",
            "Poisson's Ratio",
            "Hardness (GPa)"
        ]
        self.results_table.setRowCount(len(properties))
        for i, prop in enumerate(properties):
            self.results_table.setItem(i, 0, QTableWidgetItem(prop))
        
        layout.addWidget(self.results_table)
        
        # Min/Max display
        minmax_frame = QFrame()
        minmax_frame.setFrameShape(QFrame.StyledPanel)
        minmax_layout = QGridLayout(minmax_frame)
        
        minmax_layout.addWidget(QLabel("Min"), 0, 1)
        minmax_layout.addWidget(QLabel("Max"), 0, 2)
        minmax_layout.addWidget(QLabel("Anisotropy"), 0, 3)
        
        self.minmax_labels = {}
        props_short = ['E', 'G', 'B', 'v', 'H']
        for i, prop in enumerate(props_short):
            minmax_layout.addWidget(QLabel(prop), i+1, 0)
            self.minmax_labels[f'{prop}_min'] = QLabel("—")
            self.minmax_labels[f'{prop}_max'] = QLabel("—")
            self.minmax_labels[f'{prop}_anis'] = QLabel("—")
            minmax_layout.addWidget(self.minmax_labels[f'{prop}_min'], i+1, 1)
            minmax_layout.addWidget(self.minmax_labels[f'{prop}_max'], i+1, 2)
            minmax_layout.addWidget(self.minmax_labels[f'{prop}_anis'], i+1, 3)
        
        layout.addWidget(minmax_frame)
        
        # Copy button
        self.copy_btn = QPushButton("📋 Copy Results")
        self.copy_btn.clicked.connect(self._copy_results)
        layout.addWidget(self.copy_btn)
        
    def update_vrh_results(self, vrh_data: dict):
        """
        Update the VRH results display.
        
        Parameters
        ----------
        vrh_data : dict
            Dictionary with keys like 'E_voigt', 'E_reuss', 'E_hill', etc.
        """
        properties = ['E', 'G', 'B', 'v', 'H']
        
        for row, prop in enumerate(properties):
            for col, avg_type in enumerate(['voigt', 'reuss', 'hill']):
                key = f'{prop}_{avg_type}'
                if key in vrh_data:
                    value = vrh_data[key]
                    if prop == 'v':
                        text = f"{value:.4f}"
                    else:
                        text = f"{value:.2f}"
                    self.results_table.setItem(row, col+1, QTableWidgetItem(text))
                    
    def update_minmax(self, minmax_data: dict):
        """
        Update min/max display.
        
        Parameters
        ----------
        minmax_data : dict
            Dictionary with keys like 'E_min', 'E_max', etc.
        """
        for prop in ['E', 'G', 'B', 'v', 'H']:
            min_key = f'{prop}_min'
            max_key = f'{prop}_max'
            
            if min_key in minmax_data and max_key in minmax_data:
                min_val = minmax_data[min_key]
                max_val = minmax_data[max_key]
                
                if prop == 'v':
                    self.minmax_labels[min_key].setText(f"{min_val:.4f}")
                    self.minmax_labels[max_key].setText(f"{max_val:.4f}")
                else:
                    self.minmax_labels[min_key].setText(f"{min_val:.2f}")
                    self.minmax_labels[max_key].setText(f"{max_val:.2f}")
                
                # Calculate anisotropy ratio
                if min_val != 0:
                    anis = max_val / min_val
                    self.minmax_labels[f'{prop}_anis'].setText(f"{anis:.3f}")
                    
                    # Color code anisotropy
                    if anis > 2.0:
                        self.minmax_labels[f'{prop}_anis'].setStyleSheet("color: red;")
                    elif anis > 1.5:
                        self.minmax_labels[f'{prop}_anis'].setStyleSheet("color: orange;")
                    else:
                        self.minmax_labels[f'{prop}_anis'].setStyleSheet("color: green;")
                        
    def _copy_results(self):
        """Copy results to clipboard."""
        from PyQt5.QtWidgets import QApplication
        
        text_lines = ["VRH Elastic Properties\n"]
        text_lines.append("Property\tVoigt\tReuss\tHill")
        
        for row in range(self.results_table.rowCount()):
            row_data = []
            for col in range(self.results_table.columnCount()):
                item = self.results_table.item(row, col)
                row_data.append(item.text() if item else "")
            text_lines.append("\t".join(row_data))
        
        QApplication.clipboard().setText("\n".join(text_lines))


class ResultDisplay(QWidget):
    """
    Comprehensive result display widget showing all elastic property results.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Calculation Results")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # VRH Results
        vrh_group = QGroupBox("VRH Averaged Properties")
        vrh_layout = QVBoxLayout(vrh_group)
        self.vrh_widget = VRHResultsWidget()
        vrh_layout.addWidget(self.vrh_widget)
        layout.addWidget(vrh_group)
        
        # Direction-dependent results summary
        dir_group = QGroupBox("Direction-Dependent Summary")
        dir_layout = QVBoxLayout(dir_group)
        
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setMaximumHeight(100)
        self.summary_text.setPlaceholderText("Calculate properties to see summary...")
        dir_layout.addWidget(self.summary_text)
        
        layout.addWidget(dir_group)
        
    def update_results(self, vrh_data: dict, minmax_data: dict = None):
        """Update all result displays."""
        self.vrh_widget.update_vrh_results(vrh_data)
        if minmax_data:
            self.vrh_widget.update_minmax(minmax_data)
            self._update_summary(minmax_data)
            
    def _update_summary(self, minmax_data: dict):
        """Generate text summary of results."""
        lines = []
        
        if 'E_min' in minmax_data and 'E_max' in minmax_data:
            e_min, e_max = minmax_data['E_min'], minmax_data['E_max']
            anis = e_max / e_min if e_min != 0 else 0
            lines.append(f"Young's Modulus: {e_min:.1f} - {e_max:.1f} GPa (anisotropy: {anis:.2f})")
            
        if 'G_min' in minmax_data and 'G_max' in minmax_data:
            g_min, g_max = minmax_data['G_min'], minmax_data['G_max']
            lines.append(f"Shear Modulus: {g_min:.1f} - {g_max:.1f} GPa")
            
        if 'v_min' in minmax_data and 'v_max' in minmax_data:
            v_min, v_max = minmax_data['v_min'], minmax_data['v_max']
            lines.append(f"Poisson's Ratio: {v_min:.3f} - {v_max:.3f}")
            
        self.summary_text.setText("\n".join(lines))
        
    def clear(self):
        """Clear all results."""
        # Clear table
        for row in range(self.vrh_widget.results_table.rowCount()):
            for col in range(1, 4):
                self.vrh_widget.results_table.setItem(row, col, QTableWidgetItem("—"))
        
        # Clear minmax labels
        for label in self.vrh_widget.minmax_labels.values():
            label.setText("—")
            label.setStyleSheet("")
        
        # Clear summary
        self.summary_text.clear()
