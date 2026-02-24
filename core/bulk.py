# Bulk modulus calculation for Mat Model Lab

import numpy as np

def Bulk_3D(S, theta, phi):
    """
    Calculate Bulk modulus in 3D space.
    
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
        Bulk modulus values
    """
    ax = np.sin(theta) * np.cos(phi)
    ay = np.sin(theta) * np.sin(phi)
    az = np.cos(theta)
    
    B = np.zeros_like(ax)
    
    for i in range(6):
        for j in range(3):
            if i == 0:
                Btmp = S[i, j] * ax * ax
            elif i == 1:
                Btmp = S[i, j] * ay * ay
            elif i == 2:
                Btmp = S[i, j] * az * az
            elif i == 3:
                Btmp = S[i, j] * ay * az
            elif i == 4:
                Btmp = S[i, j] * ax * az
            elif i == 5:
                Btmp = S[i, j] * ax * ay
                
            B = B + Btmp
    
    return 1.0 / (3.0 * B)