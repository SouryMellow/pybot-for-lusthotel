import os
import discord
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} estoy en funcionamiento.')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Bienvenido {member.name}, espero este servidor sea para ti!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    x = ['xd']

    if message.content == '99':
        response = random.choice(x)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday Bro!')


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)
