# Mechanical stability criteria for elastic constants
# Based on Born stability criteria

import numpy as np


def StableofMechanical(C: np.ndarray) -> bool:
    """
    Check the mechanical stability of an elastic stiffness matrix.
    
    The stability is determined using the Born stability criteria:
    all eigenvalues of the stiffness matrix must be positive.
    
    Parameters
    ----------
    C : numpy.ndarray
        Elastic stiffness matrix (6x6 for 3D, 3x3 for 2D)
        
    Returns
    -------
    bool
        True if the structure is mechanically stable, False otherwise
        
    Examples
    --------
    >>> import numpy as np
    >>> C = np.array([[269, 161, 161, 0, 0, 0],
    ...               [161, 269, 161, 0, 0, 0],
    ...               [161, 161, 269, 0, 0, 0],
    ...               [0, 0, 0, 82, 0, 0],
    ...               [0, 0, 0, 0, 82, 0],
    ...               [0, 0, 0, 0, 0, 82]])
    >>> StableofMechanical(C)
    True
    """
    m, n = C.shape
    
    # Check if matrix is square
    if m != n:
        print('This is not an effective CIJ, the row and column of CIJ must be EQUAL.')
        return False
    
    # Handle 6x6 matrix - check if it's actually a 2D material embedded in 3D
    if n == 6:
        C_tmp = C[2:5, 2:5]  # C33, C34, C35, C43, C44, C45, C53, C54, C55
        if np.allclose(C_tmp, 0):
            # This is a 2D material, extract relevant components
            indices = [0, 1, 5]  # C11, C12, C16, C21, C22, C26, C61, C62, C66
            C = C[np.ix_(indices, indices)]
    elif n != 3:
        print('This is not an effective CIJ, the row and column must be 3 or 6')
        return False
    
    # Calculate eigenvalues
    eigenvalues = np.linalg.eigvals(C)
    
    # Check if all eigenvalues are positive (use real part for numerical stability)
    if np.all(np.real(eigenvalues) > 0):
        return True
    else:
        return False


def check_stability_detailed(C: np.ndarray, is_2d: bool = False) -> dict:
    """
    Perform detailed stability analysis of elastic stiffness matrix.
    
    Parameters
    ----------
    C : numpy.ndarray
        Elastic stiffness matrix (6x6)
    is_2d : bool, optional
        Whether the material is 2D (default False)
        
    Returns
    -------
    dict
        Dictionary containing:
        - 'stable': bool, overall stability
        - 'eigenvalues': array, eigenvalues of the matrix
        - 'min_eigenvalue': float, minimum eigenvalue
        - 'message': str, descriptive message
    """
    result = {
        'stable': False,
        'eigenvalues': None,
        'min_eigenvalue': None,
        'message': ''
    }
    
    m, n = C.shape
    
    if m != n:
        result['message'] = 'Matrix is not square'
        return result
    
    if n != 6 and n != 3:
        result['message'] = 'Matrix must be 3x3 or 6x6'
        return result

    # Check for 2D case
    if is_2d:
        # For 2D stability, we check the relevant submatrix [11, 22, 12, 66]
        # Indices 0, 1, 5
        indices = [0, 1, 5]
        C_2d = C[np.ix_(indices, indices)]
        
        eigenvalues = np.linalg.eigvals(C_2d)
        eigenvalues_real = np.real(eigenvalues)
        
        result['eigenvalues'] = eigenvalues_real
        result['min_eigenvalue'] = np.min(eigenvalues_real)
        
        # Born stability conditions for 2D: All eigenvalues > 0
        if np.all(eigenvalues_real > 0):
            result['stable'] = True
            result['message'] = 'Structure is mechanically STABLE (2D)'
        else:
            result['stable'] = False
            negative_count = np.sum(eigenvalues_real <= 0)
            result['message'] = f'Structure is UNSTABLE (2D) ({negative_count} non-positive eigenvalue(s))'
            
        return result
    
    # 3D case
    eigenvalues = np.linalg.eigvals(C)
    eigenvalues_real = np.real(eigenvalues)
    
    result['eigenvalues'] = eigenvalues_real
    result['min_eigenvalue'] = np.min(eigenvalues_real)
    
    if np.all(eigenvalues_real > 0):
        result['stable'] = True
        result['message'] = 'Structure is mechanically STABLE'
    else:
        result['stable'] = False
        negative_count = np.sum(eigenvalues_real <= 0)
        result['message'] = f'Structure is UNSTABLE ({negative_count} non-positive eigenvalue(s))'
    
    return result
