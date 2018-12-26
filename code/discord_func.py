# -*- coding: utf-8 -*-
import datetime, copy, random
from summoner_info import getSummonerId, getSummonerRank, getRankScore, getPositionPreference, getRankLog
import pandas as pd
from util import DB_PATH, changeStrToList

def updateSummoner(data, summonerNameList, errorName, update_period=7):
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
        data.to_csv(DB_PATH + '\\summonerNameData.csv', index=False, encoding="euc-kr")
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