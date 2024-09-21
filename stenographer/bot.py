import os
import csv

from datetime import datetime, timezone

import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


description = """An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here."""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="?", description=description, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
async def export(ctx):
    await ctx.channel.send(f"Hello {ctx.author.display_name}")

    channel = bot.get_channel(ctx.channel.id)

    from_date = None
    async for message in channel.history(limit=1, oldest_first=True):
        from_date = message.created_at

    to_date = datetime.now(tz=timezone.utc)

    with open("test.csv", "w+", newline="") as csvfile:
        fieldnames = ["created_at", "clean_content", "author"]
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_ALL,
            lineterminator=os.linesep,
        )
        writer.writeheader()

        while from_date <= to_date:
            async for message in channel.history(
                after=from_date, limit=100, oldest_first=True
            ):
                print(f"{message.author.display_name}: {message.clean_content}")
                writer.writerow({
                    "created_at": message.created_at,
                    "clean_content": message.clean_content,
                    "author": message.author.display_name
                })

                from_date = message.created_at

            if from_date == to_date:
                break


bot.run(DISCORD_BOT_TOKEN)
