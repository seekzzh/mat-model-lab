# Coordinate conversion functions for Mat Model Lab

import numpy as np

def Ang2Direction(theta, phi):
    """
    Convert angles to direction cosines.
    
    Parameters
    ----------
    theta : float or numpy.ndarray
        Polar angle in radians
    phi : float or numpy.ndarray
        Azimuthal angle in radians
        
    Returns
    -------
    numpy.ndarray
        Direction cosines [x, y, z]
    """
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    
    return np.array([x, y, z])

def Direction2Ang(direction):
    """
    Convert direction cosines to angles.
    
    Parameters
    ----------
    direction : numpy.ndarray
        Direction cosines [x, y, z]
        
    Returns
    -------
    tuple
        (theta, phi) - Polar and azimuthal angles in radians
    """
    x, y, z = direction
    r = np.sqrt(x**2 + y**2 + z**2)
    
    # Normalize if not already normalized
    if not np.isclose(r, 1.0):
        x, y, z = x/r, y/r, z/r
    
    theta = np.arccos(z)
    phi = np.arctan2(y, x)
    
    return theta, phi