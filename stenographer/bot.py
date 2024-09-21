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
    "id",
    "created_at",
    "edited_at",
    "clean_content",
    "author",
    "author_id",
    "author_avatar",
    "thread_id",
    "thread",
    "channel_id",
    "channel",
    "mentions",
]


description = """A discord bot that creates a CSV"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="?", description=description, intents=intents)


@bot.event
async def on_ready():
    url = (
        f"https://discordapp.com/oauth2/authorize?client_id={DISCORD_BOT_ID}&scope=bot"
    )
    print(f"Visit this link to invite the bot to your server: {url}")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
async def export(ctx):
    channels = ctx.message.channel_mentions
    print(channels)

    for channel in channels:
        filename = f"{channel.name}__[{channel.id}].csv"
        await write_message_history(
            channel.id, export_channel_id=ctx.channel.id, filename=filename
        )


async def write_message_history(channel_or_thread_id, export_channel_id, filename):
    channel_or_thread = bot.get_channel(channel_or_thread_id)
    export_channel = bot.get_channel(export_channel_id)

    with open(filename, "w+", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=FIELDNAMES,
            quoting=csv.QUOTE_ALL,
            lineterminator=os.linesep,
        )
        writer.writeheader()

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
                    "id": message.id,
                    "created_at": message.created_at,
                    "edited_at": message.edited_at,
                    "clean_content": message.clean_content,
                    "author": message.author.display_name,
                    "author_id": message.author.id,
                    "author_avatar": message.author.avatar,
                    "thread": message.thread.name if bool(message.thread) else None,
                    "thread_id": message.thread.id if bool(message.thread) else None,
                    "channel": message.channel,
                    "channel_id": message.channel.id,
                    "mentions": [message.mentions],
                }

                writer.writerow(row)

                if bool(message.thread):
                    thread_filename = f"{channel_or_thread.name}|{message.thread.name}__[{channel_or_thread.id}|{message.thread.id}].csv"
                    await write_message_history(
                        message.thread.id,
                        export_channel_id=export_channel_id,
                        filename=thread_filename,
                    )

                from_date = message.created_at

            if from_date == to_date:
                break

    await export_channel.send(
        f"Exported #{channel_or_thread.name}", file=discord.File(os.path.join(filename))
    )

    if os.path.exists(os.path.join(filename)):
        os.remove(os.path.join(filename))


def start_bot():
    bot.run(DISCORD_BOT_TOKEN)
