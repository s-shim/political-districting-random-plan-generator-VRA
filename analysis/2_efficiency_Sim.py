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
resultTable = pd.read_csv('result/2_efficiency.csv')
simIDList = list(set(list(resultTable['Simulation'])))

repWinDist = {}
demWinDist = {}
repVoteDist = {}
demVoteDist = {}
for index, row in resultTable.iterrows():
    repWinDist[row['Simulation'],row['District']] = row['USH12RWin']
    demWinDist[row['Simulation'],row['District']] = row['USH12DWin']
    repVoteDist[row['Simulation'],row['District']] = row['USH12R']
    demVoteDist[row['Simulation'],row['District']] = row['USH12D']

repWinSim = {}
demWinSim = {}
repVoteSim = {}
demVoteSim = {}
for simID in simIDList:
    repWinSim[simID] = 0
    demWinSim[simID] = 0
    repVoteSim[simID] = 0
    demVoteSim[simID] = 0
    
for index, row in resultTable.iterrows():
    repWinSim[row['Simulation']] += repWinDist[row['Simulation'],row['District']]
    demWinSim[row['Simulation']] += demWinDist[row['Simulation'],row['District']]
    repVoteSim[row['Simulation']] += repVoteDist[row['Simulation'],row['District']]
    demVoteSim[row['Simulation']] += demVoteDist[row['Simulation'],row['District']]

repWinCol = []
demWinCol = []
repVoteCol = []
demVoteCol = []
for index, row in tgs.iterrows():
    repWinCol += [repWinSim[row['Simulation']]]
    demWinCol += [demWinSim[row['Simulation']]]
    repVoteCol += [repVoteSim[row['Simulation']]]
    demVoteCol += [demVoteSim[row['Simulation']]]
    
tgs['repWin'] = repWinCol
tgs['demWin'] = demWinCol
tgs['repVote'] = repVoteCol
tgs['demVote'] = demVoteCol

tgs.to_csv(r'result/2_efficiency_Sim.csv',index=False)

