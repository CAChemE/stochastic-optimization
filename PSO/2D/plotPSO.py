import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.style.use('bmh')


def plotPSO_2D(function, limits=([-5,5],[-5,5]), particle_xycoordinates, n_points=100, *arg):
    
    # Grid points 
    x_lo = limits[0][0]
    x_up = limits[0][1]
    y_lo = limits[1][0]
    y_up = limits[1][1]                             
                                 
    x = np.linspace(lo_b, up_b, n_points) # x coordinates of the grid
    y = np.linspace(lo_b, up_b, n_points) # y coordinates of the grid

    XX, YY = np.meshgrid(x,y)
    ZZ = np.zeros_like(XX)
    
    for i in range(n_points):
        for j in range(n_points):
            ZZ[i,j] = function((XX[i,j], YY[i,j]))
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(XX,YY,ZZ,
                    rstride=3, cstride=3, alpha=0.4,
                    cmap=plt.cm.viridis)
    
    z_cut_plane = 0 
    
    # Projection of function
    z_proj = ax.contour(XX,YY,ZZ,
                              zdir='z', offset=z_cut_plane,
                              cmap=plt.cm.viridis)
    
    # Particle points
    x_particles, y_particles = particle_xycoordinates[0], particle_xycoordinates[1]
    # x_particles  
    # y_particles
    
    assert len(x_particles) == len(y_particles), "Tuple with arrays containing particle coordinates are different dimmension"
    
    n_particles = len(x_particles)
    z_particles = np.zeros(n_particles)
    
    for i in range(n_particles):
        z_particles[i] = function((x_particles[i],y_particles[i]))
    
    # Plot particles over the function
    ax.scatter(x_particles, y_particles, z_particles,
           s=50, c='r',
           depthshade=True)
    
    z_particles_projection = z_cut_plane*np.ones(n_particles)
    
    # Plot particles over the function
    ax.scatter(x_particles, y_particles, z_particles_projection,
           s=50, c='b',
           depthshade=True)
    
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$z$')
    ax.set_title('Ackley function')
    
    plt.show()

    
    return fig, ax