import pandas as pd
import networkx as nx
# from gurobipy import *
import math
import os
import glob


# define functions
def gerrymanderScore(subG):
    node_sums = {
        source: sum(lengths.values()) 
        for source, lengths in nx.all_pairs_shortest_path_length(subG)
    }
    
    # Pick the node with the minimum sum
    best_node = min(node_sums, key=node_sums.get)
    min_sum = node_sums[best_node]

    return min_sum, best_node


lines = pd.read_csv('../lines_md_2012_add.csv')
nodes = pd.read_csv('../nodes_md_2012.csv')
black_majority_minority = [4, 7]

nodeList = list(nodes['NAME'])
lineList = list(lines['Line'])
distList = list(set(list(nodes['CD'])))
district = {}
for j in distList:
    district[j] = []

G = nx.Graph()
districtID = {}
for u in nodeList:
    [district_u] = nodes.loc[nodes['NAME']==u,'CD']
    j = int(district_u)
    district[j] += [u]
    districtID[u] = j
    G.add_node(u)

for l in lineList:
    [source_l] = lines.loc[lines['Line']==l,'Source']
    [target_l] = lines.loc[lines['Line']==l,'Target']
    G.add_edge(source_l,target_l)

tgs_existing = 0
for j in distList:
    subG = G.subgraph(district[j])
    min_sum, best_node = gerrymanderScore(subG)
    tgs_existing += min_sum
    
print(tgs_existing)
    
planIDArray = [-1]
totalGerryScore = [tgs_existing]
for name in glob.glob('../result1b/report/gerryscore_b_*.csv'):
    planID = int(name[32:36])
    planIDArray += [int(planID)]

planIDArray.sort()

for planID in planIDArray:
    if planID > 0:
        reportRandomPlan = pd.read_csv('../result1b/report/gerryscore_b_%s.csv'%planID)
        tgs = 0
        for index, row in reportRandomPlan.iterrows():
            tgs += row['Gerry Score']
        totalGerryScore += [tgs]

tgsTable = pd.DataFrame()
tgsTable['Simulation'] = planIDArray
tgsTable['TGS'] = totalGerryScore
tgsTable.to_csv(r'result/1_TGS.csv',index=False)
