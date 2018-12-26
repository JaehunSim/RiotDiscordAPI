# -*- coding: utf-8 -*-
from summoner_info import getSummonerId
from minDiffPartitioning import min_diff_sets, getUniqueDivSets, divideTeam
from util import DB_PATH, DISCORD_TOKEN, changeStrToList, initialize, initialize_discord
from discord_func import updateSummoner, getDivTeamList
from discord_command import _dice, _guide, _register, _register2, _voice, _most

import pandas as pd
import time, copy
from discord.ext import commands
import discord_logging

discord_logging.main()

bot = commands.Bot(command_prefix='!')

@bot.command()
async def dice(ctx):
    text = _dice()
    await ctx.send('Your Dice: {0}'.format(text))
    
@bot.command()
async def test(ctx):
    await ctx.send('I heard you! {0}'.format(ctx.author))

@bot.command()
async def register(ctx, arg1):
    _register(ctx,arg1)
    await ctx.send('You are successfully registered as {0}'.format(arg1))

@bot.command()
async def register2(ctx, id_tag, arg1):
    _register2(id_tag,arg1)
    await ctx.send('{1} is successfully registered as {0}'.format(arg1,id_tag))
    
@bot.command()
async def voice(ctx):
    text, length = _voice(ctx)
    text += '\n총 {0}명 있습니다.'.format(length)
    await ctx.send('{0}'.format(text))

@bot.command()
async def most(ctx, arg1, N=3, hist_range_fin=1):
    text = _most(arg1, N, hist_range_fin)
    await ctx.send("{}".format(text))
    
@bot.command()
async def guide(ctx):
    text = _guide()
    await ctx.send(text)
    
@bot.command()
async def rank(ctx, arg1):
    errorName = []
    arg1 = arg1.lower()
    data = pd.read_csv(DB_PATH + '\\summonerNameData.csv', encoding="euc-kr")
    try:
        a, b, data = updateSummoner(data, [arg1],errorName)
    except ValueError: 
        await ctx.send("Summoner Name Not Found: {0}".format(errorName[0]))
        errorName.pop()
        raise ValueError
    except Exception:
        await ctx.send("UnRank Detected: {0}".format(errorName[0]))
        errorName.pop()
        raise Exception
    
    index = data[data["summonerName"] == arg1].index[0]
    rank = data["rank"][index]
    await ctx.send("{0}님의 Tier: {1}".format(arg1,rank))
    
@bot.command()
async def setrank(ctx, arg1, arg2,arg3):
    arg1= arg1.lower()
    arg2= arg2.upper()
    arg3 = arg3.upper()
    if arg2 not in ["BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER"]:
        await ctx.send("Wrong rank input: {0}".format(arg2))
        raise ValueError
    if arg3 not in ["I","II","III","IV"]:
        await ctx.send("Wrong number input: {0}".format(arg3))
        raise ValueError    
    rank = arg2+ " "+ arg3
    data = pd.read_csv(DB_PATH + '\\summonerNameData.csv', encoding="euc-kr")
    length = len(data[data["summonerName"]==arg1])
    if length == 0:
        await ctx.send("다음은 등록되지 않은 소환사입니다: {0}".format(arg1))
        raise ValueError         
    originalRank = data.loc[data[data["summonerName"]==arg1].index[0],["rank"]][0]
    data.set_value(data[data["summonerName"]==arg1].index[0],"rank",rank)
    data.to_csv(DB_PATH + '\\summonerNameData.csv', index=False, encoding="euc-kr")
    await ctx.send("{0}님의 Tier가 {1} 에서 {2}로 변경됐습니다.".format(arg1,originalRank,rank))
    
@bot.command()
async def position(ctx, arg1, arg2, arg3, arg4, arg5):
    errorName = []
    data = pd.read_csv(DB_PATH + '\\summonerNameData.csv', encoding="euc-kr")
    summonerNameList =  [arg1, arg2, arg3, arg4, arg5]
    for index,value in enumerate(summonerNameList):
        summonerNameList[index] = value.lower()
    try:
        rankScoreList,rankList,data = updateSummoner(data, summonerNameList, errorName)
    except ValueError: 
        await ctx.send("Summoner Name Not Found: {0}".format(errorName[0]))
        errorName.pop()
        raise ValueError
    except Exception:
        await ctx.send("UnRank Detected: {0}".format(errorName[0]))
        errorName.pop()
        raise Exception
        
    ppList = []
    for name in summonerNameList:
        ppList.append(data["pp"][pd.Index(data["summonerName"]).get_loc(name)])
        
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
    await ctx.send(finalText)
        
@bot.command()
async def team(ctx, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10):
    errorName = []
    await ctx.send('Starting to divide teams')
    #time
    start = time.time()
    
    #data load
    data = pd.read_csv(DB_PATH + '\\summonerNameData.csv', encoding="euc-kr")
    
    #args load
    summonerNameList = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10]
    for index,value in enumerate(summonerNameList):
        summonerNameList[index] = value.lower()
    try:
        rankScoreList,rankList,data = updateSummoner(data, summonerNameList, errorName)
    except ValueError: 
        await ctx.send("Summoner Name Not Found: {0}".format(errorName[0]))
        errorName.pop()
        raise ValueError
    except Exception:
        await ctx.send("UnRank Detected: {0}".format(errorName[0]))
        errorName.pop()
        raise Exception
    rankScoreOnly = []
    for i in rankScoreList:
        rankScoreOnly.append(i[1])
    cases = []
    for count in range(1,4):
        divSets = min_diff_sets(rankScoreOnly)
        uniqueDivSets = getUniqueDivSets(divSets)
        
        ppList = []
        for name in summonerNameList:
            ppList.append(data["pp"][pd.Index(data["summonerName"]).get_loc(name)])
        
        finalList = getDivTeamList(rankScoreList, uniqueDivSets,summonerNameList, ppList)
        
        positionOrder = {"TOP":0,"JUN":1,"MID":2,"ADC":3,"SUP":4}
        for team in finalList:
            team.sort(key= lambda x: positionOrder[x[1]])
        
        for team in finalList:
            text = ""
            for positInfo in team:
                text+= ('{0:<3}: {1:<12} '.format(positInfo[1],positInfo[0]))
            cases.append(text)
    finalText = ""
    for i in range(len(cases)):
        if i %2 ==0:
            finalText += "Case: {0}\n".format(int((i+2)/2))
            finalText += "Blue Team:\n"
        else:
            if i != len(cases):
                finalText += "Purple Team:\n"
        finalText += cases[i]+"\n"
        if i%2 == 1:
            finalText += "\n"
    await ctx.send(finalText)
    time_took = round(time.time() - start,3)
    await ctx.send('Time Taken: {} seconds'.format(time_took))
    
        
@bot.command()
async def team2(ctx, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15):
    errorName = []
    await ctx.send('Starting to divide teams')
    #time
    start = time.time()
    #data load
    data = pd.read_csv(DB_PATH + '\\summonerNameData.csv', encoding="euc-kr")
    
    #args load
    summonerNameList = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15]
    for index,value in enumerate(summonerNameList):
        summonerNameList[index] = value.lower()
    try:
        rankScoreList,rankList,data = updateSummoner(data, summonerNameList, errorName)
    except ValueError: 
        await ctx.send("Summoner Name Not Found: {0}".format(errorName[0]))
        errorName.pop()
        raise ValueError
    except Exception:
        await ctx.send("UnRank Detected: {0}".format(errorName[0]))
        errorName.pop()
        raise Exception
    rankScoreOnly = []
    for i in rankScoreList:
        rankScoreOnly.append(i[1])
    cases = []
    for count in range(3):
        w = divideTeam(rankScoreList)
        w = w[:3]
        text = ""
        for i in w:
            text2 = ""
            for j in i:
                text2 += ('{0:<8} ').format(j[0])
            text2+= "\n"
            text += text2
        cases.append(text)

    finalText = ""
    for i in range(len(cases)):
        finalText += "Case: {0}\n".format(int((i+1)))
        finalText += cases[i]+"\n"
    await ctx.send(finalText)
    time_took = round(time.time() - start,3)
    await ctx.send('Time Taken: {} seconds'.format(time_took))
    
#names = "레박 zionavel 탑에사는괴물 호매실주민센터 반찬흔한백반 luna달달 ascute 용뿌잉뿌잉 요뚜기 서새봄의구독냥이 비가내리는길 말즤 cleann 바보다랑어 범실"
#names = names.split(" ")

#start running
bot.run(DISCORD_TOKEN)
