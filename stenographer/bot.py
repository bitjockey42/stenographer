import os
import random

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
    async for message in channel.history(limit=1, oldest_first=True):
        print(message.clean_content)


bot.run(DISCORD_BOT_TOKEN)
