import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix='!lh ')


@bot.command(name='md')

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
