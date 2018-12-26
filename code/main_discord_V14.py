# -*- coding: utf-8 -*-
import random
from summoner_info import getSummonerId, getSummonerRank, getRankScore, getPositionPreference, getRankLog, getMostN
from minDiffPartitioning import min_diff_sets, getUniqueDivSets, divideTeam
import time
import datetime
import pandas as pd
import os
import sys
from discord.ext import commands
import copy

PATH = os.path.dirname(os.path.realpath(sys.argv[0]))[:-5] + "\\db"
TOKEN = 'NDYzNTE4MDc4MjkwODg2NjY2.DhyBuQ.7wvrJO-qedyJdhB-u1Ddimi20LI'
errorName =[]

import logging
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

def initialize():
    initial = pd.DataFrame([],columns = ['summonerName', 'summonerId', 'accountId', 'rank', 'pp','updated_date'])
    initial.to_csv(PATH + '\\summonerNameData.csv', index=False, encoding="euc-kr")

def initialize_discord():
    initial = pd.DataFrame([],columns = ['discord_id', 'nickname'])
    initial.to_excel(PATH + '\\discordNickNameChange.xlsx', index=False, encoding="euc-kr")

def updateSummoner(data, summonerNameList, update_period=7):
    #initial var
    rankScoreList = []
    rankList = []
    changed = False
    today = datetime.datetime.today()
    
    for summonerName in summonerNameList:
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

def getDivTeamList(rankScoreList, uniqueDivSets,summonerNameList, ppList):
    tries = 0
    preserve = rankScoreList
    while True:
        tries += 1
        
        rankScoreList = copy.deepcopy(preserve)
        team1 = []
        team2 = []
        
        chosen = uniqueDivSets[random.randint(0,len(uniqueDivSets)-1)]
        teamChoice = random.randint(0,1)
        
        #team division by uniqueDivSets
        for num in chosen[teamChoice]:
            team1_candidate = []
            for rankInfo in rankScoreList:
                score = rankInfo[1]
                if score == num:
                    team1_candidate.append(rankInfo)
            #chose btw same score
            chosen2 = team1_candidate[random.randint(0,len(team1_candidate)-1)]
            team1.append(chosen2[0])
            rankScoreList.pop(rankScoreList.index(chosen2))
            
        for name in summonerNameList:
            if name not in team1:
                team2.append(name)
                
        random.shuffle(team1)
        random.shuffle(team2)
        teams = [team1,team2]
        
        #picking position
        finalList = []
        for team in teams:
            #get team_position_rate -> getting team_DF for position matching
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
            team_DF = pd.DataFrame(team_pre, columns =["member","position","rate"])
            team_DF.sort_values("rate",inplace=True,ascending=False)
            
            pickedPosit = []
            for i in range(5):
                if len(team_DF) != 0:
                    #weighted sampling from position_rate
                    sampled = team_DF.sample(1, weights=team_DF["rate"].values).index[0]
                    
                    picked = team_DF.loc[sampled,:]
                    pickedPosit.append([team[picked["member"]],picked["position"]])
                    team_DF = team_DF[team_DF["position"] != picked["position"]]
                    team_DF = team_DF[team_DF["member"] != picked["member"]]
                    
            finalList.append(pickedPosit)
        
        #filling missing position
        if len(finalList[0]) == 5 and len(finalList[1])==5:
            break
        if tries > 20 and ((len(finalList[0]) == 5 and len(finalList[1])==4) or (len(finalList[0]) == 4 and len(finalList[1])==5) or (len(finalList[0]) == 4 and len(finalList[1])==4) ):
            for index in range(len(finalList)):
                team = finalList[index]
                if len(team) != 5:
                    team_all_members = copy.deepcopy(teams[index])
                    positions = ["TOP","JUN","MID","ADC","SUP"]
                    for memberInfo in team:
                        memberName, position = memberInfo[0], memberInfo[1]
                        team_all_members.remove(memberName)
                        positions.remove(position)
                    team.append([team_all_members[0],positions[0]])
            break
        if tries > 100:
            for index in range(len(finalList)):
                team = finalList[index]
                while len(team) != 5:
                    team_all_members = copy.deepcopy(teams[index])
                    positions = ["TOP","JUN","MID","ADC","SUP"]
                    for memberInfo in team:
                        memberName, position = memberInfo[0], memberInfo[1]
                        team_all_members.remove(memberName)
                        positions.remove(position)
                    team.append([team_all_members[0],positions[0]])
            break
    return finalList

bot = commands.Bot(command_prefix='!')

@bot.command()
async def dice(ctx):
    num = random.randint(1,100)
    await ctx.send('Your Dice: {0}'.format(num))
    
@bot.command()
async def test(ctx):
    print(ctx)
    await ctx.send('I heard you! {0}'.format(ctx.author))

@bot.command()
async def register(ctx, arg1):
    data = pd.read_excel(PATH+"\\discordNickNameChange.xlsx", encoding="euc-kr")
    id1 = int(ctx.author.id)
    if id1 not in data["discord_id"].values:
        changed = True
        data = data.append({"discord_id":id1,"nickname":arg1}, ignore_index=True)
    else:
        index = data[data["discord_id"] == id1].index[0]
        nickname = data["nickname"][index]
        if nickname != arg1:
            changed = True
            data["nickname"][index] = arg1
    if changed:
        data.to_excel(PATH + '\\discordNickNameChange.xlsx', index=False, encoding="euc-kr")
    await ctx.send('You are successfully registered as {0}'.format(arg1))
    
@bot.command()
async def voice(ctx):
    data = pd.read_excel(PATH+"\\discordNickNameChange.xlsx", encoding="euc-kr")
    voice_channel = ctx.author.voice.channel
    members = voice_channel.members
    
    names = []
    for member in members:
        if member.id in data["discord_id"].values:
            index = data[data["discord_id"] == member.id].index[0]
            name = data["nickname"][index]
            names.append(member.name)
        else:
            names.append(member.display_name)
    length = len(members)
    text = ""
    for name in names:
        text += name + " "
    text = text[:-1]
    await ctx.send('{0}'.format(text))
    await ctx.send('총 {0}명 있습니다.'.format(length))


@bot.command()
async def most(ctx, arg1):
    accountId = getSummonerId(arg1)[1]
    result = getMostN(accountId,3)
    await ctx.send("{0}, {1}, {2}".format(result[0],result[1],result[2]))
    
@bot.command()
async def guide(ctx):
    text = ""
    text += "!dice : 주사위 1~100 까지 굴리기\n"
    text += "!voice: 자신이 있는 채널 맴버들 출력\n"
    text += "!rank 아이디: Rank 확인하기\n"
    text += "!most 아이디: Most3 확인하기\n"
    text += "!position id1 id2 id3 id4 id5: 5명 팀일때 포지션 자동 분배하기\n"
    text += "!team id1 id2 ... id10: 내전 10명일때 팀,포지션 자동 분배하기\n"
    text += "!setrank id1 rank number: id1의 rank를 수정합니다. rank는 BRONZE, SILVER, GOLD, PLATINUM, DIAMOND, MASTER, CHALLENGER + I,II,III,IV 조합으로 쓰시면 됩니다.\nex). !setrank 타푸고양이 PLATINUM III"
    await ctx.send(text)
@bot.command()
async def rank(ctx, arg1):
    arg1 = arg1.lower()
    data = pd.read_csv(PATH + '\\summonerNameData.csv', encoding="euc-kr")
    try:
        a, b, rank = updateSummoner(data, [arg1])
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
        errorName.pop()
        raise ValueError
    if arg3 not in ["I","II","III","IV"]:
        await ctx.send("Wrong number input: {0}".format(arg3))
        errorName.pop()
        raise ValueError    
    rank = arg2+ " "+ arg3
    data = pd.read_csv(PATH + '\\summonerNameData.csv', encoding="euc-kr")
    length = len(data[data["summonerName"]==arg1])
    if length == 0:
        await ctx.send("다음은 등록되지 않은 소환사입니다: {0}".format(arg1))
        errorName.pop()
        raise ValueError         
    originalRank = data.loc[data[data["summonerName"]==arg1].index[0],["rank"]][0]
    data.set_value(data[data["summonerName"]==arg1].index[0],"rank",rank)
    data.to_csv(PATH + '\\summonerNameData.csv', index=False, encoding="euc-kr")
    await ctx.send("{0}님의 Tier가 {1} 에서 {2}로 변경됐습니다.".format(arg1,originalRank,rank))
    
@bot.command()
async def position(ctx, arg1, arg2, arg3, arg4, arg5):
    data = pd.read_csv(PATH + '\\summonerNameData.csv', encoding="euc-kr")
    summonerNameList =  [arg1, arg2, arg3, arg4, arg5]
    for index,value in enumerate(summonerNameList):
        summonerNameList[index] = value.lower()
    try:
        rankScoreList,rankList,data = updateSummoner(data, summonerNameList)
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
    await ctx.send('Starting to divide teams')
    #time
    start = time.time()
    
    #data load
    data = pd.read_csv(PATH + '\\summonerNameData.csv', encoding="euc-kr")
    
    #args load
    summonerNameList = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10]
    for index,value in enumerate(summonerNameList):
        summonerNameList[index] = value.lower()
    try:
        rankScoreList,rankList,data = updateSummoner(data, summonerNameList)
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
    await ctx.send('Starting to divide teams')
    #time
    start = time.time()
    #data load
    data = pd.read_csv(PATH + '\\summonerNameData.csv', encoding="euc-kr")
    
    #args load
    summonerNameList = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15]
    for index,value in enumerate(summonerNameList):
        summonerNameList[index] = value.lower()
    try:
        rankScoreList,rankList,data = updateSummoner(data, summonerNameList)
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
bot.run(TOKEN)
