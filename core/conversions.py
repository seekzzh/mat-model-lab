# Coordinate and dimension conversions for elastic constants
# Includes 2D/3D matrix conversions and angle/direction conversions

import numpy as np
from typing import Tuple


def D2toD3(Cij3: np.ndarray) -> np.ndarray:
    """
    Convert 2D elastic stiffness matrix to 3D representation.
    
    The 2D stiffness matrix (3x3) contains C11, C12, C16, C21, C22, C26, C61, C62, C66.
    This is embedded into a 6x6 matrix at positions [0,1,5] x [0,1,5].
    
    Parameters
    ----------
    Cij3 : numpy.ndarray
        2D stiffness matrix (3x3) or stacked matrices (m*3, 3)
        
    Returns
    -------
    numpy.ndarray
        6x6 stiffness matrix (or m*6, 6 for stacked input)
        
    Examples
    --------
    >>> Cij2D = np.array([[100, 50, 0],
    ...                   [50, 100, 0],
    ...                   [0, 0, 25]])
    >>> Cij3D = D2toD3(Cij2D)
    >>> Cij3D.shape
    (6, 6)
    """
    m, n = Cij3.shape
    
    if n != 3:
        raise ValueError("Input matrix must have 3 columns for 2D stiffness")
    
    num_matrices = m // 3
    Cij6 = np.zeros((num_matrices * 6, 6))
    
    # Mapping: 2D indices [0,1,2] -> 3D indices [0,1,5] (C11,C22,C66 positions)
    indices = [0, 1, 5]
    
    for i in range(num_matrices):
        # Extract 3x3 slice
        slice_2d = Cij3[i*3:(i+1)*3, :]
        # Insert into corresponding 6x6 positions
        for row_2d, row_3d in enumerate(indices):
            for col_2d, col_3d in enumerate(indices):
                Cij6[i*6 + row_3d, col_3d] = slice_2d[row_2d, col_2d]
    
    # If single matrix, return just 6x6
    if num_matrices == 1:
        return Cij6[:6, :]
    
    return Cij6


def D3toD2(Cij6: np.ndarray) -> np.ndarray:
    """
    Convert 3D elastic stiffness matrix to 2D representation.
    
    Extracts the 2D components (C11, C12, C16, C21, C22, C26, C61, C62, C66)
    from a 6x6 stiffness matrix.
    
    Parameters
    ----------
    Cij6 : numpy.ndarray
        6x6 stiffness matrix
        
    Returns
    -------
    numpy.ndarray
        3x3 stiffness matrix for 2D material
        
    Examples
    --------
    >>> Cij3D = np.eye(6) * 100
    >>> Cij2D = D3toD2(Cij3D)
    >>> Cij2D.shape
    (3, 3)
    """
    if Cij6.shape[0] != 6 or Cij6.shape[1] != 6:
        raise ValueError("Input matrix must be 6x6")
    
    # Extract positions [0,1,5] x [0,1,5]
    indices = [0, 1, 5]
    return Cij6[np.ix_(indices, indices)]


def Direction2Ang(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Convert Cartesian direction vectors to spherical angles (theta, phi).
    
    Parameters
    ----------
    x : numpy.ndarray
        X component of direction vector(s)
    y : numpy.ndarray
        Y component of direction vector(s)
    z : numpy.ndarray
        Z component of direction vector(s)
        
    Returns
    -------
    theta : numpy.ndarray
        Polar angle (angle from z-axis) in radians [0, pi]
    phi : numpy.ndarray
        Azimuthal angle (angle in xy-plane from x-axis) in radians [0, 2*pi]
        
    Notes
    -----
    The spherical coordinates follow physics convention:
    - theta: angle from positive z-axis
    - phi: angle from positive x-axis in xy-plane
    """
    # Ensure numpy arrays
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)
    
    # Calculate radius
    r = np.sqrt(x**2 + y**2 + z**2)
    
    # Handle zero radius
    r = np.where(r == 0, 1e-10, r)
    
    # Polar angle theta (angle from z-axis)
    theta = np.arccos(z / r)
    
    # Azimuthal angle phi (angle in xy-plane)
    rxy = np.sqrt(x**2 + y**2)
    
    # Initialize phi
    phi = np.zeros_like(x, dtype=float)
    
    # Where rxy is not zero, calculate phi
    mask = rxy > 1e-10
    phi = np.where(mask, np.arccos(np.clip(x / np.where(mask, rxy, 1), -1, 1)), 0)
    
    # Adjust for y < 0 (phi should be in [pi, 2*pi])
    phi = np.where(y < 0, 2*np.pi - phi, phi)
    
    # Handle origin case
    phi = np.where((np.abs(x) < 1e-10) & (np.abs(y) < 1e-10), 0, phi)
    
    return theta, phi


def Ang2Direction(theta: np.ndarray, phi: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert spherical angles to Cartesian unit direction vectors.
    
    Parameters
    ----------
    theta : numpy.ndarray
        Polar angle (angle from z-axis) in radians
    phi : numpy.ndarray
        Azimuthal angle (angle in xy-plane from x-axis) in radians
        
    Returns
    -------
    x, y, z : numpy.ndarray
        Components of the unit direction vector
        
    Examples
    --------
    >>> import numpy as np
    >>> theta = np.array([0, np.pi/2, np.pi])
    >>> phi = np.array([0, 0, 0])
    >>> x, y, z = Ang2Direction(theta, phi)
    >>> print(z)  # Should be [1, 0, -1]
    [ 1.  0. -1.]
    """
    theta = np.asarray(theta)
    phi = np.asarray(phi)
    
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    
    return x, y, z


def rotate_stiffness_matrix(C: np.ndarray, R: np.ndarray) -> np.ndarray:
    """
    Rotate a stiffness matrix by a rotation matrix.
    
    C' = M * C * M^T, where M is the 6x6 transformation matrix
    derived from the 3x3 rotation matrix R.
    
    Parameters
    ----------
    C : numpy.ndarray
        6x6 stiffness matrix
    R : numpy.ndarray
        3x3 rotation matrix
        
    Returns
    -------
    numpy.ndarray
        Rotated 6x6 stiffness matrix
    """
    if C.shape != (6, 6):
        raise ValueError("Stiffness matrix must be 6x6")
    if R.shape != (3, 3):
        raise ValueError("Rotation matrix must be 3x3")
    
    # Build the 6x6 transformation matrix M from R
    # Using Bond transformation matrix
    M = np.zeros((6, 6))
    
    # Diagonal block (normal stresses)
    for i in range(3):
        for j in range(3):
            M[i, j] = R[i, j]**2
    
    # Off-diagonal blocks (shear stresses)
    M[0, 3] = 2 * R[0, 1] * R[0, 2]
    M[0, 4] = 2 * R[0, 0] * R[0, 2]
    M[0, 5] = 2 * R[0, 0] * R[0, 1]
    M[1, 3] = 2 * R[1, 1] * R[1, 2]
    M[1, 4] = 2 * R[1, 0] * R[1, 2]
    M[1, 5] = 2 * R[1, 0] * R[1, 1]
    M[2, 3] = 2 * R[2, 1] * R[2, 2]
    M[2, 4] = 2 * R[2, 0] * R[2, 2]
    M[2, 5] = 2 * R[2, 0] * R[2, 1]
    
    M[3, 0] = R[1, 0] * R[2, 0]
    M[3, 1] = R[1, 1] * R[2, 1]
    M[3, 2] = R[1, 2] * R[2, 2]
    M[3, 3] = R[1, 1] * R[2, 2] + R[1, 2] * R[2, 1]
    M[3, 4] = R[1, 0] * R[2, 2] + R[1, 2] * R[2, 0]
    M[3, 5] = R[1, 0] * R[2, 1] + R[1, 1] * R[2, 0]
    
    M[4, 0] = R[0, 0] * R[2, 0]
    M[4, 1] = R[0, 1] * R[2, 1]
    M[4, 2] = R[0, 2] * R[2, 2]
    M[4, 3] = R[0, 1] * R[2, 2] + R[0, 2] * R[2, 1]
    M[4, 4] = R[0, 0] * R[2, 2] + R[0, 2] * R[2, 0]
    M[4, 5] = R[0, 0] * R[2, 1] + R[0, 1] * R[2, 0]
    
    M[5, 0] = R[0, 0] * R[1, 0]
    M[5, 1] = R[0, 1] * R[1, 1]
    M[5, 2] = R[0, 2] * R[1, 2]
    M[5, 3] = R[0, 1] * R[1, 2] + R[0, 2] * R[1, 1]
    M[5, 4] = R[0, 0] * R[1, 2] + R[0, 2] * R[1, 0]
    M[5, 5] = R[0, 0] * R[1, 1] + R[0, 1] * R[1, 0]
    
    return M @ C @ M.T
