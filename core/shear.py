# Shear modulus calculation for Mat Model Lab

import numpy as np

def Shear_4D(S, theta, phi, chi):
    """
    Calculate Shear modulus in 4D space (with additional angle chi).
    
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
        Shear modulus values
    """
    # Direction cosines for the first direction (n)
    n1 = np.sin(theta) * np.cos(phi)
    n2 = np.sin(theta) * np.sin(phi)
    n3 = np.cos(theta)
    
    # Direction cosines for the second direction (m)
    m1 = np.cos(chi) * np.cos(theta) * np.cos(phi) - np.sin(chi) * np.sin(phi)
    m2 = np.cos(chi) * np.cos(theta) * np.sin(phi) + np.sin(chi) * np.cos(phi)
    m3 = -np.cos(chi) * np.sin(theta)
    
    # Convert Voigt S (6x6) to Tensor S (3x3x3x3)
    # This ensures all factors of 2 and 4 are handled correctly
    # Only do this once (or it's fast enough)
    S_tensor = np.zeros((3, 3, 3, 3))
    
    # Mapping from Voigt (0-5) to Tensor pair indices (0-2, 0-2)
    voigt_map = {
        0: (0, 0), 1: (1, 1), 2: (2, 2),
        3: (1, 2), 4: (0, 2), 5: (0, 1)
    }
    
    for i in range(6):
        for j in range(6):
            # Get tensor indices types
            u, v = voigt_map[i]
            x, y = voigt_map[j]
            
            # Determine factor to divide S_voigt by to get S_tensor
            # Compliance S_voigt factors: 
            # 1 index > 2 implies factor 2 (shear term)
            # 2 indices > 2 implies factor 4 (shear-shear term)
            # Actually simplest rule: S_tensor = S_voigt / factor
            # factor = 1 * (2 if i>=3 else 1) * (2 if j>=3 else 1)
            factor = (2 if i >= 3 else 1) * (2 if j >= 3 else 1)
            val = S[i, j] / factor
            
            # Assign to all permutations of indices
            # Tensor S is symmetric in ij and kl, and symmetric under swap of (ij) and (kl)
            # We must assign to u,v,x,y and v,u,x,y etc.
            
            # Indices permutations for first pair (i)
            perms_i = [(u, v)]
            if u != v: perms_i.append((v, u))
                
            # Indices permutations for second pair (j)
            perms_j = [(x, y)]
            if x != y: perms_j.append((y, x))
            
            for p1 in perms_i:
                for p2 in perms_j:
                    S_tensor[p1[0], p1[1], p2[0], p2[1]] = val

    # Calculate 1/G = 4 * S_ijkl * n_i * m_j * n_k * m_l
    # Vectorized calculation
    if np.ndim(theta) > 0:
        n_vec = np.stack([n1, n2, n3], axis=0) # 3 x N
        m_vec = np.stack([m1, m2, m3], axis=0) # 3 x N
        
        # We need to broadcast S_tensor (3,3,3,3) against N points
        # Or use einsum: ijkl, pi, pj, pk, pl -> p (where p is point index)
        # Using loop over i,j,k,l is actually cleaner for readability and numpy speed for large N
        
        inv_G = np.zeros_like(theta)
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        if S_tensor[i, j, k, l] != 0:
                            inv_G += S_tensor[i, j, k, l] * n_vec[i] * m_vec[j] * n_vec[k] * m_vec[l]
        
        return 1.0 / (4.0 * inv_G)
    else:
        # Scalar case
        n_vec = np.array([n1, n2, n3])
        m_vec = np.array([m1, m2, m3])
        inv_G = 0.0
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        inv_G += S_tensor[i, j, k, l] * n_vec[i] * m_vec[j] * n_vec[k] * m_vec[l]
        return 1.0 / (4.0 * inv_G)

def Shear_3D(S, theta, phi):
    """
    Calculate minimum, average, and maximum Shear modulus in 3D space.
    
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
        (Gmin, Gave, Gmax) - Minimum, average, and maximum Shear modulus
    """
    if theta.ndim == 1:
        # Handle 1D input
        n_points = len(theta)
        n_chi = 100
        G = np.zeros((n_points, n_chi))
        
        count = 0
        for chi in np.linspace(-np.pi, np.pi, n_chi):
            G[:, count] = Shear_4D(S, theta, phi, chi)
            count += 1
            
        Gmin = np.min(G, axis=1)
        Gmax = np.max(G, axis=1)
        Gave = np.mean(G, axis=1)
        
        return Gmin, Gave, Gmax

    # 2D case
    m, n = theta.shape
    G = np.zeros((m, n, n))
    
    count = 0
    for chi in np.linspace(-np.pi, np.pi, n):
        G[:, :, count] = Shear_4D(S, theta, phi, chi)
        count += 1
    
    Gmin = np.zeros((m, n))
    Gmax = np.zeros((m, n))
    Gave = np.zeros((m, n))
    
    for i in range(m):
        for j in range(n):
            Gmin[i, j] = np.min(G[i, j, :])
            Gmax[i, j] = np.max(G[i, j, :])
            Gave[i, j] = np.mean(G[i, j, :])
    
    return Gmin, Gave, Gmax