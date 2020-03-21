import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from tensorflow import keras

###################### import data #################################
df1 = pd.read_csv(str(Path(__file__).resolve().parents[1]/"LSTM"/"data"/"B.csv"))
df2 = pd.read_csv(str(Path(__file__).resolve().parents[1]/"LSTM"/"data"/"CWL.csv"))
df3 = pd.read_csv(str(Path(__file__).resolve().parents[1]/"LSTM"/"data"/"K.csv"))
df4 = pd.read_csv(str(Path(__file__).resolve().parents[1]/"LSTM"/"data"/"MR.csv"))

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

################################ define model  ###############################

n_features = 7
n_steps_in, n_steps_out = X.shape[1], 1

model = Sequential()
model.add(
    LSTM(100, activation='sigmoid',
    return_sequences=True,
    input_shape=(n_steps_in, n_features))
)
model.add(LSTM(100, activation='sigmoid'))
model.add(Dense(n_steps_out))
model.compile(optimizer='adam', loss='mse', metrics=['mae', 'mse'])


# Display training progress by printing a single dot for each completed epoch
class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

# The patience parameter is the amount of epochs to check for improvement
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

# fit model
model.fit(X_train[:,:, 1:8], y_train[:,0, 1].reshape(y_train.shape[0],1), epochs=100, verbose=0,
          validation_data=(X_test[:,:, 1:8], y_test[:,0, 1].reshape(y_test.shape[0],1)),
            callbacks=[ PrintDot()]) #early_stop,

model.save(str(Path(__file__).resolve().parents[1]/"LSTM"/"save-train-model"/"model.h5"))

print('done')
