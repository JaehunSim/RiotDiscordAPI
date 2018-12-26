# -*- coding: utf-8 -*-
import random
from summoner_info import getSummonerId, getSummonerRank, getRankScore, getPositionPreference, getRankLog, getMostN
from minDiffPartitioning import min_diff_sets
import time
import datetime
import pandas as pd
import os
import sys
import logging
from discord.ext import commands
import copy
import csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def changeStrToList(str1):
    result = []
    temp = str1.split(",")
    result.append([temp[0][3:-1],int(temp[1][1:-1])])
    result.append([temp[2][3:-1],int(temp[3][1:-2])])
    return result

PATH = os.path.dirname(os.path.realpath(sys.argv[0]))[:-5] + "\\db"
TOKEN = 'NDYzNTE4MDc4MjkwODg2NjY2.DhyBuQ.7wvrJO-qedyJdhB-u1Ddimi20LI'

bot = commands.Bot(command_prefix='!')

@bot.command()
async def test(ctx):
    await ctx.send('I heard you! {0}'.format(ctx.author))

@bot.command()
async def dice(ctx):
    num = random.randint(1,100)
    await ctx.send('Your Dice: {0}'.format(num))

@bot.command()
async def most(ctx, arg1):
    accountId = getSummonerId(arg1)[1]
    result = getMostN(accountId,3)
    await ctx.send("{0}, {1}, {2}".format(result[0],result[1],result[2]))

#initial = pd.DataFrame([],columns = ['summonerName', 'summonerId', 'accountId', 'rank', 'pp','updated_date'])
#initial.to_csv(PATH + '\\summonerNameData.csv', index=False, encoding="euc-kr")

#arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10 = "타푸고양이", "3월의토끼", "벌레포식자", "고대담배", "냐냥고양이", "필요악", "장서누", "신나라소녀", "굽신오리", "내등짝을형에게"
@bot.command()
async def team(ctx, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10):
    start = time.time()
    data = pd.read_csv(PATH + '\\summonerNameData.csv', encoding="euc-kr")
    summonerNameList = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10]
    await ctx.send('Start Team Dividing')
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
                rankList.append([summonerName,rank])
                rankScore = getRankScore(rank)
                rankScoreList.append([summonerName,rankScore])               
                break
        if not gotId:
            changed = True
            temp = getSummonerId(summonerName)
            if temp == "error":
                await ctx.send("Summoner Name Not Found: {0}".format(summonerName))
                raise ValueError("Invlid SummonerName is in Input")
            summonerId = temp[0]
            accountId = temp[1]
            rank = getSummonerRank(summonerId)
            if rank=="UnRank":
                await ctx.send("UnRank Detected: {0}".format(summonerName))
                await ctx.send("다른 아이디를 넣어주세요")
                raise ValueError("UnRank is in Input")            
            rankList.append([summonerName,rank])
            rankScore = getRankScore(rank)
            rankScoreList.append([summonerName,rankScore])
            updated_date = today.strftime('%Y-%m-%d')
            rankLog = getRankLog(accountId)
            pp = getPositionPreference(rankLog,2)
            data = data.append({"summonerName":summonerName,"summonerId":summonerId,"accountId":accountId,"rank":rank,
                                "pp":pp,"updated_date":updated_date},ignore_index=True)
    
            
    
    if changed:
        data.to_csv(PATH + '\\summonerNameData.csv', index=False, encoding="euc-kr")
    
    ppList = []
    for name in summonerNameList:
        ppList.append(data["pp"][pd.Index(data["summonerName"]).get_loc(name)])
    
    rankScoreOnly = []
    for i in rankScoreList:
        rankScoreOnly.append(i[1])
    divSets = min_diff_sets(rankScoreOnly)
    
    tries = 0
    preserve = rankScoreList
    while True:
        rankScoreList = copy.deepcopy(preserve)
        tries += 1
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
        
        teams = [team1,team2]
        finalList = []
        for team in teams:
            team1PositList = []
            for member in team:
                team1PositList.append(ppList[summonerNameList.index(member)])
            
            
            team1_pre = []
            temp = []
            for index,value in enumerate(team1PositList):
                sum1 = 0
                if type(value) == str:
                    list1 = changeStrToList(value)
                else:
                    list1 = value
                for posit in list1:
                    sum1 += posit[1]
                for posit in list1:
                    team1_pre.append([index,posit[0],posit[1]/sum1])
            
            team1_DF = pd.DataFrame(team1_pre, columns =["member","position","rate"])
            team1_DF.sort_values("rate",inplace=True,ascending=False)
            pickedPosit = []
            for i in range(5):
                if len(team1_DF) != 0:
                    picked = team1_DF.iloc[0,:]
                    pickedPosit.append([team[picked["member"]],picked["position"]])
                    team1_DF = team1_DF[team1_DF["position"] != picked["position"]]
                    team1_DF = team1_DF[team1_DF["member"] != picked["member"]]
            finalList.append(pickedPosit)
        if len(finalList[0]) == 5 and len(finalList[1])==5:
            break
        if tries > 20 and ((len(finalList[0]) == 5 and len(finalList[1])==4) or (len(finalList[0]) == 4 and len(finalList[1])==4) ):
            for j in range(2):
                if len(finalList[j]) != 5:
                    temp = copy.deepcopy(teams[j])
                    for i in finalList[j]:
                        temp.pop(temp.index(i[0]))
                    positions = ["TOP","JUN","MID","ADC","SUP"]
                    for i in finalList[j]:
                        positions.pop(positions.index(i[1]))
                    finalList[j].append([temp[0],positions[0]])
            break
            
    
    positionOrder = {"TOP":0,"JUN":1,"MID":2,"ADC":3,"SUP":4}
    for team in finalList:
        team.sort(key= lambda x: positionOrder[x[1]])
    
    team1_str = ""
    for i in team1:
        team1_str+= (i+"//")
    team2_str = ""
    for i in team2:
        team2_str+= (i+"//")   
    time_took = round(time.time() - start,3)
    
    await ctx.send('Time Taken: {} seconds'.format(time_took))

    for team in finalList:
        text = ""
        for positInfo in team:
            text+= ('{0:<3}: {1:<12} '.format(positInfo[1],positInfo[0]))
        await ctx.send(text)
        
@bot.command()
async def team2(ctx, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10):
    start = time.time()
    summonerNameData = []
    with open(PATH + '\\summonerNameData.csv','r') as f:
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
                accountId = i["accountId"]
                rank = i["rank"]
                updated_date = i["updated_date"]
                rankList.append([summonerName,rank])
                rankScore = getRankScore(rank)
                rankScoreList.append([summonerName,rankScore])               
                break
        if not gotId:
            temp = getSummonerId(summonerName)
            summonerId = temp[0]
            accountId = temp[1]
            rank = getSummonerRank(summonerId)
            rankList.append([summonerName,rank])
            rankScore = getRankScore(rank)
            rankScoreList.append([summonerName,rankScore])
            updated_date = datetime.datetime.today().strftime('%Y-%m-%d')
            #rankLog = getRankLog(accountId)
            with open(PATH + '\\summonerNameData.csv',mode='a') as f:
                writer = csv.DictWriter(f,["summonerName","summonerId","accountId","rank","updated_date"])
                writer.writerow({"summonerName":summonerName,"summonerId":summonerId,
                                 "accountId":accountId, "rank":rank, "updated_date": updated_date})
        
    await ctx.send("{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}".format(rankList[0][0],rankList[0][1],rankList[1][0],rankList[1][1],rankList[2][0],rankList[2][1],rankList[3][0],rankList[3][1],rankList[4][0],rankList[4][1],rankList[5][0],rankList[5][1],rankList[6][0],rankList[6][1],rankList[7][0],rankList[7][1],rankList[8][0],rankList[8][1],rankList[9][0],rankList[9][1]))
    rankScoreOnly = []
    for i in rankScoreList:
        rankScoreOnly.append(i[1])
    divSets = min_diff_sets(rankScoreOnly)
    await ctx.send('Dividing team...')
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
    await ctx.send('Time Taken: {} seconds'.format(time_took))
    await ctx.send(' team1: {}\nteam2: {}'.format(team1_str,team2_str))
#start running
bot.run(TOKEN)
