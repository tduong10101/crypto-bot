import coin
import json
from dotenv import dotenv_values
from discord.ext import commands
import discord

config = dotenv_values(".env")

TOKEN=config['DISCORD_TOKEN']
PREFIX=config['PREFIX']

bot = discord.Client()

### PREFIX ###
bot = commands.Bot(command_prefix=PREFIX)

# succesfully message


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

### CALL ###
#!info
@bot.command(name='info', help='bot info')
async def test(ctx):
    response = 'coin-bot'
    await ctx.send(response)

#!add-coin
@bot.command(name='add-coin')
async def test(ctx, name, coins):
    coin.add_coin(name,coins)
    await ctx.send(f"added {coins} to {name}'s list")

#!get-list
@bot.command(name='get-list')
async def test(ctx, name=None):
    if name==None:
        response=coin.get_coin_lists()
    else:
        response=coin.get_coin_list(name)
    
    await ctx.send(response)

#!lp
@bot.command(name='lp')
async def test(ctx, name=None, curr="AUD"):
    if name==None:
        response=f"Give me a list name! Call {PREFIX}get-list to get current lists."
    else:
        response=coin.get_coin_price(name=name, convert=curr)
    
    await ctx.send(response)
    
bot.run(TOKEN)