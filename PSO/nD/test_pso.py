from pso import pso
from optitestfuns import ackley

intVar = []
pso(ackley, [-5, -1], [5, 1], intVar)

