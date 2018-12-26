# -*- coding: utf-8 -*-
from summoner_info import getSummonerId, getSummonerRank, getRankScore, getPositionPreference, getRankLog, getMostN
import random
import time
import datetime
import pandas as pd
import copy
import os
import sys
import copy 

PATH = os.path.dirname(os.path.realpath(sys.argv[0]))[:-5] + "\\db"
TOKEN = 'NDYzNTE4MDc4MjkwODg2NjY2.DhyBuQ.7wvrJO-qedyJdhB-u1Ddimi20LI'
errorName =[]

def changeStrToList(str1):
    result = []
    temp = str1.split(",")
    result.append([temp[0][3:-1],int(temp[1][1:-1])])
    result.append([temp[2][3:-1],int(temp[3][1:-2])])
    return result

def initialize():
    initial = pd.DataFrame([],columns = ['summonerName', 'summonerId', 'accountId', 'rank', 'pp','updated_date'])
    initial.to_csv(PATH + '\\summonerNameData.csv', index=False, encoding="euc-kr")

def updateSummoner(data, summonerNameList, update_period=2):
    #initial var
    rankScoreList = []
    rankList = []
    changed = False
    today = datetime.datetime.today()
    
    for summonerName in summonerNameList:
        summonerName = summonerName.lower()
        gotId = False
        #call from db
        for index,value in enumerate(data["summonerName"]):
            if summonerName == value:
                updated_date = data["updated_date"][index]
                datetime_up = datetime.datetime(*[int(item) for item in updated_date.split('-')])
                timediff = today - datetime_up
                if timediff.days >= update_period:
                    data.drop(index, inplace=True)
                    break
                #search successful
                gotId = True
                
                summonerId = data["summonerId"][index]
                accountId = data["accountId"][index]
                rank = data["rank"][index]
                pp = data["pp"][index]
                rankScore = getRankScore(rank)
                rankScoreList.append([summonerName,rankScore])
                rankList.append([summonerName,rank])
                break
        
        #update
        if not gotId:
            changed = True
            
            temp = getSummonerId(summonerName)
            if temp == "error":
                errorName.append(summonerName)
                raise ValueError("Invlid SummonerName is in Input")
            summonerId = temp[0]
            accountId = temp[1]
            
            rank = getSummonerRank(summonerId)
            if rank=="UnRank":
                errorName.append(summonerName)
                raise Exception("UnRank is in Input")
                
            rankScore = getRankScore(rank)
            rankScoreList.append([summonerName,rankScore])   
            
            rankList.append([summonerName,rank])
            
            rankLog = getRankLog(accountId)
            pp = getPositionPreference(rankLog,2)
            
            updated_date = today.strftime('%Y-%m-%d')
            data = data.append({"summonerName":summonerName,"summonerId":summonerId,"accountId":accountId,"rank":rank,
                                "pp":pp,"updated_date":updated_date},ignore_index=True)
    if changed:
        data.to_csv(PATH + '\\summonerNameData.csv', index=False, encoding="euc-kr")
    return rankScoreList, rankList, data
    
arg1, arg2, arg3, arg4, arg5 = "신나라소녀", "Horuskirin", "멋있어부엉", "타푸고양이", "3월의토끼"
data = pd.read_csv(PATH + '\\summonerNameData.csv', encoding="euc-kr")

summonerNameList =  [arg1, arg2, arg3, arg4, arg5]
ppList = []
for name in summonerNameList:
    ppList.append(data["pp"][pd.Index(data["summonerName"]).get_loc(name)])

try:
    rankScoreList,rankList,data = updateSummoner(data, summonerNameList)
except ValueError: 
    print("Summoner Name Not Found: {0}".format(errorName[0]))
    raise ValueError
except Exception:
    print("UnRank Detected: {0}".format(errorName[0]))
    raise Exception
   
rankScoreOnly = []
for i in rankScoreList:
    rankScoreOnly.append(i[1])

team = copy.deepcopy(summonerNameList)
teamPositList = []
for member in team:
    teamPositList.append(ppList[summonerNameList.index(member)])
team_pre = []
for index,value in enumerate(teamPositList):
    if type(value) == str:
        ppList_element = changeStrToList(value)
    else:
        ppList_element = value
    #get total
    total = 0
    for posit in ppList_element:
        total += posit[1]
        
    for posit in ppList_element:
        team_pre.append([index,posit[0],posit[1]/total])

cases = []
for caseNum in range(10):
    team = copy.deepcopy(summonerNameList)
    team_DF = pd.DataFrame(team_pre, columns =["member","position","rate"])
    pickedPosit = []
    for i in range(5):
        if len(team_DF) != 0:
            #weighted sampling from position_rate
            sampled = team_DF.sample(1, weights=team_DF["rate"].values).index[0]
            picked = team_DF.loc[sampled,:]
            pickedPosit.append([team[picked["member"]],picked["position"]])
            team_DF = team_DF[team_DF["position"] != picked["position"]]
            team_DF = team_DF[team_DF["member"] != picked["member"]] 
        
    finalList = [pickedPosit]
    
    for index in range(len(finalList)):
        team = finalList[index]
        while len(team) != 5:
            team_all_members = copy.deepcopy(summonerNameList)
            positions = ["TOP","JUN","MID","ADC","SUP"]
            for memberInfo in team:
                memberName, position = memberInfo[0], memberInfo[1]
                team_all_members.remove(memberName)
                positions.remove(position)
            team.append([team_all_members[0],positions[0]])
    
    
    positionOrder = {"TOP":0,"JUN":1,"MID":2,"ADC":3,"SUP":4}
    for team in finalList:
        team.sort(key= lambda x: positionOrder[x[1]])
    
    for team in finalList:
        text = ""
        for positInfo in team:
            text+= ('{0:<3}: {1:<12} '.format(positInfo[1],positInfo[0]))
    if text not in cases:
        cases.append(text)
    
finalText = ""
for i in range(len(cases)):
    if i>=3:
        break
    finalText += "Case: {0}\n".format(int((i+1)))
    finalText += cases[i]+"\n"
print(finalText)