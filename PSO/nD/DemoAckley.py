from pso import pso
from optitestfuns import ackley
import unittest
import math


intVar = []
result = pso(ackley, [-5,-5], [5,5], intVar)

print(result.exit)
print('x_opt: {}'.format(result.xopt))
print('FO: {:2e}'.format(result.FO))