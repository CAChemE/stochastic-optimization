import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.style.use('bmh')


def plotPSO_2D(function, particle_xycoordinates, limits=([-5,5],[-5,5]), n_points=100, *arg):
    
    # Grid points 
    x_lo = limits[0][0]
    x_up = limits[0][1]
    y_lo = limits[1][0]
    y_up = limits[1][1]                             
                                 
    x = np.linspace(x_lo, x_up, n_points) # x coordinates of the grid
    y = np.linspace(y_lo, y_up, n_points) # y coordinates of the grid

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
    x_particles = particle_xycoordinates[0]
    y_particles = particle_xycoordinates[1]
   
    assert len(x_particles) == len(y_particles), "Tuple with arrays containing particle coordinates are different dimmension"
    
    n_particles = len(x_particles)
    z_particles = np.zeros(n_particles)
    
    for i in range(n_particles):
        z_particles[i] = function((x_particles[i],y_particles[i]))
    
    # Plot particles over the function
    ax.scatter(x_particles, y_particles, z_particles,
           s=50, c='red',
           depthshade=True)
    
    z_particles_projection = z_cut_plane*np.ones(n_particles)
    
    # Plot particles over the function
    ax.scatter(x_particles, y_particles, z_particles_projection,
           s=50, c='blue',
           depthshade=False)
    
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$z$')
    
    #ax.set_title('function')
    
    plt.show()

    
    return fig, ax

def plotPSO_1D(function, particle_xcoordinates, limits=([-5,5]), n_points=100, *arg):
    
    # Grid points 
    x_lo = limits[0]
    x_up = limits[1]                         
                              
    x = np.linspace(x_lo, x_up, n_points) # x coordinates of the grid
    z = np.zeros(n_points)
   
    for i in range(n_points):
        z[i] = function(x[i])
    
    fig = plt.figure()
    ax = fig.add_subplot(111) # 111 stands for subplot(nrows, ncols, plot_number) 
    ax.plot(x,z)
    
    x_particles = particle_xcoordinates
    
    n_particles = len(x_particles)
    z_particles = np.zeros(n_particles)
    
    for i in range(n_particles):
        z_particles[i] = function(x_particles[i])
    
    # Plot particles over the function
    ax.scatter(x_particles, z_particles,
           s=50, c='red')
       
    # Plot particles over the function
    ax.scatter(x_particles,z_particles, c='red')
    
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')

    # ax.set_title('Ackley function')
    
    plt.show()
    
    return fig, ax