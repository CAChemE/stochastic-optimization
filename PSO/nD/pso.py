# coding: utf-8

import numpy as np
import sys
import time
# from optitestfuns import ackley
# from tictoc import tic, toc
from print_pso import print_results

def pso(objfnc, lb, ub, intVar, *varargin):
    """
    Standard PSO algorithm (gbest) to minimize a function

    v = 0.1 - Sept 2016
    Authors: J.Javaloyes, FJ.Navarro (CAChemE.org)
    License: BSD-Clause 3

    Parameters
    ----------
    objfnc: argument containing the objective function
    lb: lower bound (array or list with len()=n_dimensions)
    ub: upper bound (array or list with len()=n_dimensions)
    intVar: list containing the indexes for the variables that must be integers
    varargin: unused input variables

    Returns: structure containing the results
    -------

    """


    #  ----------------- PSO OPTIONS (user inputs) -----------------------------------------

    # * Population size
    swarm_size = 20       #  number of the swarm particles

    # * Termination Conditions
    maxIter    = 1000       #  maximum number of iterations
    maxFO      = sys.float_info.max     #  maximum number of function after i evaluations

    maxIterNoImprov = sys.maxsize  # maximum number of iterations without improving the objective function
    maxTime         = sys.float_info.max # time limit in seconds [s]

    tol_x   = 1e-5          # tolerance in x (norm 2)
    tol_fnc = 1e-5          # tolerance in objective function

    # * PSO parameters
    inertia_w       = 0.72  # Inertia weight
    acceleration_c1 = 1.49  # Acceleration coefficient (cognitive)
    acceleration_c2 = 1.49  # Acceleration coefficient (social)
    v_max = 0.07               # maximum velocity in absolute value
    break_coeff = 0.05      # break  # stops while loop factor for the worst particle
    Red_acceleration_c1 = 2 # Reduction factor of acceleration c1 coefficient for the worst particle


    # * Algorithm options
    print_freq = 10
    plotPSO    = False
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  inputs


    # ????????? PARTICLE SWARM OPTIMIZATION ALGORITHM CODE ????????????????????

    # # Pre-processing Operations ##############################################
    n_variables = np.size(lb) # number variables

    lb = np.array(lb)
    lb_original = lb # Lower and upper bounds must be column vectors.

    ub = np.array(ub)
    ub_original = ub


    # #  Initialization #######################################################

    # 01. Set new bounds on the integer variables -----------------------------
    # NOTE1: Bounds on integer variables must be integer numbers
    # NOTE2: New bounds are established in order to give the same probability
    #        to the variable bounds when round MATLAB function is used.
    assert isinstance(intVar, list), "intVar must be a list"

    if intVar:  # if intVar has elements (not empty)
        assert max(intVar) <= (n_variables-1), "intVar indexes out of range (Python indexing starts at 0)"
        for i in intVar: assert i >= 0, "Indexes containing int variables must be positive"

        lb[intVar] = lb[intVar] - 0.49
        ub[intVar] = ub[intVar] + 0.49

    # 02. Set the initial position of the particles ---------------------------
    aux1 =  (ub - lb)
    x = np.outer(lb, np.ones(swarm_size)) + \
        np.outer(aux1, np.ones(swarm_size))*np.random.rand(n_variables, swarm_size)

    # x = np.array([[-4.067602406241254, 1.411475292329600, 2.311848990285760]])
    x[intVar, :] = np.round(x[intVar, :])


    # 03. Set initial velocity for particles ----------------------------------
    v = np.zeros([n_variables, swarm_size])

    # 04. Evaluation of each particle -----------------------------------------
    # NOTE3: It is not possible to perform a vectorized version since our
    #        objective function can be a black box (e.g. process simulator)

    tic = time.time()
    fval = np.zeros(swarm_size)
    for iParticle in range(swarm_size):
        fval[iParticle] = objfnc(x[:, iParticle])


    # 05. Best particle position and global best particle position and fitness-
    pbest_position             = np.copy(x)
    pbest_fitness              = np.copy(fval)

    gbest_fitness              = np.nanmin(fval)
    gbest_ind                  = np.nanargmin(fval)
    
    gbest_position             = np.copy(x[:, gbest_ind])

    iter1_time = round((time.time()-tic), 2)

    # 06. Print Results -------------------------------------------------------

    # * Worst particle in each iteration
    pworst_fitness = np.nanmax(pbest_fitness)
    pworst_ind = np.nanargmax(pbest_fitness)
    pworst_position = pbest_position[:, pworst_ind]

    error_x   = np.linalg.norm(pworst_position - gbest_position, 2)
    error_fnc = np.abs(pworst_fitness - gbest_fitness)

    print_results(1, swarm_size, gbest_fitness, pworst_fitness,
                  error_fnc, error_x, swarm_size, n_variables, intVar,
                        print_freq)


    # 07. Plot Particles and Objective Function -------------------------------

    if plotPSO:
        if n_variables == 2:
            # plot_3D(objfnc, lb_original, ub_original, x, fval, 1)             # Aux Fnc # 02 ###
            pass
        elif n_variables == 1:
            pass
        else:
            raise Warning(" Only 2D and 3D plots are possible !!! ")
        
    


    # #########################################################################
    # ####### Main Body of the Algorithm ### ##################################
    # #########################################################################

    # * Control parameters & Preallocation arrays
    iter                     = 1
    timeLimit                = iter1_time
    FO_evaluations           = swarm_size
    iter_fitness_improvement = 0

    v_new  = np.copy(v)
    x_new  = np.copy(x)

    tic = time.time()
    
    pso_flag = True


    while True:

        for iP in range(swarm_size):

            # 08. Update velocity for all particles -----------------------------------

            if iter > 1 and iP == pworst_ind:

                v_new[:, iP] =  break_coeff * inertia_w * v[:, iP] +\
                    acceleration_c1 * np.random.rand(n_variables) * (pbest_position[:, iP] - x[:, iP])/Red_acceleration_c1 + \
                    acceleration_c2 * np.random.rand(n_variables) * (gbest_position - x[:, iP])
            else:
                v_new[:, iP] = inertia_w * v[:, iP] + \
                    acceleration_c1 * np.random.rand(n_variables) * (pbest_position[:, iP] - x[:, iP]) + \
                    acceleration_c2 * np.random.rand(n_variables) * (gbest_position - x[:, iP])
            

    # 09. Velocity control ----------------------------------------------------
            v_new[v_new >  v_max] =  v_max
            v_new[v_new < -v_max] = -v_max

    # 10. Update position for all particles pbest -------------------------------
            x_new[:, iP] = x[:, iP] + v_new[:, iP]

    # 11. Position control ----------------------------------------------------

            # * Lower bound
            x_new[:, iP] = (x_new[:, iP] < lb)*lb + (x_new[:, iP] >= lb)*x_new[:, iP]

            # * Upper bound
            x_new[:, iP] = (x_new[:, iP] > ub)*ub + (x_new[:, iP] <= ub)*x_new[:, iP]


    # 12. Round integer variables to the nearest integer ----------------------
    # NOTE4: we need an aux var for the position in order to round the integer
    #        variables keeping unalterd x_new for next iterations
            x_iP = x_new[:, iP]
            x_iP[intVar] = np.round(x_iP[intVar])


    # 13. Function evaluation & update personal best particle (pbest) so far --
            fval[iP] = objfnc(x_iP)

            if fval[iP] < pbest_fitness[iP]:
                pbest_fitness[iP]     = fval[iP]
                pbest_position[:, iP] = x_iP
            

    # 14. Update global best particle (gbest) ---------------------------------
            if pbest_fitness[iP] < gbest_fitness:
                gbest_fitness  = pbest_fitness[iP]
                gbest_position = x_iP
                iter_fitness_improvement = 0
            else:
                iter_fitness_improvement = iter_fitness_improvement + 1
            
         # for loop in range 1:size_swarm ##################################
            # #################################################################

        iter_time = tic - time.time()

    # 15. Print Results -------------------------------------------------------
        iter = iter + 1
        FO_evaluations = FO_evaluations + swarm_size

        timeLimit = timeLimit + iter_time

        # * Worst particle in each iteration
        pworst_fitness = np.nanmax(pbest_fitness)
        pworst_ind = np.nanargmax(pbest_fitness)
        pworst_position = pbest_position[:, pworst_ind]

        error_x   = np.linalg.norm(pworst_position - gbest_position, 2)
        error_fnc = np.abs(pworst_fitness - gbest_fitness)

        print_results(iter, FO_evaluations, gbest_fitness, pworst_fitness,
                      error_fnc, error_x, swarm_size, n_variables, intVar,
                            print_freq )

        # print('x:{}'.format(gbest_position))
        # import pdb; pdb.set_trace()

    # 16. Plot Particles and Objective Function -------------------------------

        if plotPSO:
            if n_variables == 2:
                # plot_3D(objfnc, lb_original, ub_original, x, fval, 1)             # Aux Fnc # 02 ###
                pass
            elif n_variables == 1:
                pass
            else:
                raise Warning(" Only 2D and 3D plots are possible !!! ")
    

    # 17. Check Termination criteria -----------------------------------------

        if iter >= maxIter:
            termination = 'Stop due to maximum number of major iterations.'
            break  # stops while loop
            
        elif FO_evaluations >= maxFO:
            termination = 'Stop due to maximum number of function evaluations.'
            break  # stops while loop
        elif iter_fitness_improvement >= maxIterNoImprov:
            termination = 'Number of generations without fitness improvement Reached. The objective function is under specified tolerance'
            break  # stops while loop
        elif timeLimit >= maxTime:
            termination = 'The solver was interrupted because it reached the time limit.'
            break  # stops while loop

        elif error_fnc <= tol_fnc:
            termination = ' The objective function is under specified tolerance '
            break  # stops while loop
        elif error_x <= tol_x:
            termination = ' The tolerance between best and worse particles is under specification'
            break
        else:
            termination = 'Continue: # {0} iteration'.format(iter)

        # * Position and velocity for next iteration
        x = np.copy(x_new)
        v = np.copy(v_new)

    class Result:
        pass
   
    Result.xopt  = gbest_position
    Result.FO    = gbest_fitness
    Result.exit  = termination
    return Result
