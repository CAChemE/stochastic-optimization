from pso import pso
from optitestfuns import ackley
import unittest
from numpy import isclose, array

'''Tests for the nD PSO implementation.
To run it please execute the following command in your terminal or cmd
python -m unittest test_pso.py
'''

class PSOfunctionMethodTests(unittest.TestCase):

    def test_pso1D(self):
        intVar = []
        result = pso(ackley, [-5], [5], intVar)

        theo_min = array([0])

        print(result.exit)
        print('x_opt: {}'.format(result.xopt))
        print('FO: {:2e}'.format(result.FO))

        assert isclose(result.xopt[0], theo_min, atol=1e-3), "ERROR: variable didn't converged to 0"

    def test_pso1Dinteger(self):
        intVar = [0]
        result = pso(ackley, [-5], [5], intVar)

        theo_min = array([0])

        print(result.exit)
        print('x_opt: {}'.format(result.xopt))
        print('FO: {:2e}'.format(result.FO))

        assert isclose(result.xopt[0], theo_min, atol=1e-3), "ERROR: variable didn't converged to 0"
        assert float(result.xopt[0]).is_integer(), "ERROR: variable obtained wasn't an integer"


    def test_pso2D(self):
        intVar = []
        result = pso(ackley, [-5,-5], [5,5], intVar)

        theo_min = array([0])

        print(result.exit)
        print('x_opt: {}'.format(result.xopt))
        print('FO: {:2e}'.format(result.FO))

        assert isclose(result.xopt[0], theo_min, atol=1e-3), "ERROR: first variable didn't converged to 0"
        assert isclose(result.xopt[1], theo_min, atol=1e-3), "ERROR: second variable didn't converged to 0"


    # def test_pso2Dinteger(self):
    #     intVar = [0,1]
    #     result = pso(ackley, [-5, -5], [5, 5], intVar)
    #
    #     print(result.exit)
    #     print('x_opt: {}'.format(result.xopt))
    #     print('FO: {:2e}'.format(result.FO))
    #
    #     assert math.isclose(result.xopt[0], 0, abs_tol=1e-3), "ERROR: first variable didn't converged to 0"
    #     assert math.isclose(result.xopt[1], 0, abs_tol=1e-3), "ERROR: second variable didn't converged to 0"
    #     assert float(result.xopt[0]).is_integer(), "ERROR: first variable obtained wasn't an integer"
    #     assert float(result.xopt[1]).is_integer(), "ERROR: second variable obtained wasn't an integer"

if __name__ == '__main__':
    unittest.main()