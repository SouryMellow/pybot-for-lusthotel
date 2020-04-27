import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix='!lh ')

# channel: 607768450160656402

# bot: 275813801792634880
@bot.event
async def on_ready():
    print('ready')


@bot.command(name='emojid')
async def emojid(ctx, emoji: discord.Emoji):
    await ctx.send(f'id: {emoji.id}, name: {emoji.name}')


@bot.command(name='roleid', help='Obten ID y nombre de un rol en un server.')
async def rolid(ctx, role: discord.Role):
    await ctx.send(f'id: {role.id}, name: {role.name}')


@bot.command(name='chasquido_thanos')
async def i(ctx):
    channel_ID = 607768450160656402
    message_ID = 609831791699951628
    role_ID = 701492794618937434
    msg = await ctx.guild.get_channel(
        channel_ID).fetch_message(message_ID)

    reaction = msg.reactions
    members = ctx.guild.members
    users = await reaction[0].users().flatten()

    for u in users:
        for m in members:
            if m.id == u.id:
                print(f'{m} added')
                await m.add_roles(ctx.guild.get_role(role_ID))
                break

    await ctx.send('Trabajo terminado.')


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
