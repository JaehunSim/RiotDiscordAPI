# -*- coding: utf-8 -*-
from discord.ext import commands
import pandas as pd
import os, sys

PATH = os.path.dirname(os.path.realpath(sys.argv[0]))[:-5] + "\\db"
TOKEN = 'NDYzNTE4MDc4MjkwODg2NjY2.DhyBuQ.7wvrJO-qedyJdhB-u1Ddimi20LI'

bot = commands.Bot(command_prefix='!')

@bot.command()
async def test(ctx):
    print(ctx)
    await ctx.send('I heard you! {0}'.format(ctx.author))
    
@bot.command()
async def voice(ctx):
    voice_channel = ctx.author.voice.channel
    members = voice_channel.members
    
    names = []
    for member in members:
        names.append(member.display_name)
    text = ""
    for name in names:
        text += name + " "
    text = text[:-1]
    await ctx.send('{0}'.format(text))
    
@bot.command()
async def register(ctx, arg1):
    data = pd.read_excel(PATH+"\\discordNickNameChange.xlsx", encoding="euc-kr")
    id1 = ctx.author.id
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
        data.to_csv(PATH + '\\discordNickNameChange.xlsx', index=False, encoding="euc-kr")
    await ctx.send('You are successfully registered as {0}'.format(arg1))
    

bot.run(TOKEN)    