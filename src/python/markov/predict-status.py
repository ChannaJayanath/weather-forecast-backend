import sys
import json
import pandas as pd
import numpy as np
import collections
from pathlib import Path

output = {}
########## function definitions needed for rainfall status forecasting #############

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
  return transitionMatrix

def RainFallForecast(days,current,transitionMatrix):
    transitionName = [["NN","NL","NH"],["LN","LL","LH"],["HN","HL","HH"]]
    # Choose the starting state
    states = current
    rainStatusToday = str(states)
    # Shall store the sequence of states taken. So, this only has the starting state for now.
    rainStatusList = [rainStatusToday]
    i = 0
    # To calculate the probability of the rainStatusList
    prob = 1
    while i != days:
        if rainStatusToday == "NoRain":
            change = np.random.choice(transitionName[0],replace=True,p=transitionMatrix[0])
            if change == "NN":
                prob = prob * transitionMatrix[0][0]
                rainStatusList.append("NoRain")
                pass
            elif change == "NL":
                prob = prob * transitionMatrix[0][1]
                rainStatusToday = "LightRain"
                rainStatusList.append("LightRain")
            elif change== "NH":
                prob = prob * transitionMatrix[0][2]
                rainStatusToday = "HeavyRain"
                rainStatusList.append("HeavyRain")

        elif rainStatusToday == "LightRain":
            change = np.random.choice(transitionName[1],replace=True,p=transitionMatrix[1])
            if change == "LN":
                prob = prob * transitionMatrix[1][0]
                rainStatusToday = "NoRain"
                rainStatusList.append("NoRain")
                pass
            elif change == "LL":
                prob = prob * transitionMatrix[1][1]
                rainStatusToday = "LightRain"
                rainStatusList.append("LightRain")
            elif change == "LH":
                prob = prob * transitionMatrix[1][2]
                rainStatusToday = "HeavyRain"
                rainStatusList.append("HeavyRain")

        elif rainStatusToday == "HeavyRain":
            change = np.random.choice(transitionName[2],replace=True,p=transitionMatrix[2])
            if change == "HN":
                prob = prob * transitionMatrix[2][0]
                rainStatusToday = "NoRain"
                rainStatusList.append("NoRain")
                pass
            elif change == "HL":
                prob = prob * transitionMatrix[2][1]
                rainStatusToday = "LightRain"
                rainStatusList.append("LightRain")
            elif change == "HH":
                prob = prob * transitionMatrix[2][2]
                rainStatusToday = "HeavyRain"
                rainStatusList.append("HeavyRain")
        i += 1
    return [rainStatusList, prob ]

def accuracy(original_data, predicted_data):
  simillar_count = 0
  for i in range(0,len(original_data)):
    if(original_data[i] == predicted_data[i]):
      simillar_count += 1
  return (simillar_count/len(original_data)*100)

####################################################################

########## function definitions needed for flood status forecasting #############
def filterDataWL(data):
  floodStatusArray=[]
  for i in range(len(data)):
    water_level=float(data[i])
    if(water_level<2.75):
      floodStatus="NoFlood"
    elif(water_level<3.75):
      floodStatus="Critical"
    elif(water_level<4):
      floodStatus="Warning"
    else:
      floodStatus="Flood"
    floodStatusArray.append(floodStatus)
  return floodStatusArray


def floodStatus_forecast(days, current, transitionMatrix):
    transitionName = [["NN","NC","NW","NF"],["CN","CC","CW","CF"],["WN","WC","WW","WF"],["FN","FC","FW","FF"]]
    # Choose the starting state
    floodStatusToday = str(current)
    #floodStatusToday = "Warning"
    # Shall store the sequence of states taken. So, this only has the starting state for now.
    floodStatusList = [floodStatusToday]
    i = 0
    # To calculate the probability of the floodStatusList
    prob = 1
    while i != days:
        if floodStatusToday == "NoFlood":
            change = np.random.choice(transitionName[0],replace=True,p=transitionMatrix[0])
            if change == "NN":
                prob = prob * transitionMatrix[0][0]
                floodStatusList.append("NoFlood")
                pass
            elif change == "NC":
                prob = prob * transitionMatrix[0][1]
                floodStatusToday = "Critical"
                floodStatusList.append("Critical")
            elif change== "NW":
                prob = prob * transitionMatrix[0][2]
                floodStatusToday = "Warning"
                floodStatusList.append("Warning")
            else:
                prob = prob * transitionMatrix[0][3]
                floodStatusToday = "Flood"
                floodStatusList.append("Flood")

        elif floodStatusToday == "Critical":
            change = np.random.choice(transitionName[1],replace=True,p=transitionMatrix[1])
            if change == "CN":
                prob = prob * transitionMatrix[1][0]
                floodStatusToday = "NoFlood"
                floodStatusList.append("NoFlood")
                pass
            elif change == "CC":
                prob = prob * transitionMatrix[1][1]
                floodStatusToday = "Critical"
                floodStatusList.append("Critical")
            elif change == "CW":
                prob = prob * transitionMatrix[1][2]
                floodStatusToday = "Warning"
                floodStatusList.append("Warning")
            else:
                prob = prob * transitionMatrix[1][3]
                floodStatusToday = "Flood"
                floodStatusList.append("Flood")
        elif floodStatusToday == "Warning":
            change = np.random.choice(transitionName[2],replace=True,p=transitionMatrix[2])
            if change == "WN":
                prob = prob * transitionMatrix[2][0]
                floodStatusToday = "NoFlood"
                floodStatusList.append("NoFlood")
                pass
            elif change == "WC":
                prob = prob * transitionMatrix[2][1]
                floodStatusToday = "Critical"
                floodStatusList.append("Critical")
            elif change == "WW":
                prob = prob * transitionMatrix[2][2]
                floodStatusToday = "Warning"
                floodStatusList.append("Warning")
            else:
                prob = prob * transitionMatrix[2][3]
                floodStatusToday = "Flood"
                floodStatusList.append("Flood")
        else:
            change = np.random.choice(transitionName[3],replace=True,p=transitionMatrix[3])
            if change == "FN":
                prob = prob * transitionMatrix[3][0]
                floodStatusToday = "NoFlood"
                floodStatusList.append("NoFlood")
                pass
            elif change == "FC":
                prob = prob * transitionMatrix[3][1]
                floodStatusToday = "Critical"
                floodStatusList.append("Critical")
            elif change == "FW":
                prob = prob * transitionMatrix[3][2]
                floodStatusToday = "Warning"
                floodStatusList.append("Warning")
            else:
                prob = prob * transitionMatrix[3][3]
                floodStatusToday = "Flood"
                floodStatusList.append("Flood")
        i += 1
    return [floodStatusList, prob]

##############################################################################

##################### Rainfall forecasting Calculations #####################################
sample_data_RF = pd.read_excel(str(
    Path(__file__).resolve().parents[1]/"markov"/"data"/"data.xlsx"),usecols='B:D')
date = pd.read_excel(str(
    Path(__file__).resolve().parents[1]/"markov"/"data"/"data.xlsx"),usecols='A')

columns = list(sample_data_RF)


days_to_forecast_RF= json.loads(sys.argv[1])
current_states_RF = json.loads(sys.argv[2])


for i in columns:
  temp_output={}
  #filter data for Batalagoda
  filtered_data = filterData(sample_data_RF[i])
  #changed status array
  change_status_array = ChangeStatusFunction(filtered_data)
  #calculate transition matrix
  t_matrix = CalculateTransitionMatrix(change_status_array,filtered_data)

  res_rain = RainFallForecast(int(days_to_forecast_RF[i]),str(current_states_RF[i]),t_matrix)
  calc_acc= RainFallForecast(len(filtered_data),filtered_data[0],t_matrix)

  acc= accuracy(filtered_data,calc_acc[0])

  temp_output["transitionMatrix"] = t_matrix
  temp_output['days']=int(days_to_forecast_RF[i])
  temp_output['startState']=res_rain[0][0]
  temp_output['endState']=res_rain[0][-1]
  temp_output['probability']=res_rain[1]
  temp_output['accuracy']=acc
  output[i]=temp_output
#################################################################################################


##################### Flood status forecasting Calculations #####################################
sample_data_WL = pd.read_excel(str(
    Path(__file__).resolve().parents[1]/"markov"/"data"/"data.xlsx"),usecols='E')
columns_WL = list(sample_data_WL)
days_to_forecast_FLOOD = sys.argv[3]
current_states_FlOOD = sys.argv[4]

for i in columns_WL:
  floodStatusArray = filterDataWL(sample_data_WL[i])


  changeStatusArray=[]
  noFloodCount=0
  warningCount=0
  criticalCount=0
  floodCount=0

  for i in range(len(floodStatusArray)-1):
    if(floodStatusArray[i]=="NoFlood"):
      if(floodStatusArray[i+1]=="NoFlood"):
        changeStatus="NN"
      elif(floodStatusArray[i+1]=="Critical"):
        changeStatus="NC"
      elif(floodStatusArray[i+1]=="Warning"):
        changeStatus="NW"
      elif(floodStatusArray[i+1]=="Flood"):
        changeStatus="NF"
      noFloodCount=noFloodCount+1
    elif(floodStatusArray[i]=="Warning"):
      if(floodStatusArray[i+1]=="NoFlood"):
        changeStatus="WN"
      elif(floodStatusArray[i+1]=="Critical"):
        changeStatus="WC"
      elif(floodStatusArray[i+1]=="Warning"):
        changeStatus="WW"
      elif(floodStatusArray[i+1]=="Flood"):
        changeStatus="WF"
      warningCount=warningCount+1
    elif(floodStatusArray[i]=="Critical"):
      if(floodStatusArray[i+1]=="NoFlood"):
        changeStatus="CN"
      elif(floodStatusArray[i+1]=="Critical"):
        changeStatus="CC"
      elif(floodStatusArray[i+1]=="Warning"):
        changeStatus="CW"
      elif(floodStatusArray[i+1]=="Flood"):
        changeStatus="CF"
      criticalCount=criticalCount+1
    elif(floodStatusArray[i]=="Flood"):
      if(floodStatusArray[i+1]=="NoFlood"):
        changeStatus="FN"
      elif(floodStatusArray[i+1]=="Critical"):
        changeStatus="FC"
      elif(floodStatusArray[i+1]=="Warning"):
        changeStatus="FW"
      elif(floodStatusArray[i+1]=="Flood"):
        changeStatus="FF"
      floodCount=floodCount+1
    changeStatusArray.append(changeStatus)

  #calculation
  NNCount=0
  NCCount=0
  NWCount=0
  NFCount=0

  CNCount=0
  CCCount=0
  CWCount=0
  CFCount=0

  WNCount=0
  WCCount=0
  WWCount=0
  WFCount=0

  FNCount=0
  FCCount=0
  FWCount=0
  FFCount=0


  for i in range(len(changeStatusArray)):
    if(changeStatusArray[i]=="NN"):
      NNCount=NNCount+1
    elif(changeStatusArray[i]=="NC"):
      NCCount=NCCount+1
    elif(changeStatusArray[i]=="NW"):
      NWCount=NWCount+1
    elif(changeStatusArray[i]=="NF"):
      NFCount=NFCount+1
    elif(changeStatusArray[i]=="CN"):
      CNCount=CNCount+1
    elif(changeStatusArray[i]=="CC"):
      CCCount=CCCount+1
    elif(changeStatusArray[i]=="CW"):
      CWCount=CWCount+1
    elif(changeStatusArray[i]=="CF"):
      CFCount=CFCount+1
    elif(changeStatusArray[i]=="WN"):
      WNCount=WNCount+1
    elif(changeStatusArray[i]=="WC"):
      WCCount=WCCount+1
    elif(changeStatusArray[i]=="WW"):
      WWCount=WWCount+1
    elif(changeStatusArray[i]=="WF"):
      WFCount=WFCount+1
    elif(changeStatusArray[i]=="FN"):
      FNCount=FNCount+1
    elif(changeStatusArray[i]=="FC"):
      FCCount=FCCount+1
    elif(changeStatusArray[i]=="FW"):
      FWCount=FWCount+1
    elif(changeStatusArray[i]=="FF"):
      FFCount=FFCount+1

  transitionMetrix=[]

  if((NNCount+NCCount+NWCount+NFCount)==0 or(CNCount+CCCount+CWCount+CFCount)==0 or(WNCount+WCCount+WWCount+WFCount)==0 or(FNCount+FCCount+FWCount+FFCount)==0):
      print("invalid history data input")
  else:
      transitionMetrix=[
                        [NNCount/(NNCount+NCCount+NWCount+NFCount),NCCount/(NNCount+NCCount+NWCount+NFCount),NWCount/(NNCount+NCCount+NWCount+NFCount),NFCount/(NNCount+NCCount+NWCount+NFCount)],
  [CNCount/(CNCount+CCCount+CWCount+CFCount),CCCount/(CNCount+CCCount+CWCount+CFCount),CWCount/(CNCount+CCCount+CWCount+CFCount),CFCount/(CNCount+CCCount+CWCount+CFCount)],
  [WNCount/(WNCount+WCCount+WWCount+WFCount),WCCount/(WNCount+WCCount+WWCount+WFCount),WWCount/(WNCount+WCCount+WWCount+WFCount),WFCount/(WNCount+WCCount+WWCount+WFCount)],
  [FNCount/(FNCount+FCCount+FWCount+FFCount),FCCount/(FNCount+FCCount+FWCount+FFCount),FWCount/(FNCount+FCCount+FWCount+FFCount),FFCount/(FNCount+FCCount+FWCount+FFCount)]]

  flood_res = floodStatus_forecast(int(days_to_forecast_FLOOD), str(current_states_FlOOD),transitionMetrix)
  calc_acc = floodStatus_forecast(len(floodStatusArray),floodStatusArray[0],transitionMetrix)
  acc = accuracy(floodStatusArray,calc_acc[0] )
  temp_output={}
  temp_output["transitionMatrix"] = transitionMetrix
  temp_output['days']=int(days_to_forecast_FLOOD)
  temp_output['startState']=flood_res[0][0]
  temp_output['endState']=flood_res[0][-1]
  temp_output['probability']=flood_res[1]
  output['flood']=temp_output
  temp_output['accuracy']=acc

#########################################################################################################
print(json.dumps(output))
