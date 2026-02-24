# Plot_Slice: Elastic property visualization on arbitrary crystallographic planes
# Allows slicing through 3D elastic property distributions

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional, Union
from mpl_toolkits.mplot3d import Axes3D


def Plot_Slice(S: np.ndarray, n: int, flag: Union[str, List[str]], 
               slice_plane: Union[List[float], np.ndarray],
               flag_save: bool = False, name: str = 'output',
               show: bool = True) -> Optional[plt.Figure]:
    """
    Plot elastic property distribution on an arbitrary crystallographic plane.
    
    Parameters
    ----------
    S : numpy.ndarray
        Compliance matrix (6x6)
    n : int
        Number of points for plotting (resolution)
    flag : str or list
        Property type(s) to plot:
        - 'E': Young's modulus
        - 'G': Shear modulus
        - 'B': Bulk modulus
        - 'v': Poisson's ratio
        - 'H': Hardness
    slice_plane : list or numpy.ndarray
        Miller indices [h, k, l] defining the plane normal
    flag_save : bool
        Whether to save the figure
    name : str
        Base filename for saving
    show : bool
        Whether to display the figure
        
    Returns
    -------
    fig : matplotlib.figure.Figure or None
        The figure object if show=False, else None
        
    Examples
    --------
    >>> import numpy as np
    >>> C = np.eye(6) * 100  # Simple isotropic
    >>> S = np.linalg.inv(C)
    >>> Plot_Slice(S, 100, ['E', 'G'], [1, 1, 1])
    """
    # Handle single flag
    if isinstance(flag, str):
        flag = [flag]
    
    slice_plane = np.array(slice_plane)
    figures = []
    
    for flagi in flag:
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        _plot_slice_single(ax, S, n, flagi, slice_plane)
        
        ax.set_axis_off()
        ax.view_init(elev=30, azim=45)
        
        # Set view to look at slice plane
        _set_view_for_plane(ax, slice_plane)
        
        if flag_save:
            save_name = f'{name}-{flagi}-Slice.png'
            fig.savefig(save_name, dpi=150, bbox_inches='tight')
            print(f'Saved: {save_name}')
        
        figures.append(fig)
    
    if show:
        plt.show()
        return None
    
    return figures[0] if len(figures) == 1 else figures


def _plot_slice_single(ax, S: np.ndarray, n: int, flag_type: str, 
                       slice_plane: np.ndarray):
    """
    Plot a single elastic property on a slice plane.
    """
    # Import calculation functions
    try:
        from ..core import Young_3D, Bulk_3D, Shear_3D, Poisson_3D, Hardness_3D
    except ImportError:
        from core import Young_3D, Bulk_3D, Shear_3D, Poisson_3D, Hardness_3D
    
    try:
        from ..core.conversions import Direction2Ang
    except ImportError:
        from core.conversions import Direction2Ang
    
    # Generate points on the slice plane
    t = np.linspace(0, 2 * np.pi, n + 1)
    X, Y, Z = _slice_plane_coords(t, slice_plane)
    
    # Convert to spherical coordinates
    theta, phi = Direction2Ang(X, Y, Z)
    
    # Calculate property values
    PS_vpa = np.round(slice_plane, 2)
    
    if flag_type == 'B':
        V = Bulk_3D(S, theta, phi)
        V_max = np.max(V)
        title_str = f'Bulk Modulus (GPa) - [{PS_vpa[0]} {PS_vpa[1]} {PS_vpa[2]}]'
        has_minmax = False
    elif flag_type == 'E':
        V = Young_3D(S, theta, phi)
        V_max = np.max(V)
        title_str = f"Young's Modulus (GPa) - [{PS_vpa[0]} {PS_vpa[1]} {PS_vpa[2]}]"
        has_minmax = False
    elif flag_type == 'G':
        V_min, V, V_max_arr = Shear_3D(S, theta, phi)
        V_max = np.max(V_max_arr)
        title_str = f'Shear Modulus (GPa) - [{PS_vpa[0]} {PS_vpa[1]} {PS_vpa[2]}]'
        has_minmax = True
    elif flag_type == 'v':
        V_min, V, V_max_arr = Poisson_3D(S, theta, phi)
        V_max = np.max(V_max_arr)
        V_min_val = np.min(V)
        title_str = f'Poisson Ratio - [{PS_vpa[0]} {PS_vpa[1]} {PS_vpa[2]}]'
        has_minmax = True
    elif flag_type == 'H':
        V = Hardness_3D(S, theta, phi)
        V_max = np.max(V)
        title_str = f'Hardness (GPa) - [{PS_vpa[0]} {PS_vpa[1]} {PS_vpa[2]}]'
        has_minmax = False
    else:
        raise ValueError(f"Unknown property type: {flag_type}")
    
    # Plot main curve
    ax.plot3D(V * X, V * Y, V * Z, 'r-', linewidth=2, label='Average')
    
    # Plot min/max for shear and Poisson
    if has_minmax:
        ax.plot3D(V_min * X, V_min * Y, V_min * Z, 'g--', linewidth=1.5, label='Min')
        ax.plot3D(V_max_arr * X, V_max_arr * Y, V_max_arr * Z, 'b:', linewidth=1.5, label='Max')
        ax.legend(loc='upper right')
    
    ax.set_title(title_str)
    
    # Draw polar grid circles
    _plot_circles(ax, slice_plane, n, V_max)
    
    # Draw radial lines
    _plot_radial_lines(ax, slice_plane, 12, V_max)


def _slice_plane_coords(t: np.ndarray, slice_plane: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate Cartesian coordinates for points on a plane defined by its normal.
    
    Parameters
    ----------
    t : numpy.ndarray
        Parameter for circle (0 to 2*pi)
    slice_plane : numpy.ndarray
        Normal vector [h, k, l]
        
    Returns
    -------
    X, Y, Z : numpy.ndarray
        Cartesian coordinates
    """
    a, b, c = slice_plane
    
    # Find two orthogonal vectors in the plane
    if a == 0 and b == 0:
        u = np.array([1, 0, 0])
    else:
        u = np.array([b, -a, 0])
    
    v = np.cross(slice_plane, u)
    
    # Normalize
    u = u / np.linalg.norm(u)
    v = v / np.linalg.norm(v)
    
    # Generate circle coordinates
    X = u[0] * np.cos(t) + v[0] * np.sin(t)
    Y = u[1] * np.cos(t) + v[1] * np.sin(t)
    Z = u[2] * np.cos(t) + v[2] * np.sin(t)
    
    return X, Y, Z


def _plot_circles(ax, slice_plane: np.ndarray, n: int, r_max: float):
    """Draw polar grid circles on the slice plane."""
    t = np.linspace(0, 2 * np.pi, n + 1)
    X, Y, Z = _slice_plane_coords(t, slice_plane)
    
    # Determine radius intervals
    if r_max > 0:
        dr = 10 ** np.floor(np.log10(r_max))
        if r_max / dr < 3:
            dr = dr / 2
        elif r_max / dr > 8:
            dr = dr * 2
        
        radii = np.arange(dr, r_max * 1.1, dr)
        
        for r in radii:
            alpha = 0.3 if r < r_max else 0.8
            ax.plot3D(r * X, r * Y, r * Z, 'k-', linewidth=0.5, alpha=alpha)


def _plot_radial_lines(ax, slice_plane: np.ndarray, n_lines: int, r_max: float):
    """Draw radial lines from center on the slice plane."""
    t = np.linspace(0, 2 * np.pi, n_lines + 1)
    X, Y, Z = _slice_plane_coords(t, slice_plane)
    
    for i in range(n_lines):
        ax.plot3D([0, r_max * X[i]], [0, r_max * Y[i]], [0, r_max * Z[i]], 
                  'k:', linewidth=0.5, alpha=0.3)


def _set_view_for_plane(ax, slice_plane: np.ndarray):
    """Set the 3D view to look at the slice plane."""
    # Normalize the plane normal
    normal = slice_plane / np.linalg.norm(slice_plane)
    
    # Calculate elevation and azimuth from normal vector
    elev = np.degrees(np.arcsin(normal[2]))
    azim = np.degrees(np.arctan2(normal[1], normal[0]))
    
    ax.view_init(elev=elev, azim=azim)


# ============== 2D Polar Plot for Slices ==============

def Plot_Slice_2D(S: np.ndarray, n: int, flag: Union[str, List[str]], 
                 slice_plane: Union[List[float], np.ndarray],
                 flag_save: bool = False, name: str = 'output',
                 show: bool = True, ax=None) -> Optional[plt.Figure]:
    """
    Plot elastic property distribution on a 2D polar plot for a given plane.
    
    Similar to Plot_Slice but uses a 2D polar projection.
    
    Parameters
    ----------
    S : numpy.ndarray
        Compliance matrix (6x6)
    n : int
        Number of points for plotting
    flag : str or list
        Property type(s) to plot ('E', 'G', 'B', 'v', 'H')
    slice_plane : list or numpy.ndarray
        Miller indices [h, k, l] defining the plane normal
    flag_save : bool
        Whether to save the figure
    name : str
        Base filename for saving
    show : bool
        Whether to display the figure
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on. If provided, show is ignored.
        
    Returns
    -------
    fig : matplotlib.figure.Figure or None
    """
    # Import calculation functions
    try:
        from ..core import Young_3D, Bulk_3D, Shear_3D, Poisson_3D, Hardness_3D
        from ..core.conversions import Direction2Ang
    except ImportError:
        from core import Young_3D, Bulk_3D, Shear_3D, Poisson_3D, Hardness_3D
        from core.conversions import Direction2Ang
    
    if isinstance(flag, str):
        flag = [flag]
    
    slice_plane = np.array(slice_plane)
    figures = []
    
    # If ax is provided, we can only plot one property
    if ax is not None:
        if len(flag) > 1:
            print("Warning: Multiple flags provided but only one axes. Plotting first flag only.")
        flagi = flag[0]
        
        # Generate angles for polar plot
        t = np.linspace(0, 2 * np.pi, n + 1)
        X, Y, Z = _slice_plane_coords(t, slice_plane)
        
        # Convert to spherical
        theta, phi = Direction2Ang(X, Y, Z)
        
        PS_vpa = np.round(slice_plane, 2)
        
        # Calculate property
        if flagi == 'E':
            V = Young_3D(S, theta, phi)
            title_str = f"Young's Modulus (GPa)"
        elif flagi == 'G':
            _, V, _ = Shear_3D(S, theta, phi)
            title_str = 'Shear Modulus (GPa)'
        elif flagi == 'B':
            V = Bulk_3D(S, theta, phi)
            title_str = 'Bulk Modulus (GPa)'
        elif flagi == 'v':
            _, V, _ = Poisson_3D(S, theta, phi)
            title_str = 'Poisson Ratio'
        elif flagi == 'H':
            V = Hardness_3D(S, theta, phi)
            title_str = 'Hardness (GPa)'
        else:
            raise ValueError(f"Unknown property type: {flagi}")
        
        # Plot on polar axes
        ax.set_rlabel_position(45)
        ax.plot(t, V, 'r-', linewidth=2)
        ax.fill(t, V, alpha=0.3, color='red')
        ax.set_title(f'{title_str}\n[{PS_vpa[0]} {PS_vpa[1]} {PS_vpa[2]}]')
        
        if flag_save:
            # We can't easily save just the axes here without the figure reference, 
            # but usually save is done on the figure.
            pass
            
        return None

    # Original behavior for new figures
    for flagi in flag:
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
        
        # Generate angles for polar plot
        t = np.linspace(0, 2 * np.pi, n + 1)
        X, Y, Z = _slice_plane_coords(t, slice_plane)
        
        # Convert to spherical
        theta, phi = Direction2Ang(X, Y, Z)
        
        PS_vpa = np.round(slice_plane, 2)
        
        # Calculate property
        if flagi == 'E':
            V = Young_3D(S, theta, phi)
            title_str = f"Young's Modulus (GPa)"
        elif flagi == 'G':
            _, V, _ = Shear_3D(S, theta, phi)
            title_str = 'Shear Modulus (GPa)'
        elif flagi == 'B':
            V = Bulk_3D(S, theta, phi)
            title_str = 'Bulk Modulus (GPa)'
        elif flagi == 'v':
            _, V, _ = Poisson_3D(S, theta, phi)
            title_str = 'Poisson Ratio'
        elif flagi == 'H':
            V = Hardness_3D(S, theta, phi)
            title_str = 'Hardness (GPa)'
        else:
            raise ValueError(f"Unknown property type: {flagi}")
        
        # Plot on polar axes
        ax.set_rlabel_position(45)
        ax.plot(t, V, 'r-', linewidth=2)
        ax.fill(t, V, alpha=0.3, color='red')
        ax.set_title(f'{title_str}\n[{PS_vpa[0]} {PS_vpa[1]} {PS_vpa[2]}]')
        
        if flag_save:
            save_name = f'{name}-{flagi}-Slice2D.png'
            fig.savefig(save_name, dpi=150, bbox_inches='tight')
            print(f'Saved: {save_name}')
        
        figures.append(fig)
    
    if show:
        plt.show()
        return None
    
    return figures[0] if len(figures) == 1 else figures
