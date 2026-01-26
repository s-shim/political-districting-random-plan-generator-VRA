import math
import numpy as np
import pandas as pd


def declination(vals):
    """ Compute the declination of an election.
    """
    Rwin = sorted(filter(lambda x: x <= 0.5, vals))
    Dwin = sorted(filter(lambda x: x > 0.5, vals))
    # Undefined if each party does not win at least one seat
    if len(Rwin) < 1 or len(Dwin) < 1:
        return False
    theta = np.arctan((1-2*np.mean(Rwin))*len(vals)/len(Rwin))
    gamma = np.arctan((2*np.mean(Dwin)-1)*len(vals)/len(Dwin))
    # Convert to range [-1,1]
    # A little extra precision just in case.
    return 2.0*(gamma-theta)/3.1415926535

# =============================================================================
# vals = [0.315462694,0.615413003,0.651527319,0.667727352,0.691374888,0.718754142,0.782400602,0.79353628]
# declination = declination(vals)
# print(declination)
# =============================================================================


dfDist = pd.read_csv('result/4_bipartisan.csv')
dfSim = pd.read_csv('result/4_bipartisanSim.csv')

dRate = {}
for simID in list(dfSim['Simulation']):
    dRate[simID] = []
    
for index, row in dfDist.iterrows():
    dRate[row['Simulation']] += [row['USH12D'] / (row['USH12D'] + row['USH12R'])]

dec = []
for index, row in dfSim.iterrows():
    vals = sorted(dRate[row['Simulation']])
    decVal = declination(vals)
    dec += [decVal]

dfSim['Declination'] = dec
dfSim.to_csv(r'result/5_declinationSim.csv',index=False)