"""
Material Browser Dialog

A QDialog for browsing, searching, and selecting materials from the database.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget, 
    QTableWidgetItem, QPushButton, QLabel, QComboBox, QGroupBox,
    QHeaderView, QAbstractItemView, QMessageBox, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

import numpy as np

# Import database
from mml_utils.material_db import get_database


class MaterialBrowser(QDialog):
    """Dialog for browsing and selecting materials from the database."""
    
    # Signal emitted when a material is selected and applied
    # Emits: (material_dict, category)
    materialSelected = pyqtSignal(dict, str)
    
    def __init__(self, parent=None, filter_category=None):
        """Initialize the Material Browser dialog.
        
        Parameters
        ----------
        parent : QWidget, optional
            Parent widget
        filter_category : str, optional
            If provided, only show materials from this category ('elastic', 'plastic', 'hyperelastic')
        """
        super().__init__(parent)
        self.filter_category = filter_category
        self.db = get_database()
        self.current_selection = None
        
        self.setWindowTitle("Material Database Browser")
        self.setMinimumSize(800, 600)
        self.init_ui()
        self.refresh_table()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # --- Search and Filter Row ---
        filter_layout = QHBoxLayout()
        
        # Category filter
        filter_layout.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(["All", "Elastic", "Plastic", "Hyperelastic"])
        if self.filter_category:
            index = self.category_combo.findText(self.filter_category.capitalize())
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
        self.category_combo.currentIndexChanged.connect(self.refresh_table)
        filter_layout.addWidget(self.category_combo)
        
        filter_layout.addSpacing(20)
        
        # Search bar
        filter_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to search by name...")
        self.search_input.textChanged.connect(self.refresh_table)
        filter_layout.addWidget(self.search_input, stretch=1)
        
        layout.addLayout(filter_layout)
        
        # --- Material Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Dimension", "Source"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.table.doubleClicked.connect(self.apply_selection)
        layout.addWidget(self.table)
        
        # --- Preview Pane ---
        preview_group = QGroupBox("Material Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_label = QLabel("Select a material to preview its properties.")
        self.preview_label.setWordWrap(True)
        preview_layout.addWidget(self.preview_label)
        
        self.cij_preview = QTextEdit()
        self.cij_preview.setReadOnly(True)
        self.cij_preview.setMaximumHeight(150)
        self.cij_preview.setFont(QFont("Consolas", 9))
        preview_layout.addWidget(self.cij_preview)
        
        layout.addWidget(preview_group)
        
        # --- Button Row ---
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.setEnabled(False)
        self.apply_btn.clicked.connect(self.apply_selection)
        button_layout.addWidget(self.apply_btn)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
    
    def refresh_table(self):
        """Refresh the table based on current filter and search."""
        # Get category filter
        category_text = self.category_combo.currentText().lower()
        category = None if category_text == "all" else category_text
        
        # Get search query
        query = self.search_input.text().strip()
        
        # Query database
        if query:
            materials = self.db.search(query, category)
        elif category:
            materials = [{'category': category, **m} for m in self.db.get_by_category(category)]
        else:
            materials = self.db.get_all()
        
        # Populate table
        self.table.setRowCount(len(materials))
        for row, mat in enumerate(materials):
            self.table.setItem(row, 0, QTableWidgetItem(mat.get('name', 'Unknown')))
            self.table.setItem(row, 1, QTableWidgetItem(mat.get('crystal_type', '-')))
            self.table.setItem(row, 2, QTableWidgetItem(mat.get('dimension', '3D')))
            self.table.setItem(row, 3, QTableWidgetItem(mat.get('source', '-')))
            
            # Store full material data in first column's item
            self.table.item(row, 0).setData(Qt.ItemDataRole.UserRole, mat)
        
        # Clear selection
        self.current_selection = None
        self.apply_btn.setEnabled(False)
        self.preview_label.setText("Select a material to preview its properties.")
        self.cij_preview.clear()
    
    def on_selection_changed(self):
        """Handle table selection change."""
        selected = self.table.selectedItems()
        if selected:
            row = selected[0].row()
            mat = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            self.current_selection = mat
            self.apply_btn.setEnabled(True)
            self.update_preview(mat)
        else:
            self.current_selection = None
            self.apply_btn.setEnabled(False)
            self.preview_label.setText("Select a material to preview its properties.")
            self.cij_preview.clear()
    
    def update_preview(self, mat):
        """Update the preview pane with material details."""
        name = mat.get('name', 'Unknown')
        crystal_type = mat.get('crystal_type', '-')
        description = mat.get('description', 'No description available.')
        
        self.preview_label.setText(f"<b>{name}</b> ({crystal_type})<br>{description}")
        
        # Format Cij matrix
        cij = mat.get('cij', [])
        if cij:
            cij_array = np.array(cij)
            lines = []
            for row in cij_array:
                row_str = "  ".join(f"{val:8.2f}" for val in row)
                lines.append(row_str)
            self.cij_preview.setText("Cij Matrix (GPa):\n" + "\n".join(lines))
        else:
            self.cij_preview.setText("No Cij data available.")
    
    def apply_selection(self):
        """Apply the selected material and close the dialog."""
        if self.current_selection:
            category = self.current_selection.get('category', 'elastic')
            self.materialSelected.emit(self.current_selection, category)
            self.accept()
