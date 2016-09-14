import numpy as np
import matplotlib.pyplot as plt


def ackley(x):
    """Ackley n-dimensional function

    Params:
    x =  numpy array or list containing the independent variables

    returns y = objective function value
    """

    x = np.array(x)  # converts list to numpy array
    n = x.size  # n-dimensions of the vector

    y = -20 * np.exp(-0.2 * (1 / n * np.sum(x ** 2)) ** 0.5) + \
        -np.exp(1 / n * np.sum(np.cos(2 * np.pi * x))) + 20 + np.exp(1)

    return y
