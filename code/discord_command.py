# -*- coding: utf-8 -*-
import random
from util import DB_PATH
import pandas as pd
from summoner_info import getSummonerId, getMostN

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