import pandas as pd
import os
os.chdir('/san-data/usecase/agentpm/GeoModel/Auto/')
PREM_predictions = pd.read_csv('PREM_Predict/autoPremSumPredictions.csv')
PIF_predictions = pd.read_csv('PIF_Predict/autoPIFSumPredictions.csv')

# # Look for prediction variance is beyond 1.5
# PIF_predictions.loc[PIF_predictions['2017Prediction']/PIF_predictions['2016Prediction']> 1.5,'2017Prediction'] = PIF_predictions[['2016Prediction','2015PIFSum','2014PIFSum']].mean(axis = 1)

# # Look for prediction variance is below .5
# PIF_predictions.loc[PIF_predictions['2017Prediction']/PIF_predictions['2016Prediction']< 0.5,'2017Prediction'] = PIF_predictions[['2016Prediction','2015PIFSum','2014PIFSum']].mean(axis = 1)
# # function to do a 3 year average

# PIF_predictions.loc[PIF_predictions['2017Prediction']/PIF_predictions['2016Prediction']> 1.5,'2017Prediction'] = PIF_predictions[['2016Prediction','2015PIFSum','2014PIFSum']].mean(axis = 1)

PIF_predictions['2016_Prediction'] = PIF_predictions['2016Prediction']
PIF_predictions['2017_Prediction'] = PIF_predictions[['2016Prediction','2015PIFSum','2014PIFSum']].mean(axis = 1)
PIF_predictions['2018_Prediction'] = PIF_predictions[['2016Prediction','2015PIFSum','2017_Prediction']].mean(axis = 1)
PIF_predictions['2019_Prediction'] = PIF_predictions[['2016Prediction','2018_Prediction','2017_Prediction']].mean(axis = 1)
PIF_predictions['2020_Prediction'] = PIF_predictions[['2019_Prediction','2018_Prediction','2017_Prediction']].mean(axis = 1)

PIF_predictions_mod = PIF_predictions.copy()

del PIF_predictions_mod['2016Prediction']
del PIF_predictions_mod['2017Prediction']
del PIF_predictions_mod['2018Prediction']
del PIF_predictions_mod['2019Prediction']

PIF_predictions_mod.to_csv('PIF_Predict/autoPIFSumPredictions_g.csv')

PREM_predictions['2016_Prediction'] = PREM_predictions['2016Prediction']
PREM_predictions['2017_Prediction'] = PREM_predictions[['2016Prediction','2015PremSum','2014PremSum']].mean(axis = 1)
PREM_predictions['2018_Prediction'] = PREM_predictions[['2016Prediction','2015PremSum','2017_Prediction']].mean(axis = 1)
PREM_predictions['2019_Prediction'] = PREM_predictions[['2016Prediction','2018_Prediction','2017_Prediction']].mean(axis = 1)
PREM_predictions['2020_Prediction'] = PREM_predictions[['2019_Prediction','2018_Prediction','2017_Prediction']].mean(axis = 1)

PREM_predictions_mod = PREM_predictions.copy()

del PREM_predictions_mod['2016Prediction']
del PREM_predictions_mod['2017Prediction']
del PREM_predictions_mod['2018Prediction']
del PREM_predictions_mod['2019Prediction']

PREM_predictions_mod.to_csv('PIF_Predict/autoPREMSumPredictions_g.csv')