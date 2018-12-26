# -*- coding: utf-8 -*-
from discord.ext import commands
import logging
import os, sys

PATH = os.path.dirname(os.path.realpath(sys.argv[0]))[:-5] + "\\db"
TOKEN = 'NDYzNTE4MDc4MjkwODg2NjY2.DhyBuQ.7wvrJO-qedyJdhB-u1Ddimi20LI'

e =[]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

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

#bot.run(TOKEN)
