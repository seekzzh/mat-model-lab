# Young's modulus calculation for Mat Model Lab

import numpy as np

def Young_3D(S, theta, phi):
    """
    Calculate Young's modulus in 3D space.
    
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
        Young's modulus values
    """
    ax = np.sin(theta) * np.cos(phi)
    ay = np.sin(theta) * np.sin(phi)
    az = np.cos(theta)
    
    E = np.zeros_like(ax)
    
    for i in range(6):
        if i == 0:
            Etmpi = ax * ax
        elif i == 1:
            Etmpi = ay * ay
        elif i == 2:
            Etmpi = az * az
        elif i == 3:
            Etmpi = ay * az
        elif i == 4:
            Etmpi = ax * az
        elif i == 5:
            Etmpi = ax * ay
            
        for j in range(6):
            if j == 0:
                Etmpij = S[i, j] * Etmpi * ax * ax
            elif j == 1:
                Etmpij = S[i, j] * Etmpi * ay * ay
            elif j == 2:
                Etmpij = S[i, j] * Etmpi * az * az
            elif j == 3:
                Etmpij = S[i, j] * Etmpi * ay * az
            elif j == 4:
                Etmpij = S[i, j] * Etmpi * ax * az
            elif j == 5:
                Etmpij = S[i, j] * Etmpi * ax * ay
                
            E = E + Etmpij
    
    return 1.0 / E