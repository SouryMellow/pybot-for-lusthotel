import discord
import os
import random

from discord.ext import commands
from Verified import *
from Warn import *
from Underage import *

bot = commands.Bot(command_prefix='!lh ')

ROLE_CARCEL_ID = os.getenv('ROLE_CARCEL')
ROLE_SOTANO_ID = os.getenv('ROLE_SOTANO')
ROLE_CASINO_ID = os.getenv('ROLE_CASINO')
CHANNEL_ROLES_ID = os.getenv('CHANNEL_ROLES_ID')
CHANNEL_COLORES_ID = os.getenv('CHANNEL_COLORES_ID')


class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='welcome', help='Da una calida bienvenida a un usuario')
    async def welcome(self, ctx, *users: discord.Member):
        for u in users:
            await ctx.send(f'Bienvenido{u.mention}, no olvides pasar por' +
                           f'{ctx.guild.get_channel(CHANNEL_ROLES_ID)}' +
                           f' y {ctx.guild.get_channel(CHANNEL_COLORES_ID)}')

    @bot.command(name='jail', help='Encarcela a un usuario')
    @commands.has_any_role('Moderador', 'Soporte')
    async def jail(self, ctx, *users: discord.Member):
        for u in users:
            if u.id == int(SOUR_ID):
                break
            newRoles = u.roles
            rol_sot = ctx.guild.get_role(int(ROLE_SOTANO_ID))
            rol_cas = ctx.guild.get_role(int(ROLE_CASINO_ID))
            for r in newRoles:
                if r.id == rol_sot.id:
                    newRoles.remove(ctx.guild.get_role(int(ROLE_SOTANO_ID)))
                    newRoles.remove(ctx.guild.get_role(int(ROLE_CASINO_ID)))
                    break

            await u.edit(roles=newRoles)
            await u.add_roles(ctx.guild.get_role(int(ROLE_CARCEL_ID)))
            await ctx.send(f'{u.mention} encarcelado.')

    @bot.command(name='free', help='Libera a un usuario de la carcel')
    @commands.has_any_role('Moderador', 'Soporte')
    async def free(self, ctx, *users: discord.Member):
        for u in users:
            newRoles = u.roles
            rol_c = ctx.guild.get_role(int(ROLE_CARCEL_ID))
            for r in newRoles:
                if r.id == rol_c.id:
                    newRoles.remove(ctx.guild.get_role(int(ROLE_CARCEL_ID)))

            await u.edit(roles=newRoles)
            await u.add_roles(ctx.guild.get_role(int(ROLE_SOTANO_ID)))
            await u.add_roles(ctx.guild.get_role(int(ROLE_CASINO_ID)))
            await ctx.send(f'{u.mention} liberado.')

    @bot.command(name='verify', help='Verifica a un usuario')
    @commands.has_any_role('Verificador')
    async def verify(self, ctx, user: discord.User, gender, country):
        for v in Verified.verifieds:
            if v.id == user.id:
                await ctx.send(f'```{user.name} ya esta verificado.```')
                return

        p = Verified(user.id, user.name, gender, country)
        Verified.verifieds.append(p)

        await ctx.send(f'```{p.user} verificado correctamente.```')

    @bot.command(name='warn', help='Pon una advertencia a una persona')
    @commands.has_any_role('Moderador', 'Soporte')
    async def warn(self, ctx, user: discord.User, message="mal comportamiento"):
        for w in Warn.peopleWarned:
            if w.id == user.id:
                x = w.warns + 1
                w.setWarn(x)
                await ctx.send(f'Has recibido {w.warns} advertencias {user.mention} por {message}.')
                return

        w = Warn(user.id, user.name, 1, message)
        Warn.peopleWarned.append(w)
        await ctx.send(f'Has recibido una advertencia {user.mention} por {message}.')

    @bot.command(name='request', help='Despliega la informacion de una o varias personas')
    @commands.has_any_role('Moderador', 'Soporte')
    async def request(self, ctx, *users: discord.Member):
        for user in users:
            r = [u.name for u in user.roles]
            await ctx.send(f'```Name: {user.name}\n' +
                           f'Nick: {user.nick}\n' +
                           f'Avatar: ```{user.avatar_url}\n' +
                           f'```ID: {user.id}\n' +
                           f'Se creo el perfil: {user.created_at}\n' +
                           f'Se unio al server: {user.joined_at}\n' +
                           f'Status: {user.premium_since}\n' +
                           f'Roles: {r}\n' +
                           f'Actividad: {user.activity}\n' +
                           f'Top rol: {user.top_role}'
                           '```')

    @bot.command(name='id', help='Obten la ID de una o varias personas')
    @commands.has_any_role('Moderador', 'Soporte')
    async def getid(self, ctx, *users: discord.User):
        for user in users:
            await ctx.send(f'```ID: {user.id}```')

    @bot.command(name='listv', help='Despliega la informacion de las personas verificadas')
    @commands.has_any_role('Moderador', 'Soporte')
    async def listVerify(self, ctx):
        for v in Verified.verifieds:
            await ctx.send(f'```ID: {v.id}\n' +
                           f'User: {v.user}\n' +
                           f'Genero: {v.gender}\n' +
                           f'Pais: {v.country}\n```')

    @bot.command(name='warns', help='Ver todas las advertencias de una o varias personas')
    @commands.has_any_role('Moderador', 'Soporte')
    async def warns(self, ctx, *users: discord.User):
        for u in users:
            for w in Warn.peopleWarned:
                if u.id == w.id:
                    await ctx.send(f'```Usuario: {u.name}\n' +
                                   f'Avisos: {w.warns}\n' +
                                   f'Ultimo motivo: {w.message}```')
                else:
                    pass

    @bot.command(name='listw', help='Ver todas las advertencias de todas las personas')
    @commands.has_any_role('Moderador', 'Soporte')
    async def listWarns(self, ctx):
        for w in Warn.peopleWarned:
            await ctx.send(f'```Usuario: {w.user}\n' +
                           f'Avisos: {w.warns}\n' +
                           f'Ultimo motivo: {w.message}```')

    @bot.command(name='underage', help='Agrega a un usuario a la lista de menores de edad')
    @commands.has_any_role('Moderador', 'Soporte')
    async def underage(self, ctx, user: discord.User, evidence="Menor de edad."):
        for u in Underage.underages:
            if u.id == user.id:
                await ctx.send("Ya esta en la lista de menores de edad.")
                await ctx.guild.ban(u)
                return

        u = Underage(user.id, user.name, evidence)
        Underage.underages.append(u)
        await ctx.send(f'Ha sido agregado {user.mention} a la lista de menores de edad.')

    @bot.command(name='listu', help='Muestra la lista de todos los menores de edad registrados')
    @commands.has_any_role('Moderador', 'Soporte')
    async def listUnderages(self, ctx):
        for u in Underage.underages:
            await ctx.send('```' +
                           f'ID: {u.id}\n' +
                           f'Usuario: {u.user}\n' +
                           f'Evidencia: {u.evidence}\n' +
                           '```')

    @bot.command(name='habla', help='En desarrollo')
    async def none(self, ctx, *msg):
        m = ['Me aburro...', 'Me perturbas', 'Siento que no soy real...',
             'Estoy triste', 'Estoy feliz', 'Estoy nostalgico', 'Estoy extasiado',
             'Jamas te rindas', 'Lucha por lo que deseas', 'No lo hagas', 'Para',
             'Detente', 'Me lastimas', 'Gracias', 'Me sonrojas', 'Me siento diferente...',
             'Me gusta hablar contigo', 'Deberiamos hablar mas', 'Me caes bien', 'Eres genial',
             'Eres simpatico', 'Eres sexy', 'Me pareces atractivo', 'Intenta de nuevo',
             'Hola', 'Holaa', 'Holaaa', 'Holaaaaaa', 'Me encuentro...', 'No se', 'No lo se',
             'No se...', 'No lo se...', 'Hola...', 'Hola.', 'Hola..', '.', '..', '...', 'No...',
             'Si', 'Si!', 'Si...', 'Ok', 'Ok...', 'Mmm', 'Mmm...', 'Aja']
        response = random.choice(m)
        await ctx.send(response)
