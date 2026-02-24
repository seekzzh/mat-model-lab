# 2D plotting functions for Mat Model Lab

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Fix import path issues, allowing the script to run directly or be imported as a module
try:
    # Use this path when imported as a module
    from ..core.young import Young_3D
    from ..core.bulk import Bulk_3D
    from ..core.poisson import Poisson_3D
    from ..core.shear import Shear_3D
    from ..core.hardness import Hardness_3D
    from .plot_utils import ElasticPlot_2D_plane, plot_circle
except ImportError:
    # Use this path when running the script directly
    import sys
    import os
    # Add the project root directory to the Python path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from core.young import Young_3D
    from core.bulk import Bulk_3D
    from core.poisson import Poisson_3D
    from core.shear import Shear_3D
    from core.hardness import Hardness_3D
    from visualization.plot_utils import ElasticPlot_2D_plane, plot_circle

def ElasticPlot_2D(S, n, flag, flag_plane, flag_save=False, Name=''):
    """
    Plot 2D elastic properties in specified planes.
    
    Parameters
    ----------
    S : numpy.ndarray
        Compliance matrix (6x6)
    n : int
        Number of points for plotting
    flag : list
        List of properties to plot ('B', 'E', 'G', 'v', 'H')
    flag_plane : list
        List of planes to plot ('xy', 'xz', 'yz', 'all')
    flag_save : bool, optional
        Whether to save the plots
    Name : str, optional
        Base name for saved files
    """
    for flagi in flag:
        plt.figure(figsize=(10, 8))
        ElasticPlot_2D_flag(S, n, flagi, flag_plane)
        plt.axis('equal')
        plt.axis('off')
        
        if flag_save:
            savename = f"{Name}-{flagi}-2D.jpg"
            plt.savefig(savename, dpi=300)

def ElasticPlot_2DM(S, n, flag, flag_save=False, Name=''):
    """
    Plot 2D elastic properties for 2D materials.
    
    Parameters
    ----------
    S : numpy.ndarray
        Compliance matrix (3x3 for 2D materials)
    n : int
        Number of points for plotting
    flag : list
        List of properties to plot ('E', 'G', 'v')
    flag_save : bool, optional
        Whether to save the plots
    Name : str, optional
        Base name for saved files
    """
    # Convert 3x3 to 6x6 if needed
    if S.shape[0] == 3 and S.shape[1] == 3:
        # This would require a D2toD3 function implementation
        # For now, we'll assume S is already in the correct format
        pass
    
    for flagi in flag:
        plt.figure(figsize=(10, 8))
        ElasticPlot_2DM_flag(S, n, flagi)
        plt.axis('equal')
        plt.axis('off')
        
        if flag_save:
            savename = f"{Name}-{flagi}-2D.jpg"
            plt.savefig(savename, dpi=300)

def ElasticPlot_2DM_flag(S, n, flag_type):
    """
    Plot a specific elastic property for 2D materials.
    
    Parameters
    ----------
    S : numpy.ndarray
        Compliance matrix
    n : int
        Number of points for plotting
    flag_type : str
        Property to plot ('E', 'G', 'v')
    """
    phi = np.linspace(0, 2*np.pi, n)
    X = np.cos(phi)
    Y = np.sin(phi)
    
    if flag_type == 'E':
        # This would require Young_2DM implementation
        # For now, we'll use a placeholder
        V = np.ones(n)  # Placeholder
        titlestr = 'Young Modulus (GPa)'
    elif flag_type == 'G':
        # This would require Shear_2DM implementation
        # For now, we'll use a placeholder
        V = np.ones(n)  # Placeholder
        titlestr = 'Shear Modulus (GPa)'
    elif flag_type == 'v':
        # This would require Poisson_2DM implementation
        # For now, we'll use a placeholder
        V = np.ones(n)  # Placeholder
        titlestr = 'Poisson ratio'
    
    V_Max = np.max(V)
    Vneg = np.zeros_like(V)
    Vneg[V < 0] = V[V < 0]
    Vpos = V - Vneg
    
    if np.sum(Vneg) == 0:
        p = plt.plot(V*X, V*Y, 'r', linewidth=2)
    else:
        p1 = plt.plot(Vpos*X, Vpos*Y, 'r', linewidth=2)
        p2 = plt.plot(Vneg*X, Vneg*Y, 'b--', linewidth=2)
    
    plt.title(titlestr)
    plt.grid(True)

def ElasticPlot_2D_flag(S, n, flag_type, flag_plane):
    """
    Plot a specific elastic property in specified planes.
    
    Parameters
    ----------
    S : numpy.ndarray
        Compliance matrix (6x6)
    n : int
        Number of points for plotting
    flag_type : str
        Property to plot ('B', 'E', 'G', 'v', 'H')
    flag_plane : list
        List of planes to plot ('xy', 'xz', 'yz', 'all')
    """
    t = np.linspace(0, 2*np.pi, n)
    X = np.cos(t)
    Y = np.sin(t)
    
    flag_newfigure = True
    if 'all' in flag_plane:
        flag_newfigure = False
        flag_plane = ['xy', 'xz', 'yz']
    
    for i, flag_planei in enumerate(flag_plane):
        Fig_legend = [f'${flag_type}-{flag_planei}$']
        
        theta, phi = ElasticPlot_2D_plane(flag_planei, t)
        
        if flag_type == 'B':
            V = Bulk_3D(S, theta, phi)
            V_Max = np.max(V)
            titlestr = 'Bulk Modulus (GPa)'
        elif flag_type == 'E':
            V = Young_3D(S, theta, phi)
            V_Max = np.max(V)
            titlestr = 'Young Modulus (GPa)'
        elif flag_type == 'G':
            Vmin, V, Vmax = Shear_3D(S, theta, phi)
            Fig_legend = [f'${flag_type}_{{ave}}-{flag_planei}$']
            V_Max = np.max(Vmax)
            titlestr = 'Shear Modulus (GPa)'
        elif flag_type == 'v':
            Vmin, V, Vmax = Poisson_3D(S, theta, phi)
            Fig_legend = [f'${flag_type}_{{ave}}-{flag_planei}$']
            V_Max = np.max(Vmax)
            V_Min = np.min(V)
            titlestr = 'Poisson ratio'
        elif flag_type == 'H':
            V = Hardness_3D(S, theta, phi)
            V_Max = np.max(V)
            titlestr = 'Hardness (GPa)'
        
        p = plt.plot(V*X, V*Y, 'r', linewidth=2)
        
        if flag_type == 'v' or flag_type == 'G':
            plt.hold(True) if hasattr(plt, 'hold') else None
            pmin = plt.plot(Vmin*X, Vmin*Y, 'g--', linewidth=2)
            pmax = plt.plot(Vmax*X, Vmax*Y, 'b:', linewidth=2)
            Fig_legend.append(f'${flag_type}_{{min}}-{flag_planei}$')
            Fig_legend.append(f'${flag_type}_{{max}}-{flag_planei}$')
        
        plt.legend(Fig_legend)
        plt.title(titlestr)
        plt.grid(True)
        
        # Draw circles for reference
        if 'V_Max' in locals() and V_Max > 0:
            plot_circle(100, np.linspace(0, V_Max, 5))