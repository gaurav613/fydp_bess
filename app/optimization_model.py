# -*- coding: utf-8 -*-
"""model_fullyear.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cel-7-QBi1uLYRP61dR5yOwgNNzomOJ2
"""   
import random
import gurobipy as grb
import pandas as pd
import numpy as np

# Gurobi WLS license file
# Your credentials are private and should not be shared or copied to public repositories.
# Visit https://license.gurobi.com/manager/doc/overview for more information.
WLSACCESSID='6467d903-5c72-46b0-89de-4cc058f8df40'
WLSSECRET='2e64aa23-f34c-4f10-bf2f-25ec48e06700'
LICENSEID=770264

# Setup Gurobi License for model
# Create environment with WLS license
e = grb.Env(empty=True)
e.setParam('WLSACCESSID', WLSACCESSID)
e.setParam('WLSSECRET', WLSSECRET)
e.setParam('LICENSEID', LICENSEID)
# e.start()

# Create the model within the Gurobi environment
# opt_model = grb.Model(name="MIP Model",env=e)


def optimize(user_inputs):
  opt_model = grb.Model(name="MIP Model")
  # read inputs from user
  bill_type = user_inputs['BillType']

  if bill_type=="tiered":
        pass

  elif bill_type == "timeofuse":
        # UmN = household usage during on-peak [kWh]
        UN_m = user_inputs['On_Peak_KWH']
        # UmM = household usage during mid-peak [kWh]
        UM_m = user_inputs['Mid_Peak_KWH']
        # UmF = household usage during off-peak [kWh]
        UF_m = user_inputs['Off_Peak_KWH']

        # Month of the user's provided eletricity bill
        month_bill = int(user_inputs['Month_of_bill'][:2])
        # print(month_bill)
        # Nearest geographic location of the household
        user_geo = 'Toronto'

        # Additional charges
        del_charge = user_inputs['DeliveryCharges']
        reg_charge = user_inputs['RegulatoryCharges']
        ####
        
  # Read backend data from github
  intensity_scores = pd.read_csv("https://raw.githubusercontent.com/gaurav613/fydp_bess/main/Data/Intensity_score.csv")
  var_geo_month = pd.read_csv("https://raw.githubusercontent.com/gaurav613/fydp_bess/main/Data/Month_Variation.csv")

  """Variables: Decision Variables and Parameters"""
  # return user_inputs
  # Decision Variables

  # indexes for time sections
  months = range(1,13)
  hours = range(0,24)
  years = range(0,10)
  # Total cost
  cost_my  = {(i,k):opt_model.addVar(vtype=grb.GRB.CONTINUOUS, 
                                    name="cost_{0}_N/A_{1}".format(i,k)) 
  for i in months for k in years}
  # Total GHG Emission
  ghg_m  = [opt_model.addVar(vtype=grb.GRB.CONTINUOUS, name="ghg_{}_N/A_N/A".format(month)) for month in months]

  # Total cost in each time-of-use period
  # TN_m: on-peak period
  TN_my = {(i,k):opt_model.addVar(vtype=grb.GRB.CONTINUOUS,
                                  name="TN_N/A_{0}_{1}".format(i,k)) 
  for i in months for k in years}
  # TM_m: mid-peak period
  TM_my = {(i,k):opt_model.addVar(vtype=grb.GRB.CONTINUOUS,
                                  name="TM_N/A_{0}_{1}".format(i,k)) 
  for i in months for k in years}
  # TF_m: off-peak period
  TF_my = {(i,k):opt_model.addVar(vtype=grb.GRB.CONTINUOUS,
                                  name="TF_N/A_{0}_{1}".format(i,k)) 
  for i in months for k in years}
  # binary indicators for hour span to charge or discharge
  HC_hm  = {(i,j):opt_model.addVar(vtype=grb.GRB.BINARY,
                          name="HC_{0}_{1}_N/A".format(i,j)) 
  for i in months for j in hours}

  HD_hm  = {(i,j):opt_model.addVar(vtype=grb.GRB.BINARY,
                          name="HD_{0}_{1}_N/A".format(i,j)) 
  for i in months for j in hours}

  # energy charged at hour h
  PC_hm = {(i,j):opt_model.addVar(vtype=grb.GRB.CONTINUOUS,
                          name="PC_{0}_{1}_N/A".format(i,j)) 
  for i in months for j in hours}

  # energy discharged at hour h
  PD_hm = {(i,j):opt_model.addVar(vtype=grb.GRB.CONTINUOUS,
                          name="PD_{0}_{1}_N/A".format(i,j)) 
  for i in months for j in hours}

  # energy from grid at hour h
  PG_hm = {(i,j):opt_model.addVar(vtype=grb.GRB.CONTINUOUS,
                          name="PG_{0}_{1}_N/A".format(i,j)) 
  for i in months for j in hours}

  # State/inventory of battery energy stored
  SoC_hm = {(i,j):opt_model.addVar(vtype=grb.GRB.CONTINUOUS,
                          name="SoC_{0}_{1}_N/A".format(i,j)) 
  for i in months for j in hours}

  #### User inputs
  # UmN = household usage during on-peak [kWh]
  # UN_m = 500
  # # UmM = household usage during mid-peak [kWh]
  # UM_m = 300
  # # UmF = household usage during off-peak [kWh]
  # UF_m = 380
  # # Ph,mG ,Ph,mU = Energy from the grid/usage by user at hour, h [kWh]
  PU_hm = []# usage

  # # Initialize the fixed usage demand
  for month in months:
    PU_hm.append([0]*24)

  # # Month of the user's provided eletricity bill
  # month_bill = 1

  # # Nearest geographic location of the household
  # user_geo = 'Toronto'

  # # Additional charges
  # del_charge = 20
  # reg_charge = 10
  ####

  ## Fixed parameters from backend
  # Fixed GHG intensity factor
  I_hm = []
  for month in months:
    I_hm.append(intensity_scores[intensity_scores['Month'] == month]['avg_GHGIntensity'].tolist())

  # monthly variation factor based on the provided user monthly bill
  geo_var = var_geo_month.loc[var_geo_month['City'] == user_geo]
  geo_var = geo_var.drop(columns=['City'])
  geo_var = geo_var.values.flatten().tolist()

  Demand_var_m = [0 for month in months]
  for i in months:
    Demand_var_m[i-1] = geo_var[i-1]/geo_var[month_bill-1]

  ## TOU parameters
  # Time-of-use hours in winter season
  # on peak hours
  on_hours_winter = [7,8,9,10,17,18]
  # mid peak hours
  mid_hours_winter = [11,12,13,14,15,16]
  # off peack hours
  off_hours_winter = [0,1,2,3,4,5,6,19,20,21,22,23]

  # Time-of-use hours in summer season
  # on peak hours
  on_hours_summer = [11,12,13,14,15,16]
  # mid peak hours
  mid_hours_summer = [7,8,9,10,17,18]
  # off peack hours
  off_hours_summer = [0,1,2,3,4,5,6,19,20,21,22,23]

  # Winter months
  months_winter = [1,2,3,4,11,12]
  # Summer months
  months_summer = [5,6,7,8,9,10]

  ## eletricity rates
  # CN = fixed on-peak electricity pricing [$/kWh]
  CN = 0.17
  # CM = fixed mid-peak electricity pricing [$/kWh]
  CM = 0.113
  # CF = fixed off-peak electricity pricing [$/kWh]
  CF = 0.082
  # Interest rate
  beta_y = 0.05

  ## Battery specifications
  # Depth of discharge factor [%] (Saved energy for backup)
  depth = 0.8
  # = 90%, efficiency rating of battery
  efficiency = 0.9
  # Max capacity of battery, 13.5 kWh
  capacity = 13.5
  # c=d==5 [kWh], max rate of energy charge/discharge
  rate = 5 #kWh

  ## Converting monthly household usage into hourly usage
  days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31]

  # winter months
  # on-peak periods
  for i in months_winter:
    for j in on_hours_winter:
      PU_hm[i-1][j] = Demand_var_m[i-1]*round(UN_m/days_in_month[i-1]/(6),4)
  # mid-peak periods
  for i in months_winter:
    for j in mid_hours_winter:
      PU_hm[i-1][j] = Demand_var_m[i-1]*round(UM_m/days_in_month[i-1]/(6),4) 
  # off-peak periods
  for i in months_winter:
    for j in off_hours_winter:
      PU_hm[i-1][j] = Demand_var_m[i-1]*round(UF_m/days_in_month[i-1]/(12),4) 

  # summer months
  # on-peak periods
  for i in months_summer:
    for j in on_hours_summer:
      PU_hm[i-1][j] = Demand_var_m[i-1]*round(UN_m/days_in_month[i-1]/(6),4)

  # on-peak periods
  for i in months_summer:
    for j in mid_hours_summer:
      PU_hm[i-1][j] = Demand_var_m[i-1]*round(UM_m/days_in_month[i-1]/(6),4) 
  # on-peak periods
  for i in months_summer:
    for j in off_hours_summer:
      PU_hm[i-1][j] = Demand_var_m[i-1]*round(UF_m/days_in_month[i-1]/(12),4)

  # Constraints

  # State of battery constraints
  # Battery always starts the day at depth of discharge and cannot discharge
  opt_model.addConstrs(SoC_hm[i,0] == (capacity * (1-depth)) for i in months)
  opt_model.addConstrs(PD_hm[i,0] == 0 for i in months)

  # Tracking state of battery across each hour
  opt_model.addConstrs(SoC_hm[i,j-1] + (PC_hm[i,j-1]) - (PD_hm[i,j-1]) == SoC_hm[i,j] for i in months for j in hours[1:])

  # Last hour of the day goes back to the start of the next day
  opt_model.addConstrs(SoC_hm[i,23] + (PC_hm[i,23]) - (PD_hm[i,23]) == SoC_hm[i,0] for i in months)

  # Prevent charging and discharging at same hour
  opt_model.addConstrs(HC_hm[i,j] + HD_hm[i,j] <= 1 for i in months for j in hours)

  # Maximum rate of charge and discharge
  opt_model.addConstrs(PC_hm[i,j] <= rate for i in months for j in hours)
  opt_model.addConstrs(PD_hm[i,j] <= rate for i in months for j in hours)

  # Maximum storage capacity of battery
  opt_model.addConstrs(SoC_hm[i,j] - capacity <= 0 for i in months for j in hours)

  # Minimum battery energy at depth of discharge
  opt_model.addConstrs(SoC_hm[i,j] - (capacity*(1-depth)) >= 0 for i in months for j in hours)

  # Supply & Demand constraint of energy
  opt_model.addConstrs((efficiency*PD_hm[i,j])+ PG_hm[i,j] - (PU_hm[i-1][j]) - PC_hm[i,j] == 0 for i in months for j in hours)

  # Total cost constraints
  for k in years:
    opt_model.addConstrs(grb.quicksum((PG_hm[i,j])*CN for j in on_hours_winter)*days_in_month[i-1]*((1+beta_y)**float(k)) == TN_my[i,k] for i in months_winter)
    opt_model.addConstrs(grb.quicksum((PG_hm[i,j])*CM for j in mid_hours_winter)*days_in_month[i-1]*((1+beta_y)**float(k)) == TM_my[i,k] for i in months_winter)
    opt_model.addConstrs(grb.quicksum((PG_hm[i,j])*CF for j in off_hours_winter)*days_in_month[i-1]*((1+beta_y)**float(k)) == TF_my[i,k] for i in months_winter)

    opt_model.addConstrs(grb.quicksum((PG_hm[i,j])*CN for j in on_hours_summer)*days_in_month[i-1]*((1+beta_y)**float(k)) == TN_my[i,k] for i in months_summer)
    opt_model.addConstrs(grb.quicksum((PG_hm[i,j])*CM for j in mid_hours_summer)*days_in_month[i-1]*((1+beta_y)**float(k)) == TM_my[i,k] for i in months_summer)
    opt_model.addConstrs(grb.quicksum((PG_hm[i,j])*CF for j in off_hours_summer)*days_in_month[i-1]*((1+beta_y)**float(k)) == TF_my[i,k] for i in months_summer)
  # Indicator constraints 
  for i in months:
    for j in hours:
      opt_model.addConstr((HC_hm[i,j] == 0) >> (PC_hm[i,j] == 0.0))
      opt_model.addConstr((HD_hm[i,j] == 0) >> (PD_hm[i,j] == 0.0))
      # Minimum amount of eletricity [kWh] to charge to increment $0.01 based on off-peak price
      opt_model.addConstr((HC_hm[i,j] == 1) >> (PC_hm[i,j] >= 0.012))
      opt_model.addConstr((HD_hm[i,j] == 1) >> (PD_hm[i,j] >= 0.012))

  ## Objective function
  # Aggregate total cost & GHG emissions into one variable
  opt_model.addConstrs(((TN_my[i,k]+TM_my[i,k]+TF_my[i,k])) == cost_my[i,k] for i in months for k in years)
  opt_model.addConstrs(grb.quicksum(I_hm[i-1][j]*PG_hm[i,j] for j in hours) == ghg_m[i-1] for i in months)
  # Set objective functions
  opt_model.setObjectiveN(sum(cost_my[i,k] for i in months for k in years),0,priority=1)
  opt_model.setObjectiveN(grb.quicksum(ghg_m[i-1] for i in months),1,priority=0)
  opt_model.ModelSense = grb.GRB.MINIMIZE

  # Optimize the model
  opt_model.ObjNPriority = 1
  opt_model.optimize()

  # Generate results from model

  # Convert results into a list and then into dataframe
  results = opt_model.getVars()
  results_list = []

  for var in results:
    results_list.append([var.varName,round(var.x,2)])

  results_df = pd.DataFrame (results_list, columns = ['Var', 'Val'])
  results_df[['Var', 'Month','Hour','Year']] = results_df['Var'].str.split('_', expand = True)
  HC_results = results_df[results_df.Var.str.match('HC')]
  HD_results = results_df[results_df.Var.str.match('HD')]
  PC_results = results_df[results_df.Var.str.match('PC')]
  PD_results = results_df[results_df.Var.str.match('PD')]
  PG_results = results_df[results_df.Var.str.match('PG')]
  SoC_results = results_df[results_df.Var.str.match('SoC')]
  SoC_results

  ## Optimization model results
  ## Total cost and total GHG emissions if using a tesla powerwall
  cost_results = results_df[results_df.Var.str.match('cost')]
  ghg_results = results_df[results_df.Var.str.match('ghg')]

  ## Calculating cost savings
  # Compute actual current cost of household
  Act_cost = [[0 for month in months] for year in years]
  cost_bill =  UN_m*CN+UM_m*CM+UF_m*CF 
  for k in years:
    for i in months:
      Act_cost[k][i-1] = round(((1+beta_y)**float(k))*((Demand_var_m[i-1]*cost_bill) + del_charge + reg_charge),2)

  # Compute the estimated cost based on powerwall usage
  Est_cost = [np.round([cost_results['Val'].loc
                        [(cost_results['Month'].astype(int) == i) &
                        (cost_results['Year'].astype(int) == k)].values[0] + 
                        del_charge + reg_charge for i in months],2) for k in years]

  cost_savings = [[np.round(Act_cost[k][i-1] - Est_cost[k][i-1],2) for i in months] for k in years]

  ## Calculating GHG Emissions
  # Compute actual current GHG emissions of household in g/CO2
  Act_GHG = [0 for month in months]

  for i in months:
    Act_GHG[i-1] = round(sum(I_hm[i-1][j]*(PU_hm[i-1][j]) for j in hours),2)

  Est_GHG = [round(ghg_results['Val'].loc[(ghg_results['Month'].astype(int) == i)].values[0],2) for i in months]

  GHG_red = [np.round(Act_GHG[i-1] - Est_GHG[i-1],2) for i in months]

  #### Formatting output data
  cost_output = pd.DataFrame(columns={'Year','Month','Act_cost','Est_cost','Cost_savings'})
  cost_output = pd.DataFrame(columns=['Year','Month','Act_cost','Est_cost','Cost_savings'])
  for k in years:
    cost_output_year = {'Year': [2022+k for month in months],
                        'Month': [month for month in months],
                        'Act_cost': Act_cost[k],
                        'Est_cost': Est_cost[k],
                        'Cost_savings': cost_savings[k]
    }
    cost_output = cost_output.append(pd.DataFrame(cost_output_year), ignore_index=False)


  GHG_output = pd.DataFrame({'Year': [2022 for month in months],
                              'Month': [month for month in months],
                              'Act_GHG': Act_GHG,
                              'Est_GHG': Est_GHG,
                              'GHG_red': GHG_red,
                              })

  return cost_output
  ####