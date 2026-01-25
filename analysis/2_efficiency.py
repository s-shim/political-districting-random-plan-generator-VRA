import pandas as pd
import networkx as nx
# from gurobipy import *
import math
import os
import glob
import copy


nodes = pd.read_csv('../nodes_md_2012.csv')
nodeList = list(nodes['NAME'])
distList = list(set(list(nodes['CD'])))
numDistricts = len(distList)
tgs = pd.read_csv('result/1_TGS.csv')

# Agenda:
# Perform Step 0 (comment out Step 1)
# Perform Step 1 (comment out Step 0)

# =============================================================================
# # Step 0: Construct initial table '2_efficiency.csv'
# planIDArray = []
# for name in glob.glob('../result1b/report/gerryscore_b_*.csv'):
#     planID = int(name[32:36])
#     planIDArray += [int(planID)]
# 
# planIDArray.sort()
# resultTable = pd.read_csv('../result1b/report/gerryscore_b_1000.csv')
# for planID in planIDArray:
#     if planID != 1000:
#         reportScore = pd.read_csv('../result1b/report/gerryscore_b_%s.csv'%planID)
#         for index, row in reportScore.iterrows():
#             resultTable.loc[len(resultTable)] = row
# 
# resultTable.to_csv(r'result/2_efficiency.csv',index=False)    
# =============================================================================


# Step 1: Comupute Efficiency
resultTable = pd.read_csv('result/2_efficiency.csv')
planIDArray = list(set(list(resultTable['Simulation'])))
planIDArray.sort()


republicans = {}
democrats = {}
for index, row in nodes.iterrows():
    republicans[row['NAME']] = int(row['USH12R'])
    democrats[row['NAME']] = int(row['USH12D'])
    

republicansDist = {}
democratsDist = {}
republicansWin = {}
democratsWin = {}
repSim = {}
demSim = {}
for planID in planIDArray:
    repSim[planID] = 0
    demSim[planID] = 0
    if planID < 0:
        for j in range(1,1+numDistricts):
            republicansDist[planID,j] = 0
            democratsDist[planID,j] = 0
            republicansWin[planID,j] = 0
            democratsWin[planID,j] = 0
    else:
        for j in range(numDistricts):
            republicansDist[planID,j] = 0
            democratsDist[planID,j] = 0
            republicansWin[planID,j] = 0
            democratsWin[planID,j] = 0
            
for planID in planIDArray:
    if planID < 0:
        randomPlan = copy.deepcopy(nodes)
        for index, row in randomPlan.iterrows():
            republicansDist[planID,row['CD']] += republicans[row['NAME']]
            democratsDist[planID,row['CD']] += democrats[row['NAME']]
    else:
        randomPlan = pd.read_csv('../result1b/solution/randomPlan_MD2010_b_%s.csv'%planID)
        for index, row in randomPlan.iterrows():
            republicansDist[planID,row['District']] += republicans[row['Node']]
            democratsDist[planID,row['District']] += democrats[row['Node']]
        
for planID in planIDArray:
    if planID < 0:
        for j in range(1,1+numDistricts):
            if republicansDist[planID,j] > democratsDist[planID,j]:
                republicansWin[planID,j] += 1
            else:
                democratsWin[planID,j] += 1
    else:
        for j in range(numDistricts):
            if republicansDist[planID,j] > democratsDist[planID,j]:
                republicansWin[planID,j] += 1
            else:
                democratsWin[planID,j] += 1

republicansColumn = []
democratsColumn = []
republicansWinColumn = []
democratsWinColumn = []
for index, row in resultTable.iterrows():
    planID = row['Simulation']
    j = row['District']
    republicansColumn += [republicansDist[planID,j]]
    democratsColumn += [democratsDist[planID,j]]
    republicansWinColumn += [republicansWin[planID,j]]
    democratsWinColumn += [democratsWin[planID,j]]
            
resultTable['USH12R'] = republicansColumn
resultTable['USH12D'] = democratsColumn
resultTable['USH12RWin'] = republicansWinColumn
resultTable['USH12DWin'] = democratsWinColumn

resultTable.to_csv(r'result/2_efficiency.csv',index=False)





