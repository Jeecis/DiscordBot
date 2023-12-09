import datetime
import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands, tasks
from dataclasses import dataclass
from WebScraping import Scraper
from news import News
from gpt import AI
import typing
import functools
import asyncio
from fixblocking import NoBlock

BOT_TOKEN = os.environ["DISCORD_API_KEY"]
# BOT_TOKEN = "MTE0NjE2MTgyODgwNDY5NDA4Ng.Gj1_IV.jPzDVmIvOJEDg9h0gZfMS9lT5Fk7TK_0vemUX4"
# print(BOT_TOKEN)
CHANNEL_ID = 996336625556652102
MAX_SESSION_TIME_MINUTES = 1


@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0


bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())


# session =Session()

@bot.command()
async def sync(ctx: commands.Context, guild: discord.Guild = None) -> None:
    print("Syncing commands")
    sync=0
    if guild is None:
        print("Guild is None")
        sync=len(await bot.tree.sync())
    else:
        print("Guild found")
        sync=len(await bot.tree.sync(guild=guild))

    print(f"Synced {sync} command(s)")

@bot.event
async def on_ready():
    print("Is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Wussup")
    # try:
    #     synced = await bot.tree.sync(guild=discord.Object(850296892347777036))
    #     print(f"Synced {len(synced)} command(s)")
    # except Exception as e:
    #     print(e)


@bot.tree.command(name="news")
async def news(interaction: discord.Interaction, link: str):
    web_link = await get_news(link, interaction.channel.id)
    await interaction.response.send_message(web_link, ephemeral=True)
    # print(args[2])


@tasks.loop(minutes=60)
async def get_news(link, channel_id):
    media = Scraper(link)
    string = media.scrape()
    channel = bot.get_channel(channel_id)
    return string


@bot.tree.command(name="stocknews")
async def stocknews(interaction: discord.Interaction, prompt: str):
    try:

        await interaction.response.send_message("Please wait...", ephemeral=True)
        channel = bot.get_channel(interaction.channel.id)

        result = await newsAPI(prompt, interaction.channel.id)
        print(result)
        await interaction.delete_original_response()

        embed = discord.Embed(title="Author: " + interaction.user.name, colour=discord.Colour(0x3e038c))

        embed.add_field(name="Coefficient:", value=result, inline=False)
        await channel.send(embed=embed)
        await channel.send(f"{interaction.user.mention} " + result)

        #
        # msg = await interaction.edit_original_response()
        # await msg.edit(content=result)
    except discord.errors.NotFound:
        # Handle NotFound error
        print("Interaction not found or expired.")
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")


@bot.tree.command(name="ai")
async def ai(interaction: discord.Interaction, prompt: str):
    try:

        await interaction.response.send_message("Please wait...", ephemeral=True)
        channel = bot.get_channel(interaction.channel.id)

        task = asyncio.create_task(run_ai(prompt, interaction.channel.id))
        result = await task
        print(result)
        await interaction.delete_original_response()

        embed = discord.Embed(title="Author: " + interaction.user.name, colour=discord.Colour(0x3e038c))

        embed.add_field(name="Prompt:", value=prompt, inline=False)
        await channel.send(embed=embed)
        await channel.send(f"{interaction.user.mention} " + result)

        #
        # msg = await interaction.edit_original_response()
        # await msg.edit(content=result)
    except discord.errors.NotFound:
        # Handle NotFound error
        print("Interaction not found or expired.")
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")

@NoBlock.to_thread
def run_ai(prompt, channel_id):
    ai_chat = AI(prompt)
    string = ai_chat.askAI()
    channel = bot.get_channel(channel_id)
    return string

@tasks.loop(minutes=1)
async def newsAPI(prompt, channel_id):
    news_obj = News(prompt)
    resp = await news_obj.getNews()
    channel = bot.get_channel(channel_id)
    return resp


bot.run(BOT_TOKEN)





