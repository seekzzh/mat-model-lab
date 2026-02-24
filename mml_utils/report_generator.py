import os
import base64
import numpy as np
import datetime
from typing import Optional, Dict

# Import core calculation modules
try:
    from ..core.elastic_vrh import ElasticVRH3D
    from ..core.stability import check_stability_detailed
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from core.elastic_vrh import ElasticVRH3D
    from core.stability import check_stability_detailed

def generate_report(
    filename: str,
    cij_matrix: np.ndarray,
    material_name: str = "Unknown Material",
    crystal_type: str = "Unknown",
    plots: Optional[Dict[str, str]] = None
) -> str:
    """
    Generate an HTML report for the elastic properties.

    Parameters
    ----------
    filename : str
        Path to save the HTML file.
    cij_matrix : numpy.ndarray
        Elastic stiffness matrix (6x6).
    material_name : str, optional
        Name of the material.
    crystal_type : str, optional
        Crystal symmetry type.
    plots : dict, optional
        Dictionary of {Plot Title: Image Path}.

    Returns
    -------
    str
        The absolute path of the generated report.
    """
    
    # Import 2D VRH module
    try:
        from ..core.elastic_vrh_2d import ElasticVRH2D
    except ImportError:
        from core.elastic_vrh_2d import ElasticVRH2D

    # Check if 2D material: rows/cols 2, 3, 4 (corresponding to C33, C23, C13) should be zero.
    # Non-zero positions for 2D: indices 0 (C11), 1 (C22), 5 (C66).
    
    is_2d = False
    if np.all(np.abs(cij_matrix[[2, 3, 4], :]) < 1e-6) and np.all(np.abs(cij_matrix[:, [2, 3, 4]]) < 1e-6):
        is_2d = True
        
    if is_2d:
        vrh_results = ElasticVRH2D(cij_matrix)
        sij_matrix = np.zeros_like(cij_matrix)
        # Invert the non-singular 2D submatrix [0, 1, 5] for display
        try:
             indices = [0, 1, 5]
             C_sub = cij_matrix[np.ix_(indices, indices)]
             S_sub = np.linalg.inv(C_sub)
             
             for r_i, r in enumerate(indices):
                 for c_i, c in enumerate(indices):
                     sij_matrix[r, c] = S_sub[r_i, c_i]
        except (np.linalg.LinAlgError, ValueError):
             pass
    else:
        vrh_results = ElasticVRH3D(cij_matrix)
        try:
            sij_matrix = np.linalg.inv(cij_matrix)
        except np.linalg.LinAlgError:
            sij_matrix = np.zeros_like(cij_matrix)
            
    stability_results = check_stability_detailed(cij_matrix, is_2d=is_2d)

    
    # 2. Encode Images if provided
    img_html = ""
    if plots:
        img_html = "<h2>Property Visualization</h2><div class='plot-grid'>"
        for title, path in plots.items():
            if os.path.exists(path):
                with open(path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    img_html += f'''
                    <div class="plot-card">
                        <h3>{title}</h3>
                        <img src="data:image/png;base64,{encoded_string}" alt="{title}">
                    </div>
                    '''
        img_html += "</div>"


    # 3. Format Matrices for HTML
    def matrix_to_html_table(mat, title):
        rows = mat.shape[0]
        html = f'<div class="matrix-box"><h3>{title}</h3><table>'
        for i in range(rows):
            html += "<tr>"
            for j in range(rows):
                val = mat[i, j]
                # Highlight non-zero values slightly
                style = 'class="nonzero"' if abs(val) > 1e-6 else 'class="zero"'
                if title.startswith("Compliance"):
                    # Compliance usually small, scientific notation might be needed, but let's stick to .4f or .5f
                    # 1/GPa = 10^-3 1/MPa? Compliance units are 1/GPa
                    html += f'<td {style}>{val:.5f}</td>'
                else:
                    html += f'<td {style}>{val:.1f}</td>'
            html += "</tr>"
        html += "</table></div>"
        return html

    cij_html = matrix_to_html_table(cij_matrix, "Stiffness Matrix (C<sub>ij</sub>) [GPa]")
    sij_html = matrix_to_html_table(sij_matrix, "Compliance Matrix (S<sub>ij</sub>) [1/GPa]")

    # 4. Format Engineering Constants Table
    eng_table_html = f"""
    <table class="results-table">
        <tr>
            <th>Property</th>
            <th>Voigt (Upper Bound)</th>
            <th>Reuss (Lower Bound)</th>
            <th>Hill (Average)</th>
        </tr>
        <tr>
            <td><b>Bulk Modulus (B)</b></td>
            <td>{vrh_results['K_V']:.2f} GPa</td>
            <td>{vrh_results['K_R']:.2f} GPa</td>
            <td>{vrh_results['K_VRH']:.2f} GPa</td>
        </tr>
        <tr>
            <td><b>Shear Modulus (G)</b></td>
            <td>{vrh_results['G_V']:.2f} GPa</td>
            <td>{vrh_results['G_R']:.2f} GPa</td>
            <td>{vrh_results['G_VRH']:.2f} GPa</td>
        </tr>
        <tr>
            <td colspan="4" class="separator"></td>
        </tr>
        <tr>
            <td><b>Young's Modulus (E)</b></td>
            <td colspan="3" class="highlight">{vrh_results['E']:.2f} GPa</td>
        </tr>
        <tr>
            <td><b>Poisson's Ratio (ν)</b></td>
            <td colspan="3" class="highlight">{vrh_results['v']:.3f}</td>
        </tr>
         <tr>
            <td><b>Hardness (H)</b></td>
            <td colspan="3">{vrh_results['H']:.2f} GPa (Chen-Niu Model)</td>
        </tr>
        <tr>
            <td><b>Universal Anisotropy Index (A<sup>U</sup>)</b></td>
            <td colspan="3">{vrh_results['A']:.3f}</td>
        </tr>
         <tr>
            <td><b>Pugh's Ratio (B/G)</b></td>
            <td colspan="3">{vrh_results['k_G']:.3f} ({'Ductile' if vrh_results['k_G'] > 1.75 else 'Brittle'})</td>
        </tr>
    </table>
    """

    # 5. Build Full HTML
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    stability_color = "green" if stability_results['stable'] else "red"
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Mat Model Lab Report - {material_name}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; }}
        .container {{ background-color: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; border-bottom: 1px solid #eee; }}
        .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; background: #f0f7fb; padding: 15px; border-radius: 5px; }}
        .info-item {{ margin-bottom: 5px; }}
        .label {{ font-weight: bold; color: #555; }}
        
        /* Tables */
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ padding: 10px; border: 1px solid #ddd; text-align: center; }}
        th {{ background-color: #f2f2f2; font-weight: 600; color: #444; }}
        
        .matrix-box {{ margin-bottom: 20px; overflow-x: auto; }}
        .matrix-box table {{ font-family: monospace; font-size: 0.95em; }}
        .nonzero {{ color: #000; font-weight: 500; }}
        .zero {{ color: #ccc; }}
        
        .results-table th {{ width: 25%; }}
        .highlight {{ font-weight: bold; color: #2980b9; font-size: 1.1em; }}
        .separator {{ background-color: #fafafa; height: 5px; padding: 0; }}
        
        .plot-container {{ text-align: center; margin: 30px 0; border: 1px solid #eee; padding: 10px; }}
        .plot-container img {{ max-width: 100%; height: auto; border-radius: 4px; }}
        
        /* Grid for Multiple Plots */
        .plot-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0; }}
        .plot-card {{ border: 1px solid #eee; padding: 10px; text-align: center; background: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .plot-card h3 {{ margin-top: 5px; font-size: 1.1em; color: #555; border-bottom: none; }}
        .plot-card img {{ max-width: 100%; height: auto; border-radius: 4px; }}
        
        .stability-box {{ padding: 15px; border-left: 5px solid {stability_color}; background-color: #fff; margin: 20px 0; font-weight: bold; }}
        
        footer {{ margin-top: 40px; text-align: center; font-size: 0.8em; color: #888; border-top: 1px solid #eee; padding-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Elastic Property Analysis Report</h1>
        
        <div class="info-grid">
            <div class="info-item"><span class="label">Material Name:</span> {material_name}</div>
            <div class="info-item"><span class="label">Crystal System:</span> {crystal_type}</div>
            <div class="info-item"><span class="label">Analysis Date:</span> {current_date}</div>
            <div class="info-item"><span class="label">Software:</span> Mat Model Lab</div>
        </div>

        <h2>Mechanical Stability</h2>
        <div class="stability-box" style="color: {stability_color}">
            {stability_results['message']}
        </div>

        <h2>Engineering Elastic Constants (VRH Average)</h2>
        <p>Values calculated using Voigt-Reuss-Hill approximation.</p>
        {eng_table_html}

        {img_html}

        <h2>Elastic Tensors</h2>
        <div style="display: flex; gap: 20px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 350px;">
                {cij_html}
            </div>
            <div style="flex: 1; min-width: 350px;">
                {sij_html}
            </div>
        </div>

        <footer>
            Generated by Mat Model Lab
        </footer>
    </div>
</body>
</html>
    """

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    return os.path.abspath(filename)
