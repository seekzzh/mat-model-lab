# Data I/O module for Mat Model Lab
# Supports reading/writing elastic constants in various formats

import os
import numpy as np
from typing import Tuple, List, Optional, Dict, Any


def Elastic_Read(file_path: str, file_type: Optional[str] = None) -> Tuple[np.ndarray, List[str], str]:
    """
    Read elastic constants from file.
    
    Supports txt/dat, xlsx/xls, and mat file formats.
    
    Parameters
    ----------
    file_path : str
        Path to the file containing elastic constants
    file_type : str, optional
        Type of file ('txt', 'xlsx', 'mat'). If None, determined from file extension.
        
    Returns
    -------
    Cij : numpy.ndarray
        Elastic stiffness matrices, shape (6, 6, n) or (3, 3, n)
    ComName : list
        List of material/compound names
    State : str
        Status message ('OK' or error/warning message)
        
    Examples
    --------
    >>> Cij, names, state = Elastic_Read('data.txt')
    >>> print(f"Found {Cij.shape[2]} materials, status: {state}")
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if file_type is None:
        _, ext = os.path.splitext(file_path)
        file_type = ext[1:].lower()
    
    filename = os.path.splitext(os.path.basename(file_path))[0]
    
    if file_type in ('xlsx', 'xls'):
        Cij, ComName, State = _read_excel(file_path, filename)
    elif file_type in ('txt', 'dat'):
        Cij, ComName, State = _read_txt(file_path, filename)
    elif file_type == 'mat':
        Cij, ComName, State = _read_mat(file_path, filename)
    else:
        Cij, ComName, State = _read_txt(file_path, filename)
    
    # Convert 3x3 to 6x6 if needed
    if Cij.shape[1] == 3:
        from ..core.conversions import D2toD3
        num_cij = Cij.shape[2]
        Cij_6x6 = np.zeros((6, 6, num_cij))
        for i in range(num_cij):
            Cij_6x6[:, :, i] = D2toD3(Cij[:, :, i])
        Cij = Cij_6x6
    
    return Cij, ComName, State


def _read_txt(file_path: str, filename: str) -> Tuple[np.ndarray, List[str], str]:
    """
    Read elastic constants from text file.
    
    File format: 
    - Optional name lines (containing letters)
    - Numerical data: 6 columns for 3D, 3 columns for 2D
    - Multiple Cij matrices separated by name lines
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if not lines:
        return _no_data_error()
    
    numeric_data = []
    names = []
    
    for line in lines:
        line = line.strip()
        if not line or line.isspace():
            continue
        
        # Check if line contains letters (name line)
        has_letter = any(c.isalpha() for c in line)
        if has_letter:
            names.append(line)
        else:
            # Try to parse as numeric data
            try:
                values = [float(x) for x in line.split()]
                if values:
                    numeric_data.append(values)
            except ValueError:
                continue
    
    if not numeric_data:
        return _no_data_error()
    
    # Convert to numpy array
    data = np.array(numeric_data)
    n_cols = data.shape[1]
    
    if n_cols not in (3, 6):
        return _no_effective_data_error()
    
    # Reshape into individual Cij matrices
    total_rows = data.shape[0]
    extra_lines = total_rows % n_cols
    
    if extra_lines:
        state = f'The row of data is not divisible by {n_cols}. The last {extra_lines} lines are neglected.'
        data = data[:total_rows - extra_lines, :]
    else:
        state = 'OK'
    
    n_cij = data.shape[0] // n_cols
    if n_cij == 0:
        return _no_data_error()
    
    # Reshape: (n_rows, n_cols) -> (n_cols, n_cols, n_cij)
    Cij = np.zeros((n_cols, n_cols, n_cij))
    for i in range(n_cij):
        start_row = i * n_cols
        end_row = (i + 1) * n_cols
        Cij[:, :, i] = data[start_row:end_row, :]
    
    # Generate names if not provided
    if len(names) == 0:
        names = [f'{filename}-{i+1}' for i in range(n_cij)]
    elif len(names) < n_cij:
        names.extend([f'{filename}-{i+1}' for i in range(len(names), n_cij)])
    
    print(f'There are {n_cij} CIJs.')
    return Cij, names[:n_cij], state


def _read_excel(file_path: str, filename: str) -> Tuple[np.ndarray, List[str], str]:
    """
    Read elastic constants from Excel file.
    
    Each sheet can contain multiple Cij matrices.
    First column can optionally contain names.
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas is required to read Excel files. Install with: pip install pandas openpyxl")
    
    try:
        import openpyxl
    except ImportError:
        raise ImportError("openpyxl is required to read .xlsx files. Install with: pip install openpyxl")
    
    xl = pd.ExcelFile(file_path)
    sheet_names = xl.sheet_names
    print(f'There are {len(sheet_names)} sheets.')
    
    all_cij = []
    all_names = []
    state = 'OK'
    
    for sheet_idx, sheet_name in enumerate(sheet_names):
        print(f'Reading the {sheet_idx + 1}th sheet.')
        
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        
        if df.empty:
            continue
        
        # 1. Clean up DataFrame: Drop completely empty rows and columns
        df = df.dropna(how='all', axis=0) # Drop empty rows
        df = df.dropna(how='all', axis=1) # Drop empty columns
        
        if df.empty:
            continue

        # 2. Try to separate names from numeric data
        # Check if first column contains strings (robust check)
        first_col = df.iloc[:, 0]
        # Count non-numeric items in first column
        non_numeric_count = first_col.apply(lambda x: isinstance(x, str) and not x.replace('.', '', 1).isdigit()).sum()
        
        # Heuristic: if more than half are non-numeric strings, distinct from data, assume it's names
        has_names = non_numeric_count > 0 
        
        if has_names:
            names = first_col.dropna().tolist()
            # Filter out basic numbers that might be read as strings
            names = [str(n) for n in names if str(n).strip()]
            data_df = df.iloc[:, 1:]
        else:
            names = []
            data_df = df
            
        # Ensure data is numeric, coerce errors to NaN
        data = data_df.apply(pd.to_numeric, errors='coerce').values
        
        # Clean data: remove rows that contain ANY NaN (strict data integrity)
        # But this might be too strict for 2D data if empty columns exist? 
        # For 6x6 or 3x3, we expect full rows.
        data = data[~np.isnan(data).any(axis=1)]
        
        if data.size == 0:
            continue
        
        n_cols = data.shape[1]
        if n_cols not in (3, 6):
            if n_cols == 7 and has_names: # Common case where name col wasn't perfectly separated or index col existed
                 # Try to drop first column again
                 data = data[:, 1:]
                 n_cols = data.shape[1]
            
            if n_cols not in (3, 6):
                state = f'Sheet {sheet_name}: Column count must be 3 or 6, found {n_cols}'
                continue
        
        # Reshape into Cij matrices
        total_rows = data.shape[0]
        extra_lines = total_rows % n_cols
        
        if extra_lines:
            state = f'The row of data is not divisible by {n_cols}. The last {extra_lines} lines are neglected.'
            data = data[:total_rows - extra_lines, :]
        
        n_cij = data.shape[0] // n_cols
        if n_cij == 0:
            continue
        
        print(f'There are {n_cij} CIJs.')
        
        for i in range(n_cij):
            start_row = i * n_cols
            end_row = (i + 1) * n_cols
            Cij_i = data[start_row:end_row, :]
            all_cij.append(Cij_i)
            
            if len(names) > i:
                all_names.append(names[i])
            else:
                all_names.append(f'{filename}-{sheet_name}-{i+1}')
    
    if not all_cij:
        return _no_data_error()
    
    # Stack all Cij matrices
    n_cols = all_cij[0].shape[1]
    Cij = np.zeros((n_cols, n_cols, len(all_cij)))
    for i, cij in enumerate(all_cij):
        Cij[:, :, i] = cij
    
    print(f'There are {len(all_cij)} CIJs in this file.')
    return Cij, all_names, state


def _read_mat(file_path: str, filename: str) -> Tuple[np.ndarray, List[str], str]:
    """
    Read elastic constants from MATLAB .mat file.
    
    Expects variables containing 6x6 or 3x3 numeric matrices.
    Cell arrays are treated as name lists.
    """
    try:
        from scipy.io import loadmat
    except ImportError:
        raise ImportError("scipy is required to read .mat files. Install with: pip install scipy")
    
    data = loadmat(file_path)
    
    # Filter out private variables (starting with __)
    field_names = [k for k in data.keys() if not k.startswith('__')]
    
    if not field_names:
        return _no_data_error()
    
    all_cij = []
    all_names = []
    names_from_cell = None
    state = 'OK'
    
    for field_name in field_names:
        field_data = data[field_name]
        
        # Check if it's a cell array (for names)
        if isinstance(field_data, np.ndarray) and field_data.dtype == object:
            # Try to extract as names
            try:
                names_from_cell = [str(x[0]) if hasattr(x, '__iter__') else str(x) 
                                   for x in field_data.flatten()]
            except (TypeError, IndexError, ValueError):
                pass
            continue
        
        # Check if it's numeric data
        if not isinstance(field_data, np.ndarray) or not np.issubdtype(field_data.dtype, np.number):
            continue
        
        n_cols = field_data.shape[1] if len(field_data.shape) > 1 else 0
        if n_cols not in (3, 6):
            continue
        
        # Reshape into Cij matrices
        total_rows = field_data.shape[0]
        extra_lines = total_rows % n_cols
        
        if extra_lines:
            state = f'The row of data is not divisible by {n_cols}. The last {extra_lines} lines are neglected.'
            field_data = field_data[:total_rows - extra_lines, :]
        
        n_cij = field_data.shape[0] // n_cols
        if n_cij == 0:
            continue
        
        for i in range(n_cij):
            start_row = i * n_cols
            end_row = (i + 1) * n_cols
            Cij_i = field_data[start_row:end_row, :]
            all_cij.append(Cij_i)
            all_names.append(f'{filename}-{field_name}-{i+1}')
    
    if not all_cij:
        return _no_data_error()
    
    # Use cell array names if available
    if names_from_cell and len(names_from_cell) >= len(all_cij):
        all_names = names_from_cell[:len(all_cij)]
    
    # Stack all Cij matrices
    n_cols = all_cij[0].shape[1]
    Cij = np.zeros((n_cols, n_cols, len(all_cij)))
    for i, cij in enumerate(all_cij):
        Cij[:, :, i] = cij
    
    print(f'There are {len(all_cij)} CIJs.')
    return Cij, all_names, state


def _no_data_error() -> Tuple[np.ndarray, List[str], str]:
    """Return default values when no data found."""
    state = 'There is NO DATA in this file.'
    print(state)
    _tips_for_warning()
    return np.zeros((6, 6, 1)), [''], state


def _no_effective_data_error() -> Tuple[np.ndarray, List[str], str]:
    """Return default values when no effective CIJ data found."""
    state = 'There is NO EFFECTIVE CIJ data in this file.'
    print(state)
    _tips_for_warning()
    return np.zeros((6, 6, 1)), [''], state


def _tips_for_warning():
    """Print format tips."""
    print('The format should be:')
    print('CIJ1Name(Optional)')
    print('CIJ1(6x6 or 3x3)')
    print('CIJ2Name(Optional)')
    print('CIJ2(The size is the same as CIJ1)')
    print('......')
    print('  ')


# ============== Data Export Functions ==============

def write_txt(Cij: np.ndarray, file_path: str, names: Optional[List[str]] = None):
    """
    Write elastic constants to text file.
    
    Parameters
    ----------
    Cij : numpy.ndarray
        Elastic stiffness matrices, shape (6, 6, n) or (3, 3, n)
    file_path : str
        Output file path
    names : list, optional
        Material names for each Cij matrix
    """
    n_rows, n_cols, n_cij = Cij.shape
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for i in range(n_cij):
            # Write name if provided
            if names and i < len(names):
                f.write(f'{names[i]}\n')
            
            # Write Cij matrix
            for row in range(n_rows):
                line = ' '.join(f'{Cij[row, col, i]:.6f}' for col in range(n_cols))
                f.write(line + '\n')
            
            f.write('\n')
    
    print(f'Written {n_cij} CIJs to {file_path}')


def write_xlsx(Cij: np.ndarray, file_path: str, names: Optional[List[str]] = None):
    """
    Write elastic constants to Excel file.
    
    Parameters
    ----------
    Cij : numpy.ndarray
        Elastic stiffness matrices, shape (6, 6, n) or (3, 3, n)
    file_path : str
        Output file path
    names : list, optional
        Material names for each Cij matrix
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas is required to write Excel files. Install with: pip install pandas openpyxl")
    
    n_rows, n_cols, n_cij = Cij.shape
    
    # Prepare data
    all_data = []
    for i in range(n_cij):
        for row in range(n_rows):
            row_data = [Cij[row, col, i] for col in range(n_cols)]
            if row == 0 and names and i < len(names):
                row_data = [names[i]] + row_data
            else:
                row_data = [''] + row_data
            all_data.append(row_data)
    
    # Create DataFrame and save
    columns = ['Name'] + [f'C{j+1}' for j in range(n_cols)]
    df = pd.DataFrame(all_data, columns=columns)
    df.to_excel(file_path, index=False)
    
    print(f'Written {n_cij} CIJs to {file_path}')


def write_mat(Cij: np.ndarray, file_path: str, names: Optional[List[str]] = None, 
              var_name: str = 'Cij'):
    """
    Write elastic constants to MATLAB .mat file.
    
    Parameters
    ----------
    Cij : numpy.ndarray
        Elastic stiffness matrices, shape (6, 6, n) or (3, 3, n)
    file_path : str
        Output file path
    names : list, optional
        Material names for each Cij matrix
    var_name : str
        Variable name in .mat file (default: 'Cij')
    """
    try:
        from scipy.io import savemat
    except ImportError:
        raise ImportError("scipy is required to write .mat files. Install with: pip install scipy")
    
    data_dict = {var_name: Cij}
    if names:
        data_dict['names'] = np.array(names, dtype=object)
    
    savemat(file_path, data_dict)
    print(f'Written {Cij.shape[2]} CIJs to {file_path}')