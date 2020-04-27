import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!lh ')


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='unban', help='Desbanea a uno o mas usuarios del servidor')
    @commands.has_any_role('Moderador', 'Soporte')
    async def unban(self, ctx, *users: discord.User):
        for u in users:
            await ctx.guild.unban(u)
            await ctx.send(f'{u.mention} ha sido desbaneado.')

    @bot.command(name='roleid', help='Obten ID y nombre de un rol en un server.')
    async def rolid(self, ctx, role: discord.Role):
        await ctx.send(f'id: {role.id}, name: {role.name}')

    @bot.command(name='kick', help='Expulsa a uno o mas usuarios del servidor')
    @commands.has_any_role('Moderador', 'Soporte')
    async def kick(self, ctx, *users: discord.User):
        for u in users:
            await ctx.guild.kick(u)
            await ctx.send(f'{u.mention} ha sido expulsado.')

    @bot.command(name='ban', help='Banea a uno o mas usuarios del servidor')
    @commands.has_any_role('Moderador', 'Soporte')
    async def ban(self, ctx, *users: discord.User):
        for u in users:
            await ctx.guild.ban(u)
            await ctx.send(f'{u.mention} ha sido baneado.')

    @bot.command(name='info', help='Mas informacion sobre este bot')
    async def info(self, ctx):
        await ctx.send('Want to help me? : https://github.com/SouryMellow/pybot-for-lusthotel')
