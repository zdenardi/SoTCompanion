from discord.ext import commands
from discord.ui import view
import discord
from scraper import SoTScraper
from pprint import pprint
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot("!", intents=discord.Intents.all())
client = discord.Client(intents=intents)
sentCookies = SoTScraper.getCookies()
print(CHANNEL_ID)


@bot.event
async def on_ready():
    global crew_list
    global sentCookies
    WELCOME_MESSAGE = "Arrr, Salty ready for orders 🏴‍☠️"
    print(WELCOME_MESSAGE)
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(WELCOME_MESSAGE)


@bot.command()
async def hello(ctx):

    await ctx.send("Greetings Matey")


@bot.command()
async def whoDoYouServe(ctx):
    await ctx.send("The seas are the only thing that control me")


@bot.command()
async def gold(ctx, pirate):
    match pirate:
        case "Zach":
            await ctx.send("Zach has 1 gold")
        case "Kevin":
            await ctx.send("Kevin has 2 gold")
        case _:
            await ctx.send("I'm not ready for that command yet")


@bot.command()
async def shipStat(ctx, ship):
    match ship:
        case "LockSmith":
            await ctx.send("By Last Check, the Locksmith earned 762,880 Gold 💰")
        case _:
            await ctx.send("I'm not ready for that command yet")


@bot.command()
async def printCrew(ctx):
    global sentCookies
    res = ""
    crew_list = SoTScraper.getCrew(sentCookies)
    for crew in crew_list:
        res = res + crew["Gamertag"] + "|" + crew["Role"] + "\n"
    await ctx.send(res)


@bot.command()
async def shipsCheck(ctx):
    global sentCookies
    ships_list = SoTScraper.getShips(sentCookies)
    embed = discord.Embed(title="Ship Sailing Status", color=discord.Color.blue())
    for ship in ships_list:
        name = ship["Name"]
        state = "Docked" if ship["SailingState"] == "NotAtSeaAvailable" else "Sailing"
        type = ship["Type"]

        embed.add_field(
            name=name, value="Type: " + type + " \n" + " Status: " + state + " \n"
        )

    await ctx.send(embed=embed)


@bot.command()
async def listChronicle(ctx):
    global sentCookies
    c_list = SoTScraper.getChronicle(sentCookies)
    embed = discord.Embed(title="Ship Chronicles", color=discord.Color.blue())

    for c in c_list:
        if "Item" in c:
            item = c["Item"]
            date = datetime.fromisoformat(c["CreatedAtUtc"])
            ship_name = item.get("ShipName")
            gold_earned = str(item.get("GoldEarned"))
            captain = item.get("Gamertag")
            days_at_sea = str(item.get("DaysAtSea"))
            embed.add_field(
                name="☠️" + ship_name,
                value="Gold Earned: "
                + "💰"
                + gold_earned
                + " \n"
                + "Captain: "
                + "🏴‍☠️"
                + captain
                + " \n"
                + "Days At Sea: "
                + "🌊"
                + days_at_sea
                + "\n"
                + "Date: "
                + date.strftime("%m/%d, %H:%M"),
            )

    await ctx.send(embed=embed)


# await channel.send("Kevin, I will soon replace you")


bot.run(BOT_TOKEN)
