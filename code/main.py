# -*- coding: utf-8 -*-
from util import DISCORD_TOKEN, RF_MODEL, ptpDFList
#from util import initialize, initialize_discord
from discord_command import _dice, _guide, _register, _register2, _voice, _most, _rank, _setrank, _position, _team, _team2, _predict
from discord.ext import commands
import discord_logging
discord_logging.main()

bot = commands.Bot(command_prefix='#')

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
    text = _rank(arg1,errorName)
    await ctx.send(text)
    
@bot.command()
async def setrank(ctx, arg1, arg2,arg3):
    text = _setrank(arg1,arg2,arg3)
    await ctx.send(text)
    
@bot.command()
async def position(ctx, arg1, arg2, arg3, arg4, arg5):
    errorName = []
    text = _position(arg1, arg2, arg3, arg4, arg5, errorName)
    await ctx.send(text)
        
@bot.command()
async def team(ctx, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10):
    errorName = []
    await ctx.send('Starting to divide teams')
    text = _team(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, errorName)
    await ctx.send(text)
    
@bot.command()
async def team2(ctx, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15):  
    errorName = []
    await ctx.send('Starting to divide teams')
    text = _team2(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, errorName)
    await ctx.send(text)   
    
@bot.command()
async def predict(ctx, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, RF_MODEL=RF_MODEL, ptpDFList=ptpDFList):  
    text = _predict(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, RF_MODEL, ptpDFList)
    await ctx.send(text)   
    
#names = "레박 zionavel 탑에사는괴물 호매실주민센터 반찬흔한백반 luna달달 ascute 용뿌잉뿌잉 요뚜기 서새봄의구독냥이 비가내리는길 말즤 cleann 바보다랑어 범실"
#names = names.split(" ")

#start running
bot.run(DISCORD_TOKEN)
