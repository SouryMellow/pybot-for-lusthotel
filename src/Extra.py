import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!lh ')


class Extra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='sum', help='Suma una serie de numeros')
    async def sum(self, ctx, *nums: float):
        z = 0
        for n in nums:
            z = z + n
        await ctx.send(z)

    @bot.command(name='res', help='Resta una serie de numeros')
    async def res(self, ctx, *nums: float):
        z = 0
        for n in nums:
            z = z - n
        await ctx.send(z)

    @bot.command(name='mul', help='Multiplica una serie de numeros')
    async def mul(self, ctx, *nums: float):
        if len(nums) > 100:
            await ctx.send("No creo que necesites tantos numeros...")
        z = 1
        for n in nums:
            z = z * n
        await ctx.send(z)
