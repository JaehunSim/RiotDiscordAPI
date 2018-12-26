# -*- coding: utf-8 -*-
import requests
import time
import warnings
from collections import Counter
import pandas as pd
warnings.filterwarnings("ignore")
APIKEY = "RGAPI-0416bf72-4fe9-4fd2-b6b5-057237db2a2d"
REGION = "kr"

import os
import sys
PATH = os.path.dirname(os.path.realpath(sys.argv[0]))[:-5] + "\\db"

def getDataFromURL(URL):
    response = requests.get(URL)
    #time.sleep(0.8)
    count = 0
    #correct retrieval
    if len(str(response.json())) > 100:
        return response.json()
    if "not found" in response.json()["status"]["message"]:
        return "noSummoner"
    #if rate limit exceeds, then try 5 more times, for each time sleep 10 secs.
    else:
        while True:
            try:
                while(response.json()["status"]["status_code"]==429):
                    if count >= 10:
                        return "error"
                    time.sleep(15)
                    response = requests.get(URL)
                    time.sleep(0.8)
                    if len(str(response.json())) > 100:
                        return response.json()
                    count +=1
                time.sleep(3)
                response = requests.get(URL)
                return response.json()
            except:
                time.sleep(0.8)
                response = requests.get(URL)
                if len(str(response.json())) > 100:
                    return response.json()      
                
def getDataFromURL2(URL):
    response = requests.get(URL)
    length = len(str(response.json()))
    while length <= 100:
        response = requests.get(URL)
        length = len(str(response.json()))
        time.sleep(0.1)
    return response.json()  

def getSummonerId(summonerName, region=REGION):
    #summonerId, accountId
    URL = "https://"+str(region)+".api.riotgames.com/lol/summoner/v3/summoners/by-name/"+summonerName+"?api_key="+APIKEY
    result = getDataFromURL(URL)
    if result=="noSummoner":
        return "error"
    summonerId = result["id"]
    accountId = result["accountId"]
    return summonerId, accountId

def getSummonerRank(summonerId, region=REGION):
    URL = "https://"+str(region)+".api.riotgames.com/lol/league/v3/positions/by-summoner/"+str(summonerId)+"?api_key="+APIKEY
    result = requests.get(URL).json()
    if result == []:
        return "UnRank"
    for type1 in result:
        if type1["queueType"] == "RANKED_SOLO_5x5":
            break
    tier = type1["tier"]
    rank = type1["rank"]
    result = tier + " " + rank
    return result

def getRankScore(rank):
    rankScoreDict = {"BRONZE":0, "SILVER":1, "GOLD":2,"PLATINUM":3, "DIAMOND":4, "MASTER": 5, "CHALLENGER":6}
    numberDict = {"I":5, "II":4, "III": 3, "IV":2, "V":1}
    temp = rank.split(" ")
    result = rankScoreDict[temp[0]] * 5 + numberDict[temp[1]]
    return result

def getRankLog(accountId,region=REGION,beginIndex=0,endIndex=100,queue=420):
    #420: Solo
    #700: 격전
    #460: 3:3
    #450: 무작위총력전
    #440: 자유랭
    URL = "https://"+str(region)+".api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(accountId)+"?beginIndex="+str(beginIndex)+"&endIndex="+str(endIndex)+"&queue="+str(queue)+"&api_key="+APIKEY
    result = getDataFromURL(URL)["matches"]
    return result

def getMostN(accountId, n,region=REGION):
    championMapData = pd.read_excel(PATH + "\\championID.xlsx")
    beginIndex=0
    URL = "https://"+str(region)+".api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(accountId)+"?beginIndex="+str(beginIndex)+"&api_key="+APIKEY
    result = getDataFromURL(URL)["matches"]
    beginIndex=100
    URL = "https://"+str(region)+".api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(accountId)+"?beginIndex="+str(beginIndex)+"&api_key="+APIKEY
    result2 = getDataFromURL(URL)["matches"]
    result.extend(result2)
    for game in result:
        if game["queue"] == 450:
            result.remove(game)
    temp = []
    for game in result:
        temp.append(game["champion"])
    
    playedDF = pd.DataFrame(temp, columns=["id"])
    championList = pd.merge(playedDF,championMapData,how="left")["name"]
    mostN = championList.value_counts()[:n]
    return list(mostN.index)

def getPositionPreference(rankLog,n):
    data = pd.read_excel(PATH+ "\\positionMap.xlsx")
    temp = []
    for game in rankLog:
        temp2 = game["lane"]
        temp2 += "-"+ game["role"]
        temp.append(temp2)
    def getRole(x):
        return data["role"][data["position"][data["position"] == x].index[0]]
    roleList = []
    for i in temp:
        roleList.append(getRole(i))
    counted = Counter(roleList)
    counted = counted.most_common(n)
    return counted

def getChampionPlayedList(rankLog):
    temp = []
    for game in rankLog:
        temp.append(game["champion"])
    return temp



def predictPosition(cpl,n):
    championMapData = pd.read_excel(PATH + "\\championID.xlsx")
    cpl = pd.DataFrame(cpl, columns=["id"])
    championList = pd.merge(cpl,championMapData,how="left")["key"]
    championList = pd.DataFrame(championList)
    predictionData = pd.read_csv(PATH+"\\predictPositionV2.csv")
    predPositDF = pd.merge(championList,predictionData, how="left").loc[:,["role","chance"]]
    roleGrouped = predPositDF.groupby("role").sum()
    roleGrouped.sort_values("chance",ascending=False, inplace=True)
    result = []
    for i in range(n):
        result.append((roleGrouped.index[i],roleGrouped.values[i][0]))
    return result

getInfo = getSummonerId("고대담배")
summonerId = getInfo[0]
accountId = getInfo[1]
#rank = getSummonerRank(summonerId)
#rankScore = getRankScore(rank)
#rankLog = getRankLog(accountId)
mc = getMostN(accountId,5)
#pp = getPositionPreference(rankLog,2)
#cpl = getChampionPlayedList(rankLog)
