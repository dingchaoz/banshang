import pandas as pd
import numpy as np
import os
os.chdir('/san-data/usecase/agentpm/AgentProductionModel')

# the original top 10 source zips for each agent
# dfRes = pd.read_csv('radiusZips.csv')

# Groupby homezip and tuple all top 10zips 
# dfRes_byZip = dfRes.groupby('HOMEZIP')['TOP10ZIPS'].apply(lambda x: list(x)).reset_index()
# list(dfRes_byZip[dfRes_byZip['HOMEZIP'] == '89117'].TOP10ZIPS)


## take the mean across agents to aggregate to per zip feature

feature2015 = pd.read_csv('top10ZipFeatures/top10ZipFeatures_2015.csv')

feature2015_byZIP = feature2015.groupby('HOMEZIP')[feature2015.columns[15:]].mean().reset_index()

feature2014_byZIP.to_csv('top10ZipFeatures/byZIPtop10ZipFeatures_2015.csv',index = None)

feature2014 = pd.read_csv('top10ZipFeatures/top10ZipFeatures_2014.csv')

feature2014_byZIP = feature2014.groupby('HOMEZIP')[feature2014.columns[15:]].mean().reset_index()

feature2014_byZIP.to_csv('top10ZipFeatures/byZIPtop10ZipFeatures_2014.csv',index = None)

feature2013 = pd.read_csv('top10ZipFeatures/top10ZipFeatures_2013.csv')

feature2013_byZIP = feature2013.groupby('HOMEZIP')[feature2013.columns[15:]].mean().reset_index()

feature2013_byZIP.to_csv('top10ZipFeatures/byZIPtop10ZipFeatures_2013.csv',index = None)

feature2012 = pd.read_csv('top10ZipFeatures/top10ZipFeatures_2012.csv')

feature2012_byZIP = feature2012.groupby('HOMEZIP')[feature2012.columns[15:]].mean().reset_index()

feature2012_byZIP.to_csv('top10ZipFeatures/byZIPtop10ZipFeatures_2012.csv',index = None)

feature2011 = pd.read_csv('top10ZipFeatures/top10ZipFeatures_2011.csv')

feature2011_byZIP = feature2011.groupby('HOMEZIP')[feature2011.columns[15:]].mean().reset_index()

feature2011_byZIP.to_csv('top10ZipFeatures/byZIPtop10ZipFeatures_2011.csv',index = None)

feature2010 = pd.read_csv('top10ZipFeatures/top10ZipFeatures_2010.csv')

feature2010_byZIP = feature2010.groupby('HOMEZIP')[feature2010.columns[15:]].mean().reset_index()

feature2010_byZIP.to_csv('top10ZipFeatures/byZIPtop10ZipFeatures_2010.csv',index = None)


# produce top 10 neibor zip for each zip we had data for Dan as a display feature in UI
top10zipPerzip2010 = feature2010.drop_duplicates('HOMEZIP',keep = 'first')
top10zipPerzip2011 = feature2011.drop_duplicates('HOMEZIP',keep = 'first')
top10zipPerzip2012 = feature2012.drop_duplicates('HOMEZIP',keep = 'first')
top10zipPerzip2013 = feature2013.drop_duplicates('HOMEZIP',keep = 'first')
top10zipPerzip2014 = feature2014.drop_duplicates('HOMEZIP',keep = 'first')
top10zipPerzip2015 = feature2015.drop_duplicates('HOMEZIP',keep = 'first')

top10zipPerzip2015.to_csv('top10ZipFeatures/top10zipPerzip2015.csv',index = None)
top10zipPerzip2014.to_csv('top10ZipFeatures/top10zipPerzip2014.csv',index = None)
top10zipPerzip2013.to_csv('top10ZipFeatures/top10zipPerzip2013.csv',index = None)
top10zipPerzip2012.to_csv('top10ZipFeatures/top10zipPerzip2012.csv',index = None)
top10zipPerzip2011.to_csv('top10ZipFeatures/top10zipPerzip2011.csv',index = None)
top10zipPerzip2010.to_csv('top10ZipFeatures/top10zipPerzip2010.csv',index = None)

### Aggregate the zip0 - zip9 features
# Create zip0-9 aggregated features

def getAggFeatures(dframe):
	uniquefeatures = dframe.filter(regex = 'zip0').columns.tolist()
	uniquefeatures = [x.split('zip0_')[1] for x in uniquefeatures]


	# Create a placeholder for agged features
	agg_features = pd.DataFrame()
	for i,feature in enumerate(uniquefeatures):
		agg_features[i] = dframe.filter(regex = feature).sum(axis = 1)

	# Add column name
	agg_features.columns = uniquefeatures
	# Add premsum and pifsum columns
	agg_features = pd.concat([dframe.HOMEZIP,agg_features],axis = 1)

	return agg_features

feature2010agg_byZIP = getAggFeatures(feature2010_byZIP)
feature2011agg_byZIP = getAggFeatures(feature2011_byZIP)
feature2012agg_byZIP = getAggFeatures(feature2012_byZIP)
feature2013agg_byZIP = getAggFeatures(feature2013_byZIP)
feature2014agg_byZIP = getAggFeatures(feature2014_byZIP)
feature2015agg_byZIP = getAggFeatures(feature2015_byZIP)

feature2010agg_byZIP.to_csv('top10ZipFeatures/byZIPtop10ZipFeaturesAgg_2010.csv',index = None)
feature2011agg_byZIP.to_csv('top10ZipFeatures/byZIPtop10ZipFeaturesAgg_2011.csv',index = None)
feature2012agg_byZIP.to_csv('top10ZipFeatures/byZIPtop10ZipFeaturesAgg_2012.csv',index = None)
feature2013agg_byZIP.to_csv('top10ZipFeatures/byZIPtop10ZipFeaturesAgg_2013.csv',index = None)
feature2014agg_byZIP.to_csv('top10ZipFeatures/byZIPtop10ZipFeaturesAgg_2014.csv',index = None)
feature2015agg_byZIP.to_csv('top10ZipFeatures/byZIPtop10ZipFeaturesAgg_2015.csv',index = None)




