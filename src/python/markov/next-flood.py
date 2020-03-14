import sys
import json
import pandas as pd
import numpy as np
import collections
from pathlib import Path

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


def accuracy(original_data, predicted_data):
  simillar_count = 0
  for i in range(0,len(original_data)):
    if(original_data[i] == predicted_data[i]):
      simillar_count += 1
  return (simillar_count/len(original_data)*100)

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



def next_flood_forecast(current, transitionMatrix):
    transitionName = [["NN","NC","NW","NF"],["CN","CC","CW","CF"],["WN","WC","WW","WF"],["FN","FC","FW","FF"]]
    # Choose the starting state
    floodStatusToday = str(current)
    #floodStatusToday = "Warning"
    # Shall store the sequence of states taken. So, this only has the starting state for now.
    floodStatusList = [floodStatusToday]

    # To calculate the probability of the floodStatusList
    prob = 1
    while True:
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
                break

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
                break

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
                break

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
                break

    return [floodStatusList, prob]

##############################################################################

##################### Flood status forecasting Calculations #####################################
output={}

sample_data_WL = pd.read_excel(str(
    Path(__file__).resolve().parents[1]/"markov"/"data"/"data.xlsx"),usecols='E')
columns_WL = list(sample_data_WL)
current_states_FlOOD = sys.argv[1]

for col in columns_WL:
  floodStatusArray = filterDataWL(sample_data_WL[col])


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


  for j in range(len(changeStatusArray)):
    if(changeStatusArray[j]=="NN"):
      NNCount=NNCount+1
    elif(changeStatusArray[j]=="NC"):
      NCCount=NCCount+1
    elif(changeStatusArray[j]=="NW"):
      NWCount=NWCount+1
    elif(changeStatusArray[j]=="NF"):
      NFCount=NFCount+1
    elif(changeStatusArray[j]=="CN"):
      CNCount=CNCount+1
    elif(changeStatusArray[j]=="CC"):
      CCCount=CCCount+1
    elif(changeStatusArray[j]=="CW"):
      CWCount=CWCount+1
    elif(changeStatusArray[j]=="CF"):
      CFCount=CFCount+1
    elif(changeStatusArray[j]=="WN"):
      WNCount=WNCount+1
    elif(changeStatusArray[j]=="WC"):
      WCCount=WCCount+1
    elif(changeStatusArray[j]=="WW"):
      WWCount=WWCount+1
    elif(changeStatusArray[j]=="WF"):
      WFCount=WFCount+1
    elif(changeStatusArray[j]=="FN"):
      FNCount=FNCount+1
    elif(changeStatusArray[j]=="FC"):
      FCCount=FCCount+1
    elif(changeStatusArray[j]=="FW"):
      FWCount=FWCount+1
    elif(changeStatusArray[j]=="FF"):
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

  flood_res = next_flood_forecast( str(current_states_FlOOD),transitionMetrix)
  calc_acc = floodStatus_forecast(len(floodStatusArray),floodStatusArray[0],transitionMetrix)
  acc = accuracy(floodStatusArray,calc_acc[0] )
  temp_output={}
  temp_output["transitionMatrix"] = transitionMetrix
  temp_output['days']=len(flood_res[0]) - 1
  temp_output['startState']=flood_res[0][0]
  temp_output['endState']=flood_res[0][-1]
  temp_output['possibleStates']=flood_res[0]
  temp_output['probability']=flood_res[1]
  temp_output['accuracy']=acc
  output['flood_' + col]=temp_output

#########################################################################################################
print(json.dumps(output))
