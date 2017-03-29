import os
import pandas as pd
import numpy as np
os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')

# usage example getMostSimZip(target_ZIP,targetdframe,candidframe)
def getMostSimZip(target_ZIP,targetdframe,candidframe):

# target_ZIP is the zip we are going to find a most similar match for it, this zip
# is usually a zip without state farm info
#targetdframe is zipsiminfo_allmerged which has all 40k zips info and contais target_ZIP
#candidframe is the state farm data zips such as feature2010agg_byZIP which has the candidate zips

# usage example: getMostSimZip(1001,zipsiminfo_allmerged,feature2010agg_byZIP)

	# searc within +/- 0.5 degree which at most is about +/- 70 miles radius search
	# target_ZIP = 1001
	target_LAT = targetdframe[targetdframe.ZIP == target_ZIP].Latitude.values[0]
	target_LON = targetdframe[targetdframe.ZIP == target_ZIP].Longitude.values[0]
	target_SIZE = targetdframe[targetdframe.ZIP == target_ZIP]['size'].values[0]

	#size mask
	maskSize = targetdframe['size'] == target_SIZE
	# lat mask
	maskLat = (targetdframe['Latitude'] >= target_LAT - 0.5) & (targetdframe['Latitude'] <= target_LAT + 0.5)
	# lon mask
	maskLon = (targetdframe['Longitude'] >= target_LON - 0.5) & (targetdframe['Longitude'] <= target_LON + 0.5)
	# combine mask
	mask = maskSize & maskLon & maskLat

	# join with all zips to get those info for state farm data zips
	dframe = targetdframe[targetdframe.ZIP.isin(list(candidframe.HOMEZIP))]
	# apply mask and filter data
	simiZips = dframe[mask]

	from scipy.spatial import distance

	target_XY = (targetdframe[targetdframe.ZIP == target_ZIP].x.values[0],targetdframe[targetdframe.ZIP == target_ZIP].y.values[0])
	dist = 100
	mostSimZip = None
	for i in range(simiZips.shape[0]):
		candidate_XY = (simiZips.iloc[i,0],simiZips.iloc[i,1])
		candidate_dist = distance.euclidean(target_XY,candidate_XY)
		if (candidate_dist < dist) & (simiZips.iloc[i,2]!= target_ZIP):
			mostSimZip = simiZips.iloc[i,2]

	if mostSimZip == None:
		print "yes"
		simiZips = candidframe
		dist = float('inf')
		for i in range(simiZips.shape[0]):
			candidate_XY = (simiZips.iloc[i,0],simiZips.iloc[i,1])
			candidate_dist = distance.euclidean(target_XY,candidate_XY)
			if (candidate_dist < dist) & (simiZips.iloc[i,2]!= target_ZIP):
				mostSimZip = simiZips.iloc[i,2]

	print mostSimZip

	return mostSimZip

# treat as we will produce NMA in all zipcodes
# use demographic features of those zips as features
# the features were aggregated by the neibor zips that was suggested by history data
# any zip that has no history data will use the sim matrix

# usage example: getMostSimZip(1001,zipsiminfo_allmerged,feature2010agg_byZIP)
zipsiminfo_allmerged = pd.read_csv('zipSimilarity/allzips_sim_info.csv')
feature2015agg_byZIP = pd.read_csv('top10ZipFeatures/byZIPtop10ZipFeaturesAgg_2015.csv')

# Get the list of zips where we don't have agents 
zipAgents = feature2015agg_byZIP.HOMEZIP
zipAll = zipsiminfo_allmerged.ZIP
zipNoAgents = set(zipAll) - set(zipAgents)

# Get similar zip of state farm agent placed to those zips that we haven't placed agent
# this can take long to finish
similarZips = [getMostSimZip(x,zipsiminfo_allmerged,feature2015agg_byZIP) for x in zipNoAgents]
t_simi_zips = pd.DataFrame(list(zipNoAgents),similarZips)
t_simi_zips.reset_index(inplace = True)
t_simi_zips.columns = ['similarzip','noagentzip']
t_simi_zips.to_csv('zipSimilarity/noAgent_Sim_Zips.csv',index = None)

# it has about 2068 zips haave no similar zip returned in 75 miles radius, so relook for similar zips nation wide

newsimizip = [getMostSimZip(x,zipsiminfo_allmerged,feature2015agg_byZIP)for x in t_simi_zips[t_simi_zips.similarzip.isnull()].noagentzip]
#: 33690

# this is current new agent training model frame look alike
yX_DF_NewAgents3 = pd.read_csv('datapull/tplus3XY_newAgents.csv')

# get the zip code of those agents in the above list
# then get zip codes not 













