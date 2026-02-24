import numpy as np
import pandas as pd
import os
import sys

# Add parent directory to path to allow importing core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.crystal_type import CRYSTAL_TYPES_3D, fill_symmetric_matrix, get_independent_constants

def generate_examples():
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Generating examples in: {output_dir}")
    
    # Define sample data for each type (approximate real values or stable theoretic values)
    # Units: GPa
    sample_data = {
        'Cubic': {'c11': 168.4, 'c12': 121.4, 'c44': 75.4}, # Copper
        'Hexagonal': {'c11': 165.0, 'c12': 31.0, 'c13': 50.0, 'c33': 62.0, 'c44': 39.6}, # Zinc
        'Tetragonal_1': {'c11': 275.0, 'c12': 179.0, 'c13': 152.0, 'c33': 165.0, 'c44': 54.3, 'c66': 113.0}, # Generic BaTiO3-like
        'Tetragonal_2': {'c11': 280.0, 'c12': 180.0, 'c13': 150.0, 'c16': 10.0, 'c33': 160.0, 'c44': 60.0, 'c66': 110.0},
        'Trigonal_1': {'c11': 200.0, 'c12': 60.0, 'c13': 50.0, 'c14': 20.0, 'c33': 250.0, 'c44': 70.0},
        'Trigonal_2': {'c11': 87.0, 'c12': 7.0, 'c13': 12.0, 'c14': 18.0, 'c15': 5.0, 'c33': 107.0, 'c44': 58.0}, # Quartz-ish
        'Orthorhombic': {'c11': 320.5, 'c12': 68.2, 'c13': 71.6, 'c22': 196.5, 'c23': 76.8, 'c33': 233.5, 'c44': 64.0, 'c55': 77.0, 'c66': 78.7}, # Olivine
        'Monoclinic_1': {'c11': 150.0, 'c12': 50.0, 'c13': 40.0, 'c16': 10.0, 'c22': 180.0, 'c23': 60.0, 'c26': 5.0, 'c33': 160.0, 'c36': 8.0, 'c44': 45.0, 'c45': 5.0, 'c55': 55.0, 'c66': 65.0},
        'Monoclinic_2': {'c11': 140.0, 'c12': 45.0, 'c13': 35.0, 'c14': 10.0, 'c22': 170.0, 'c23': 55.0, 'c24': 8.0, 'c33': 150.0, 'c34': 6.0, 'c44': 40.0, 'c55': 50.0, 'c56': 4.0, 'c66': 60.0},
        'Triclinic': {
             'c11': 100.0, 'c12': 30.0, 'c13': 20.0, 'c14': 1.0, 'c15': 2.0, 'c16': 3.0,
             'c22': 110.0, 'c23': 35.0, 'c24': 4.0, 'c25': 5.0, 'c26': 6.0,
             'c33': 120.0, 'c34': 7.0, 'c35': 8.0, 'c36': 9.0,
             'c44': 40.0, 'c45': 0.5, 'c46': 0.6,
             'c55': 45.0, 'c56': 0.7,
             'c66': 50.0
        }
    }
    
    for type_id, type_info in CRYSTAL_TYPES_3D.items():
        name = type_info['name']
        print(f"Generating example for: {name}...")
        
        # 1. Create Data
        # Retrieve constants from sample dict
        independent_vars = type_info['independent']
        
        # Build independent C matrix (sparse 6x6)
        C = np.zeros((6, 6))
        
        type_samples = sample_data.get(name, {})
        
        for const_name in independent_vars:
            val = type_samples.get(const_name, 0.0)
            if val == 0.0:
                 print(f"  Warning: No sample data for {const_name} in {name}, using 10.0")
                 val = 10.0
                 
            # Parse indices cIJ
            i = int(const_name[1]) - 1
            j = int(const_name[2]) - 1
            C[i, j] = val
        
        # 2. Fill Symmetry
        C_filled = fill_symmetric_matrix(C, type_id, is_3d=True)
        
        # 3. Create DataFrame
        df = pd.DataFrame(C_filled)
        
        # Add a name column (optional, but good for format)
        # Format: Name, C1, C2, ..., C6
        df_export = df.copy()
        first_col_val = [f"{name}_Example"] + [""] * 5
        df_export.insert(0, 'Name', first_col_val)
        
        # 4. Save to Excel
        filename_xlsx = f"{name}_Example.xlsx"
        filepath_xlsx = os.path.join(output_dir, filename_xlsx)
        df_export.to_excel(filepath_xlsx, index=False, header=False)
        print(f"  Saved to {filepath_xlsx}")
        
        # 5. Save to Text
        filename_txt = f"{name}_Example.txt"
        filepath_txt = os.path.join(output_dir, filename_txt)
        with open(filepath_txt, 'w') as f:
            f.write(f"{name}_Example\n")
            np.savetxt(f, C_filled, fmt='%.1f')
        print(f"  Saved to {filepath_txt}")

if __name__ == "__main__":
    generate_examples()
