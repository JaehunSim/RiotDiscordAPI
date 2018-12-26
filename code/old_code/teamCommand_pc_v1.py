# -*- coding: utf-8 -*-
import random
from summoner_info import getSummonerId, getSummonerRank, getRankScore, getPositionPreference, getRankLog
from minDiffPartitioning import min_diff_sets
import time
import datetime
import pandas as pd
import csv

PATH = r"C:\Users\tapu1\Desktop\python\discord_lol"
TOKEN = 'NDYzNTE4MDc4MjkwODg2NjY2.DhyBuQ.7wvrJO-qedyJdhB-u1Ddimi20LI'

arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10 = "타푸고양이", "3월의토끼", "벌레포식자", "고대담배", "냐냥고양이", "필요악", "장서누", "신나라소녀", "굽신오리", "내등짝을형에게"
    
start = time.time()
summonerNameData = []
with open(PATH + '\\summonerNameData.csv','r') as f:
    summonerNameload = csv.DictReader(f,delimiter=',')
    for row in summonerNameload:
        summonerNameData.append(row)
summonerNameList = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10]
rankScoreList = []
rankList = []
today = datetime.datetime.today()
for summonerName in summonerNameList:
    gotId = False
    upDateNeeded = False
    for i in summonerNameData:
        if summonerName == i["summonerName"]:
            updated_date = i["updated_date"]
            datetime_up = datetime.datetime(*[int(item) for item in updated_date.split('-')])
            timediff = today - datetime_up
            if timediff.days >= 2:
                upDateNeeded = True
                break
            gotId = True
            summonerId = i["summonerId"]
            accountId = i["accountId"]
            rank = i["rank"]
            pp = i["pp"]
            rankList.append([summonerName,rank])
            rankScore = getRankScore(rank)
            rankScoreList.append([summonerName,rankScore])               
            break
    if not gotId or upDateNeeded:
        temp = getSummonerId(summonerName)
        summonerId = temp[0]
        accountId = temp[1]
        rank = getSummonerRank(summonerId)
        rankList.append([summonerName,rank])
        rankScore = getRankScore(rank)
        rankScoreList.append([summonerName,rankScore])
        updated_date = today.strftime('%Y-%m-%d')
        rankLog = getRankLog(accountId)
        pp = getPositionPreference(rankLog)
        tempPP = ""
        for i in pp:
            tempPP+= str(i) +"\n"
        tempPP = tempPP[:-1]
        with open(PATH + '\\summonerNameData.csv',mode='a') as f:
            writer = csv.DictWriter(f,["summonerName","summonerId","accountId","rank","pp","updated_date"])
            writer.writerow({"summonerName":summonerName,"summonerId":summonerId,
                             "accountId":accountId, "rank":rank, "pp":pp, "updated_date": updated_date})
rankScoreOnly = []
for i in rankScoreList:
    rankScoreOnly.append(i[1])
divSets = min_diff_sets(rankScoreOnly)
chosen = [["1"]]
while len(chosen[0]) != 5:
    chosen = divSets[random.randint(0,len(divSets)-1)]
team1 = []
teamChoice = random.randint(0,1)
for num in chosen[teamChoice]:
    temp = []
    for i in rankScoreList:
        if i[1] == num:
            temp.append(i)
    chosen2 = temp[random.randint(0,len(temp)-1)]
    team1.append(chosen2[0])
    rankScoreList.pop(rankScoreList.index(chosen2))
team2 = []
for i in summonerNameList:
    if i not in team1:
        team2.append(i)
random.shuffle(team1)
random.shuffle(team2)
team1_str = ""
for i in team1:
    team1_str+= (i+"//")
team2_str = ""
for i in team2:
    team2_str+= (i+"//")   
time_took = round(time.time() - start,3)

print(time_took)
print(team1_str)
print(team2_str)

    