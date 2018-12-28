# -*- coding: utf-8 -*-
import random
from util import DB_PATH, changeStrToList
import pandas as pd
from summoner_info import getSummonerId, getMostN
from minDiffPartitioning import min_diff_sets, getUniqueDivSets, divideTeam
from discord_func import updateSummoner, getDivTeamList
import copy, time

def _dice():
    num = random.randint(1,100)
    return num

def _guide():
    text = ""
    text += "1. !dice : 주사위 1~100 까지 굴리기\n"
    text += "2. !voice: 자신이 있는 채널 맴버들 출력\n"
    text += "3. !rank 아이디: Rank 확인하기\n"
    text += "4. !most 아이디 N 기간: MostN 확인하기. 기간은 0~5 사이 지정. default: N=3, 기간=1\n"
    text += "5. !position id1 id2 id3 id4 id5: 5명 팀일때 포지션 자동 분배하기\n"
    text += "6. !team id1 id2 ... id10: 내전 10명일때 팀,포지션 자동 분배하기\n"
    text += "7. !setrank id1 rank number: id1의 rank를 수정합니다.\n\tex). !setrank 타푸고양이 PLATINUM III\n"
    text += "8. !register id1: 자신의 discord 아이디를 id1으로 등록합니다.\n"
    text += "9. !register2 id#tag id1: id#tag의 discord 아이디를 id1으로 등록합니다.\n"
    return text


def _register(ctx, arg1):
    data = pd.read_csv(DB_PATH+"\\discordNickNameChange.csv", encoding="euc-kr")
    #https://discordpy.readthedocs.io/en/rewrite/api.html#member
    id_tag = ctx.author.name + "#" + ctx.author.discriminator
    changed = False
    if id_tag not in data["discord_id_tag"].values:
        changed = True
        data = data.append({"discord_id_tag":id_tag,"nickname":arg1}, ignore_index=True)
    else:
        index = data[data["discord_id_tag"] == id_tag].index[0]
        nickname = data["nickname"][index]
        if nickname != arg1:
            changed = True
            data["nickname"][index] = arg1
    if changed:
        data.to_csv(DB_PATH + '\\discordNickNameChange.csv', index=False, encoding="euc-kr")
        
def _register2(id_tag, arg1):
    data = pd.read_csv(DB_PATH+"\\discordNickNameChange.csv", encoding="euc-kr")
    changed = False
    if id_tag not in data["discord_id_tag"].values:
        changed = True
        data = data.append({"discord_id_tag":id_tag,"nickname":arg1}, ignore_index=True)
    else:
        index = data[data["discord_id_tag"] == id_tag].index[0]
        nickname = data["nickname"][index]
        if nickname != arg1:
            changed = True
            data["nickname"][index] = arg1
    if changed:
        data.to_csv(DB_PATH + '\\discordNickNameChange.csv', index=False, encoding="euc-kr")
        
def _voice(ctx):
    data = pd.read_csv(DB_PATH+"\\discordNickNameChange.csv", encoding="euc-kr")
    voice_channel = ctx.author.voice.channel
    members = voice_channel.members
    names = []
    for member in members:
        id_tag = member.name + "#" + member.discriminator
#        await ctx.send('Your id: {0}'.format(member.id))
        if id_tag in data["discord_id_tag"].values:
            index = data[data["discord_id_tag"] == id_tag].index[0]
            name = data["nickname"][index]
            names.append(name)
        else:
            names.append(member.display_name)
    length = len(members)
    text = ""
    for name in names:
        text += name + " "
    text = text[:-1]
    return text, length

def _most(arg1, N, hist_range_fin):
    accountId = getSummonerId(arg1)[1]
    result, result2, result3 = getMostN(accountId,N, hist_range_fin)
    text = "{}".format(", ".join(result))
    if len(result2) >= 1:
        text += "\n주챔: {}".format(", ".join(result2))
    if len(result3) >= 1:
        text += "\n랭크 주챔: {}".format(", ".join(result3))
    return text

def _rank(arg1, errorName):
    arg1 = arg1.lower()
    data = pd.read_csv(DB_PATH + '\\summonerNameData.csv', encoding="euc-kr")
    try:
        a, b, data = updateSummoner(data, [arg1],errorName)
    except ValueError: 
        return "Summoner Name Not Found: {0}".format(errorName[0])
    except Exception:
        return "UnRank Detected: {0}".format(errorName[0])
    
    index = data[data["summonerName"] == arg1].index[0]
    rank = data["rank"][index]
    return "{0}님의 Tier: {1}".format(arg1,rank)
        
def _setrank(arg1, arg2,arg3):
    arg1= arg1.lower()
    arg2= arg2.upper()
    arg3 = arg3.upper()
    if arg2 not in ["BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER"]:
        return "Wrong rank input: {0}".format(arg2)
    if arg3 not in ["I","II","III","IV"]:
        return "Wrong number input: {0}".format(arg3)
    rank = arg2+ " "+ arg3
    data = pd.read_csv(DB_PATH + '\\summonerNameData.csv', encoding="euc-kr")
    length = len(data[data["summonerName"]==arg1])
    if length == 0:
        return "다음은 등록되지 않은 소환사입니다: {0}".format(arg1)        
    originalRank = data.loc[data[data["summonerName"]==arg1].index[0],["rank"]][0]
    data.set_value(data[data["summonerName"]==arg1].index[0],"rank",rank)
    data.to_csv(DB_PATH + '\\summonerNameData.csv', index=False, encoding="euc-kr")
    return "{0}님의 Tier가 {1} 에서 {2}로 변경됐습니다.".format(arg1,originalRank,rank)

def _position(arg1, arg2, arg3, arg4, arg5, errorName):
    data = pd.read_csv(DB_PATH + '\\summonerNameData.csv', encoding="euc-kr")
    summonerNameList =  [arg1, arg2, arg3, arg4, arg5]
    for index,value in enumerate(summonerNameList):
        summonerNameList[index] = value.lower()
    try:
        rankScoreList,rankList,data = updateSummoner(data, summonerNameList, errorName)
    except ValueError: 
        return "Summoner Name Not Found: {0}".format(errorName[0])
    except Exception:
        return "UnRank Detected: {0}".format(errorName[0])
        
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
    return finalText

def _team(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, errorName):
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
        return "Summoner Name Not Found: {0}".format(errorName[0])
    except Exception:
        return "UnRank Detected: {0}".format(errorName[0])
        
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
    time_took = round(time.time() - start,3)
    finalText += 'Time Taken: {} seconds'.format(time_took)
    return finalText

def _team2(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, errorName):
    start = time.time()
    data = pd.read_csv(DB_PATH + '\\summonerNameData.csv', encoding="euc-kr")
    summonerNameList = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15]
    for index,value in enumerate(summonerNameList):
        summonerNameList[index] = value.lower()
        
    try:
        rankScoreList,rankList,data = updateSummoner(data, summonerNameList, errorName)
    except ValueError: 
        return "Summoner Name Not Found: {0}".format(errorName[0])
    except Exception:
        return "UnRank Detected: {0}".format(errorName[0])
    
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
    time_took = round(time.time() - start,3)
    finalText += 'Time Taken: {} seconds'.format(time_took)
    return finalText

def _predict(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, RF_MODEL,ptpDFList):
    start = time.time()
    championData = pd.read_excel(DB_PATH+"\\championID.xlsx")
    argList = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10]
    games = []
    tempList = []
    for arg in argList:
        if arg in championData["name_2"].values:
            index1 = championData[championData["name_2"]==arg].index[0]
            tempList.append(championData["key"][index1])
        else:
            return "Wrong champion name: {}".format(arg)
    games.append(tempList)
    gamesDF = pd.DataFrame(games, 
                           columns=['team1_TOP', 'team1_JUN', 'team1_MID', 'team1_ADC', 'team1_SUP',
           'team2_TOP', 'team2_JUN', 'team2_MID', 'team2_ADC', 'team2_SUP'])
    for i in range(5):
        data2 = gamesDF.iloc[:,[i,5+i]]
        posit = gamesDF.columns[i][-3].lower()
        posit2 = gamesDF.columns[i+5][-3].lower()
        tempList = []
        for j in range(len(data2)):
            tempList.append(ptpDFList[i][data2.iloc[j,1]][data2.iloc[j,0]])
        gamesDF[posit+posit2+"s"] = tempList
    
    for i in range(5):
        data2 = gamesDF.iloc[:,[i,6]]
        posit = gamesDF.columns[i][-3].lower()
        posit2 = gamesDF.columns[6][-3].lower()
        tempList = []
        for j in range(len(data2)):
            tempList.append(ptpDFList[5+i][data2.iloc[j,1]][data2.iloc[j,0]])
        gamesDF[posit+posit2+"s"] = tempList
    for i in range(5):
        data2 = gamesDF.iloc[:,[1,5+i]]
        posit = gamesDF.columns[1][-3].lower()
        posit2 = gamesDF.columns[5+i][-3].lower()
        tempList = []
        for j in range(len(data2)):
            tempList.append(ptpDFList[10+i][data2.iloc[j,1]][data2.iloc[j,0]])
        gamesDF[posit+posit2+"s"] = tempList
        
    positList = [[0,2],[0,3],[2,3],[3,4],[5,7],[5,8],[7,8],[8,9]]
    count = 0
    for j,k in positList:
        data2 = gamesDF.iloc[:,[j,k]]
        posit = gamesDF.columns[j][-3].lower()
        posit2 = gamesDF.columns[k][-3].lower()
        tempList = []
        for l in range(len(data2)):
            tempList.append(ptpDFList[15+count][data2.iloc[l,1]][data2.iloc[l,0]])
        if j>= 5:
            gamesDF[posit+posit2+"2"] = tempList
        else:
            gamesDF[posit+posit2+"1"] = tempList
        count +=1
    
    data4 = gamesDF.iloc[:,[10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]]
    winRate = RF_MODEL.predict_proba(data4)[:,1]
    if winRate[0] >= 0.75:
        text = "1팀 조합이 유리합니다.\n"
    elif winRate[0] <= 0.25:
        text = "2팀 조합이 유리합니다.\n"
    else:
        text = "비등합니다!\n"
    text += "1팀이 이길 확률 {}".format(winRate[0])
    time_took = round(time.time() - start,3)
#    text += 'Time Taken: {} seconds'.format(time_took)
    return text

#names = "판테온 카밀 카시오페아 이렐리아 조이 라이즈 카직스 신드라 이즈리얼 그라가스"
#names = names.split(" ")
#from util import RF_MODEL,ptpDFList
#names.append(RF_MODEL)
#names.append(ptpDFList)
#w = _predict(*names)
