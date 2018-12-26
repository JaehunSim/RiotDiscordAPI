# -*- coding: utf-8 -*-
import random
from summoner_info import getSummonerId, getSummonerRank, getRankScore, getPositionPreference, getRankLog, getChampionPlayedList, predictPosition
from minDiffPartitioning import min_diff_sets
import time
import datetime
import pandas as pd
import os
import sys

PATH = os.path.dirname(os.path.realpath(sys.argv[0]))[:-5] + "\\db"
TOKEN = 'NDYzNTE4MDc4MjkwODg2NjY2.DhyBuQ.7wvrJO-qedyJdhB-u1Ddimi20LI'

initial = pd.DataFrame([],columns = ['summonerName', 'summonerId', 'accountId', 'rank', 'pp', 'cpl_pred','updated_date'])
initial.to_csv(PATH + '\\summonerNameData.csv', index=False, encoding="euc-kr")

arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10 = "타푸고양이", "3월의토끼", "벌레포식자", "고대담배", "냐냥고양이", "필요악", "장서누", "신나라소녀", "굽신오리", "내등짝을형에게"

start = time.time()
data = pd.read_csv(PATH + '\\summonerNameData.csv', encoding="euc-kr")
summonerNameList = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10]
rankScoreList = []
rankList = []
today = datetime.datetime.today()
changed = False
for summonerName in summonerNameList:
    gotId = False
    for index,value in enumerate(data["summonerName"]):
        if summonerName == value:
            updated_date = data["updated_date"][index]
            datetime_up = datetime.datetime(*[int(item) for item in updated_date.split('-')])
            timediff = today - datetime_up
            if timediff.days >= 2:
                print(1)
                data.drop(index, inplace=True)
                break
            gotId = True
            summonerId = data["summonerId"][index]
            accountId = data["accountId"][index]
            rank = data["rank"][index]
            pp = data["pp"][index]
            cpl_pred = data["cpl_pred"][index]
            rankList.append([summonerName,rank])
            rankScore = getRankScore(rank)
            rankScoreList.append([summonerName,rankScore])               
            break
    if not gotId:
        changed = True
        temp = getSummonerId(summonerName)
        summonerId = temp[0]
        accountId = temp[1]
        rank = getSummonerRank(summonerId)
        rankList.append([summonerName,rank])
        rankScore = getRankScore(rank)
        rankScoreList.append([summonerName,rankScore])
        updated_date = today.strftime('%Y-%m-%d')
        rankLog = getRankLog(accountId)
        pp = getPositionPreference(rankLog,2)
        cpl = getChampionPlayedList(rankLog)
        cpl_pred = predictPosition(cpl,2)
        data = data.append({"summonerName":summonerName,"summonerId":summonerId,"accountId":accountId,"rank":rank,
                            "pp":pp,"cpl_pred":cpl_pred,"updated_date":updated_date},ignore_index=True)

        

if changed:
    data.to_csv(PATH + '\\summonerNameData.csv', index=False, encoding="euc-kr")


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

    