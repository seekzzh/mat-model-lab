# VRH average elastic constants calculation for Mat Model Lab

import numpy as np

def ElasticVRH3D(C):
    """
    Calculate Voigt-Reuss-Hill average elastic constants for 3D materials.
    
    Parameters
    ----------
    C : numpy.ndarray
        Stiffness matrix (6x6)
        
    Returns
    -------
    dict
        Dictionary containing various elastic properties:
        - K_V: Voigt average bulk modulus
        - K_R: Reuss average bulk modulus
        - K_VRH: Voigt-Reuss-Hill average bulk modulus
        - G_V: Voigt average shear modulus
        - G_R: Reuss average shear modulus
        - G_VRH: Voigt-Reuss-Hill average shear modulus
        - E: Young's modulus
        - v: Poisson's ratio
        - A: Anisotropy index
    """
    # Voigt average
    K_V = (C[0, 0] + C[1, 1] + C[2, 2] + 2 * (C[0, 1] + C[0, 2] + C[1, 2])) / 9
    G_V = (C[0, 0] + C[1, 1] + C[2, 2] - (C[0, 1] + C[0, 2] + C[1, 2]) + 3 * (C[3, 3] + C[4, 4] + C[5, 5])) / 15
    
    # Reuss average
    S = np.linalg.inv(C)
    K_R = 1 / (S[0, 0] + S[1, 1] + S[2, 2] + 2 * (S[0, 1] + S[0, 2] + S[1, 2]))
    G_R = 15 / (4 * (S[0, 0] + S[1, 1] + S[2, 2]) - 4 * (S[0, 1] + S[0, 2] + S[1, 2]) + 3 * (S[3, 3] + S[4, 4] + S[5, 5]))
    
    # Hill average
    K_VRH = (K_V + K_R) / 2
    G_VRH = (G_V + G_R) / 2
    
    # Young's modulus and Poisson's ratio
    E = 9 * K_VRH * G_VRH / (3 * K_VRH + G_VRH)
    v = (3 * K_VRH - 2 * G_VRH) / (6 * K_VRH + 2 * G_VRH)
    
    # Universal anisotropy index
    A = 5 * G_V / G_R + K_V / K_R - 6
    
    # Cauchy pressure
    P_C = C[0, 1] - C[3, 3]
    
    # Pugh's ratio
    k_G = K_VRH / G_VRH
    
    # Hardness (Chen's model)
    H = 2 * (G_VRH**2 / K_VRH)**0.585 - 3
    
    # Return results as a dictionary
    results = {
        'K_V': K_V,
        'K_R': K_R,
        'K_VRH': K_VRH,
        'G_V': G_V,
        'G_R': G_R,
        'G_VRH': G_VRH,
        'E': E,
        'v': v,
        'A': A,
        'P_C': P_C,
        'k_G': k_G,
        'H': H
    }
    
    return results