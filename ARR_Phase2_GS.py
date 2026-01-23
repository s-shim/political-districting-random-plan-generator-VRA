import pandas as pd
import networkx as nx
import random
import math
from itertools import product
import copy
import datetime
import time


# define functions
def gerrymanderScore(districtG):
    node_sums = {
        source: sum(lengths.values()) 
        for source, lengths in nx.all_pairs_shortest_path_length(districtG)
    }
    
    # Pick the node with the minimum sum
    best_node = min(node_sums, key=node_sums.get)
    min_sum = node_sums[best_node]

    return min_sum, best_node


def PTBX(seed,numDistricts,G):
    ptbX = {}
    for u in G.nodes():
        for g in range(numDistricts):
            ptbX[u,g] = seed[u,g] * random.random()
            #ptbX[u,g] = halfX[u,g] + (1 - halfX[u,g]) * random.random()
    return ptbX


def ptbXkey(e):
    (u,g) = e
    return ptbX[u,g]


def RMSD_Evaluate(seed,numDistricts,nodeList):     
    RMSD = 0.0
    for u in nodeList:
        for j in range(numDistricts):
            RMSD += (seed[u,j] - 0.5) ** 2
    RMSD = RMSD / (len(nodeList) * numDistricts)
    RMSD = math.sqrt(RMSD)
    return RMSD


def Rounding(nextPairFunction0,numDistricts,district,neighborsOf,done):    
    # next units
    nextPairFunction = copy.deepcopy(nextPairFunction0)
    nextPairs = set()
    nextNodes = []
    for j in range(numDistricts):
        for u in district[j]:
            for v in neighborsOf[u]:
                if done[v] == 0:
                    nextPairs.add((v,j))
                    nextPairFunction[v,j] = 1
                if done[v] == -1:
                    done[v] = 0
                    nextNodes += [v]
                    nextPairs.add((v,j))
                    nextPairFunction[v,j] = 1
    
    while len(nextPairs) > 0:
        (node_maxPair, district_maxPair) = max(nextPairs,key=ptbXkey)
        district[district_maxPair] += [node_maxPair]
        done[node_maxPair] = 1
        nextNodes.remove(node_maxPair) 
        for j in range(numDistricts):
            if nextPairFunction[node_maxPair,j] == 1:
                nextPairFunction[node_maxPair,j] = 0 
                nextPairs.remove((node_maxPair,j))
            
        for v in neighborsOf[node_maxPair]:
            if done[v] == 0:
                nextPairs.add((v,district_maxPair))
                nextPairFunction[v,district_maxPair] = 1
            if done[v] == -1:
                done[v] = 0 
                nextNodes.append(v)
                nextPairs.add((v,district_maxPair))
                nextPairFunction[v,district_maxPair] = 1
    
    return district


def EQERROR(district,population,b_population,min_pop,max_pop,numDistricts):
    totalError = 0
    pop_district = {}
    b_pop_district = {}
    for i in range(numDistricts):
        population_i = 0
        pop_district[i] = 0
        b_pop_district[i] = 0
        for u in district[i]:
            population_i += population[u]
            pop_district[i] += population[u]
            b_pop_district[i] += b_population[u]
        lower_error = min_pop - population_i
        upper_error = population_i - max_pop
        totalError += max(0,lower_error,upper_error)
    return totalError, pop_district, b_pop_district


def b_error2(j):
    return b_error[j]


print(datetime.datetime.now(),'START')
tic = time.time()

# input data and parameters
lines = pd.read_csv('lines_md_2010_add.csv')
nodes = pd.read_csv('nodes_md_2010.csv')
planID = 'District'
census = pd.read_csv('precinct2010.csv') # ADJ_POPULA precinct2010
tol = 0.05
districtIDList = sorted(list(set(nodes[planID])))
numDistricts = len(districtIDList)
nodeList = list(nodes['NAME'])
lineList = list(lines['Line'])
prodList = list(product(nodeList, range(len(districtIDList))))
simID = 1001
num_majority_black = 2
majority_percent = 0.51

done0 = {}
for u in nodeList:
    done0[u] = -1

nextPairFunction0 = {}
for (u,j) in prodList:
    nextPairFunction0[u,j] = 0

# construct adjacency graph and profile census data
population = {}
b_population = {}

G = nx.Graph()

pop_sum = 0
for v in nodeList:    
    G.add_node(v)  
    
    [districtID_v] = nodes.loc[nodes['NAME']==v,planID]

    [population_v] = census.loc[census['NAME']==v,'ADJ_POPULA']
    population[v] = population_v
    pop_sum += population_v    

    [b_population_v] = census.loc[census['NAME']==v,'ADJ_BLACK']
    b_population[v] = b_population_v
    
avg_pop = pop_sum / len(districtIDList)
min_pop = avg_pop * (1 - tol)
max_pop = avg_pop * (1 + tol)
    
for l in lineList:
    [Source_l] = lines.loc[lines['Line']==l,'Source']
    [Target_l] = lines.loc[lines['Line']==l,'Target']

    G.add_edge(Source_l,Target_l)

neighborsOf = {}
for v in nodeList:
    neighborsOf[v] = list(G.neighbors(v))


# define centroid
halfX = {}    
for u in nodeList:
    for j in range(numDistricts):
        halfX[u,j] = 0.5

seed = copy.deepcopy(halfX)
RMSD = RMSD_Evaluate(seed,numDistricts,nodeList)


ptbX = PTBX(seed,numDistricts,G)

# initial none-mpty districts 
#incumbent = pd.read_csv('result2_20260107/solution/randomPlan_MD2010_b_3110.csv') # 3110	10818 
incumbent = pd.read_csv('result2_GS/minGerrySolution_b.csv') # 'result2_GS/minGerryScore_b.csv'

district = {}
for j in range(numDistricts):
    district[j] = []
for index, row in incumbent.iterrows():
    district[row['District']] += [row['Node']]

totalError, pop_district, b_pop_district = EQERROR(district,population,b_population,min_pop,max_pop,numDistricts)
b_error = {}
for j in range(numDistricts):
    b_error[j] = pop_district[j] - (1 / majority_percent) * b_pop_district[j]   
b_list = sorted(list(range(numDistricts)),key=b_error2)
for j in range(num_majority_black):
    totalError += max(0,b_error[b_list[j]])

gerryIncumbent = 0
for j in range(numDistricts):
    subG = G.subgraph(district[j])
    gerryScore, center = gerrymanderScore(subG)
    gerryIncumbent += gerryScore
    
print('totalError of incumbent =',totalError)

bestDistrict = copy.deepcopy(district)
bestTrial = 0
bestError = totalError
bestScore = gerryIncumbent    
trial = 0
print(trial,totalError,bestScore)


totalTrials = 1000000
seed = copy.deepcopy(halfX)
nLocal = 0
move = True
for trial in range(1,totalTrials):
    ptbX = PTBX(seed,numDistricts,G)    
    RMSD = RMSD_Evaluate(seed,numDistricts,nodeList)
    
    # initial none-mpty districts 
    sortList = sorted(prodList, key=ptbXkey, reverse=True)
    district = {}
    doneNodes = []
    done = copy.deepcopy(done0)
    for j in range(numDistricts):
        district[j] = []
    for j in range(numDistricts):
        if len(district[j]) == 0:
            for (u,k) in sortList:
                if k == j:
                    district[j] += [u]
                    done[u] = 1
                    doneNodes += [u]
                    break   
    district = Rounding(nextPairFunction0,numDistricts,district,neighborsOf,done)   
    totalError, pop_district, b_pop_district = EQERROR(district,population,b_population,min_pop,max_pop,numDistricts)
    b_error = {}
    for j in range(numDistricts):
        b_error[j] = pop_district[j] - (1 / majority_percent) * b_pop_district[j]   
    b_list = sorted(list(range(numDistricts)),key=b_error2)
    for j in range(num_majority_black):
        totalError += max(0,b_error[b_list[j]])
    
    if totalError < 0.0001:
        same = True
        for g in range(numDistricts):
            if same == False:
                break
            for u in bestDistrict[g]:
                if u not in district[g]:
                    same = False
                    break
        if same == True:
            nLocal += 1
            move = True
            if random.random() < min(1, nLocal/20) * RMSD:
                seed = copy.deepcopy(halfX)
                nLocal = 0
                move = False
        else:
            nLocal = 0
            move = True
            
            gerryIncumbent = 0
            for j in range(numDistricts):
                subG = G.subgraph(district[j])
                gerryScore, center = gerrymanderScore(subG)
                gerryIncumbent += gerryScore
                
            if bestScore > gerryIncumbent:
                bestScore = gerryIncumbent
                bestError = totalError
                bestTrial = trial
                bestDistrict = copy.deepcopy(district)
                toc = time.time()
                print(bestTrial,bestScore,bestError,toc-tic,datetime.datetime.now())
                
                b_district = {}
                for j in range(numDistricts):
                    b_district[j] = 0
                for j in range(num_majority_black):
                    b_district[b_list[j]] = 1

                districtInverse = {}
                triList = []
                gsList = []
                lenList = []
                avgScore = {}
                connList = []
                vraList = []
                for g in range(numDistricts):
                    vraList += [b_district[g]]
                    triList += [bestTrial]
                    districtG = G.subgraph(bestDistrict[g])
                    connList += [nx.is_connected(districtG)]
                    gs, cen = gerrymanderScore(districtG)
                    gsList += [gs]
                    lenList += [len(bestDistrict[g])]
                    for u in bestDistrict[g]:
                        districtInverse[u] = g
                        avgScore[u] = gs / len(bestDistrict[g])
                gsTable = pd.DataFrame(list(zip(triList,list(range(numDistricts)),vraList,connList,lenList,gsList)),columns =['Trial','District','Black','Connected', 'Size','Gerry Score'])
                gsTable.to_csv(r'result2_GS/minGerryScore_b.csv', index = False)#Check
                        
                districtArray = []
                avgList = []
                vraDList = []
                for v in nodeList:                    
                    vraDList += [b_district[districtInverse[v]]]
                    districtArray += [districtInverse[v]]
                    avgList += [avgScore[v]]
                feasSolution = pd.DataFrame(list(zip(nodeList,districtArray,vraDList,avgList)),columns =['Node','District','Black','avgScore'])
                feasSolution.to_csv(r'result2_GS/minGerrySolution_b.csv', index = False)#Check


    else:
        move = True
        nLocal = 0

    if move == True:
        alpha = 1 / (1 + math.exp(4 * RMSD))
        for g in range(numDistricts):
            for u in G.nodes():
                seed[u,g] = (1 - alpha) * seed[u,g]

        for g in range(numDistricts):
            for u in bestDistrict[g]:
                seed[u,g] += alpha * 1

print(datetime.datetime.now(),'END')
toc = time.time()
print('Elapse time =',toc - tic)







