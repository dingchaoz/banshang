import os
import pandas as pd
import numpy as np
os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')

# treat as we will produce NMA in all zipcodes
# use demographic features of those zips as features
# the features were aggregated by the neibor zips that was suggested by history data
# any zip that has no history data will use the sim matrix


# this is current new agent training model frame look alike
yX_DF_NewAgents3 = pd.read_csv('datapull/tplus3XY_newAgents.csv')

# get the zip code of those agents in the above list
# then get zip codes not 