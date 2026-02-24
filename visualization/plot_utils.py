# Utility functions for plotting in Mat Model Lab

import numpy as np
import matplotlib.pyplot as plt

def ElasticPlot_2D_plane(plane, t):
    """
    Convert plane specification to theta and phi angles.
    
    Parameters
    ----------
    plane : str
        Plane specification ('xy', 'xz', 'yz')
    t : numpy.ndarray
        Array of angles for plotting
        
    Returns
    -------
    theta : numpy.ndarray
        Polar angle in radians
    phi : numpy.ndarray
        Azimuthal angle in radians
    """
    if plane == 'xy':
        theta = np.pi/2 * np.ones_like(t)
        phi = t
    elif plane == 'yz':
        theta = t
        phi = np.pi/2 * np.ones_like(t)
    elif plane == 'xz':
        theta = t
        phi = np.zeros_like(t)
    return theta, phi

def plot_circle(n, r):
    """
    Plot reference circles on the current figure.
    
    Parameters
    ----------
    n : int
        Number of points for plotting the circle
    r : array_like
        Radii of circles to plot
    """
    t = np.linspace(0, 2*np.pi, n)
    X = np.cos(t)
    Y = np.sin(t)
    t_txt = 80/180*np.pi
    x_txt = 0.97*r*np.cos(t_txt)
    y_txt = 0.97*r*np.sin(t_txt)
    n_circle = len(r)
    plt.hold(True) if hasattr(plt, 'hold') else None
    
    for i in range(n_circle):
        if i == n_circle - 1:
            plt.plot(r[i]*X, r[i]*Y, 'k', linewidth=0.5)
            plt.text(x_txt[i], y_txt[i], str(r[i]), fontsize=10)
        else:
            plt.plot(r[i]*X, r[i]*Y, 'k:', linewidth=0.5)
            plt.text(x_txt[i], y_txt[i], str(r[i]), fontsize=10)