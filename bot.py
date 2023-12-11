import os
import discord
from discord.ext import commands, tasks
from dataclasses import dataclass
from WebScraping import Scraper
from news import News
from gpt import AI
import asyncio
from fixblocking import NoBlock

BOT_TOKEN = os.environ["DISCORD_API_KEY"]
CHANNEL_ID = 996336625556652102


bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

class Web:
    def __init__(self, web_link):
        self.web_link = web_link

#Program varibles
stocknames=[]
channelID=996336625556652102
website=Web("")


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

@bot.command()
async def setCID(ctx: commands.Context):
    channelID=ctx.channel.id
    print(channelID)
    await ctx.send("Chennel ID has been set!")

@bot.event
async def on_ready():
    print("Is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Wussup")

@bot.tree.command(name="news")
async def news(interaction: discord.Interaction, link: str):
    await interaction.response.send_message("Please wait...", ephemeral=True)
    website.web_link=link
    await get_news()
    await interaction.delete_original_response()
    # print(args[2])


@tasks.loop(minutes=60)
async def get_news():
    media = Scraper(website.web_link)
    string = media.scrape()
    await bot.get_channel(channelID).send(string)



@tasks.loop(minutes=60)
async def stocknews():
    try:
        msg=await bot.get_channel(channelID).send("Please wait...")
        print("len of stocknames: "+str(len(stocknames)))

        for stock in stocknames:
            news_obj=News(stock)
            result = await newsAPI(stock)
            embed = discord.Embed(title="Stock: " + stock, colour=discord.Colour(0x3e038c))
            embed.add_field(name="Investment case:", value=result, inline=False)
            embed.add_field(name="Current price:", value=news_obj.getStockPrice()[1], inline=False)
            await bot.get_channel(channelID).send(embed=embed)

        await msg.delete()
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

    except Exception as e:

        print(f"An error occurred: {e}")

@NoBlock.to_thread
def run_ai(prompt, channel_id):
    ai_chat = AI(prompt)
    string = ai_chat.askAI()
    channel = bot.get_channel(channel_id)
    return string

async def newsAPI(prompt):
    news_obj = News(prompt)
    resp = await news_obj.getNews()
    return resp

@bot.tree.command(name="startstockloop")
async def startStock(interaction: discord.Interaction):
    await interaction.response.send_message("Starting stock loop", ephemeral=True)
    try:
        await stocknews.start()
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurredj: {e}")
    await interaction.delete_original_response()

# @bot.tree.command(name="stopstockloop")
@bot.tree.command(name="stopstockloop")
async def startStock(interaction: discord.Interaction):
    await interaction.response.send_message("Stopping stock loop", ephemeral=True)
    try:
        await newsAPI.stop()
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
    await interaction.delete_original_response()

@bot.tree.command(name="startnewsloop")
async def startStock(interaction: discord.Interaction):
    await interaction.response.send_message("Starting news loop", ephemeral=True)
    try:
        await get_news.start()
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
    await interaction.delete_original_response()

# @bot.tree.command(name="stopnewsloop")
@bot.tree.command(name="stopnewsloop")
async def startStock(interaction: discord.Interaction):
    await interaction.response.send_message("Stopping news loop", ephemeral=True)
    try:
        await get_news.stop()
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
    await interaction.delete_original_response()

@bot.tree.command(name="addstock")
async def startStock(interaction: discord.Interaction, prompt: str):
    await interaction.response.send_message("Please wait", ephemeral=True)
    news_obj=News(prompt)
    stock_name=news_obj.getStock()
    if stock_name==-1:
        await bot.get_channel(channelID).send("Invalid stock or description")
        await interaction.delete_original_response()
    else:
        stocknames.append(stock_name)
        await bot.get_channel(channelID).send("Successfully added: "+stock_name)
        await interaction.delete_original_response()

@bot.tree.command(name="getprice")
async def getprice(interaction: discord.Interaction, prompt: str):
    await interaction.response.send_message("Please wait", ephemeral=True)
    news_obj=News(prompt)
    price=news_obj.getStockPrice()
    if price==-1:
        await bot.get_channel(channelID).send("Invalid stock or description")
    else:
        embed = discord.Embed(title="Stock: " + price[0], colour=discord.Colour(0x3e038c))
        embed.add_field(name="Price:", value=price[1], inline=False)
        await bot.get_channel(channelID).send(embed=embed)

    await interaction.delete_original_response()

@bot.tree.command(name="addnews")
async def startStock(interaction: discord.Interaction, prompt: str):
    await interaction.response.send_message("Please wait", ephemeral=True)
    website.web_link=prompt
    await bot.get_channel(channelID).send("Adding the website to the list: "+website.web_link)
    await interaction.delete_original_response()



bot.run(BOT_TOKEN)





