import os
import discord
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(message.content)


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)
