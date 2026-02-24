# Crystal type identification and related utilities
# Based on the symmetry of elastic stiffness matrix

import numpy as np
from typing import Dict, List, Tuple

# Crystal type definitions for 3D materials
CRYSTAL_TYPES_3D = {
    1: {'name': 'Cubic', 'independent': ['c11', 'c12', 'c44']},
    2: {'name': 'Tetragonal_1', 'independent': ['c11', 'c12', 'c13', 'c33', 'c44', 'c66']},
    3: {'name': 'Tetragonal_2', 'independent': ['c11', 'c12', 'c13', 'c16', 'c33', 'c44', 'c66']},
    4: {'name': 'Orthorhombic', 'independent': ['c11', 'c12', 'c13', 'c22', 'c23', 'c33', 'c44', 'c55', 'c66']},
    5: {'name': 'Hexagonal', 'independent': ['c11', 'c12', 'c13', 'c33', 'c44']},
    6: {'name': 'Trigonal_1', 'independent': ['c11', 'c12', 'c13', 'c14', 'c33', 'c44']},
    7: {'name': 'Trigonal_2', 'independent': ['c11', 'c12', 'c13', 'c14', 'c15', 'c33', 'c44']},
    8: {'name': 'Monoclinic_1', 'independent': ['c11', 'c12', 'c13', 'c16', 'c22', 'c23', 'c26', 'c33', 'c36', 'c44', 'c45', 'c55', 'c66']}, # Z-axis unique (Image c)
    9: {'name': 'Monoclinic_2', 'independent': ['c11', 'c12', 'c13', 'c14', 'c22', 'c23', 'c24', 'c33', 'c34', 'c44', 'c55', 'c56', 'c66']}, # X-axis unique (Image d - check C14/C56)
    10: {'name': 'Triclinic', 'independent': ['c11', 'c12', 'c13', 'c14', 'c15', 'c16', 'c22', 'c23', 'c24', 'c25', 'c26', 'c33', 'c34', 'c35', 'c36', 'c44', 'c45', 'c46', 'c55', 'c56', 'c66']}
}

# Crystal type definitions for 2D materials
CRYSTAL_TYPES_2D = {
    1: {'name': 'Hexagonal', 'independent': ['c11', 'c12']},
    2: {'name': 'Square', 'independent': ['c11', 'c12', 'c66']},
    3: {'name': 'Rectangular', 'independent': ['c11', 'c12', 'c22', 'c66']},
    4: {'name': 'Oblique', 'independent': ['c11', 'c12', 'c16', 'c22', 'c26', 'c66']}
}


def get_crystal_type_name(crystal_type: int, is_3d: bool = True) -> str:
    """
    Get the name of a crystal type by its index.
    
    Parameters
    ----------
    crystal_type : int
        Crystal type index (1-9 for 3D, 1-4 for 2D)
    is_3d : bool
        True for 3D materials, False for 2D
        
    Returns
    -------
    str
        Name of the crystal type
    """
    types = CRYSTAL_TYPES_3D if is_3d else CRYSTAL_TYPES_2D
    if crystal_type in types:
        return types[crystal_type]['name']
    return 'Unknown'


def get_independent_constants(crystal_type: int, is_3d: bool = True) -> List[str]:
    """
    Get the list of independent elastic constants for a crystal type.
    
    Parameters
    ----------
    crystal_type : int
        Crystal type index
    is_3d : bool
        True for 3D materials, False for 2D
        
    Returns
    -------
    list
        List of independent constant names (e.g., ['c11', 'c12', 'c44'])
    """
    types = CRYSTAL_TYPES_3D if is_3d else CRYSTAL_TYPES_2D
    if crystal_type in types:
        return types[crystal_type]['independent']
    return []


def get_enabled_indices(crystal_type: int, is_3d: bool = True) -> List[Tuple[int, int]]:
    """
    Get the matrix indices that should be enabled for input for a crystal type.
    
    Parameters
    ----------
    crystal_type : int
        Crystal type index
    is_3d : bool
        True for 3D materials, False for 2D
        
    Returns
    -------
    list
        List of (i, j) tuples representing matrix indices (0-indexed)
    """
    independent = get_independent_constants(crystal_type, is_3d)
    indices = []
    for const in independent:
        i = int(const[1]) - 1  # Convert from 1-indexed to 0-indexed
        j = int(const[2]) - 1
        indices.append((i, j))
    return indices


def fill_symmetric_matrix(C: np.ndarray, crystal_type: int, is_3d: bool = True) -> np.ndarray:
    """
    Fill a stiffness matrix according to crystal symmetry rules.
    
    Given the independent components, fills in the dependent components
    based on the crystal symmetry.
    
    Parameters
    ----------
    C : numpy.ndarray
        Input stiffness matrix with independent components set
    crystal_type : int
        Crystal type index
    is_3d : bool
        True for 3D materials, False for 2D
        
    Returns
    -------
    numpy.ndarray
        Complete stiffness matrix with all symmetric elements filled
    """
    C_filled = C.copy()
    
    # First, ensure matrix is symmetric (Cij = Cji)
    for i in range(C.shape[0]):
        for j in range(i + 1, C.shape[1]):
            if C_filled[i, j] != 0:
                C_filled[j, i] = C_filled[i, j]
            elif C_filled[j, i] != 0:
                C_filled[i, j] = C_filled[j, i]
    
    if is_3d:
        # Apply special symmetry rules for different crystal types
        if crystal_type == 1:  # Cubic
            # C11 = C22 = C33, C12 = C13 = C23, C44 = C55 = C66
            C_filled[1, 1] = C_filled[0, 0]  # C22 = C11
            C_filled[2, 2] = C_filled[0, 0]  # C33 = C11
            C_filled[0, 2] = C_filled[0, 1]  # C13 = C12
            C_filled[2, 0] = C_filled[0, 1]  # C31 = C12
            C_filled[1, 2] = C_filled[0, 1]  # C23 = C12
            C_filled[2, 1] = C_filled[0, 1]  # C32 = C12
            C_filled[4, 4] = C_filled[3, 3]  # C55 = C44
            C_filled[5, 5] = C_filled[3, 3]  # C66 = C44

        elif crystal_type == 2: # Tetragonal_1
            # C22=C11, C23=C13, C55=C44, C16=0
            C_filled[1, 1] = C_filled[0, 0] # C22 = C11
            C_filled[1, 2] = C_filled[0, 2] # C23 = C13
            C_filled[2, 1] = C_filled[0, 2] # C32 = C13
            C_filled[4, 4] = C_filled[3, 3] # C55 = C44
            
        elif crystal_type == 3: # Tetragonal_2
            # C22=C11, C23=C13, C55=C44, C26=-C16
            C_filled[1, 1] = C_filled[0, 0] # C22 = C11
            C_filled[1, 2] = C_filled[0, 2] # C23 = C13
            C_filled[2, 1] = C_filled[0, 2] # C32 = C13
            C_filled[4, 4] = C_filled[3, 3] # C55 = C44
            # C26 = -C16
            C_filled[1, 5] = -C_filled[0, 5] 
            C_filled[5, 1] = -C_filled[0, 5]

        elif crystal_type == 5:  # Hexagonal
            # C11 = C22, C13 = C23, C44 = C55, C66 = (C11 - C12)/2
            C_filled[1, 1] = C_filled[0, 0]  # C22 = C11
            C_filled[1, 2] = C_filled[0, 2]  # C23 = C13
            C_filled[2, 1] = C_filled[0, 2]  # C32 = C13
            C_filled[4, 4] = C_filled[3, 3]  # C55 = C44
            C_filled[5, 5] = (C_filled[0, 0] - C_filled[0, 1]) / 2  # C66 = (C11-C12)/2
            
        elif crystal_type == 6: # Trigonal_1
            # C22=C11, C24=-C14, C55=C44, C56=C14, C23=C13, C66=(C11-C12)/2
            C_filled[1, 1] = C_filled[0, 0]  # C22 = C11
            C_filled[1, 2] = C_filled[0, 2]  # C23 = C13
            C_filled[2, 1] = C_filled[0, 2]  # C32 = C13
            C_filled[4, 4] = C_filled[3, 3]  # C55 = C44
            
            # C24 = -C14
            C_filled[1, 3] = -C_filled[0, 3]
            C_filled[3, 1] = -C_filled[0, 3]
            # C56 = C14
            C_filled[4, 5] = C_filled[0, 3]
            C_filled[5, 4] = C_filled[0, 3]
            
            C_filled[5, 5] = (C_filled[0, 0] - C_filled[0, 1]) / 2  # C66 = (C11-C12)/2
        
        elif crystal_type == 7: # Trigonal_2
            # C22=C11, C24=-C14, C55=C44, C56=C14, C23=C13, C66=(C11-C12)/2
            # PLUS C25=-C15, C46=-C15
            C_filled[1, 1] = C_filled[0, 0]  # C22 = C11
            C_filled[1, 2] = C_filled[0, 2]  # C23 = C13
            C_filled[2, 1] = C_filled[0, 2]  # C32 = C13
            C_filled[4, 4] = C_filled[3, 3]  # C55 = C44
            
            # C24 = -C14
            C_filled[1, 3] = -C_filled[0, 3]
            C_filled[3, 1] = -C_filled[0, 3]
            # C56 = C14
            C_filled[4, 5] = C_filled[0, 3]
            C_filled[5, 4] = C_filled[0, 3]
            
            # C25 = -C15
            C_filled[1, 4] = -C_filled[0, 4]
            C_filled[4, 1] = -C_filled[0, 4]
            # C46 = -C15
            C_filled[3, 5] = -C_filled[0, 4]
            C_filled[5, 3] = -C_filled[0, 4]
            
            C_filled[5, 5] = (C_filled[0, 0] - C_filled[0, 1]) / 2  # C66 = (C11-C12)/2
    else:
        # 2D symmetry rules
        if crystal_type == 1:  # Hexagonal 2D
            # C22 = C11, C66 = (C11 - C12) / 2
            C_filled[1, 1] = C_filled[0, 0]
            C_filled[5, 5] = (C_filled[0, 0] - C_filled[0, 1]) / 2
        elif crystal_type == 2:  # Square 2D
            # C22 = C11 (C12, C66 independent)
            C_filled[1, 1] = C_filled[0, 0]
    
    return C_filled


def identify_crystal_type(C: np.ndarray, tolerance: float = 1e-6) -> Tuple[int, str]:
    """
    Attempt to identify the crystal type from a stiffness matrix.
    
    Parameters
    ----------
    C : numpy.ndarray
        6x6 stiffness matrix
    tolerance : float
        Tolerance for comparing values to zero
        
    Returns
    -------
    tuple
        (crystal_type_index, crystal_type_name)
    """
    # Check if it's a 3D or 2D matrix
    if C.shape != (6, 6):
        return 0, 'Unknown (not 6x6)'
    
    # Count non-zero elements (above tolerance)
    def is_zero(x):
        return np.abs(x) < tolerance
    
    # Check for cubic symmetry
    # Priority list based on "Degree of Symmetry" (fewest independent constants first)
    # Cubic(3) -> Hexagonal(5) -> Tetragonal_1(6) -> Trigonal_1(6) -> Tetragonal_2(7) 
    # -> Trigonal_2(7) -> Orthorhombic(9) -> Monoclinic_1(13) -> Monoclinic_2(13) -> Triclinic(21)
    
    # Sort types by number of independent constants
    sorted_types = sorted(CRYSTAL_TYPES_3D.items(), key=lambda x: len(x[1]['independent']))
    
    for type_id, type_info in sorted_types:
        # 1. Extract only the independent constants from the input matrix
        # and create a sparse test matrix (zeros elsewhere)
        C_test = np.zeros((6, 6))
        independent_vars = type_info['independent']
        
        for const_name in independent_vars:
            i = int(const_name[1]) - 1
            j = int(const_name[2]) - 1
            val = C[i, j]
            C_test[i, j] = val
            C_test[j, i] = val
            
        # 2. Reconstruct the ideal full symmetric matrix for this type
        C_ideal = fill_symmetric_matrix(C_test, type_id, is_3d=True)
        
        # 3. Compare with original input
        # If the input matrix matches the ideal reconstruction, it belongs to this type
        # Since we check from most restrictive to least restrictive, the first match is the best fit.
        if np.allclose(C, C_ideal, atol=tolerance, rtol=tolerance):
            return type_id, type_info['name']
            
    # Fallback (should be covered by Triclinic)
    return 10, 'Triclinic'


def list_crystal_types(is_3d: bool = True) -> Dict[int, str]:
    """
    Get a dictionary of all crystal types.
    
    Parameters
    ----------
    is_3d : bool
        True for 3D materials, False for 2D
        
    Returns
    -------
    dict
        Dictionary mapping crystal type index to name
    """
    types = CRYSTAL_TYPES_3D if is_3d else CRYSTAL_TYPES_2D
    return {k: v['name'] for k, v in types.items()}
