# -*- coding: utf-8 -*-
import random
from summoner_info import getSummonerId, getSummonerRank, getRankScore, getPositionPreference, getRankLog
from minDiffPartitioning import min_diff_sets
arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10 = "타푸고양이", "3월의토끼", "벌레포식자", "고대담배", "냐냥고양이", "필요악", "장서누", "신나라소녀", "굽신오리", "내등짝을형에게"
import csv
summonerNameData = []
with open('summonerNameData.csv','r') as f:
    summonerNameload = csv.DictReader(f,delimiter=',')
    for row in summonerNameload:
        summonerNameData.append(row)
summonerNameList = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10]
await ctx.send('Start Team Dividing')
rankScoreList = []
rankList = []
for summonerName in summonerNameList:
    gotId = False
    for i in summonerNameData:
        if summonerName == i["summonerName"]:
            gotId = True
            summonerId = i["summonerId"]
            break
    if not gotId:
        temp = getSummonerId(summonerName)
        summonerId = temp[0]
        with open('summonerNameData.csv',mode='a') as f:
            writer = csv.DictWriter(f,["summonerName","summonerId"])
            writer.writerow({"summonerName":summonerName,"summonerId":summonerId})
    rank = getSummonerRank(summonerId)
    rankList.append([summonerName,rank])
    rankScore = getRankScore(rank)
    rankScoreList.append([summonerName,rankScore])
    
await ctx.send('Rank_Call_Finished')
await ctx.send("{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}".format(rankList[0][0],rankList[0][1],rankList[1][0],rankList[1][1],rankList[2][0],rankList[2][1],rankList[3][0],rankList[3][1],rankList[4][0],rankList[4][1],rankList[5][0],rankList[5][1],rankList[6][0],rankList[6][1],rankList[7][0],rankList[7][1],rankList[8][0],rankList[8][1],rankList[9][0],rankList[9][1]))
rankScoreOnly = []
for i in rankScoreList:
    rankScoreOnly.append(i[1])
divSets = min_diff_sets(rankScoreOnly)
await ctx.send('hello3')
chosen = [["1"]]
while len(chosen[0]) != 5:
    chosen = divSets[random.randint(0,len(divSets)-1)]
await ctx.send('hello4')
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
await ctx.send('hello5')
await ctx.send(' team1: {}\nteam2: {}'.format(team1_str,team2_str))