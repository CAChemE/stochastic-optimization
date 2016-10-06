# coding: utf-8

import numpy as np
import time
import datetime as dt

from print_pso import print_results



def pso_gbest(objfnc, lb, ub, intVar, *arg):
'''Standard PSO algorithm (gbest) for minimizing a n dimensional function
  Input argurments:
	objfnc:  objective function 
	lb:  array containing lower bound on independent variables (len of array determines the dimensions)
	ub: array containing upper bound on independent variables (len of array determines the dimensions)
	intVar: array containing the index of the interger (indpendent) variables
	
	returns: Result Class
					Result.best_fitness = gbest_fitness
					Result.x_best       = gbest_x
					Result.iterations   = n_iter
					Result.FO_eval      = FO_eval
					Result.error_x      = error_x
					Result.error_fnc    = error_fnc
					Result.exit         = termination
  
	 Author: Juan Javaloyes Antón & FJ Navarro-Brull (Sept 2016)
     License: BSD-CL 3 javaloyes.juan@gmail.com 
     More info at: https://github.com/CAChemE/stochastic-optimization
'''
    
    Problem = arg[0]
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>[ PSO OPTIONS ]>>>>>>>>>>>>>>>>>>>> User inputs
    # * Population size
    swarm_size = 20          #  number of the swarm particles
    
    # * Termination Conditions
    maxIter    = 30          #  maximum number of iterations
    maxFO      = 1e5         #  maximun number of function evaluations
    
    maxIterNoImprov = 1e5    # maximun number of iterations without improving the objective function
    maxTime         = 1e5    # time limit in seconds [s] [or np.finfo(np.float64).max for realmax]
    
    tol_x   = 1e-5           # tolerance in x (norm 2)
    tol_fnc = 1e-5           # tolerance in objective function
    
    # * PSO parameters
    inertia_w       = 0.72   # Inertia weigth
    acceleration_c1 = 1.49   # Acceleration coefficient (cognitive)
    acceleration_c2 = 1.49   # Acceleraton coefficient (social)
    v_max = 2                # Maximun velocity in absolute value
    break_coeff = 0.05       # Break factor for the worst particle
    Red_acceleration_c1 = 2  # Reduction factor of accelaration c1 coefficient for the worst particle
    
    
    # * Algorithm options
    print_freq = 1
    plotPSO    = 'on'
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End inputs
            
            
# ········· PARTICLE SWARM OPTIMIZATION ALGORITHM CODE ····················
    
# # Preprocessing Operations ##############################################
    n_variables = np.size(lb)  # number of variables
    lb = np.array(lb)
    ub = np.array(ub)
    
    lb_original = np.copy(lb) # copy of original bounds for plotting
    ub_original = np.copy(ub)
    
    
# #  Initialization #######################################################
    
# 01. Set new bounds on the integer variables -----------------------------
# NOTE1: Bounds on integer variables must be integer numbers
# NOTE2: New bounds are established in order to give the same probability
#        to the variable bounds when round MATLAB function is used.    
    
    if np.ndim(intVar)>=1:
        lb[intVar] = lb[intVar] - 0.49
        ub[intVar] = ub[intVar] + 0.49
        
# 02. Set the initial position of the particles ---------------------------
    aux1 = (ub - lb) 
    x = np.outer(lb, np.ones(swarm_size)) + \
        np.outer(aux1, np.ones(swarm_size))*np.random.rand(n_variables, swarm_size)
        
    # * Round intger variables     
    x[intVar,:] = np.rint(x[intVar,:])
        
# 03. Set initial velocity for particles ----------------------------------
    v = np.zeros((n_variables, swarm_size))
    
# 04. Evaluation of each particle -----------------------------------------
# NOTE3: It is not possible to perform a vectorized version since our
#        objective function can be a black box (e.g. process simulator) 
    
    start_initialization = dt.datetime.now()
    tic_initialization   = time.time()
    
    fval = np.zeros((swarm_size))
    for iParticle in range(swarm_size):
        fval[iParticle] = objfnc(x[:,iParticle], Problem)


# 05. Best particle position and global best particle position and fitness-
    pbest_x        = np.copy(x)
    pbest_fitness  = np.copy(fval)
    
    gbest_fitness  = np.min(fval)
    gbest_ind      = np.argmin(fval)
    gbest_x        = x[:,gbest_ind]
    
    toc_initialization =  time.time() -  tic_initialization   
    
    stop_initialization = dt.datetime.now()  
    elapsed_time_initialization = (stop_initialization - start_initialization).microseconds
    
# 06. Worst particle in each iteration ----------------------------------------
    
    pworst_fitness = np.max(fval) 
    pworst_ind     = np.argmax(fval)
    pworst_x       = x[:,pworst_ind]
    
    error_x   = np.linalg.norm(pworst_x - gbest_x, ord = 2)
    error_fnc = np.linalg.norm(pworst_fitness - gbest_fitness)
    
# 07. Print results
    print_results(1, swarm_size, gbest_fitness, pworst_fitness,
                  error_fnc, error_x, swarm_size, n_variables, intVar,
                  print_freq)

# 08. Plot objective function and paticles for 2D and 3D test functions


# #########################################################################
# ####### Main Body of the Algorithm ### ##################################
# #########################################################################

    # * Control parameters & Preallocation arrays
    n_iter                   = 1
    timeLimit                = toc_initialization 
    FO_eval                  = swarm_size
    iter_fitness_improvement = 0
    
    v_new  = np.copy(v)
    x_new  = np.copy(x)
    x_plot = np.copy(x)
    
    
    
    while 1:
        start_iter_time = time.time()
    
        for iP in range(swarm_size):
            
# 09. Update velocity for all particles -----------------------------------
            if n_iter > 1 and iP == pworst_ind:
                v_new[:,iP] = break_coeff * inertia_w * v[:,iP] + \
                    acceleration_c1 * np.random.rand(1,n_variables) * (pbest_x[:,iP] - x[:,iP])/Red_acceleration_c1 + \
                    acceleration_c2 * np.random.rand(1,n_variables) * (gbest_x - x[:,iP])
            else:
                v_new[:,iP] = inertia_w * v[:,iP] + \
                    acceleration_c1 * np.random.rand(1,n_variables) * (pbest_x[:,iP] - x[:,iP]) + \
                    acceleration_c2 * np.random.rand(1,n_variables) * (gbest_x - x[:,iP])
            # end if
            
# 10. Velocity control --------------------------------------------------------    
            v_new[v_new > v_max]  =  v_max
            v_new[v_new < -v_max] = -v_max
            
# 11. Update position for all particlespbes -----------------------------------
            x_new[:,iP] = x[:,iP] + v_new[:,iP]

# 12. Position control ----------------------------------------------------
            # * Lower bound
            x_new[:,iP] = (x_new[:,iP] < lb) * lb + (x_new[:,iP] >= lb) *x_new[:,iP]                   
                   
            # * Upper bound
            x_new[:,iP]  = (x_new[:,iP] > ub) * ub + (x_new[:,iP] <= ub)*x_new[:,iP]
                
# 13. Round integer variables to the nearest integer ----------------------
# NOTE4: we need an aux var for the position in order to round the integer
#        variables keeping unalterd x_new for next iterations
            x_iP = np.copy(x_new[:,iP])
            
            x_iP[intVar] =  np.rint(x_iP[intVar])
                
            x_plot[:,iP] = x_iP # for plotting

# 14. Function evaluation  ----------------------------------------------------
            fval[iP] = objfnc(x_iP, Problem)
            
# 15. Update personal best particle (pbest) so far ----------------------------            
            if fval[iP] < pbest_fitness[iP]:
                pbest_fitness[iP] = fval[iP]
                pbest_x[:,iP]     =  x_iP

# 16. Update global best particle (gbest) ---------------------------------
            if pbest_fitness[iP] < gbest_fitness:
                gbest_fitness  = pbest_fitness[iP]
                gbest_x        = x_iP
                iter_fitness_improvement = 0
            else:
                iter_fitness_improvement = iter_fitness_improvement + 1
                
            stop_iter_time = time.time() - start_iter_time
    
# =============================================================================
#       end for loop in range of swarm size
# =============================================================================
    
# 17. Uptdate Control parameters    
            
        n_iter = n_iter + 1

        FO_eval = FO_eval + swarm_size
        timeLimit = timeLimit + stop_iter_time
            
# * Worst particle in each iteration
        pworst_fitness = np.max(pbest_fitness) 
        pworst_ind     = np.argmax(pbest_fitness)
        pworst_x       = pbest_x[:,pworst_ind]
            
        error_x   = np.linalg.norm(pworst_x - gbest_x, ord = 2)
        error_fnc = np.linalg.norm(pworst_fitness - gbest_fitness)
    
# 18. Print iteration results    
        print_results(n_iter, FO_eval, gbest_fitness, pworst_fitness,
                  error_fnc, error_x, swarm_size, n_variables, intVar,
                  print_freq)

# 19. Plot Particles and Objective Function -------------------------------

# 20. Check Termination Criterias -----------------------------------------

        if n_iter >= maxIter:
            termination = 'Stop due to maximum number of major iterations.'
            break
        elif FO_eval >= maxFO:
            termination = 'Stop due to maximum number of function evaluations.'
            break
        elif iter_fitness_improvement >= maxIterNoImprov:
            termination = 'Number of generations without fitness improvement Reached. The objective function is under specified tolerance'      
            break
        elif timeLimit >= maxTime:
            termination = 'The solver was interrupted because it reached the time limit.'       
            break 
#        elif error_fnc <= tol_fnc: 
#            termination = ' The objective function is under specified tolerance '        
#            break
#        elif error_x <= tol_x: 
#            termination = ' The tolerance between best and worst particles is under specification'      
#            break

    
# 21. Position and velocity for next iteration
        x = np.copy(x_new)
        v = np.copy(v_new)
# =============================================================================
#   end while loop
# =============================================================================
    
    class Result:
        pass
    
    Result.best_fitness = gbest_fitness
    Result.x_best       = gbest_x
    Result.iterations   = n_iter
    Result.FO_eval      = FO_eval
    Result.error_x      = error_x
    Result.error_fnc    = error_fnc
    Result.exit         = termination
    
    return Result    

# end def        
        
            
                
        




