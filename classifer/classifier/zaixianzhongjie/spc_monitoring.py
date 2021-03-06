import os
import glob
import pandas as pd
import seaborn as sns
import math
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt
import json
from sklearn import metrics
from spc import *
import sys, getopt
import datetime
from dateutil.parser import parse
from datetime import timedelta
from dateutil.relativedelta import relativedelta

# usage:
# python spc_monitoring.py -t 201612
# Run SPC for this time:  201610

"""
Set target month, if not specified in argument, set today's month
"""
def setTarget(arg = None):
   if arg == None:
      target = datetime.date.today()
   else:
      target = datetime.date(int(arg[:4]),int(arg[4:]),1)


   target += relativedelta(months=-2)

   if len(str(target.month)) == 1:
   		res = str(target.year) + '0' + str(target.month)
   else:
   		res = str(target.year) + str(target.month)

   return res

"""
Validate the date argument format is correct
"""

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y%m')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYYMM")

"""
Input handling
"""

def takeInput(argv):

   target = setTarget()
   
   try:
      opts, args = getopt.getopt(argv,"t:",["target="])
   except getopt.GetoptError:
      print 'spc_monitoring.py -t <yyyymm>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'spc_monitoring.py -t <yyyymm>'
         sys.exit()
      elif opt in ("-t", "--target"):
         validate(arg)
         target = setTarget(arg)
         # print parse(arg)
      else:
         print 'invalid input'

   print 'Run SPC for this time: ', target
   return target


"""
read the df which has residual histories
"""

def getLatestDF():
	# Read current pd file
	df_final = pd.read_csv('../csv/ts_actual_forecast_20161-12.csv')
	return df_final


"""
if the target month is earlier than the latest month in the history df
exit with message this month has been run
"""


def validateTarget(latestDF,target):

	lastMonth = list(latestDF.filter(regex = 'ERR_').columns)[-1].split('_')[1]
	plastM = parse(lastMonth[:4]+'/' + lastMonth[4:])
	ptargetM = parse(target[:4]+'/' + target[4:])

	if ptargetM <= plastM:
		existing_outlier = eval(open('outlier_' + target,'r').read())
		num_outlier = len(existing_outlier)
		print 'The targeted month SPC had been produced, there are',num_outlier,'outliers'
		sys.exit()
"""
Get the actual conv rate of the target month
"""

def getActual(target):

	targetDate = target[:4]+'-'+target[4:]+'-01'
	try:
		atlas = pd.read_csv('../csv/atlas_time_series.csv')
		atlas_t = atlas[atlas.QUOT_MONTH_new == targetDate][['ASSOC_ID','CONV_RATE']]
	except Exception as e:
		print str(e)

	if len(atlas_t) == 0:
		sys.exit('The targeted month actual conv data has not been pulled' )


	return targetDate,atlas_t

"""
Create the actual, socre and err of target month df
"""
def getTargetDF(target,atlas_t):

	targetF = target + '_time_series_scores.csv'
	if os.path.isfile(targetF) == False:
		sys.exit('There is no targeted score file generated yet, please contact model developer')

	tPrediction_ = pd.read_csv(targetF)
	# remove new agents
	tPrediction_ = tPrediction_[tPrediction_['old_score'] == tPrediction_['score']]
	# remove agents who didn't meet threshold
	tPrediction_ = tPrediction_[tPrediction_['old_score'] != 0]
	# get the scores and associate id only
	tPrediction_ = tPrediction_[tPrediction_.CSE_RSLT_IND == 1][['ASSOC_ID','score']]

	targetDF = tPrediction_.merge(atlas_t,on='ASSOC_ID')
	targetDF['ERR'] = targetDF.CONV_RATE - targetDF.score
	targetDF.columns = ['ASSOC_ID','SCORE_'+target,'CONV_RATE_'+target,'ERR_'+target]

	return targetDF


# def threshFilter(targetDate,atlas):
#
# 	# Get last 4 month data only preparing compute thresh
# 	last4M = atlas[atlas['QUOT_MONTH_new'] <= targetDate]
# 	# Apply filter of 40 counts or not
# 	thresh = last4M.groupby('ASSOC_ID')['QUOT_CNT'].agg(np.sum) >= 40
# 	# Reset index
# 	thresh = thresh.reset_index()
# 	# Filter out not meeting quote counts agent
# 	thresh = thresh[thresh.QUOT_CNT == True]
# 	# Delete true or false col
# 	del thresh['QUOT_CNT']
#
# 	return thresh

"""
Append the target df to history df

"""

def newLatestDF(latestDF,targetDF):
	newlatestDF = latestDF.merge(targetDF,on ='ASSOC_ID',how = 'left')
	# newlatestDF = newlatestDF.merge(thresh,on= 'ASSOC_ID', how = 'left')
	newlatestDF.to_csv('../csv/ts_actual_forecast_20161-12.csv',index = None)

	return newlatestDF

"""
Run spc
the commented out section is for plotting
"""

def runSPC(newlatestDF):

	## SPC running
	ERRS = newlatestDF.filter(regex = 'ERR_')
	dlist = []

	for i in range(0,ERRS.shape[0]):
	    x = ERRS.iloc[i,:].tolist()
	    cc = Spc(x, CHART_X_MR_X)
	    if len(cc._find_violating_points()) > 0:
	        d = {}
	        d[newlatestDF.iloc[i,0]] = cc._find_violating_points()
	        dlist.append(d)
	#     cc.get_chart()
	#     plt.title(df_final2.iloc[i,0] + ' forecast error control chart')
	#     plt.annotate(cc._find_violating_points(), xy=(0.05, 0.85), xycoords='axes fraction')
	#     plt.xticks(range(0,10),labels,rotation = 'horizontal')
	#     pp.savefig(fig)
	#     plt.close(fig)
	    
	#pp.close()
	#print dlist

	return dlist


"""
save the spc run result
"""


def saveDlist(dlist,target):

	saveFile = 'spcRun_' + target
	with open(saveFile, 'w') as fout:
		json.dump(dlist, fout)

	outlierInfo = []
	with open(saveFile) as f:
		for line in f:
			outlierInfo.append(json.loads(line))

	# os.remove(saveFile)

	return outlierInfo

"""
count outliers for target month

"""

def spotOutlier(dinfo,target):

	outlier2_3M = {}
	for i in dinfo[0]:
	    if (len(i.values()[0].values()) >=2):
	        outlier2_3M[i.keys()[0]] = (i.values())
	 
	outlier2cont = {}       
	for key, value in outlier2_3M.iteritems():
		if (value[0].values()[1][0] - value[0].values()[0][-1] == 1) and (value[0].values()[1][0] == 10) :
			outlier2cont[key] = value


	print 'There are %i outliers' %(len(outlier2cont))

	saveFile = 'outlier_' + target
	with open(saveFile, 'w') as fout:
		json.dump(outlier2cont, fout)

	return outlier2cont


"""
TODO
1. fix 201701 not returning agent associate id as key in the outlier file -- DONE
2. set the target delta to 2 month -- DONE
3. if target month has been ran, exit printing out number of outlier agents -- DONE
4. generate outlier spc plots monthly
4. write a script to generate report of the last x month, x is an input argument
   report like: append plots of previous x months into one pdf report, and also
   write out those agents quotes, leads, cse conversion rate details


"""


def main(argv):


	os.chdir('/san-data/usecase/atlasid/output_file/')
	target = takeInput(argv)
	latestDF = getLatestDF()
	validateTarget(latestDF,target)
	targetDate,atlas_t = getActual(target)
	targetDF = getTargetDF(target,atlas_t)
	#thresh = threshFilter(targetDate,atlas)
	newlatestDF = newLatestDF(latestDF,targetDF)
	dlist = runSPC(newlatestDF)
	dinfo = saveDlist(dlist,target)
	outlier2cont = spotOutlier(dinfo,target)


if __name__ == "__main__":
   main(sys.argv[1:])

# validate target date in the beginginig before loading any file
# add try, except and logging
# add func if date is already ran, refer ppl to an existing file where records all months outliers
# add lines to save newupdated latest df

# jan = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/jan_time_series_scores.csv')
# feb = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/feb_time_series_scores.csv')
# march = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/mar_time_series_scores.csv')
# april = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/apr_time_series_scores.csv')
# may = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/may_time_series_scores.csv')
# june = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/jun_time_series_scores.csv')
# july = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/jul_time_series_scores.csv')
# aug = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/aug_time_series_scores.csv')
# sep = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/sep_time_series_scores.csv')
# oct = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/oct_time_series_scores.csv')
# nov = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/nov_time_series_scores.csv')

# atlas = pd.read_csv('/san-data/usecase/atlasid/csv/atlas_time_series.csv')

# jan = jan[jan.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
# feb = feb[feb.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
# march = march[march.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
# april = april[april.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
# may = may[may.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
# june = june[june.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
# july = july[july.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
# aug = aug[aug.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
# sep = sep[sep.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
# oct = oct[oct.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
# nov = nov[nov.CSE_RSLT_IND == 1][['ASSOC_ID','score']]


# atlas = atlas[atlas.CSE_RSLT_IND == 1]
# atlas_jan = atlas[atlas.QUOT_MONTH_new == '2016-01-01'][['ASSOC_ID','CONV_RATE']]
# atlas_feb = atlas[atlas.QUOT_MONTH_new == '2016-02-01'][['ASSOC_ID','CONV_RATE']]
# atlas_march = atlas[atlas.QUOT_MONTH_new == '2016-03-01'][['ASSOC_ID','CONV_RATE']]
# atlas_april = atlas[atlas.QUOT_MONTH_new == '2016-04-01'][['ASSOC_ID','CONV_RATE']]
# atlas_may = atlas[atlas.QUOT_MONTH_new == '2016-05-01'][['ASSOC_ID','CONV_RATE']]
# atlas_june = atlas[atlas.QUOT_MONTH_new == '2016-06-01'][['ASSOC_ID','CONV_RATE']]
# atlas_july = atlas[atlas.QUOT_MONTH_new == '2016-07-01'][['ASSOC_ID','CONV_RATE']]
# atlas_aug = atlas[atlas.QUOT_MONTH_new == '2016-08-01'][['ASSOC_ID','CONV_RATE']]
# atlas_sep = atlas[atlas.QUOT_MONTH_new == '2016-09-01'][['ASSOC_ID','CONV_RATE']]
# atlas_oct = atlas[atlas.QUOT_MONTH_new == '2016-10-01'][['ASSOC_ID','CONV_RATE']]
# atlas_nov = atlas[atlas.QUOT_MONTH_new == '2016-11-01'][['ASSOC_ID','CONV_RATE']]

# dfs = [atlas_jan,atlas_feb,atlas_march,atlas_april,atlas_may,atlas_june,atlas_july,atlas_aug,atlas_sep,atlas_oct,atlas_nov,jan,feb,march,april,may,june,july,aug,sep,oct,nov]
# df_final = reduce(lambda left,right: pd.merge(left,right,on='ASSOC_ID'), dfs)

# conv_cols = ['CONV_RATE_2016'+ str(i) for i in range(1,12)]
# score_cols = ['SCORE_2016'+ str(i) for i in range(1,12)]

########################################################
# os.chdir('/san-data/usecase/atlasid/output_file/')
# atlas = pd.read_csv('/san-data/usecase/atlasid/csv/atlas_time_series.csv')
# atlas_newmonth = atlas[atlas.QUOT_MONTH_new == '2017-01-01'][['ASSOC_ID','CONV_RATE']]
# newmonth = pd.read_csv('/san-data/usecase/atlasid/output_file/201701_time_series_scores.csv')
# newmonth = newmonth[newmonth.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
# df_final = pd.read_csv('../csv/ts_actual_forecast.csv')

# newmonth.columns = ['ASSOC_ID','SCORE_201701']
# atlas_newmonth.columns = ['ASSOC_ID','CONV_RATE_201701']
# newmonth_merged = newmonth.merge(atlas_newmonth,on = 'ASSOC_ID')
# df_final = df_final.merge(newmonth_merged,on = 'ASSOC_ID')
# cols = df_final.columns.tolist()
# newcols = cols[:13] + [cols[-1]] + cols[13:25] + [cols[-2]] + cols[25:-2]
# df_final = df_final[newcols]
# df_final['ERR_201701'] = df_final['CONV_RATE_201701'] - df_final['SCORE_201701']
# df_final.to_csv('../csv/ts_actual_forecast.csv',index = None)
########################################################


# cols = ['ASSOC_ID'] + conv_cols + score_cols
# df_final.columns = cols

# for i in range(1,12):
#     df_final['ERR_2016'+str(i)] = df_final['CONV_RATE_2016'+str(i)] - df_final['SCORE_2016'+str(i)]

# df_final.to_csv('ts_actual_forecast_20161-11.csv',index = None)