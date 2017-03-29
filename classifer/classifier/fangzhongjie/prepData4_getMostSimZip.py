import os
import pandas as pd
import numpy as np
os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')


# get each zip's 2 encoded 
zipsim_df = pd.read_csv('zipSimilarity/zipsimilarity_tsne.csv')
# Read zip merged file with all demographics features
zipdf = pd.read_csv('zipmerged2010-2015.csv')
# Read zipinfo csv which has the state, county info per zip
zipinfo = pd.read_csv('us_postal_codes.csv')

# merge to get the info into the demo features
zipdfjoined = zipdf.set_index('ZIP').join(zipinfo.set_index('Postal Code'))
del zipdfjoined['Unnamed: 7']
zipdfjoined.reset_index(inplace = True)

# merge with the simi i2 encoded 
zipsiminfo_allmerged = zipsim_df.merge(zipdfjoined,left_on = 'ZIP',right_on='index')
# determine if city/rural/urban size of the zip code
zipsiminfo_allmerged['size'] = ['City' if x >25000 else 'Rural' if x < 50000 else 'Surb' for x in zipsiminfo_allmerged['CURRENT_POP.2015']]
# save
zipsiminfo_allmerged.to_csv('zipSimilarity/allzips_sim_info.csv',index = None)

