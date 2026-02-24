# Hardness calculation for Mat Model Lab

import numpy as np
from .young import Young_3D
from .shear import Shear_3D

def Hardness_3D(S, theta, phi):
    """
    Calculate Hardness in 3D space.
    
    Parameters
    ----------
    S : numpy.ndarray
        Compliance matrix (6x6)
    theta : numpy.ndarray
        Polar angle in radians
    phi : numpy.ndarray
        Azimuthal angle in radians
        
    Returns
    -------
    numpy.ndarray
        Hardness values
    """
    E = Young_3D(S, theta, phi)
    _, G, _ = Shear_3D(S, theta, phi)
    
    # Calculate hardness using Chen's model
    # H = 2 * (k²G)^0.585 - 3 where k = G/E
    k = G / E
    k2G = k**2 * G
    
    # Handle negative values to avoid NaN (use absolute value for power, then restore sign)
    # For physical materials, k²G should be positive, but numerical issues can cause problems
    k2G_safe = np.maximum(k2G, 1e-10)  # Avoid negative and zero values
    H = 2 * (k2G_safe)**0.585 - 3
    
    # Replace any remaining invalid values with 0
    H = np.nan_to_num(H, nan=0.0, posinf=0.0, neginf=0.0)
    
    return H

def Hardness_4D(S, theta, phi, chi):
    """
    Calculate Hardness in 4D space (with additional angle chi).
    
    .. note::
        This function is not yet implemented. Contributions are welcome.
    
    Parameters
    ----------
    S : numpy.ndarray
        Compliance matrix (6x6)
    theta : numpy.ndarray
        Polar angle in radians
    phi : numpy.ndarray
        Azimuthal angle in radians
    chi : float or numpy.ndarray
        Additional angle in radians
        
    Raises
    ------
    NotImplementedError
        This function is planned for future implementation.
    """
    raise NotImplementedError(
        "Hardness_4D is not yet implemented. "
        "See https://github.com/seekzzh/mat-model-lab/issues for updates."
    )