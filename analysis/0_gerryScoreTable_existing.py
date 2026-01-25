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
    
simList = []
gsList = []
lenList = []
avgScore = {}
connList = []
vraList = []
for g in distList:
    if g in black_majority_minority:
        vraList += [1]
    else:
        vraList += [0]        
    simList += [-1]
    subG = G.subgraph(district[g])
    connList += [nx.is_connected(subG)]
    gs, cen = gerrymanderScore(subG)
    gsList += [gs]
    lenList += [len(district[g])]
    for u in district[g]:
        avgScore[u] = gs / len(district[g])
gsTable = pd.DataFrame(list(zip(simList,distList,vraList,connList,lenList,gsList)),columns =['Simulation','District','Black','Connected', 'Size','Gerry Score'])
gsTable.to_csv(r'result/2_efficiency-1.csv', index = False)#Check
