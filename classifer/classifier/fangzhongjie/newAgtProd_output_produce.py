import os
import pandas as pd
import numpy as np
os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')

# the similar zip matching to non-agent-zip
t_simi_zips = pd.read_csv('zipSimilarity/noAgent_Sim_Zips.csv')
# sim zips completed info csv
zipsiminfo_allmerged = pd.read_csv('zipSimilarity/allzips_sim_info.csv')
# the features of agent-exist-zip
feature2015agg_byZIP = pd.read_csv('top10ZipFeatures/byZIPtop10ZipFeaturesAgg_2015.csv')

# merge to get no-agent-zip's similar zips' neiborzip demo features
merged_noagentzip = t_simi_zips.merge(feature2015agg_byZIP,left_on='similarzip',right_on='HOMEZIP')
del merged_noagentzip['similarzip']
del merged_noagentzip['HOMEZIP']
merged_noagentzip.rename(columns={'noagentzip': 'HOMEZIP',}, inplace=True)

# concat with existing agent zip's demo features to get all
noagtzip_included_feature2015agg_byZIP = pd.concat([feature2015agg_byZIP,merged_noagentzip],axis = 0)

#manually assign values to those feature columns 
noagtzip_included_feature2015agg_byZIP['pifsum'] = 0
noagtzip_included_feature2015agg_byZIP['premsum'] = 0
noagtzip_included_feature2015agg_byZIP['agtstcode'] = 0
"""
needs use the exact market_area def TODO
"""
areas = list (set(yX_DF_NewAgents5.MARKET_AREA))
noagtzip_included_feature2015agg_byZIP['MARKET_AREA'] = np.random.choice(areas,noagtzip_included_feature2015agg_byZIP.shape[0])
noagtzip_included_feature2015agg_byZIP['STCODE'] = 0
noagtzip_included_feature2015agg_byZIP['APPT_TYPE'] = 1
noagtzip_included_feature2015agg_byZIP['APPT_DATE'] = '2016-01-01'
noagtzip_included_feature2015agg_byZIP['NEW_MARKET'] = 1
noagtzip_included_feature2015agg_byZIP['asgn_type2'] = 1
noagtzip_included_feature2015agg_byZIP['ASGN_DATE'] = '2016-01-01'
noagtzip_included_feature2015agg_byZIP['SUM_of_ASGN_A_POLS'] = 0
noagtzip_included_feature2015agg_byZIP['SUM_of_ASGN_A_PREM'] = 0
noagtzip_included_feature2015agg_byZIP['SUM_of_ASGN_F_POLS'] = 0
noagtzip_included_feature2015agg_byZIP['SUM_of_ASGN_F_PREM'] = 0

noagtzip_included_feature2015agg_byZIP.to_csv('datapull/ProdAllZipsFeatures_newAgents.csv',index = None)

# this is current new agent training model frame look alike
yX_DF_NewAgents5 = pd.read_csv('datapull/tplus5XY_newAgents.csv')

# get the zip code of those agents in the above list
# then get zip codes not 













