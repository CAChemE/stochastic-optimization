# -*- coding: utf-8 -*-

import os
import win32com.client as win32

"""


# -------------------------------------------------------------------------
#   SIMULATION-BASED OPTIMIZATION OF A SINGLE CONVENTIONAL DISTILLATION 
#        COLUMN USING THE PARTICLE SWARM OPTIMIZATION ALGORITHM
#--------------------------------------------------------------------------
#                                      Juan Javaloyes Antón. Sep 2016 
#--------------------------------------------------------------------------
# # 03 # Aspen Hysys Python Interface - Conventional Distillation Column Test
#--------------------------------------------------------------------------

"""



# >>>>>>>>>>>>>>>[ Aspen Hysys - Python Interface ]>>>>>>>>>>>>>>> > User inputs
# Aspen Hysys file name
#hy_filename            = 'Test_Column.hsc'
#hy_best_model_filename = 'Best_Column.hsc'
#hy_visible             =  1

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >End inputs

def hy_Dist_Col_Object(Problem, *varargin):
    
    hy_filename            = Problem.hy_filename
    hy_best_model_filename = Problem.hy_best_model_filename
    hy_visible             = Problem.hy_visible            

    # 01  Full path to Aspen Hysys File & Best Solution Hysys File

    hyFilePath = os.path.abspath(hy_filename)
    hy_beswt_solution_FilePath = os.path.abspath(hy_best_model_filename)

    # 02 Initialize  Aspen Hysys application
    print(' # Connecting to the Aspen Hysys App ... ')
    HyApp = win32.Dispatch('HYSYS.Application')

    # 03 Open Aspen Hysys File
    #    HyCase = HyApp.SimulationCases.Open(hyFilePath)
    
    HyCase = HyApp.ActiveDocument

    # 04 Aspen Hysys Environment Visible
    HyCase.Visible = hy_visible


    # 05 Aspen Hysys File Name
    HySysFile = HyCase.Title.Value
    print(' ')
    print('HySys File: ----------  ', HySysFile)

    # 06 Aspen Hysys Fluid Package Name
    package_name = HyCase.Flowsheet.FluidPackage.PropertyPackageName
    print('HySys Fluid Package: ---  ', package_name)
    print(' ')


    ### Access to Main Aspen Hysys Objects #########################################
    # -----------------------------------------------------------------------------

    # 07 Main Aspen Hysys Document Objects
    HySolver          = HyCase.Solver                      # Access to Hysys Solver
    #    HyFlowsheet       = HyCase.Flowsheet                   # Access to main Flowsheet
    HyOperations      = HyCase.Flowsheet.Operations        # Access to the Unit Operations
    HyMaterialStream  = HyCase.Flowsheet.MaterialStreams   # Access to the material streams
    HyEnergyStream    = HyCase.Flowsheet.EnergyStreams     # Access to the energy streams 


    # 08 Access to Distillation Column Environment

    #   Interfacing with the Aspen Hysys Objects needed to compute the Total
    #   Annual Cost of the Conventional Distillation Column #

    # 08.1 Access to Hysys Distillation Column and Column  Flowsheet
    Column_Name                = HyOperations.Names[0]
    class DistColumn:
        pass
    DistColumn.Column          = HyOperations.Item(Column_Name)
    DistColumn.ColumnFlowsheet = DistColumn.Column.ColumnFlowsheet

    # 08.1.1 Access to Column  objects
    DistColumn.Specifications = DistColumn.ColumnFlowsheet.Specifications # RR/BR/....
    DistColumn.Operations     = DistColumn.ColumnFlowsheet.Operations     # Main TS/Reboiler/Condenser
    DistColumn.FeedStreams    = DistColumn.ColumnFlowsheet.FeedStreams    # Access to Feed Streams (material and energy) for the Column Environment (Main TS, Reboiler y Condenser)

    # 08.1.1.1  Access  to Main TS of the distillation column (Column Environment)
    DistColumn.Main_TS = DistColumn.ColumnFlowsheet.Operations.Item('Main TS')     # Access to Main TS in Column Environment

    # 08.1.1.2 Access to Feed stream object of the Main Tray Section
    DistColumn.FeedMainTS = DistColumn.FeedStreams.Item('Feed')

    # 08.2. Material Streams
    class MaterialStream:
        pass

    MaterialStream.Distillate = HyMaterialStream.Item('Distillate')
    MaterialStream.Bottoms    = HyMaterialStream.Item('Bottoms')
    
    # 08.3. Energy Streams
    class EnergyStream:
        pass
    
    EnergyStream.Qreb  = HyEnergyStream.Item('Qreb')
    EnergyStream.Qcond = HyEnergyStream.Item('Qcond')

    # 09 ...: HYSYS OBJECTS :...
    class HyObject:
        pass

    HyObject.HyApp          = HyApp
    HyObject.HyCase         = HyCase
    HyObject.DistColumn     = DistColumn
    HyObject.MaterialStream = MaterialStream
    HyObject.EnergyStream   = EnergyStream
    HyObject.HySolver       = HySolver
    HyObject.CDC_model_Root = hy_beswt_solution_FilePath                                    # Full   Path to Best Solution Aspen Hysys file
    HyObject.folder_paht    = hy_beswt_solution_FilePath[0:-len(hy_best_model_filename)]    # Folder Path
    
    print( '# Aspen Hysys - Python Interface has been Established....')
    return(HyObject)



