import numpy as np

def  print_results(iter, FO_evaluations, gbest, pworst,
                        error_fnc, error_x, swarm_size, n_variables,
                        intVar, print_freq):
    """
    Auxiliary function to  print PSO results

    :param iter: numer of iteration
    :param FO_evaluations:
    :param gbest: global best particle
    :param pworst: worst particle
    :param error_fnc: normalized error of the obj function ||pworst_fitness - gbest_fitness||
    :param error_x: normalized error of the obj function ||pworst_position - gbest_position||
    :param swarm_size: number of particles
    :param n_variables: number of dimmesions
    :param intVar: array or list containing the indexes for the variables that must be integers
    :param print_freq: frequency with the number of iterations that prints
    :return:
    """
    intVar = np.array(intVar)

    if iter == 1:
        print(' \n')
        print('# STANDARD PARTICLE SWARM OPTIMIZATION ALGORITHM - gbest version ### \n')
        print('     * Swarm size ................. {}'.format(swarm_size))
        print('     * # continuous variables ..... {}'.format(n_variables - np.size(intVar)))
        print('     * # integer variables .......  {}'.format(np.size(intVar)))
        print(' \n')


    if (iter == 1) or (iter/(print_freq) == round(iter/print_freq)):
        if (iter == 1) or (iter/(print_freq*20) == round(iter/(print_freq))):
            print('  --------------------------------------------------------------------------------------------\n')
            print('   Iteration \t FO_evals \t gBest Fitness \t pWorst Fitness\t   error_FO \t error_x\n')
            print('  --------------------------------------------------------------------------------------------\n')


        print('{:8.0f} \t {:5.0f} \t {:15.3e} \t {:11.3e} \t {:11.3e} \t {:6.3e}'.format(
        iter, FO_evaluations, gbest, pworst, error_fnc, error_x))



