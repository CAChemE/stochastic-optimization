import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.style.use('bmh')


def plotPSO_2D(function, limits=([-5,5],[-5,5]),
               particles_xy=([],[]), particles_uv=([],[]),
               n_points=100, *arg):
    """Creates a figure of 1x2 with a 3D projection representation of a 2D function and a its projection
    
    Params:
        function: a 2D or nD objective function
        limits: define the bounds of the function
        particles_xy a tuple contatining 2 lists with the x and y coordinate of the particles
        particles_xy a tuple contatining 2 lists with the u and v velocities of the particles
        n_points: number of points where the function is evaluated to be plotted, the bigger the finner"""
    

    # Grid points 
    x_lo = limits[0][0]
    x_up = limits[0][1]
    y_lo = limits[1][0]
    y_up = limits[1][1]
    
    assert x_lo<x_up, "Unbound x limits, the first value of the list needs to be higher"
    assert y_lo<y_up, "Unbound x limits, the first value of the list needs to be higher"
                                 
    x = np.linspace(x_lo, x_up, n_points) # x coordinates of the grid
    y = np.linspace(y_lo, y_up, n_points) # y coordinates of the grid

    XX, YY = np.meshgrid(x,y)
    ZZ = np.zeros_like(XX)
    
    for i in range(n_points):
        for j in range(n_points):
            ZZ[i,j] = function((XX[i,j], YY[i,j]))
    
    fig = plt.figure(figsize=(12,4))
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')

    ax1.plot_surface(XX,YY,ZZ,
                    rstride=3, cstride=3, alpha=0.4,
                    cmap=plt.cm.viridis, zorder=1)
        
    z_cut_plane = 0 
    
    ax1.set_xlabel('$x$')
    ax1.set_ylabel('$y$')
    ax1.set_zlabel('$z$')
    
    ax1.set_title(function.__name__)

    # Projection of function
    z_proj = ax1.contourf(XX,YY,ZZ,
                              zdir='z', offset=z_cut_plane,
                              cmap=plt.cm.viridis, zorder=1)
    
    # Particle points
    x_particles = particles_xy[0]
    y_particles = particles_xy[1]
    
    # Particle velocities
    u_particles = particles_uv[0]
    v_particles = particles_uv[1]
    
    assert len(x_particles) == len(y_particles), "Tuple with arrays containing particle coordinates are different dimmension"
    assert len(u_particles) == len(v_particles), "Tuple with arrays containing particle velocities are different dimmension"
    
    n_particles = len(x_particles)
    n_velocities = len(u_particles)
    
    if n_particles>=1:
        z_particles = np.zeros(n_particles)
    
        for i in range(n_particles):
            z_particles[i] = function((x_particles[i],y_particles[i]))

        # Plot particles over the function 
        ax1.scatter(x_particles, y_particles, z_particles,
               s=50, c='magenta',
               depthshade=False, zorder=1000)

        z_particles_projection = z_cut_plane*np.ones(n_particles)

        # Plot particles below the function (projection)
        ax1.scatter(x_particles, y_particles, z_particles_projection,
               s=50, c='red',
               depthshade=False, zorder=1000)
    
    
    # 2D projection (right figure)
    ax2 = fig.add_subplot(1, 2, 2)
    
    # Projection of function
    cf2d = ax2.contourf(XX,YY,ZZ,
                 zdir='z', offset=z_cut_plane,
                 cmap=plt.cm.viridis, zorder=1)
    
    # Particles (2D)
    if n_particles>=1:
        ax2.scatter(x_particles, y_particles,
               s=50, c='red', zorder=2)
        
        if n_velocities>=1:
            ax2.quiver(x_particles,y_particles,u_particles,v_particles,
                      angles='xy', scale_units='xy', scale=1)

            tag_particles = range(n_particles)

            for j, txt in enumerate(tag_particles):
                ax2.annotate(txt, (x_particles[j],y_particles[j]), zorder=3)
    
    
    ax2.set_title('xy plane')
    fig.colorbar(cf2d, shrink=1)
    
    #plt.savefig(function.__name__+'_2D', bbox_inches='tight')
    plt.show()


  
    return fig, (ax1, ax2)

def plotPSO_1D(function, limits=([-5,5]), particles_coordinates=([]), particles_velocities=([]), n_points=100, *arg):
    """Returns and shows a figure of a 2D representation of a 1D function
    
    Params:
        function: a 2D or nD objective function
        limits: define the bounds of the function
        particles_coordinates: a tuple contatining 2 lists with the x and y coordinate of the particles
        particles_velocities: a tuple contatining 2 lists with the u and v velocities of the particles
        n_points: number of points where the function is evaluated to be plotted, the bigger the finner"""
    
    # Grid points 
    x_lo = limits[0]
    x_up = limits[1]                         
                              
    x = np.linspace(x_lo, x_up, n_points) # x coordinates of the grid
    z = np.zeros(n_points)
   
    for i in range(n_points):
        z[i] = function(x[i])
    
    fig = plt.figure()
    ax = fig.add_subplot(111) # 111 stands for subplot(nrows, ncols, plot_number) 
    ax.plot(x,z, zorder=1)
    
    particles_coordinates = np.array(particles_coordinates)
    particles_velocities = np.array(particles_velocities)
    
    assert particles_coordinates.ndim <=1, \
    "Arrays containing particle coordinates have more than 1 dimmension"
    
    if particles_coordinates.shape[0] is not 0: 
        x_particles = particles_coordinates
        n_particles = x_particles.shape[0]

        z_particles = np.zeros(n_particles)


        for i in range(n_particles):
            z_particles[i] = function(x_particles[i])

        # Plot particles over the function
        ax.scatter(x_particles, z_particles,
               s=50, c='red', zorder=2)
        
        if particles_velocities.shape[0] is not 0:  
            u_particles = particles_velocities
            
            n_velocities = u_particles.shape[0]
            
            v_particles = np.zeros(n_particles)
    
            ax1.quiver(x_particles,z_particles,u_particles,v_particles,
                      angles='xy', scale_units='xy', scale=1)

            tag_particles = range(n_particles)

            for j, txt in enumerate(tag_particles):
                ax1.annotate(txt, (x_particles[j,i],z_particles[j,i]))
    
    
    
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')

    ax.set_title(function.__name__)
    
    #plt.savefig(function.__name__+'_1D', bbox_inches='tight')
    plt.show()
    
    return fig, ax