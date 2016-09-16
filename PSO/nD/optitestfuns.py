import numpy as np
import matplotlib.pyplot as plt


def ackley(x):
    """Ackley n-dimensional function

    Params:
    x =  numpy array or list containing the independent variables
    returns y = objective function value
    
    Best solution:
    f(x_i*) = y = 0  (i dimensions)
    x_i* = 0
    
    -30 <= x_i <= 30
    """
    

    x = np.array(x)  # converts list to numpy array
    n = x.size  # n-dimensions of the vector

    y = -20 * np.exp(-0.2 * (1 / n * np.sum(x ** 2)) ** 0.5) + \
        -np.exp(1 / n * np.sum(np.cos(2 * np.pi * x))) + 20 + np.exp(1)

    return y


def griewangk(x):
    """Griewank n-dimensional function

    Params:
    x =  numpy array or list containing the independent variables
    returns y = objective function value
    
    Best solution:
    f(x_i*) = y = 0  (i dimensions)
    x_i* = 0
    
    -100 <= x_i <= 100
    """

    x = np.array(x)  # converts list to numpy array
    n = x.size  # n-dimensions of the vector
    j = np.arange(n)
    
    y = 1/4000 * np.sum(x**2) - np.prod(np.cos(x/(j + 1)**0.5)) + 1

    return y

def rastrigin(x):
    """Rastrigin n-dimensional function

    Params:
    x =  numpy array or list containing the independent variables
    returns y = objective function value
    
    Best solution:
    f(x_i*) = y = 0  (i dimensions)
    x_i* = 0
    
    -5.12 <= x_i <= 5.12
    """

    x = np.array(x)  # converts list to numpy array
    n = x.size  # n-dimensions of the vector
    
    y = np.sum(x**2 - 10*np.cos(2*np.pi*x)+10)

    return y

def salomon(x):
    """Salomon n-dimensional function

    Params:
    x =  numpy array or list containing the independent variables
    returns y = objective function value
    
    Best solution:
    f(x_i*) = y = 0  (i dimensions)
    x_i* = 0
    
    -100 <= x_i <= 100
    """

    x = np.array(x)  # converts list to numpy array
    n = x.size  # n-dimensions of the vector
    
    x_norm = np.sqrt(np.sum(x**2))
    
    y = -np.cos(2*np.pi*x_norm) + 0.1*x_norm+1

    return y

def odd_square(x):
    """Whitley n-dimensional function

    Params:
    x =  numpy array or list containing the independent variables
    returns y = objective function value
    
    Best solution:
    f(x_i*) = y = 0  (i dimensions)
    x_i* = 0
    
    -5*pi <= x_i <= 5*pi
    """
    
    x = np.array(x)  # converts list to numpy array
    n = x.size  # n-dimensions of the vector
    
    assert n<=10, "Error: more than 10 dimensions were given, you need modify function params to run"
    b = np.array([1, 1.3, 0.8, -0.4, -1.3, 1.6, -0.2, -0.6, 0.5, 1.4,
                  1, 1.3, 0.8, -0.4, -1.3, 1.6, -0.2, -0.6, 0.5, 1.4])
    
    b = b[0:n]
    
    d = n*np.max((x-b)**2)
    h = np.sum((x-b)**2)
        
    y = -np.exp(-d/(2*np.pi))*np.cos(np.pi*d)*(1 + (0.02*h)/(d+0.01))

    return y


