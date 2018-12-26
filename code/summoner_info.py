# -*- coding: utf-8 -*-
import requests
import time
import warnings
from collections import Counter
import pandas as pd
from util import RIOT_API_KEY, REGION, DB_PATH

warnings.filterwarnings("ignore")

#https://developer.riotgames.com/game-constants.html

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
    URL = "https://"+str(region)+".api.riotgames.com/lol/summoner/v3/summoners/by-name/"+summonerName+"?api_key="+RIOT_API_KEY
    result = getDataFromURL(URL)
    if result=="noSummoner":
        return "error"
    summonerId = result["id"]
    accountId = result["accountId"]
    return summonerId, accountId

def getSummonerRank(summonerId, region=REGION):
    URL = "https://"+str(region)+".api.riotgames.com/lol/league/v3/positions/by-summoner/"+str(summonerId)+"?api_key="+RIOT_API_KEY
    result = requests.get(URL).json()
    if result == []:
        return "UnRank"
    result2 = ""
    for type1 in result:
        if type1["queueType"] == "RANKED_SOLO_5x5":
            result2 = type1
            break
    if result2 =="":
        return "UnRank"
    tier = result2["tier"]
    rank = result2["rank"]
    result = tier + " " + rank
    return result

def getRankScore(rank):
    rankScoreDict = {"IRON": 0, "BRONZE":1, "SILVER":2, "GOLD":3,"PLATINUM":4, "DIAMOND":5, "MASTER": 6, "CHALLENGER":7}
    numberDict = {"I":4, "II":3, "III": 2, "IV":1}
    temp = rank.split(" ")
    result = rankScoreDict[temp[0]] * 4 + numberDict[temp[1]]
    return result

def getRankScore2(rank):
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
    URL = "https://"+str(region)+".api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(accountId)+"?beginIndex="+str(beginIndex)+"&endIndex="+str(endIndex)+"&queue="+str(queue)+"&api_key="+RIOT_API_KEY
    result = getDataFromURL(URL)["matches"]
    return result

def getMostN(accountId, n, hist_range_fin, region=REGION, high_param=0.1):
    #hist_range_fin * 100 +100까지 기록 반영
    championMapData = pd.read_excel(DB_PATH + "\\championID.xlsx")
    beginIndex=0
    URL = "https://"+str(region)+".api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(accountId)+"?beginIndex="+str(beginIndex)+"&api_key="+RIOT_API_KEY
    got = getDataFromURL(URL)
    result = got["matches"]
    total = got["totalGames"]
    total += -100
    if total > 0 :
        for i in range(int(total/100)+1):
            if i == hist_range_fin:
                break
            beginIndex= (i+1) * 100
            URL = "https://"+str(region)+".api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(accountId)+"?beginIndex="+str(beginIndex)+"&api_key="+RIOT_API_KEY
            result2 = getDataFromURL(URL)["matches"]
            result.extend(result2)
    final_result = []
    for game in result:
        if game["queue"] in [420,430,440]:
            final_result.append(game)
    temp = []
    for game in final_result:
        temp.append([game["champion"],game["queue"]])
    
    playedDF = pd.DataFrame(temp, columns=["id","queue"])
    championList = pd.merge(playedDF,championMapData,how="left")
    
    queueDict = {420:0.5,430:0.2,440:0.3}
    championList["Weight"] = championList["queue"].apply(lambda x: queueDict[x])
    weightChamp = championList.groupby("name").sum()["Weight"]
    weightChamp = weightChamp.sort_values(ascending=False)
        
    countChamp = championList["name"].value_counts(normalize=True)
    mostN = countChamp[:n]
    highMostN = list(countChamp[countChamp >= high_param][:n].index)
    weightMostN = list(weightChamp[:n].index)
    if len(championList[championList["queue"]==420]) < len(championList) * 0.2:
        weightMostN = []
    
    return list(mostN.index), highMostN, weightMostN

def getPositionPreference(rankLog,n):
    data = pd.read_excel(DB_PATH+ "\\positionMap.xlsx")
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
    championMapData = pd.read_excel(DB_PATH + "\\championID.xlsx")
    cpl = pd.DataFrame(cpl, columns=["id"])
    championList = pd.merge(cpl,championMapData,how="left")["key"]
    championList = pd.DataFrame(championList)
    predictionData = pd.read_csv(DB_PATH+"\\predictPositionV2.csv")
    predPositDF = pd.merge(championList,predictionData, how="left").loc[:,["role","chance"]]
    roleGrouped = predPositDF.groupby("role").sum()
    roleGrouped.sort_values("chance",ascending=False, inplace=True)
    result = []
    for i in range(n):
        result.append((roleGrouped.index[i],roleGrouped.values[i][0]))
    return result

getInfo = getSummonerId("불연속")
summonerId = getInfo[0]
#accountId = getInfo[1]
#mc = getMostN(accountId,3,0)
    
rank = getSummonerRank(summonerId)
#rankScore = getRankScore(rank)
#rankLog = getRankLog(accountId)
#pp = getPositionPreference(rankLog,2)
#cpl = getChampionPlayedList(rankLog)

#region=REGION
#n = 5
#hist_range_fin= 3
#high_param=0.1
