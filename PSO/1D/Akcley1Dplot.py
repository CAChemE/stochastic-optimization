import numpy as np
import matplotlib.pyplot as plt
# import scipy as sp
# import time


#%matplotlib inline
plt.style.use('bmh')

x_lo = -2
x_up = 2
n_points = 100

x = np.linspace(x_lo, x_up, n_points)
y = np.zeros(n_points)

def f(x):
    '''Ackley n-dimensional function
    x =  numpy array containing the independt variables as a vector
    
    returns y = objective function value
    '''
    n = np.array(x).size # n-dimensions of the vector 
    y = -20*np.exp(-0.2*(1/n*np.sum(x**2))**0.5) + \
        -np.exp(1/n*np.sum(np.cos(2*np.pi*x))) + 20 + np.exp(1);
        
    return y

for i in range(n_points):
    x_i = x[i]
    y[i] = f(x_i)

plt.plot(x,y)
plt.ylabel('$f(x) = \sin(x)+x\cos(2x)$')
plt.xlabel('$x$')
plt.title('Function to be optimized')