# -*- coding: utf-8 -*-
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
TOKEN = 'NDYzNTE4MDc4MjkwODg2NjY2.DhyBuQ.7wvrJO-qedyJdhB-u1Ddimi20LI'

import random
from summoner_info import getSummonerId, getSummonerRank, getRankScore, getPositionPreference, getRankLog
from minDiffPartitioning import min_diff_sets
bot = commands.Bot(command_prefix='!')

@bot.command()
async def test(ctx):
    await ctx.send('I heard you! {0}'.format(ctx.author))

@bot.command()
async def dice(ctx):
    num = random.randint(1,100)
    await ctx.send('Your Dice: {0}'.format(num))

@bot.command()
async def team(ctx, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10):
    summonerNameList = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10]
    rankScoreList = []
    #positionList = []
    for summonerName in summonerNameList:
        summonerId = getSummonerId(summonerName)[0]
        #accountId = getSummonerId(summonerName)[1]
        rank = getSummonerRank(summonerId)
        rankScore = getRankScore(rank)
        rankScoreList.append([summonerName,rankScore])
        
        #rankLog = getRankLog(accountId)
        #pp = getPositionPreference(rankLog)
        #positionList.append([summonerName,pp])
    rankScoreOnly = []
    for i in rankScoreList:
        rankScoreOnly.append(i[1])
    divSets = min_diff_sets(rankScoreOnly)
    
    chosen = [["1"]]
    while len(chosen[0]) != 5:
        chosen = divSets[random.randint(0,len(divSets)-1)]
    
    team1 = []
    for num in chosen[0]:
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
    
    team1_str = ""
    for i in team1:
        team1_str+= (i+"//")
    
    team2_str = ""
    for i in team2:
        team2_str+= (i+"//")
    
    await ctx.send(' team1: {}\nteam2: {}'.format(team1_str,team2_str))

@bot.command()
async def team2(ctx, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10):
    summonerNameList = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10]
    await ctx.send('hello')
    rankScoreList = []
    #positionList = []
    for summonerName in summonerNameList:
        summonerId = getSummonerId(summonerName)[0]
        #accountId = getSummonerId(summonerName)[1]
        rank = getSummonerRank(summonerId)
        rankScore = getRankScore(rank)
        rankScoreList.append([summonerName,rankScore])
        
        #rankLog = getRankLog(accountId)
        #pp = getPositionPreference(rankLog)
        #positionList.append([summonerName,pp])
    await ctx.send('hello2')
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
    for num in chosen[0]:
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
    await ctx.send('hello5')
    
    team1_str = ""
    for i in team1:
        team1_str+= (i+"//")
    
    team2_str = ""
    for i in team2:
        team2_str+= (i+"//")
    
    await ctx.send(' team1: {}\nteam2: {}'.format(team1_str,team2_str))
    
#arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10 = "타푸고양이", "3월의토끼", "벌레포식자", "고대담배", "냐냥고양이", "필요악", "장서누", "신나라소녀", "굽신오리", "내등짝을형에게"
    
#start running
bot.run(TOKEN)