
# coding: utf-8

# # Particle Swarm Optimization Algorithm (in Python!) 

# First of all, let's import the libraries we'll need (remember we are using Python 3)

# In[1]:

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import time


# get_ipython().magic('matplotlib inline')
plt.style.use('bmh')


# We can define and plot the function we want to optimize:

# In[2]:

x_lo = 0
x_up = 10
n_points = 100

x = np.linspace(x_lo, x_up, n_points)

def f(x):
    return x*np.sin(x) + x*np.cos(3*x)

y = f(x)

# plt.plot(x,y)
# plt.ylabel('$f(x) = \sin(x)+x\cos(2x)$')
# plt.xlabel('$x$')
# plt.title('Function to be optimized')


# ## PSO Initialization

# In[3]:

n_particles = 2
n_iterations = 5

x_particles = np.zeros((n_particles, n_iterations))
x_particles[:, 0] = np.random.uniform(x_lo, x_up, size=n_particles)

x_best_particles = np.copy(x_particles[:, 0])

y_particles = f(x_particles[:, 0])
y_best_global = np.min(y_particles[:])
index_best_global = np.argmin(y_particles[:])
x_best_p_global = x_particles[index_best_global,0]

velocity_lo = x_lo-x_up # TODO use absolute value to avoid problems
velocity_up = x_up-x_lo

v_particles = np.zeros((n_particles, n_iterations))
v_particles[:, 0] = 0.01*np.random.uniform(velocity_lo, velocity_up, size=n_particles)


# In[4]:

x_particles


# ## PSO Algorithm

# In[5]:

# PSO parameters
# from IPython.core.debugger import Tracer

# PSO parameters
from IPython.core.debugger import Tracer

omega = 1e-3
phi_p = 1e-3  # particle best weight
phi_g = 1e-3  # global global weight

iteration = 1
while iteration <= n_iterations - 1:
    for i in range(n_particles):
        x_p = x_particles[i, iteration-1]
        v_p = v_particles[i, iteration-1]
        x_best_p = x_best_particles[i]

        r_p = np.random.uniform(0, 1)
        r_g = np.random.uniform(0, 1)

        v_p_new = omega * v_p + \
                  phi_p * r_p * (x_best_p - x_p) + \
                  phi_g * r_g * (x_best_p_global - x_p)

        x_p_new = x_p + v_p_new

        if not x_lo <= x_p_new <= x_up:
            x_p_new = x_p  # ignore new position, it's out of the domain

        x_particles[i, iteration] = x_p_new

        y_p_best = f(x_best_p)
        y_p_new = f(x_p_new)

        if y_p_new < y_p_best:
            x_best_particles[i] = x_p_new

            y_p_best_global = f(x_best_p_global)
            if y_p_new < y_p_best_global:
                x_best_p_global = x_p_new

    iteration = iteration + 1


# In[6]:

# x_best_p_global


# In[7]:

# x_particles


# # Animation

# In[7]:

# from __future__ import print_function
# from ipywidgets import interact, interactive, fixed
# import ipywidgets as widgets


# In[8]:

y_particles = f(x_particles)


# In[9]:

def plotPSO(i=0): #iteration
    plt.plot(x,y)
    plt.ylabel('$f(x) = \sin(x)+x\cos(2x)$')
    plt.xlabel('$x$')
    plt.title('Function to be optimized')
    plt.plot(x_particles[:,i],y_particles[:,i],'ro')


# In[10]:

# interact(plotPSO, i=(0,n_iterations-1))


# In[ ]:



