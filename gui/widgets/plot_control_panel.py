# Plot Control Panel Widget for Mat Model Lab GUI
# Provides controls for visualization settings

import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QSpinBox, QDoubleSpinBox, QGroupBox,
                             QComboBox, QPushButton, QCheckBox, QRadioButton,
                             QButtonGroup, QFrame, QLineEdit, QTabWidget)
from PyQt6.QtCore import pyqtSignal, Qt


class PlotControlPanel(QWidget):
    """
    Panel for controlling visualization settings.
    
    Signals
    -------
    plot_requested : dict
        Emitted when user requests a plot, contains settings dict
    save_requested : dict
        Emitted when user requests to save current plot
    """
    
    plot_requested = pyqtSignal(dict)
    save_requested = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Use tabs for different plot modes
        self.tabs = QTabWidget()
        
        # 3D Plot Tab
        self.tab_3d = QWidget()
        self._setup_3d_tab()
        self.tabs.addTab(self.tab_3d, "3D Plot")
        
        # 2D Slice Tab
        self.tab_2d = QWidget()
        self._setup_2d_tab()
        self.tabs.addTab(self.tab_2d, "2D Slice")
        
        # Custom Slice Tab
        self.tab_slice = QWidget()
        self._setup_slice_tab()
        self.tabs.addTab(self.tab_slice, "Custom Slice")
        
        layout.addWidget(self.tabs)
        
        # Property selection (common to all tabs)
        prop_group = QGroupBox("Properties")
        prop_layout = QGridLayout(prop_group)
        
        self.property_checkboxes = {}
        properties = [
            ('E', "Young's Modulus"),
            ('G', "Shear Modulus"),
            ('B', "Bulk Modulus"),
            ('v', "Poisson's Ratio"),
            ('H', "Hardness")
        ]
        
        for i, (key, label) in enumerate(properties):
            cb = QCheckBox(label)
            cb.setChecked(key in ['E', 'G'])  # Default selection
            self.property_checkboxes[key] = cb
            prop_layout.addWidget(cb, i // 2, i % 2)
        
        layout.addWidget(prop_group)
        
        # Resolution setting
        res_layout = QHBoxLayout()
        res_label = QLabel("Resolution:")
        self.resolution_spin = QSpinBox()
        self.resolution_spin.setRange(20, 500)
        self.resolution_spin.setValue(100)
        self.resolution_spin.setSingleStep(10)
        self.resolution_spin.setToolTip("Number of points for plotting")
        res_layout.addWidget(res_label)
        res_layout.addWidget(self.resolution_spin)
        res_layout.addStretch()
        layout.addLayout(res_layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        self.plot_btn = QPushButton("🔄 Plot")
        self.plot_btn.setMinimumHeight(35)
        self.plot_btn.clicked.connect(self._on_plot_clicked)
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.clicked.connect(self._on_save_clicked)
        button_layout.addWidget(self.plot_btn)
        button_layout.addWidget(self.save_btn)
        layout.addLayout(button_layout)
        
    def _setup_3d_tab(self):
        """Set up 3D plot options."""
        layout = QVBoxLayout(self.tab_3d)
        
        # Display mode
        mode_group = QGroupBox("Display Mode")
        mode_layout = QVBoxLayout(mode_group)
        
        self.mode_3d_group = QButtonGroup(self)
        modes = [("Surface", "surface"), ("Wireframe", "wireframe"), ("Points", "points")]
        for i, (label, value) in enumerate(modes):
            rb = QRadioButton(label)
            rb.setProperty("mode", value)
            self.mode_3d_group.addButton(rb, i)
            mode_layout.addWidget(rb)
            if i == 0:
                rb.setChecked(True)
        
        layout.addWidget(mode_group)
        
        # Colormap selection
        cmap_layout = QHBoxLayout()
        cmap_label = QLabel("Colormap:")
        self.colormap_combo = QComboBox()
        self.colormap_combo.addItems(['jet', 'viridis', 'plasma', 'coolwarm', 'rainbow', 'hot'])
        cmap_layout.addWidget(cmap_label)
        cmap_layout.addWidget(self.colormap_combo)
        layout.addLayout(cmap_layout)
        
        # Transparency
        alpha_layout = QHBoxLayout()
        alpha_label = QLabel("Transparency:")
        self.alpha_spin = QDoubleSpinBox()
        self.alpha_spin.setRange(0.1, 1.0)
        self.alpha_spin.setSingleStep(0.1)
        self.alpha_spin.setValue(0.8)
        alpha_layout.addWidget(alpha_label)
        alpha_layout.addWidget(self.alpha_spin)
        layout.addLayout(alpha_layout)
        
        layout.addStretch()
        
    def _setup_2d_tab(self):
        """Set up 2D slice options for principal planes."""
        layout = QVBoxLayout(self.tab_2d)
        
        # Plane selection
        plane_group = QGroupBox("Principal Planes")
        plane_layout = QVBoxLayout(plane_group)
        
        self.plane_checkboxes = {}
        for plane in ['XY', 'XZ', 'YZ']:
            cb = QCheckBox(f"{plane} Plane")
            cb.setChecked(True)
            self.plane_checkboxes[plane.lower()] = cb
            plane_layout.addWidget(cb)
        
        layout.addWidget(plane_group)
        
        # Polar plot option
        self.polar_plot_check = QCheckBox("Use Polar Coordinates")
        self.polar_plot_check.setChecked(True)
        layout.addWidget(self.polar_plot_check)
        
        layout.addStretch()
        
    def _setup_slice_tab(self):
        """Set up custom crystallographic plane slice."""
        layout = QVBoxLayout(self.tab_slice)
        
        # Miller indices input
        miller_group = QGroupBox("Miller Indices [h k l]")
        miller_layout = QHBoxLayout(miller_group)
        
        self.miller_h = QDoubleSpinBox()
        self.miller_k = QDoubleSpinBox()
        self.miller_l = QDoubleSpinBox()
        
        for spin, default in [(self.miller_h, 1), (self.miller_k, 1), (self.miller_l, 1)]:
            spin.setRange(-10, 10)
            spin.setDecimals(2)
            spin.setValue(default)
            spin.setSingleStep(0.1)
            miller_layout.addWidget(spin)
        
        layout.addWidget(miller_group)
        
        # Quick presets
        preset_group = QGroupBox("Quick Presets")
        preset_layout = QGridLayout(preset_group)
        
        presets = [
            ("[100]", (1, 0, 0)),
            ("[110]", (1, 1, 0)),
            ("[111]", (1, 1, 1)),
            ("[001]", (0, 0, 1)),
        ]
        
        for i, (label, values) in enumerate(presets):
            btn = QPushButton(label)
            btn.setProperty("values", values)
            btn.clicked.connect(self._on_preset_clicked)
            preset_layout.addWidget(btn, i // 2, i % 2)
        
        layout.addWidget(preset_group)
        
        # 3D or 2D visualization
        vis_group = QGroupBox("Visualization")
        vis_layout = QVBoxLayout(vis_group)
        self.slice_3d_radio = QRadioButton("3D View")
        self.slice_2d_radio = QRadioButton("2D Polar")
        self.slice_2d_radio.setChecked(True)
        vis_layout.addWidget(self.slice_3d_radio)
        vis_layout.addWidget(self.slice_2d_radio)
        layout.addWidget(vis_group)
        
        layout.addStretch()
        
    def _on_preset_clicked(self):
        """Handle preset button click."""
        btn = self.sender()
        h, k, l = btn.property("values")
        self.miller_h.setValue(h)
        self.miller_k.setValue(k)
        self.miller_l.setValue(l)
        
    def _on_plot_clicked(self):
        """Handle plot button click."""
        settings = self.get_settings()
        self.plot_requested.emit(settings)
        
    def _on_save_clicked(self):
        """Handle save button click."""
        settings = self.get_settings()
        self.save_requested.emit(settings)
        
    def get_settings(self) -> dict:
        """Get current plot settings as a dictionary."""
        # Get selected properties
        properties = [key for key, cb in self.property_checkboxes.items() if cb.isChecked()]
        
        # Get current tab
        current_tab = self.tabs.currentIndex()
        
        settings = {
            'properties': properties,
            'resolution': self.resolution_spin.value(),
            'mode': 'unknown',
        }
        
        if current_tab == 0:  # 3D Plot
            settings['mode'] = '3d'
            checked = self.mode_3d_group.checkedButton()
            settings['display_mode'] = checked.property("mode") if checked else 'surface'
            settings['colormap'] = self.colormap_combo.currentText()
            settings['alpha'] = self.alpha_spin.value()
            
        elif current_tab == 1:  # 2D Slice
            settings['mode'] = '2d'
            settings['planes'] = [k for k, cb in self.plane_checkboxes.items() if cb.isChecked()]
            settings['polar'] = self.polar_plot_check.isChecked()
            
        elif current_tab == 2:  # Custom Slice
            settings['mode'] = 'slice'
            settings['miller'] = (self.miller_h.value(), 
                                  self.miller_k.value(), 
                                  self.miller_l.value())
            settings['slice_3d'] = self.slice_3d_radio.isChecked()
            
        return settings
    
    def get_selected_properties(self) -> list:
        """Get list of selected property codes."""
        return [key for key, cb in self.property_checkboxes.items() if cb.isChecked()]
