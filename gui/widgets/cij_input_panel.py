# Cij Input Panel Widget for Mat Model Lab GUI
# Provides elastic constant input with crystal type awareness

import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QDoubleSpinBox, QGroupBox, QComboBox,
                             QPushButton, QFrame, QMessageBox, QInputDialog)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

# Import crystal type utilities
try:
    from ...core.crystal_type import (CRYSTAL_TYPES_3D, CRYSTAL_TYPES_2D,
                                       get_independent_constants, get_enabled_indices,
                                       fill_symmetric_matrix)
    from ...core.stability import StableofMechanical, check_stability_detailed
except ImportError:
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from core.crystal_type import (CRYSTAL_TYPES_3D, CRYSTAL_TYPES_2D,
                                   get_independent_constants, get_enabled_indices,
                                   fill_symmetric_matrix)
    from core.stability import StableofMechanical, check_stability_detailed


class CijInputPanel(QWidget):
    """
    Panel for inputting elastic constants with crystal type awareness.
    
    Signals
    -------
    cij_changed : numpy.ndarray
        Emitted when elastic constants are modified
    stability_changed : bool
        Emitted when stability status changes
    """
    
    cij_changed = pyqtSignal(np.ndarray)
    stability_changed = pyqtSignal(bool)
    
    def __init__(self, parent=None, is_3d=True):
        super().__init__(parent)
        self.is_3d = is_3d
        self.cij = np.zeros((6, 6))
        self.cij_inputs = {}
        self.cij_labels = {}
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Material type selection
        type_layout = QHBoxLayout()
        type_label = QLabel("Material Type:")
        self.material_type_combo = QComboBox()
        self.material_type_combo.addItems(["3D Material", "2D Material"])
        self.material_type_combo.currentIndexChanged.connect(self._on_material_type_changed)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.material_type_combo)
        type_layout.addStretch()
        layout.addLayout(type_layout)
        
        # Crystal type selection
        crystal_layout = QHBoxLayout()
        crystal_label = QLabel("Crystal Type:")
        self.crystal_type_combo = QComboBox()
        self._update_crystal_types()
        self.crystal_type_combo.currentIndexChanged.connect(self._on_crystal_type_changed)
        crystal_layout.addWidget(crystal_label)
        crystal_layout.addWidget(self.crystal_type_combo)
        crystal_layout.addStretch()
        layout.addLayout(crystal_layout)
        
        # Stability indicator
        self.stability_frame = QFrame()
        self.stability_frame.setFrameShape(QFrame.StyledPanel)
        stability_layout = QHBoxLayout(self.stability_frame)
        stability_layout.setContentsMargins(5, 2, 5, 2)
        self.stability_icon = QLabel("●")
        self.stability_icon.setFont(QFont("Arial", 12))
        self.stability_label = QLabel("Stability: Unknown")
        stability_layout.addWidget(self.stability_icon)
        stability_layout.addWidget(self.stability_label)
        stability_layout.addStretch()
        layout.addWidget(self.stability_frame)
        
        # Cij matrix input group
        self.cij_group = QGroupBox("Elastic Stiffness Constants (Cij) (GPa)")
        self.cij_layout = QGridLayout(self.cij_group)
        self.cij_layout.setSpacing(5)
        
        # Create 6x6 input grid (upper triangular)
        self._create_cij_inputs()
        
        layout.addWidget(self.cij_group)
        
        # Load/Apply buttons
        button_layout = QHBoxLayout()
        self.load_preset_btn = QPushButton("Load Preset")
        self.load_preset_btn.clicked.connect(self._load_preset)
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self._clear_all)
        self.apply_btn = QPushButton("Apply Symmetry")
        self.apply_btn.clicked.connect(self._apply_symmetry)
        button_layout.addWidget(self.load_preset_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.apply_btn)
        layout.addLayout(button_layout)
        
        # Initial crystal type update
        self._on_crystal_type_changed(0)
        
    def _create_cij_inputs(self):
        """Create the 6x6 matrix input fields."""
        # Clear existing
        while self.cij_layout.count():
            item = self.cij_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.cij_inputs.clear()
        self.cij_labels.clear()
        
        # Create header row
        for j in range(6):
            header = QLabel(f"{j+1}")
            header.setAlignment(Qt.AlignCenter)
            header.setFont(QFont("Arial", 9, QFont.Bold))
            self.cij_layout.addWidget(header, 0, j+1)
        
        # Create input fields
        for i in range(6):
            # Row header
            row_header = QLabel(f"C{i+1}x")
            row_header.setFont(QFont("Arial", 9, QFont.Bold))
            self.cij_layout.addWidget(row_header, i+1, 0)
            
            for j in range(6):
                if j >= i:  # Upper triangular only (symmetric matrix)
                    spin = QDoubleSpinBox()
                    spin.setRange(-9999, 9999)
                    spin.setDecimals(2)
                    spin.setSingleStep(1.0)
                    spin.setMinimumWidth(60)
                    spin.setMaximumWidth(80)
                    spin.valueChanged.connect(self._on_value_changed)
                    self.cij_inputs[(i, j)] = spin
                    self.cij_layout.addWidget(spin, i+1, j+1)
                else:
                    # Lower triangle: show symmetric value as label
                    lbl = QLabel("—")
                    lbl.setAlignment(Qt.AlignCenter)
                    lbl.setStyleSheet("color: gray;")
                    self.cij_labels[(i, j)] = lbl
                    self.cij_layout.addWidget(lbl, i+1, j+1)
    
    def _update_crystal_types(self):
        """Update crystal type combo box based on material dimension."""
        self.crystal_type_combo.blockSignals(True)
        self.crystal_type_combo.clear()
        
        types = CRYSTAL_TYPES_3D if self.is_3d else CRYSTAL_TYPES_2D
        for idx, info in types.items():
            self.crystal_type_combo.addItem(info['name'], idx)
        
        self.crystal_type_combo.blockSignals(False)
    
    def _on_material_type_changed(self, index):
        """Handle material type (2D/3D) change."""
        self.is_3d = (index == 0)
        self._update_crystal_types()
        self._on_crystal_type_changed(0)
    
    def _on_crystal_type_changed(self, index):
        """Handle crystal type change - show/hide appropriate inputs."""
        crystal_type = self.crystal_type_combo.currentData()
        if crystal_type is None:
            crystal_type = 1
        
        # Get enabled indices for this crystal type
        enabled_indices = get_enabled_indices(crystal_type, self.is_3d)
        
        # Hide all inputs first
        for (i, j), spin in self.cij_inputs.items():
            spin.setEnabled(False)
            spin.setStyleSheet("background-color: #f0f0f0;")
        
        # Enable relevant inputs
        for (i, j) in enabled_indices:
            if (i, j) in self.cij_inputs:
                self.cij_inputs[(i, j)].setEnabled(True)
                self.cij_inputs[(i, j)].setStyleSheet("background-color: white;")
    
    def _on_value_changed(self):
        """Handle any Cij value change."""
        self._read_cij_values()
        self._check_stability()
        self.cij_changed.emit(self.cij.copy())
    
    def _read_cij_values(self):
        """Read all Cij values from input fields."""
        self.cij = np.zeros((6, 6))
        for (i, j), spin in self.cij_inputs.items():
            value = spin.value()
            self.cij[i, j] = value
            self.cij[j, i] = value  # Symmetric
    
    def _check_stability(self):
        """Check and display mechanical stability."""
        result = check_stability_detailed(self.cij)
        is_stable = result['stable']
        
        if is_stable:
            self.stability_icon.setText("●")
            self.stability_icon.setStyleSheet("color: green;")
            self.stability_label.setText("Stable")
            self.stability_label.setStyleSheet("color: green;")
        else:
            self.stability_icon.setText("●")
            self.stability_icon.setStyleSheet("color: red;")
            self.stability_label.setText("Unstable")
            self.stability_label.setStyleSheet("color: red;")
        
        self.stability_changed.emit(is_stable)
    
    def _apply_symmetry(self):
        """Apply crystal symmetry to fill dependent constants."""
        crystal_type = self.crystal_type_combo.currentData() or 1
        self._read_cij_values()
        self.cij = fill_symmetric_matrix(self.cij, crystal_type, self.is_3d)
        self._update_display()
        self._check_stability()
        self.cij_changed.emit(self.cij.copy())
    
    def _clear_all(self):
        """Clear all input values."""
        for spin in self.cij_inputs.values():
            spin.blockSignals(True)
            spin.setValue(0.0)
            spin.blockSignals(False)
        self.cij = np.zeros((6, 6))
        self._check_stability()
        self.cij_changed.emit(self.cij.copy())
    
    def _load_preset(self):
        """Load a preset material."""
        # Example presets
        presets = {
            "Iron (Cubic)": np.array([
                [230, 135, 135, 0, 0, 0],
                [135, 230, 135, 0, 0, 0],
                [135, 135, 230, 0, 0, 0],
                [0, 0, 0, 117, 0, 0],
                [0, 0, 0, 0, 117, 0],
                [0, 0, 0, 0, 0, 117]
            ], dtype=float),
            "Aluminum (Cubic)": np.array([
                [108, 62, 62, 0, 0, 0],
                [62, 108, 62, 0, 0, 0],
                [62, 62, 108, 0, 0, 0],
                [0, 0, 0, 28, 0, 0],
                [0, 0, 0, 0, 28, 0],
                [0, 0, 0, 0, 0, 28]
            ], dtype=float),
            "Zinc (Hexagonal)": np.array([
                [165, 31, 50, 0, 0, 0],
                [31, 165, 50, 0, 0, 0],
                [50, 50, 62, 0, 0, 0],
                [0, 0, 0, 39, 0, 0],
                [0, 0, 0, 0, 39, 0],
                [0, 0, 0, 0, 0, 67]
            ], dtype=float)
        }
        
        from PyQt5.QtWidgets import QInputDialog
        name, ok = QInputDialog.getItem(self, "Load Preset", "Select material:",
                                        list(presets.keys()), 0, False)
        if ok and name:
            self.set_cij(presets[name])
    
    def _update_display(self):
        """Update all input displays from internal Cij matrix."""
        for (i, j), spin in self.cij_inputs.items():
            spin.blockSignals(True)
            spin.setValue(self.cij[i, j])
            spin.blockSignals(False)
    
    def get_cij(self) -> np.ndarray:
        """Get the current Cij matrix."""
        self._read_cij_values()
        return self.cij.copy()
    
    def set_cij(self, cij: np.ndarray):
        """Set the Cij matrix and update display."""
        self.cij = cij.copy()
        self._update_display()
        self._check_stability()
        self.cij_changed.emit(self.cij.copy())
    
    def get_compliance(self) -> np.ndarray:
        """Get the compliance matrix (inverse of stiffness)."""
        try:
            return np.linalg.inv(self.cij)
        except np.linalg.LinAlgError:
            QMessageBox.warning(self, "Warning", "Stiffness matrix is singular!")
            return None
