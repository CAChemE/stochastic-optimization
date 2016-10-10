# -*- coding: utf-8 -*-

import numpy as np
import os
"""
% -------------------------------------------------------------------------
%   SIMULATION-BASED OPTIMIZATION OF A SINGLE CONVENTIONAL DISTILLATION 
%        COLUMN USING THE PARTICLE SWARM OPTIMIZATION ALGORITHEM
%--------------------------------------------------------------------------
%                                      Juan Javaloyes Antón. Sep 2016 v.3
%--------------------------------------------------------------------------
% # 05 # Total Annual Cost
%--------------------------------------------------------------------------
"""

def tac_column(Problem):
    """
    # ### >> Total Annual Cost << Conventional Distillation Column ########
    #     - Investment costs:
    #           * Tower
    #           * Trays
    #           * Reboiler
    #           * Condenser
    #     - Operating Costs
    #           * Heating Steam
    #           * Cooling Water 
    #----------------------------------------------------------------------
    """
    
       
    # 01 # Recover Hysys Objects from structure Problem
    HyObject       = Problem.HyObject          # Main Aspen Hysys Objects
    MaterialStream = HyObject.MaterialStream   # Column material streams
    EnergyStream   = HyObject.EnergyStream     # Column energy streams
    
    # 02 # Import Data from Aspen Hysys Model
    NT = HyObject.DistColumn.Main_TS.NumberOfTrays               # Column Active  Trays
    
    TD    = MaterialStream.Distillate.Temperature.GetValue('C')  # Distillate Temperature    
    TB    = MaterialStream.Bottoms.Temperature.GetValue('C')     # Residue Temperature
    
    Qcond = EnergyStream.Qcond.HeatFlow.GetValue('kW')           # Condenser duty
    Qreb  = EnergyStream.Qreb.HeatFlow.GetValue('kW')            # Reboiler Duty
    
    # 03 # Run Aspen Hysys Script "Col_diam_V8.SCP" to update column diameter
    #    Problem.HyObject.HyCase.Application.PlayScript(os.path.abspath('Column_Diameter.SCP'))
    column_diameter  =  max( HyObject.HyCase.UtilityObjects.Item('Tray Sizing-1').DiameterValue)  # [m]
    
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<< User Inputs
    # # Equipment and Utility Parameter Cost ##################################
    
    # * Global parameters
    CEPIC_Actual  = 576.1                    # Annual Index 2014
    CEPIC_2001    = 397                      # Base Annual Index
    UpdateFactor = CEPIC_Actual/CEPIC_2001
    
    # * Annualization Factor parameters ***************************************
    i  = 0.1 # interest_rate
    n  = 8   # equipment life time yrs
    
    
    # * Utility Costs *********************************************************
    WATER = 0.354 * (1/1e9) * 3600 * 1e3   # $/GJ [30 ºC to 40-45 ºC] (R.Turton 4º Ed. Table 8.3)               ==> [$ /kW·h]    
    STEAM = 14.04 * (1/1e9) * 3600 * 1e3   # $/GJ Low Pressure Steam [5barg, 160ºC] (R.Turton 4º Ed. Table 8.3) ==> [$ /kW·h]
    YEAR  = 8000                           # Operating hours per year                   
    
    # * Equip Cost Constants (K). See Appendix A - R .Turton ******************
    Ktray  = np.array([2.9949,  0.4465,  0.3961])  # Trays (sieves)               Area    m2
    Ktower = np.array([3.4974,  0.4485,  0.1074])  # Towers (tray)                Volume  m3
    Khx    = np.array([4.3247, -0.3030,  0.1634])  # Heat Echangers (fixed tube)  Area    m2
    
    # * Bare module Cost Factor: direct and indirect costs for each unit ******
    FBMtray  = 1                    # Table A.6 & Figure A.9 (Trays - sieve trays)    
    FBMtower = (2.25 + 1.82 * 1.0)  # Table A.4 & Figure A.8 (Process vessels - vertical (including towers)) 
    FBMhx    = (1.63 + 1.66 * 1.3)  # Table A.4 & Figure A.8 (fixed tube sheet)
    
    # * Cooler ****************************************************************
    Ucooler = 800  # [W/(m2 K)] 
    Twin    = 30   # Temperatura Entrada Agua Refrigeración Condensador [ºC]  
    Twout   = 40   # Temperatura Salida Agua Refrigeración  Condensador [ºC] 
       
    # * Heater ****************************************************************
    Uheater = 820  # [W/(m2 K)] 
    Tstm    = 160  # Low Pressure Steam temperature (R.Turton 4º Ed. Table 8.3)  
    
    # Tower Column
    tray_Spacing = 0.6096  # [m]    
    
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> # END Equipment and Utility Parameter Cost
    
    # 04 # Operating Cost ########################################################
    
    # * Cooling Water Cost [$/yr] *********************************************
    coolingWater_Cost =  Qcond * WATER * YEAR
    
    # * Steam Cost [$/yr] *****************************************************
    Steam_Cost = Qreb * STEAM * YEAR
    
    # 05 # Capital Cost ##########################################################
        
    # * Column dimensions
    column_area   = np.pi * np.square(column_diameter) / 4   # Sieve area [m2]
    column_heigh  = (3 + NT) * tray_Spacing                  # Tower Heigh [m]
    column_volume = column_area * column_heigh               # Volume Tower [m3]
    
    # * Column Shell **********************************************************
    # Purchase cost  for base conditions
    column_Cp0  = 10**( Ktower[0] + Ktower[1] *  np.log10(column_volume) + 
                                    Ktower[2] * (np.log10(column_volume)**2))
    
    # Bare Module cost
    column_CBM_old = column_Cp0     * FBMtower 
    column_CBM     = column_CBM_old * UpdateFactor # [$] ======================
    
    
    # * Column trays **********************************************************
    # Purchase cost  for base conditions
    tray_Cp0  = 10**( Ktray[0] + Ktray[1] *  np.log10(column_area) + 
                                 Ktray[2] * (np.log10(column_area)**2))                     
    # Tray factor
    if NT < 20:
        Fq = 10**(0.4771 + 0.0816 * np.log10(NT) - 0.3473 * (np.log10(NT))**2)
    else:
        Fq = 1
    
                             
    # Bare Module cost
    tray_CBM_old = tray_Cp0     * FBMtray * Fq
    tray_CBM     = tray_CBM_old * NT * UpdateFactor # [$] ================
    
    
    # * Column Condenser ******************************************************
    inc_T_cond = ((TD - Twout) - (TD - Twin))/ np.log ((TD - Twout)/(TD - Twin))
    condenser_area  = Qcond/(Ucooler * inc_T_cond) * 1e3 # *1e3 porque U esta en W.
    
    # Purchase cost  for base conditions
    condenser_Cp0  = 10**( Khx[0] + Khx[1] *  np.log10(condenser_area) + 
                                    Khx[2] * (np.log10(condenser_area)**2))
    
    # Bare Module cost
    condenser_CBM_old = condenser_Cp0     * FBMhx 
    condenser_CBM     = condenser_CBM_old * UpdateFactor # [$] ================
    
    
    # * Column Reboiler *******************************************************
    inc_T_reb     = Tstm - TB
    reboiler_area =  Qreb/(Uheater * inc_T_reb) * 1e3  # *1e3 porque U esta en W.
    
    # Purchase cost  for base conditions
    reboiler_Cp0  = 10**( Khx[0] + Khx[1] *  np.log10(reboiler_area) + 
                                   Khx[2] * (np.log10(reboiler_area)**2))
    
    # Bare Module cost
    reboiler_CBM_old = reboiler_Cp0     * FBMhx 
    reboiler_CBM     = reboiler_CBM_old * UpdateFactor # [$] ==================
    
    
    # 06 # Total Annual Cost #####################################################
    
    # * Total Operating Cost
    Cop = coolingWater_Cost + Steam_Cost
    
    # * Total Capital Cost
    Ccap = column_CBM + tray_CBM + condenser_CBM + reboiler_CBM
    
    # * Annualization factor (R. Smith)
    F = i*(1 + i)**n /((1 + i)**n - 1);
    
    # * TAC ===================================================================
    TAC = (Cop + Ccap * F) * 1e-6 # [MM $/yr]
    # ============================================== END TAC calculations #####    
    
    class ColumnCost:
        pass
    ColumnCost.CoolingWater = coolingWater_Cost
    ColumnCost.Stea         = Steam_Cost
    ColumnCost.Shell        = column_CBM
    ColumnCost.Trays        = tray_CBM
    ColumnCost.condenser    = condenser_CBM
    ColumnCost.reboiler     = reboiler_CBM
    ColumnCost.F            = F
    ColumnCost.TAC          = TAC
    
    return (ColumnCost)