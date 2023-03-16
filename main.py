import os
import discord
import requests
from discord import app_commands
from discord.ext import commands
from discord import Embed
import asyncio
import random

# Set up the Discord client and intents
bot = commands.Bot(command_prefix='s!', intents=discord.Intents.all())

def random_color():
    return random.randint(0, 0xFFFFFF)

@bot.event
async def on_ready():
    print('{0.user} is ready!'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} users!"))
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.tree.command(name='chkbtc', description='Checks the status of a Bitcoin transaction and provides Blockchain information.')
async def chkbtc(interaction: discord.Interaction, txid: str):
    try:
        
        response = requests.get(f'https://mempool.space/api/tx/{txid}')
        data = response.json()
        embed = Embed(title=f'Blockchain information for', description=f'**{txid}**', color=discord.Color.from_rgb(255,191,0))
        embed.add_field(name='Confirmed', value=data['status']['confirmed'])
        embed.add_field(name='Using Coinbase', value=data['vin'][0]['is_coinbase'])
        embed.set_footer(text='Information Provided By Crypto Bot')
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        embed = Embed(title=f'Error', color=discord.Color.from_rgb(231,76,60))
        embed.add_field(name='Invalid txid', value='TXID not found')
        embed.set_footer(text='Try a different TXID')
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name='alertbtc', description='Sends a DM when a Bitcoin transaction has been confirmed.')
async def alert_btc(interaction: discord.Interaction, txid: str):
    try:
        url = f"https://mempool.space/api/tx/{txid}"
        response = requests.get(url).json()
        confirmed = response.get("status", {}).get("confirmed")
        if confirmed:
            embed = Embed(title=f'Blockchain information for', description=f'**{txid}**', color=discord.Color.from_rgb(46,204,113))
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/853999284520484885.gif?size=240&quality=lossless")
            embed.add_field(name='Confirmed', value=confirmed)
            embed.add_field(name='Using Coinbase', value=response['vin'][0]['is_coinbase'])
            embed.set_footer(text='Information Provided By Crypto Bot')
            await interaction.response.send_message(embed=embed)
        else:
            embed = Embed(title='Waiting for confirmation', color=discord.Color.from_rgb(255,191,0))
            embed.add_field(name='Transaction ID', value=txid)
            embed.set_footer(text='Information Provided By Crypto Bot')
            await interaction.response.send_message(embed=embed)
            while True:
                response = requests.get(url).json()
                confirmed = response.get("status", {}).get("confirmed")
                if confirmed:
                    embed = Embed(title=f'Blockchain information for', description=f'**{txid}**', color=discord.Color.from_rgb(46,204,113)())
                    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/853999284520484885.gif?size=240&quality=lossless")
                    embed.add_field(name='Confirmed', value=confirmed)
                    embed.add_field(name='Using Coinbase', value=response['vin'][0]['is_coinbase'])
                    embed.set_footer(text='Information Provided By Crypto Bot')
                    await interaction.followup.send(embed=embed)
                    break
                else:
                    await asyncio.sleep(30)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        embed = Embed(title=f'Error', color=discord.Color.from_rgb(231,76,60)())
        embed.add_field(name='Invalid txid', value='TXID not found')
        embed.set_footer(text='Try a different TXID')
        await interaction.response.send_message(embed=embed)


# Start the client
bot.run("token")
