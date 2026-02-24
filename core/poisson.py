# Poisson's ratio calculation for Mat Model Lab

import numpy as np

def Poisson_4D(S, theta, phi, chi):
    """
    Calculate Poisson's ratio in 4D space (with additional angle chi).
    
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
        
    Returns
    -------
    numpy.ndarray
        Poisson's ratio values
    """
    # Direction cosines for the first direction
    l1 = np.sin(theta) * np.cos(phi)
    m1 = np.sin(theta) * np.sin(phi)
    n1 = np.cos(theta)
    
    # Direction cosines for the second direction
    l2 = np.cos(chi) * np.cos(theta) * np.cos(phi) - np.sin(chi) * np.sin(phi)
    m2 = np.cos(chi) * np.cos(theta) * np.sin(phi) + np.sin(chi) * np.cos(phi)
    n2 = -np.cos(chi) * np.sin(theta)
    
    # Calculate numerator and denominator for Poisson's ratio
    numerator = 0
    denominator = 0
    
    for i in range(6):
        if i == 0:
            a1i = l1 * l1
            a2i = l2 * l2
        elif i == 1:
            a1i = m1 * m1
            a2i = m2 * m2
        elif i == 2:
            a1i = n1 * n1
            a2i = n2 * n2
        elif i == 3:
            a1i = m1 * n1
            a2i = m2 * n2
        elif i == 4:
            a1i = l1 * n1
            a2i = l2 * n2
        elif i == 5:
            a1i = l1 * m1
            a2i = l2 * m2
            
        for j in range(6):
            if j == 0:
                a1j = l1 * l1
                a2j = l2 * l2
            elif j == 1:
                a1j = m1 * m1
                a2j = m2 * m2
            elif j == 2:
                a1j = n1 * n1
                a2j = n2 * n2
            elif j == 3:
                a1j = m1 * n1
                a2j = m2 * n2
            elif j == 4:
                a1j = l1 * n1
                a2j = l2 * n2
            elif j == 5:
                a1j = l1 * m1
                a2j = l2 * m2
                
            numerator += S[i, j] * a1i * a2j
            if i == j:
                denominator += S[i, j] * a1i * a1j
    
    return -numerator / denominator

def Poisson_3D(S, theta, phi):
    """
    Calculate minimum, average, and maximum Poisson's ratio in 3D space.
    
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
    tuple
        (vmin, vave, vmax) - Minimum, average, and maximum Poisson's ratio
    """
    if theta.ndim == 1:
        # Handle 1D input (e.g. for slice plotting)
        n_points = len(theta)
        n_chi = 100 # Resolution for chi rotation
        v = np.zeros((n_points, n_chi))
        
        count = 0
        for chi in np.linspace(-np.pi, np.pi, n_chi):
            v[:, count] = Poisson_4D(S, theta, phi, chi)
            count += 1
            
        vmin = np.min(v, axis=1)
        vmax = np.max(v, axis=1)
        vave = np.mean(v, axis=1)
        
        return vmin, vave, vmax

    # 2D case (Original logic)
    m, n = theta.shape
    v = np.zeros((m, n, n))
    
    count = 0
    for chi in np.linspace(-np.pi, np.pi, n):
        v[:, :, count] = Poisson_4D(S, theta, phi, chi)
        count += 1
    
    vmin = np.zeros((m, n))
    vmax = np.zeros((m, n))
    vave = np.zeros((m, n))
    
    for i in range(m):
        for j in range(n):
            vmin[i, j] = np.min(v[i, j, :])
            vmax[i, j] = np.max(v[i, j, :])
            vave[i, j] = np.mean(v[i, j, :])
    
    return vmin, vave, vmax