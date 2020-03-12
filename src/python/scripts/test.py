import sys
import json
import pandas as pd
import numpy as np
import collections
from pathlib import Path


########## function definitions needed for rainfall forecasting #############

def filterData(data):
  filteredRainFall=[]
  for i in range(len(data)):
    rain_fall=float(data[i])
    if(rain_fall== 0):
      rainFallStatus="NoRain"
    elif(rain_fall<50):
      rainFallStatus="LightRain"
    else:
      rainFallStatus="HeavyRain"
    filteredRainFall.append(rainFallStatus)
  return filteredRainFall

def ChangeStatusFunction(data):
  changeStatusArray=[]
  noRainCount=0
  lightRainCount=0
  heavyRainCount=0

  for i in range(len(data)-1):
    if(data[i]=="NoRain"):
      if(data[i+1]=="NoRain"):
        changeStatus="NN"
      elif(data[i+1]=="LightRain"):
        changeStatus="NL"
      elif(data[i+1]=="HeavyRain"):
        changeStatus="NH"
      noRainCount=noRainCount+1
    elif(data[i]=="HeavyRain"):
      if(data[i+1]=="NoRain"):
        changeStatus="HN"
      elif(data[i+1]=="LightRain"):
        changeStatus="HL"
      elif(data[i+1]=="HeavyRain"):
        changeStatus="HH"
      heavyRainCount=heavyRainCount+1
    elif(data[i]=="LightRain"):
      if(data[i+1]=="NoRain"):
        changeStatus="LN"
      elif(data[i+1]=="LightRain"):
        changeStatus="LL"
      elif(data[i+1]=="HeavyRain"):
        changeStatus="LH"
      lightRainCount=lightRainCount+1
    changeStatusArray.append(changeStatus)
  return changeStatusArray

def CalculateTransitionMatrix(data,list):
  changeStatusArray_numpy = np.array(data)
  counted_array = collections.Counter(changeStatusArray_numpy)

  NNCount = counted_array['NN']
  NLCount = counted_array['NL']
  NHCount = counted_array['NH']

  LNCount = counted_array['LN']
  LLCount = counted_array['LL']
  LHCount = counted_array['LH']

  HNCount = counted_array['HN']
  HLCount = counted_array['HL']
  HHCount = counted_array['HH']
  list.pop()
  NoRainCount = list.count('NoRain')
  LightRainCount = list.count('LightRain')
  HeavyRainCount = list.count('HeavyRain')
  transitionMatrix=[]

  if((NoRainCount)==0 or(LightRainCount)==0 or(HeavyRainCount)==0):
      print("invalid history data input")
  else:
      transitionMatrix=[
                        [NNCount/NoRainCount,NLCount/NoRainCount,NHCount/NoRainCount],
  [LNCount/LightRainCount,LLCount/LightRainCount,LHCount/LightRainCount],
  [HNCount/HeavyRainCount,HLCount/HeavyRainCount,HHCount/HeavyRainCount]]
  print(transitionMatrix)
  return transitionMatrix

def RainFallForecast(days,current,transitionMatrix,isPrint=True):
    transitionName = [["NN","NL","NH"],["LN","LL","LH"],["HN","HL","HH"]]
    # Choose the starting state
    states = current
    rainStatusToday = str(states)
    if(isPrint):
      print("Start state: " + rainStatusToday)
    # Shall store the sequence of states taken. So, this only has the starting state for now.
    floodStatusList = [rainStatusToday]
    i = 0
    # To calculate the probability of the floodStatusList
    prob = 1
    while i != days:
        if rainStatusToday == "NoRain":
            change = np.random.choice(transitionName[0],replace=True,p=transitionMatrix[0])
            if change == "NN":
                prob = prob * transitionMatrix[0][0]
                floodStatusList.append("NoRain")
                pass
            elif change == "NL":
                prob = prob * transitionMatrix[0][1]
                rainStatusToday = "LightRain"
                floodStatusList.append("LightRain")
            elif change== "NH":
                prob = prob * transitionMatrix[0][2]
                rainStatusToday = "HeavyRain"
                floodStatusList.append("HeavyRain")

        elif rainStatusToday == "LightRain":
            change = np.random.choice(transitionName[1],replace=True,p=transitionMatrix[1])
            if change == "LN":
                prob = prob * transitionMatrix[1][0]
                rainStatusToday = "NoRain"
                floodStatusList.append("NoRain")
                pass
            elif change == "LL":
                prob = prob * transitionMatrix[1][1]
                rainStatusToday = "LightRain"
                floodStatusList.append("LightRain")
            elif change == "LH":
                prob = prob * transitionMatrix[1][2]
                rainStatusToday = "HeavyRain"
                floodStatusList.append("HeavyRain")

        elif rainStatusToday == "HeavyRain":
            change = np.random.choice(transitionName[2],replace=True,p=transitionMatrix[2])
            if change == "HN":
                prob = prob * transitionMatrix[2][0]
                rainStatusToday = "NoRain"
                floodStatusList.append("NoRain")
                pass
            elif change == "HL":
                prob = prob * transitionMatrix[2][1]
                rainStatusToday = "LightRain"
                floodStatusList.append("LightRain")
            elif change == "HH":
                prob = prob * transitionMatrix[2][2]
                rainStatusToday = "HeavyRain"
                floodStatusList.append("HeavyRain")
        i += 1
    if(isPrint):
      print("Possible states: " + str(floodStatusList))
      print("End state after "+ str(days) + " days: " + rainStatusToday)
      print("Probability of the possible sequence of states: " + str(prob))
    return floodStatusList

def accuracy(original_data, predicted_data):
  simillar_count = 0
  for i in range(0,len(original_data)):
    if(original_data[i] == predicted_data[i]):
      simillar_count += 1
  return (simillar_count/len(original_data)*100)

####################################################################

sample_data_RF = pd.read_excel(str(
    Path(__file__).resolve().parents[1]/"data"/"data.xlsx"),usecols='B:D')
date = pd.read_excel(str(
    Path(__file__).resolve().parents[1]/"data"/"data.xlsx"),usecols='A')

columns = list(sample_data_RF)
print(columns)


days_to_forecast_RF= json.loads(sys.argv[1])
current_states_RF = json.loads(sys.argv[2])


for i in columns:
  #filter data for Batalagoda
  filtered_data = filterData(sample_data_RF[i])
  #changed status array
  change_status_array = ChangeStatusFunction(filtered_data)
  #calculate transition matrix
  t_matrix = CalculateTransitionMatrix(change_status_array,filtered_data)

  RainFallForecast(int(days_to_forecast_RF[i]),str(current_states_RF[i]),t_matrix)
  calc= RainFallForecast(len(filtered_data),filtered_data[0],t_matrix,False)

  acc= accuracy(filtered_data,calc)
  print("Accuracy: %f"%acc)




print('python script executed')
