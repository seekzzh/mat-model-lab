
import numpy as np
from typing import Dict

def ElasticVRH2D(C: np.ndarray) -> Dict[str, float]:
    """
    Calculate 2D elastic properties using Voigt-Reuss-Hill approximation.
    
    Parameters
    ----------
    C : numpy.ndarray
        Elastic stiffness matrix (6x6). 
        For 2D, we expect non-zeros at indices [0,1,5] corresponding to 11, 12, 22, 66.
        Or for generalized 2D, relevant indices are 0,1,5.
        
    Returns
    -------
    dict
        Dictionary containing calculated properties (E, G, v, B, etc.)
    """
    # Extract relevant 2D stiffness components
    # Indices: 0->11, 1->22, 5->66 (in 0-based 6x6)
    # Actually for 2D, we usually consider plane stress conditions.
    # The relevant submatrix for in-plane behavior is indices 0, 1, 5 (11, 22, 12, 66).
    
    # 2D VRH is significantly simpler or different.
    # Voigt bounds for 2D isotropic aggregate:
    # 2D Bulk Modulus K_V and Shear Modulus G_V
    
    c11 = C[0, 0]
    c22 = C[1, 1]
    c12 = C[0, 1]
    c66 = C[5, 5]
    
    # Voigt upper bounds (2D)
    # Formulas from literature for 2D polycrystals (e.g., graphene)
    # K_V = (C11 + C22 + 2*C12) / 4
    # G_V = (C11 + C22 - 2*C12 + 4*C66) / 8
    
    K_V = (c11 + c22 + 2 * c12) / 4.0
    G_V = (c11 + c22 - 2 * c12 + 4 * c66) / 8.0
    
    # Reuss lower bounds (2D)
    # Invert the planar stiffness submatrix to get compliance
    
    # Construct 3x3 planar stiffness matrix from indices [0, 1, 5]
    C_planar = np.zeros((3, 3))
    C_planar[0, 0] = C[0, 0] # 11
    C_planar[0, 1] = C[0, 1] # 12
    C_planar[0, 2] = C[0, 5] # 16
    
    C_planar[1, 0] = C[1, 0] # 21
    C_planar[1, 1] = C[1, 1] # 22
    C_planar[1, 2] = C[1, 5] # 26
    
    C_planar[2, 0] = C[5, 0] # 61
    C_planar[2, 1] = C[5, 1] # 62
    C_planar[2, 2] = C[5, 5] # 66
    
    try:
        S_planar = np.linalg.inv(C_planar)
    except np.linalg.LinAlgError:
        S_planar = np.zeros((3, 3))
        
    s11 = S_planar[0, 0]
    s22 = S_planar[1, 1]
    s12 = S_planar[0, 1]
    s66 = S_planar[2, 2]
    
    # 2D Reuss bounds:
    # K_R = 1 / (s11 + s22 + 2*s12)
    # G_R = 2 / (s11 + s22 - 2*s12 + s66)
    # These formulas reduce to the isotropic case: G = 1/s66 when s66 = 2(s11-s12).
    K_R = 1.0 / (s11 + s22 + 2 * s12) if (s11 + s22 + 2 * s12) != 0 else 0
    
    G_R = 2.0 / (s11 + s22 - 2 * s12 + s66)
    
    K_VRH = (K_V + K_R) / 2.0
    G_VRH = (G_V + G_R) / 2.0
    
    # Engineering constants from Hill average
    # For 2D Isotropic:
    # E = 2G(1+v) = 3K(1-v) ? No, 2D relations are different.
    # In 2D: E = 4KG / (K+G)
    # v = (K-G) / (K+G)
    
    E_iso = 4.0 * K_VRH * G_VRH / (K_VRH + G_VRH) if (K_VRH + G_VRH) != 0 else 0
    v_iso = (K_VRH - G_VRH) / (K_VRH + G_VRH) if (K_VRH + G_VRH) != 0 else 0
    
    # Hardness (Chen-Niu still useful?) - Maybe scaling differently.
    # Let's just calculate it generally but note it might be approximate.
    # H = (1 - 2*v_iso) * E_iso / (6 * (1 + v_iso)) ? 3D formula.
    # We'll omit H or just use same formula for consistency but hide it in UI usually.
    # But this function returns dict, let's include it.
    H_iso = 0.0 # Placeholder
    
    # Anisotropy
    # A_U = 5 G_V / G_R + K_V / K_R - 6 (3D).
    # 2D Anisotropy?
    # Let's use Universal Anisotropy Index definition: A_U = K_V/K_R + G_V/G_R - 2 (for 2D?)
    # Since K_V=K_R and G_V=G_R for isotropy -> 1+1-2=0. Correct.
    A_U = (K_V / K_R) + (G_V / G_R) - 2.0 if (K_R != 0 and G_R != 0) else 0
    
    return {
        'K_V': K_V, 'K_R': K_R, 'K_VRH': K_VRH,
        'G_V': G_V, 'G_R': G_R, 'G_VRH': G_VRH,
        'E': E_iso,
        'v': v_iso,
        'H': H_iso,
        'A': A_U,
        'k_G': K_VRH / G_VRH if G_VRH != 0 else 0
    }
