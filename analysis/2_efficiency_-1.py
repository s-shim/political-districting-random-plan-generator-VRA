import pandas as pd
import networkx as nx
# from gurobipy import *
import math
import os
import glob


nodes = pd.read_csv('../nodes_md_2012.csv')
nodeList = list(nodes['NAME'])
distList = list(set(list(nodes['CD'])))
numDistricts = len(distList)


# Step 1: Comupute Efficiency
resultTable = pd.read_csv('result/2_efficiency-1.csv')
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
for planID in planIDArray:
    for j in distList:
        republicansDist[planID,j] = 0
        democratsDist[planID,j] = 0
        republicansWin[planID,j] = 0
        democratsWin[planID,j] = 0
            
    for index, row in nodes.iterrows():
        republicansDist[planID,row['CD']] += republicans[row['NAME']]
        democratsDist[planID,row['CD']] += democrats[row['NAME']]
        
    for j in distList:
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

resultTable.to_csv(r'result/2_efficiency-1.csv',index=False)





