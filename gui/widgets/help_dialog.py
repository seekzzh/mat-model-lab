from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

class HelpDialog(QDialog):
    def __init__(self, parent=None, is_dark=False):
        super().__init__(parent)
        self.setWindowTitle("Mat Model Lab Documentation")
        self.resize(900, 700)
        self.is_dark = is_dark
        
        layout = QVBoxLayout(self)
        
        # Text Browser for HTML content
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setHtml(self.get_help_content())
        
        # Apply theme-specific palette or style to the widget itself if needed
        # (Though HTML CSS handles most content, the scrollbar might need main app style)
        
        layout.addWidget(self.text_browser)
        
        # Button bar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        
    def get_help_content(self):
        """Returns the HTML content for the documentation"""
        # Define colors based on theme
        if self.is_dark:
            bg_color = "#2b2b2b"
            text_color = "#e0e0e0"
            header_color = "#64b5f6" # Light Blue
            subheader_color = "#81c784" # Light Green
            code_bg = "#3c3c3c"
            pre_bg = "#1e1e1e"
            pre_text = "#a5d6a7" # Light green text for matrices
            border_color = "#555"
            blockquote_border = "#666"
            blockquote_text = "#bbb"
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
            border_color = "#eee"
            blockquote_border = "#ddd"
            blockquote_text = "#666"
            note_bg = "#e8f4f8"
            note_border = "#3498db"

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: sans-serif; line-height: 1.6; color: {text_color}; background-color: {bg_color}; }}
                h1 {{ color: {header_color}; border-bottom: 2px solid {border_color}; padding-bottom: 10px; }}
                h2 {{ color: {subheader_color}; margin-top: 20px; border-bottom: 1px solid {border_color}; }}
                h3 {{ color: {header_color}; font-size: 1.1em; margin-top: 15px; }}
                ul {{ margin-bottom: 15px; }}
                li {{ margin-bottom: 5px; }}
                code {{ background-color: {code_bg}; padding: 2px 4px; border-radius: 3px; font-family: monospace; color: {text_color}; }}
                pre {{ background-color: {pre_bg}; color: {pre_text}; padding: 15px; border-radius: 5px; overflow-x: auto; font-family: monospace; font-size: 14px; border: 1px solid {border_color}; }}
                blockquote {{ border-left: 4px solid {blockquote_border}; margin: 15px 0; padding-left: 15px; color: {blockquote_text}; }}
                .note {{ background-color: {note_bg}; padding: 15px; border-radius: 5px; border-left: 5px solid {note_border}; }}
            </style>
        </head>
        <body>
            <h1>Mat Model Lab</h1>
            <p>A comprehensive tool for material constitutive model analysis, visualization, and finite element code generation.</p>
            
            <h2>Introduction</h2>
            <p>Mat Model Lab is a Python-based toolkit for material model analysis. The Elasticity module is based on the original ElasticPOST MATLAB version.</p>
            
            <h2>Features</h2>
            
            <h3>Core Calculations</h3>
            <ul>
                <li><b>Elastic Moduli:</b> Young's Modulus, Shear Modulus, Bulk Modulus</li>
                <li><b>Poisson's Ratio:</b> Direction-dependent Poisson's ratio analysis</li>
                <li><b>Hardness:</b> Chen-Niu hardness model</li>
                <li><b>VRH Average:</b> Voigt-Reuss-Hill elastic constant averaging</li>
                <li><b>Stability Check:</b> Born mechanical stability criteria</li>
            </ul>
            
            <h3>Visualization</h3>
            <ul>
                <li><b>3D Plot:</b> 3D surface distribution of elastic properties</li>
                <li><b>2D Plot:</b> Standard crystal plane slices (XY, XZ, YZ)</li>
                <li><b>Arbitrary Slice:</b> Custom Miller index (hkl) direction slices</li>
            </ul>
            
            <h3>Data Handling</h3>
            <ul>
                <li>Supports multiple formats: <code>.txt</code>, <code>.xlsx</code>, <code>.mat</code></li>
                <li>Batch processing support</li>
            </ul>

            <h2>Theory Support</h2>
            
            <h3>Elastic Moduli Calculation</h3>
            <p>The software calculates the spatial distribution of elastic properties based on the compliance matrix <b>S</b> (inverse of stiffness matrix <b>C</b>).</p>
            <ul>
                <li><b>Young's Modulus (E):</b> E = 1 / S'<sub>11</sub></li>
                <li><b>Linear Compressibility (β):</b> β = S'<sub>11</sub> + S'<sub>12</sub> + S'<sub>13</sub></li>
                <li><b>Shear Modulus (G):</b> G = 1 / (4S'<sub>66</sub>)</li>
                <li><b>Poisson's Ratio (ν):</b> ν = -S'<sub>12</sub> / S'<sub>11</sub></li>
            </ul>
            <p><i>Note: S' denotes the compliance matrix transformed to the specific direction (θ, φ).</i></p>

            <h3>Polycrystalline Averaging (VRH)</h3>
            <p>The code implements the <b>Voigt-Reuss-Hill (VRH)</b> approximation for polycrystalline properties:</p>
            <ul>
                <li><b>Voigt Bound:</b> Upper bound (assumption of uniform strain).</li>
                <li><b>Reuss Bound:</b> Lower bound (assumption of uniform stress).</li>
                <li><b>Hill Average:</b> Arithmetic mean of Voigt and Reuss bounds: X<sub>Hill</sub> = (X<sub>Voigt</sub> + X<sub>Reuss</sub>) / 2</li>
            </ul>

            <h3>Hardness Model</h3>
            <p>Hardness is estimated using the <b>Chen-Niu model</b> (2011), which correlates hardness with the shear modulus (G) and Young's modulus (E):</p>
            <blockquote>H = 2 * (k<sup>2</sup>G)<sup>0.585</sup> - 3</blockquote>
            <p>Where k = G/E acts as an indicator of ductility/brittleness.</p>

            <h2>Supported Crystal Systems</h2>
            <p>The software supports compliance with the following 10 crystal symmetries. The matrix forms below show the <b>Independent Constants</b> (editable) and their relationships.</p>

            <h3>1. Triclinic</h3>
            <pre>
C11  C12  C13  C14  C15  C16
C12  C22  C23  C24  C25  C26
C13  C23  C33  C34  C35  C36
C14  C24  C34  C44  C45  C46
C15  C25  C35  C45  C55  C56
C16  C26  C36  C46  C56  C66
            </pre>

            <h3>2. Monoclinic_1 (Diad // z-axis)</h3>
            <pre>
C11  C12  C13   .    .   C16
C12  C22  C23   .    .   C26
C13  C23  C33   .    .   C36
 .    .    .   C44  C45   .
 .    .    .   C45  C55   .
C16  C26  C36   .    .   C66
            </pre>

            <h3>3. Monoclinic_2 (Diad // y-axis)</h3>
            <pre>
C11  C12  C13   .   C15   .
C12  C22  C23   .   C25   .
C13  C23  C33   .   C35   .
 .    .    .   C44   .   C46
C15  C25  C35   .   C55   .
 .    .    .   C46   .   C66
            </pre>

            <h3>4. Orthorhombic</h3>
            <pre>
C11  C12  C13   .    .    .
C12  C22  C23   .    .    .
C13  C23  C33   .    .    .
 .    .    .   C44   .    .
 .    .    .    .   C55   .
 .    .    .    .    .   C66
            </pre>

            <h3>5. Tetragonal_1 (4/mmm)</h3>
            <p>Constraints: C22=C11, C23=C13, C55=C44</p>
            <pre>
C11  C12  C13   .    .    .
C12  C11  C13   .    .    .
C13  C13  C33   .    .    .
 .    .    .   C44   .    .
 .    .    .    .   C44   .
 .    .    .    .    .   C66
            </pre>

            <h3>6. Tetragonal_2 (4)</h3>
            <p>Constraints: C22=C11, C23=C13, C55=C44, C26=-C16</p>
            <pre>
C11  C12  C13   .    .   C16
C12  C11  C13   .    .  -C16
C13  C13  C33   .    .    .
 .    .    .   C44   .    .
 .    .    .    .   C44   .
C16 -C16   .    .    .   C66
            </pre>

            <h3>7. Trigonal_1 (-3m)</h3>
            <p>Constraints: C22=C11, C23=C13, C55=C44, C24=-C14, C56=C14, C66=(C11-C12)/2</p>
            <pre>
C11  C12  C13  C14   .    .
C12  C11  C13 -C14   .    .
C13  C13  C33   .    .    .
C14 -C14   .   C44   .    .
 .    .    .    .   C44  C14
 .    .    .    .   C14  (C11-C12)/2
            </pre>
            
            <h3>8. Trigonal_2 (-3)</h3>
            <p>Constraints: C22=C11, C23=C13, C55=C44, C24=-C14, C56=C14, C25=-C15, C46=-C15, C66=(C11-C12)/2</p>
            <pre>
C11  C12  C13  C14  C15   .
C12  C11  C13 -C14 -C15   .
C13  C13  C33   .    .    .
C14 -C14   .   C44   .  -C15
C15 -C15   .    .   C44  C14
 .    .    .  -C15  C14  (C11-C12)/2
            </pre>

            <h3>9. Hexagonal</h3>
            <p>Constraints: Transverse Isotropy. C66=(C11-C12)/2</p>
            <pre>
C11  C12  C13   .    .    .
C12  C11  C13   .    .    .
C13  C13  C33   .    .    .
 .    .    .   C44   .    .
 .    .    .    .   C44   .
 .    .    .    .    .   (C11-C12)/2
            </pre>

            <h3>10. Cubic</h3>
            <p>Constraints: C22=C33=C11, C12=C13=C23, C44=C55=C66</p>
            <pre>
C11  C12  C12   .    .    .
C12  C11  C12   .    .    .
C12  C12  C11   .    .    .
 .    .    .   C44   .    .
 .    .    .    .   C44   .
 .    .    .    .    .   C44
            </pre>

            <h2>How to Use</h2>
            
            <h3>Input Data</h3>
            <ul>
                <li><b>Manual Input:</b> Select your crystal system (e.g., Cubic, Hexagonal) and manually fill in the non-zero stiffness matrix (Cij) elements.</li>
                <li><b>From File:</b> Click "Select File" to load elastic constants from a supported file. The program will automatically detect the format.</li>
            </ul>
            
            <h3>Visualization</h3>
            <ul>
                <li><b>3D Plot:</b> Select "3D Plot" in Visualization Options, choose the property to display, and click Calculate.</li>
                <li><b>2D Plot:</b> Select "2D Plot". You can choose "Standard" planes or "Arbitrary (hkl)" to define a custom slicing plane.</li>
            </ul>
            
            <h2>Citation</h2>
            <p>If you use the Elasticity module in your research, please cite:</p>
            <blockquote>
                Mingqing Liao, Yong Liu, Nan Qu et al. ElasticPOST: A Matlab Toolbox for Post-processing of Elastic Anisotropy with Graphic User Interface. <i>Computer Physics Communications</i> (2019)
            </blockquote>
            <p><i>The Elasticity module of Mat Model Lab is based on ElasticPOST.</i></p>
        </body>
        </html>
        """
