import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

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

############################### Analyzing data ##############################
sns.set(rc={'figure.figsize':(50, 10)})
# Start and end of the date range to extract
start, end = '2012-02-23', '2012-12-31'
# Plot daily and weekly resampled time series together
fig, ax = plt.subplots()
ax.plot(df2.loc[:, 'WL'],
marker='.', linestyle='-', linewidth=0.5, label='Water Height')
ax.plot(df1.loc[:, 'BR'],
marker='.', markersize=8, linestyle='-', label='BRainfall')
ax.plot(df3.loc[:, 'KR'],
marker='.', markersize=8, linestyle='-', label='KRainfall')
ax.plot(df4.loc[:, 'MR'],
marker='.', markersize=8, linestyle='-', label='MRainfall')
ax.plot(df4.loc[:, 'CR'],
marker='.', markersize=8, linestyle='-', label='CRainfall')
ax.set_ylabel('Water Height')
ax.legend()
fig.savefig(str(Path(__file__).resolve().parents[1]/"LSTM"/"graphs"/"analyze"/"1.png"), bbox_inches='tight')
plt.close(fig)

#hourly arranged

data_columns_B = ['BR','Btem']
df1= df1[data_columns_B].resample('H').mean()
data_columns_K = ['KR','Ktem']
df3= df3[data_columns_K].resample('H').mean()
data_columns_WL = ['WL']
df2= df2[data_columns_WL].resample('H').mean()
data_columns_MC = ['MR','CR']
df4= df4[data_columns_MC].resample('H').mean()

sns.set(rc={'figure.figsize':(50, 10)})
# Start and end of the date range to extract
start, end = '2012-11-01', '2012-12-31'
# Plot daily and weekly resampled time series together
fig, ax = plt.subplots()
ax.plot(df2.loc[start:end, 'WL']*20, marker='', linestyle='-', linewidth=0.5, label='Water Height')
ax.plot(df1.loc[start:end, 'BR'], marker='.', markersize=8, linestyle='-', label='BRainfall')
ax.plot(df3.loc[start:end, 'KR'], marker='.', markersize=8, linestyle='-', label='KRainfall')
ax.plot(df4.loc[start:end, 'MR'], marker='.', markersize=8, linestyle='-', label='MRainfall')
ax.plot(df4.loc[start:end, 'CR'], marker='.', markersize=8, linestyle='-', label='CRainfall')
ax.set_ylabel('Water Height')
ax.legend()
fig.savefig(str(Path(__file__).resolve().parents[1]/"LSTM"/"graphs"/"analyze"/"2.png"), bbox_inches='tight')
plt.close(fig)


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
sns.set(rc={'figure.figsize':(17, 10)})
# Start and end of the date range to extract
start, end = '2012-02-23', '2012-12-31'
# Plot daily and weekly resampled time series together
fig, ax = plt.subplots()
ax.plot(df2.loc[:, 'WL'],
marker='.', linestyle='-', linewidth=0.5, label='Water Height')
ax.plot(df1.loc[:, 'BR'],
marker='.', markersize=8, linestyle='-', label='BRainfall')
ax.plot(df3.loc[:, 'KR'],
marker='.', markersize=8, linestyle='-', label='KRainfall')
ax.plot(df4.loc[:, 'MR'],
marker='.', markersize=8, linestyle='-', label='MRainfall')
ax.plot(df4.loc[:, 'CR'],
marker='.', markersize=8, linestyle='-', label='CRainfall')
ax.set_ylabel('Water Height')
ax.legend()
fig.savefig(str(Path(__file__).resolve().parents[1]/"LSTM"/"graphs"/"analyze"/"3.png"), bbox_inches='tight')
plt.close(fig)

sns.set(rc={'figure.figsize':(17, 5)})
# Start and end of the date range to extract
start, end = '2012-02-23', '2019-12-31'
# Plot daily and weekly resampled time series together
fig, ax = plt.subplots()
ax.plot(df.loc[:, 'water-level'],
marker='.', linestyle='-', linewidth=0.5, label='Water Height')
ax.plot(df.loc[:, 'Batalagoda_rain-fall'],
marker='.', markersize=8, linestyle='-', label='BRainfall')
ax.plot(df.loc[:, 'Btemperature'],
marker='.', markersize=8, linestyle='-', label='BTemperature')
ax.plot(df.loc[:, 'Ktemperature'],
marker='.', markersize=8, linestyle='-', label='KTemperature')
ax.plot(df.loc[:, 'Kurunegala_rain-fall'],
marker='.', markersize=8, linestyle='-', label='KRainfall')
ax.plot(df.loc[:, 'Mediyawa_rain-fall'],
marker='.', markersize=8, linestyle='-', label='MRainfall')
ax.plot(df.loc[:, 'Chilaw_rain-fall'],
marker='.', markersize=8, linestyle='-', label='CRainfall')
ax.set_ylabel('Water Height')
ax.legend()
fig.savefig(str(Path(__file__).resolve().parents[1]/"LSTM"/"graphs"/"analyze"/"4.png"), bbox_inches='tight')
plt.close(fig)


################  plots a graphical correlation matrix ##########################
def plot_corr(df,size=11):
    """
    Function plots a graphical correlation matrix for each pair of columns in the dataframe.

    Input:
        df: pandas DataFrame
        size: vertical and horizontal size of the plot

    Displays:
        matrix of correlation between columns.  Yellow means that they are highly correlated.

    """
    corr = df.corr() # calling the correlation function on the datafrmae
    fig, ax = plt.subplots(figsize=(size,size))
    ax.matshow(corr) # color code the rectangles by correlation value
    plt.xticks(range(len(corr.columns)),corr.columns) # draw x tickmarks
    plt.yticks(range(len(corr.columns)),corr.columns) # draw y tickmarks
    fig.savefig(str(Path(__file__).resolve().parents[1]/"LSTM"/"graphs"/"analyze"/"5.png"), bbox_inches='tight')
    plt.close(fig)


plot_corr(df)

print('done')
