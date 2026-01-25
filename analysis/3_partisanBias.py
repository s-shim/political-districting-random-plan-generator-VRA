import pandas as pd
import networkx as nx
# from gurobipy import *
import math
import os
import glob


numDistricts = 8
df = pd.read_csv('result/2_efficiency.csv')
tgs = pd.read_csv('result/1_TGS.csv')

republicansDist = {}
democratsDist = {}
for index, row in df.iterrows():
    republicansDist[row['Simulation'],row['District']] = row['USH12R'] 
    democratsDist[row['Simulation'],row['District']] = row['USH12D'] 

simList = list(set(list(df['Simulation'])))


republicansSim = {}
democratsSim = {}
republicansWin = {}
democratsWin = {}
republicansAdj = {}
democratsAdj = {}
repWinSim = {}
demWinSim = {}
for simID in simList:
    republicansSim[simID] = 0
    democratsSim[simID] = 0
    if simID < 0:
        for j in range(1,1+numDistricts):
            republicansSim[simID] += republicansDist[simID,j] 
            democratsSim[simID] += democratsDist[simID,j]
        repShare = republicansSim[simID] / (republicansSim[simID] + democratsSim[simID])
        demShare = democratsSim[simID] / (republicansSim[simID] + democratsSim[simID])        
        repWinSim[simID] = 0
        demWinSim[simID] = 0
        for j in range(1,1+numDistricts):
            republicansAdj[simID,j] = republicansDist[simID,j] * 0.5 / repShare
            democratsAdj[simID,j] = democratsDist[simID,j] * 0.5 / demShare 
            if republicansAdj[simID,j] > democratsAdj[simID,j]:
                republicansWin[simID,j] = 1
                democratsWin[simID,j] = 0
            else:
                republicansWin[simID,j] = 0
                democratsWin[simID,j] = 1
            repWinSim[simID] += republicansWin[simID,j]
            demWinSim[simID] += democratsWin[simID,j]            
    else:
        for j in range(numDistricts):
            republicansSim[simID] += republicansDist[simID,j] 
            democratsSim[simID] += democratsDist[simID,j]
        repShare = republicansSim[simID] / (republicansSim[simID] + democratsSim[simID])
        demShare = democratsSim[simID] / (republicansSim[simID] + democratsSim[simID])        
        repWinSim[simID] = 0
        demWinSim[simID] = 0
        for j in range(numDistricts):
            republicansAdj[simID,j] = republicansDist[simID,j] * 0.5 / repShare
            democratsAdj[simID,j] = democratsDist[simID,j] * 0.5 / demShare 
            if republicansAdj[simID,j] > democratsAdj[simID,j]:
                republicansWin[simID,j] = 1
                democratsWin[simID,j] = 0
            else:
                republicansWin[simID,j] = 0
                democratsWin[simID,j] = 1
            repWinSim[simID] += republicansWin[simID,j]
            demWinSim[simID] += democratsWin[simID,j]            

repWinCol = []
demWinCol = []
for index, row in df.iterrows():
    repWinCol += [republicansWin[row['Simulation'],row['District']]]
    demWinCol += [democratsWin[row['Simulation'],row['District']]]
df['bipartisanR'] = repWinCol    
df['bipartisanD'] = demWinCol
df.to_csv(r'result/3_bipartisan.csv',index=False)    

repSimCol = [] 
demSimCol = []
for index, row in tgs.iterrows():
    simID = row['Simulation']
    print(simID)
    repSimCol += [repWinSim[simID]] 
    demSimCol += [demWinSim[simID]]
tgs['bipartisanR'] = repSimCol            
tgs['bipartisanD'] = demSimCol            
tgs.to_csv(r'result/3_bipartisanSim.csv',index=False)    
            
            
            
            
            
            
            
            
            
            
            
            


