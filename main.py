import discord
import os
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True

client= discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello')

client.run('MTE0NjE2MTgyODgwNDY5NDA4Ng.GFBf76.OlJGcXmufWOfmaco0jJtfpOSN430LvgQjqMFJs')