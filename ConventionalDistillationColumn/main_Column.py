# -*- coding: utf-8 -*-

from pso_column import distCol_optimization

"""
# -------------------------------------------------------------------------
#   SIMULATION-BASED OPTIMIZATION OF A SINGLE CONVENTIONAL DISTILLATION 
#        COLUMN USING THE PARTICLE SWARM OPTIMIZATION ALGORITHEM
#--------------------------------------------------------------------------
#     Juan Javaloyes Antón / FJ Navarro-Brull (Sept 2016)
#     License: BSD-CL 3 javaloyes.juan@gmail.com 
#     More info at: https://github.com/CAChemE/stochastic-optimization
#--------------------------------------------------------------------------
# # 01 # Main Script
#--------------------------------------------------------------------------
#-------------------------------------------------------------------------                                            
# Conventional Distillation Column Superstructure
#
#
#                                ----
#                  _ _ _ _ _ _ _|    |
#                  |            |    |
#                  |             ----
#              --------           |        D
#             |        |<------------------------>
#             |......  |
#             |  ......|    NR_lb < NR < NR_up
#             |......  |
#  F          |  ------|        ---- Fixed Trays
# ----------> |------  |        .... Conditional Trays
#             |  ------|
#             |......  |
#             |  ......|   NS_lb < NS < NS_up
#             |......  |
#             |        |<---------|          
#              --------           |
#                 |               |
#                 |             ----          B
#                  _ _ _ _ _ _ |    |--------------->
#                              |    |
#                               ----
#--------------------------------------------------------------------------

# List of files
# ---------------------------------------------------------------------------------------------------------------------------------------------------|
#   Nº        Name                    Description                                |  Notes                                                            |
# ---------------------------------------------------------------------------------------------------------------------------------------------------|
#  #01 ...... Test_Column ........... Main script                                |   User Inputs                                                     |
# ---------------------------------------------------------------------------------------------------------------------------------------------------|
#  #02 ...... pso_column ............ Call to hyInterface to start the        |                                                                   |
#                                     connection with Aspen Hysys and runs the   | Do not modify                                                     | 
#                                     pso_gbest algorithm                        |                                                                   |
# ---------------------------------------------------------------------------------------------------------------------------------------------------|
#  #03 ...... hyInterface  .......... Aspen Hysys - Python Interface             | If some labels of the Aspen Hysys model are modify, user must     |
#                                                                                | modify also this function.                                        |          
# ---------------------------------------------------------------------------------------------------------------------------------------------------|
#  #04 ...... tac_column   ........ Calculates TAC (total annual cost)            | User can modify economic parameters or cost correlations.         |
#                                   of the conv. distillation column             | This functions is within the Test_Column_ObjFnc.py file           |
#----------------------------------------------------------------------------------------------------------------------------------------------------|
#  #05 ...... print_results       ... print main results in screen               |  Function is inside the file named print_pso.py                   |
#----------------------------------------------------------------------------------------------------------------------------------------------------|
#  #06 ...... PSO_Algorithm  ... Includes Global Best version of the             | User can modify PSO Algorithm parameters                          |                                        |
#----------------------------------------------------------------------------------------------------------------------------------------------------|

"""
# # User inputs >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# # 01 Hysys file name
hy_filename = 'Test_Column.hsc'

# # 02 
hy_best_model_filename = 'Best_Solution_Test_Column.hsc'

# # 03 Bounds on the conditional trays
#      RR BR NR  NS
lb = [1, 1, 10, 10]
ub = [2, 2, 30, 30]

# # 04 Binary variables index
IntVars = [2, 3]

# # 05 Aspen Hysys Graphical User Interface Visible
hy_visible = 1  # [1 ==> Visible    0 ==> No Visible]


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<< END


# # Problem Structure -----------------------------------------------------
class Problem:
    pass

Problem.hy_filename            = hy_filename
Problem.hy_best_model_filename = hy_best_model_filename
Problem.lb                     = lb  
Problem.ub                     = ub  
Problem.IntVars                = IntVars
Problem.hy_visible             = hy_visible


# # Run PSO ###############################################################
Result = distCol_optimization(Problem) # from pso_column
print('Obj_fnc = ', Result.best_fitness)
print('x_best  = ', Result.x_best)
#---------------------------------------------------------------------- end