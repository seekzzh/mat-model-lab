# 3D plotting functions for Mat Model Lab

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
# Fix import path issues, allowing the script to run directly or be imported as a module
try:
    # Use this path when imported as a module
    from ..core.young import Young_3D
    from ..core.bulk import Bulk_3D
    from ..core.poisson import Poisson_3D
    from ..core.shear import Shear_3D
    from ..core.hardness import Hardness_3D
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

def ElasticPlot_3D(S, n, flag, flag_amm='Ave', flag_save=False, Name=''):
    """
    Plot 3D elastic properties.
    
    Parameters
    ----------
    S : numpy.ndarray
        Compliance matrix (6x6)
    n : int
        Number of points for plotting
    flag : list
        List of properties to plot ('B', 'E', 'G', 'v', 'H')
    flag_amm : str, optional
        'Ave', 'Min', 'Max', or 'All' for properties with multiple values
    flag_save : bool, optional
        Whether to save the plots
    Name : str, optional
        Base name for saved files
    """
    theta, phi = np.meshgrid(np.linspace(0, np.pi, n+1), np.linspace(-np.pi, np.pi, 2*n+1))
    
    for flagi in flag:
        fig = plt.figure(figsize=(10, 8))
        ElasticPlot_3D_flag(S, theta, phi, flagi, flag_amm)
        
        plt.colormap('jet')
        plt.colorbar()
        plt.box(True)
        plt.axis('equal')
        plt.axis('off')
        
        # Add lighting effect
        ax = fig.gca(projection='3d')
        ax.view_init(elev=30, azim=45)
        
        if flag_save:
            savename = f"{Name}-{flagi}-3D.jpg"
            plt.savefig(savename, dpi=300)

def ElasticPlot_3D_flag(S, theta, phi, flag_type, flag_amm):
    """
    Plot a specific elastic property in 3D.
    
    Parameters
    ----------
    S : numpy.ndarray
        Compliance matrix (6x6)
    theta : numpy.ndarray
        Polar angle in radians
    phi : numpy.ndarray
        Azimuthal angle in radians
    flag_type : str
        Property to plot ('B', 'E', 'G', 'v', 'H')
    flag_amm : str
        'Ave', 'Min', 'Max', or 'All' for properties with multiple values
    """
    X = np.sin(theta) * np.cos(phi)
    Y = np.sin(theta) * np.sin(phi)
    Z = np.cos(theta)
    row_x, col_x = X.shape
    
    if flag_type == 'B':
        V = Bulk_3D(S, theta, phi)
        titlestr = 'Bulk Modulus (GPa)'
    elif flag_type == 'E':
        V = Young_3D(S, theta, phi)
        titlestr = 'Young Modulus (GPa)'
    elif flag_type == 'G':
        Vmin, Vave, Vmax = Shear_3D(S, theta, phi)
        if flag_amm == 'Ave':
            V = Vave
        elif flag_amm == 'Min':
            V = Vmin
        elif flag_amm == 'Max':
            V = Vmax
        elif flag_amm == 'All':
            V = np.zeros((row_x, col_x, 3))
            V[:, :, 0] = Vmin
            V[:, :, 1] = Vave
            V[:, :, 2] = Vmax
        titlestr = 'Shear Modulus (GPa)'
    elif flag_type == 'v':
        Vmin, Vave, Vmax = Poisson_3D(S, theta, phi)
        if flag_amm == 'Ave':
            V = Vave
        elif flag_amm == 'Min':
            V = Vmin
        elif flag_amm == 'Max':
            V = Vmax
        elif flag_amm == 'All':
            V = np.zeros((row_x, col_x, 3))
            V[:, :, 0] = Vmin
            V[:, :, 1] = Vave
            V[:, :, 2] = Vmax
        titlestr = 'Poisson ratio'
    elif flag_type == 'H':
        V = Hardness_3D(S, theta, phi)
        titlestr = 'Hardness (GPa)'
    
    fig = plt.gcf()
    ax = fig.gca(projection='3d')
    
    n_V = V.shape[2] if len(V.shape) > 2 else 1
    transparency = [1.0, 0.7, 0.4]  # Transparency for multiple surfaces
    
    if n_V == 1:
        if len(V.shape) == 2:
            Vtmp = V
        else:
            Vtmp = V[:, :, 0]
        surf = ax.plot_surface(
            Vtmp * X, Vtmp * Y, Vtmp * Z,
            facecolors=cm.jet(Vtmp/np.max(Vtmp)),
            alpha=transparency[0],
            linewidth=0,
            antialiased=True
        )
    else:
        for i in range(n_V):
            Vtmp = V[:, :, i]
            surf = ax.plot_surface(
                Vtmp * X, Vtmp * Y, Vtmp * Z,
                facecolors=cm.jet(Vtmp/np.max(Vtmp)),
                alpha=transparency[i],
                linewidth=0,
                antialiased=True
            )
    
    plt.title(titlestr)