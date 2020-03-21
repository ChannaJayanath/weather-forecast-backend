import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from tensorflow import keras

###################### import data #################################
df1 = pd.read_csv(str(Path(__file__).resolve().parents[1]/"LSTM"/"data"/"B.csv"))
df2 = pd.read_csv(str(Path(__file__).resolve().parents[1]/"LSTM"/"data"/"CWL.csv"))
df3 = pd.read_csv(str(Path(__file__).resolve().parents[1]/"LSTM"/"data"/"K.csv"))
df4 = pd.read_csv(str(Path(__file__).resolve().parents[1]/"LSTM"/"data"/"MR.csv"))

output={}
######################## preprocessing #####################################
df1 = df1.set_index('Date')
df1.index = pd.to_datetime(df1.index)
df2 = df2.set_index('Date')
df2.index = pd.to_datetime(df2.index)
df3 = df3.set_index('Date')
df3.index = pd.to_datetime(df3.index)
df4 = df4.set_index('Date')
df4.index = pd.to_datetime(df4.index)

#hourly arranged

data_columns_B = ['BR','Btem']
df1= df1[data_columns_B].resample('H').mean()
data_columns_K = ['KR','Ktem']
df3= df3[data_columns_K].resample('H').mean()
data_columns_WL = ['WL']
df2= df2[data_columns_WL].resample('H').mean()
data_columns_MC = ['MR','CR']
df4= df4[data_columns_MC].resample('H').mean()


############################# Merging data ##############################################
df_A = df1.reset_index()
df_B = df2.reset_index()
df_C = df3.reset_index()
df_D = df4.reset_index()
df_E = df2.copy()

df_A.columns = ['Date', 'Batalagoda_rain-fall', 'Btemperature']
df_B.columns = ['Date', 'water-level']
df_C.columns = ['Date', 'Kurunegala_rain-fall', 'Ktemperature']
df_D.columns = ['Date', 'Mediyawa_rain-fall', 'Chilaw_rain-fall']
df = pd.merge(df_A, df_C, on='Date', how='outer')
df = df.merge(df_D, on='Date', how='outer')
df = df.merge(df_B, on='Date', how='outer')
df = df.set_index('Date')
df.index = pd.to_datetime(df.index)
#Handling Missing values
df = df.dropna()

############################### Making Sequences ###################################

# split a multivariate sequence into samples
def split_sequences_daily(sequences, timeOffset):
    X, y = list(), list()
    for index, row in sequences.iterrows():
        end_ix = index + timeOffset
        # get size of final output sequence
        arr_size = timeOffset.days + 1
        # check if we are beyond the dataset
        if (end_ix in sequences.index.values):
            break
        # gather input and output parts of the pattern
        seq_x = sequences[index:end_ix][['water-level','Batalagoda_rain-fall','Btemperature','Kurunegala_rain-fall','Ktemperature','Mediyawa_rain-fall','Chilaw_rain-fall']].reset_index().values
        seq_y = sequences[end_ix: end_ix]['water-level'].reset_index().values
        # arr_size = timeOffset.hours + 1
        #adding first timestep water level to x sequence
        wl_seq = np.zeros(seq_x.shape[0])
        wl_seq[0] = sequences[index:index][['water-level']].values
        seq_x[:, -1] = wl_seq

        if(sequences[index:end_ix][['water-level','Batalagoda_rain-fall','Btemperature','Kurunegala_rain-fall','Ktemperature','Mediyawa_rain-fall','Chilaw_rain-fall']].shape[0] >= arr_size):
            X.append(seq_x)
            y.append(seq_y)
    return np.array(X) , np.array(y)

ds_start, ds_end = '2012-11-01', '2012-12-31'
X, y = split_sequences_daily(df[:], pd.DateOffset(days=5))

sequence_index = 0
ver_df = pd.DataFrame(X[:,sequence_index, 0:7],index=X[:,sequence_index, 0])
ver_df.columns = ['time','Batalagoda_rain-fall','Btemperature','Kurunegala_rain-fall','Ktemperature','Mediyawa_rainfall','Chilaw_rainfall']


############################# Splitting Dataset ################################

split_size = 0.8

split_val = round(X.shape[0]*split_size)

X_train = X[:split_val]
X_test = X[split_val:]

y_train = y[:split_val]
y_test = y[split_val:]

################################ load trained model for testing  ###############################
from keras.models import load_model
model = load_model(str(Path(__file__).resolve().parents[1]/"LSTM"/"save-train-model"/"model.h5"))


test_data = True #False

if(test_data):
    pred_data = X_test
    obs_data = y_test
else:
    pred_data = X_train
    obs_data = y_train

yhat = model.predict(pred_data[:,:,1:8], verbose=0)
y_test_comb = np.dstack((obs_data, yhat)).reshape(pred_data.shape[0], 3)

test_df = pd.DataFrame(y_test_comb,index=y_test_comb[:,0])
test_df.columns = ['time', 'observed', 'estimated']

test_df = test_df.set_index('time')
test_df.index = pd.to_datetime(test_df.index)

sns.set(rc={'figure.figsize':(17, 10)})
# Start and end of the date range to extract
start, end = '2012-01-01', '2012-12-31'
# start, end = '2019-03-01', '2019-05-01'
# Plot daily and weekly resampled time series together
fig, ax = plt.subplots()
ax.plot(test_df['observed'][:], marker='.', linestyle='-', linewidth=0.5, label='observed')
ax.plot(test_df['estimated'][:], marker='.', markersize=8, linestyle='-', linewidth=0.7, label='estimated')
ax.set_ylabel('Water Height')
ax.legend()
ax.set_title("LSTM Chillaw WL Prediction")
fig.savefig(str(Path(__file__).resolve().parents[1]/"LSTM"/"graphs"/"test"/"1.png"), bbox_inches='tight')
plt.close(fig)

output['isGraphCreated'] = True

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

MSE = mean_squared_error(test_df['observed'], test_df['estimated'])
RMSE = MSE**0.5
output['RMSE'] = RMSE

r2 = r2_score(test_df['observed'], test_df['estimated'])
output['R2'] = r2

from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(test_df['observed'], test_df['estimated'])
output['MAE'] = mae


print(json.dumps(output))
