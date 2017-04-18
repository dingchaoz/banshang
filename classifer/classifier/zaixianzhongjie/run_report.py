import pandas as pd
import os


os.chdir('/san-data/usecase/atlasid/csv')
tsResidual = pd.read_csv('ts_actual_forecast_20161-12.csv')

target = '201701'
outlier = eval(open('../output_file/outlier_' + target,'r').read())

outlier_index_ts = tsResidual[tsResidual.ASSOC_ID.isin(outlier.keys())].index


ERRS = tsResidual[tsResidual.filter(regex = 'ERR_').columns]
ACTUALS = tsResidual[tsResidual.filter(regex = 'CONV_RATE_').columns]
PREDICTS = tsResidual[tsResidual.filter(regex = 'SCORE_').columns]
MONTHS =  [s.split('ERR_')[1] for s in [tsResidual.filter(regex = 'ERR_').columns][0]]

### create df for outlier 1 for plotting

df1 = pd.DataFrame(ERRS.iloc[outlier_index_ts[0],:].reset_index().iloc[:,1])
df2 = pd.DataFrame(ACTUALS.iloc[outlier_index_ts[0],:].reset_index().iloc[:,1])
df3 = pd.DataFrame(PREDICTS.iloc[outlier_index_ts[0],:].reset_index().iloc[:,1])


outlier1 = pd.concat([df1,df2,df3],axis = 1)
outlier1.columns = ['ERR','ACTUAL','PREDICT']
outlier1['MONTH'] = MONTHS
outlier1['MONTH'] = outlier1.MONTH.astype('int')


df_count = pd.DataFrame(atlas[atlas.ASSOC_ID == outlier.keys()[0]][['QUOT_MONTH_new','QUOT_MONTH','CONV_RATE','QUOT_CNT']])
df_count.columns = ['QUOT_MONTH_new','QUOT_MONTH','CONV_RATE','QUOT_CNT']

# Merge
x = outlier1.merge(df_count,left_on = 'MONTH',right_on = 'QUOT_MONTH',how = 'right')
del x['MONTH']
del x['QUOT_MONTH']
x.sort_values(by='QUOT_MONTH_new',inplace = True)