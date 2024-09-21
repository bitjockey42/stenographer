import os
import csv

from datetime import timedelta

import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_BOT_ID = int(os.getenv("DISCORD_BOT_ID"))
FIELDNAMES = [
    "created_at",
    "clean_content",
    "author",
    "author_id",
    "thread_id",
    "thread",
]


description = """An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here."""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="?", description=description, intents=intents)


@bot.event
async def on_ready():
    url = f"https://discordapp.com/oauth2/authorize?client_id={DISCORD_BOT_ID}&scope=bot"
    print(f"Visit this link to invite the bot to your server: {url}")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
async def export(ctx):
    await ctx.channel.send(f"Hello {ctx.author.display_name}")

    with open(f"{ctx.channel.id}.csv", "w+", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=FIELDNAMES,
            quoting=csv.QUOTE_ALL,
            lineterminator=os.linesep,
        )
        writer.writeheader()

        await write_message_history(ctx.channel.id, writer=writer)


async def write_message_history(channel_or_thread_id, writer):
    channel_or_thread = bot.get_channel(channel_or_thread_id)
    from_date = None
    async for message in channel_or_thread.history(limit=1, oldest_first=True):
        from_date = message.created_at - timedelta(days=1)

    to_date = None
    async for message in channel_or_thread.history(limit=1):
        to_date = message.created_at

    while from_date <= to_date:
        async for message in channel_or_thread.history(
            after=from_date, limit=100, oldest_first=True
        ):
            if (
                message.clean_content.startswith("?export")
                or message.author.id == DISCORD_BOT_ID
            ):
                from_date = message.created_at
                continue

            row = {
                "created_at": message.created_at,
                "clean_content": message.clean_content,
                "author": message.author.display_name,
                "author_id": message.author.id,
                "thread": message.thread.name if bool(message.thread) else None,
                "thread_id": message.thread.id if bool(message.thread) else None,
            }

            writer.writerow(row)

            if bool(message.thread):
                with open(f"{message.thread.id}.csv", "w+", newline="") as csvfile:
                    thread_writer = csv.DictWriter(
                        csvfile,
                        fieldnames=FIELDNAMES,
                        quoting=csv.QUOTE_ALL,
                        lineterminator=os.linesep,
                    )
                    thread_writer.writeheader()
                    await write_message_history(message.thread.id, writer=thread_writer)

            from_date = message.created_at

        if from_date == to_date:
            break


bot.run(DISCORD_BOT_TOKEN)
