# Mat Model Lab

<div align="center">

**Material Constitutive Model Analysis, Visualization, and Code Generation Tool**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/) [![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)](https://www.riverbankcomputing.com/software/pyqt/) [![License](https://img.shields.io/badge/License-GPL--3.0-orange.svg)](LICENSE)

</div>

## Introduction

Mat Model Lab is a comprehensive material constitutive model tool for post-processing, visualization, and FEA code generation of material mechanical properties. The software provides a modern graphical interface and supports elastic constant analysis for various crystal types.

## Modules

| Module              | Description                          | Status       |
| ------------------- | ------------------------------------ | ------------ |
| **Elasticity**      | Elastic constant post-processing     | ✅ Complete   |
| **Plasticity**      | Plastic constitutive model analysis  | 🚧 In Development |
| **Hyperelasticity** | Hyperelastic model & UMAT generation | 🚧 In Development |

## Features

### Elasticity Module

- **Elastic Modulus Calculation**: Young's modulus, Shear modulus, Bulk modulus
- **Poisson's Ratio Analysis**: Direction-dependent Poisson's ratio
- **Hardness Prediction**: Chen-Niu hardness model
- **VRH Averaging**: Voigt-Reuss-Hill elastic constant averaging
- **Stability Check**: Born mechanical stability criteria
- **Material Database**: Built-in elastic parameter library
- **Visualization**: 2D/3D elastic property distribution plots
- **Report Generation**: HTML/PDF/Word report export
- **Model Export**: ABAQUS/COMSOL material model export

### Supported Crystal Systems

This software supports 10 crystal types with their specific elastic matrix forms.
See: [Supported Crystal Systems and Matrix Forms](CRYSTAL_TYPES.md)

## Installation

### Dependencies

```bash
# Install dependencies
pip install numpy scipy matplotlib PyQt6 pandas openpyxl python-docx

# Or use requirements.txt
pip install -r requirements.txt
```

### Dependency List

| Package     | Version | Purpose          |
| ----------- | ------- | ---------------- |
| numpy       | >=1.20  | Matrix operations |
| scipy       | >=1.7   | Scientific computing |
| matplotlib  | >=3.5   | Plotting         |
| PyQt6       | >=6.0   | GUI framework    |
| pandas      | >=1.4   | Excel I/O        |
| openpyxl    | >=3.0   | Excel engine     |
| python-docx | >=1.0   | Word export      |

## Usage

### Graphical Interface

```bash
python -m main
```

### Python API

```python
import numpy as np
from core import Young_3D, ElasticVRH3D, StableofMechanical
from visualization import ElasticPlot_3D, Plot_Slice
from mml_utils import Elastic_Read

# Read elastic constants
Cij, names, status = Elastic_Read('data.txt')

# Check stability
is_stable = StableofMechanical(Cij[:,:,0])
print(f"Stable: {is_stable}")

# Calculate VRH averages
vrh = ElasticVRH3D(Cij[:,:,0])

# 3D visualization
S = np.linalg.inv(Cij[:,:,0])
ElasticPlot_3D(S, n=100, flag=['E', 'G'])
```

## Project Structure

```
mat_model_lab/
├── core/                 # Core computation module
├── visualization/        # Visualization module
├── mml_utils/            # Utility modules
│   ├── data_io.py        # Data I/O
│   ├── material_db.py    # Material database
│   └── report_generator.py
├── gui/                  # Graphical interface
│   ├── main_window.py    # Main window
│   ├── modules/          # Feature modules
│   └── widgets/          # UI components
│       ├── about_dialog.py
│       └── documentation_dialog.py
├── assets/               # Resource files
│   └── database/         # Material database
└── main.py               # Entry point
```

## UI Preview

The software provides a modern Dark/Light theme interface, featuring:

- 📊 Interactive 2D/3D elastic property visualization
- 📁 Quick material database selection
- 📄 Multi-format report export
- 🔧 ABAQUS/COMSOL model generation

## Acknowledgment

The elasticity module of Mat Model Lab was originally based on **ElasticPOST**.

> Mingqing Liao, Yong Liu, Nan Qu et al. ElasticPOST: A Matlab Toolbox for Post-processing of Elastic Anisotropy with Graphic User Interface. *Computer Physics Communications* (2019)

Thanks to the ElasticPOST team for their pioneering work.

## Citation

If you use the elasticity module of this software in your research, please cite the above paper.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).