import os
import discord
import random

import csv
import operator
import json
import pandas as pd

from Verified import *
from Warn import *

from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
bot = commands.Bot(command_prefix='!lh ')


@bot.command(name='verify', help='Verifica a un usuario. (SOLO MODERADOR). e:[!lh verify @{user} {sexo} {pais}]')
@commands.has_role('Moderador')
async def verify(ctx, user: discord.User, gender, country):
    for v in Verified.verifieds:
        if v.id == user.id:
            await ctx.send(f'```{user.name} ya esta verificado.```')
            return

    p = Verified(user.id, user.name, gender, country)
    Verified.verifieds.append(p)

    await ctx.send(f'```{p.user} verificado correctamente.```')


@bot.command(name='warn', help='Pon una advertencia a una persona. (SOLO MODERADOR). e:[!lh warn @{user} *{message (No necesario)}]')
@commands.has_role('Moderador')
async def warn(ctx, user: discord.User, message="mal comportamiento"):
    for w in Warn.peopleWarned:
        if w.id == user.id:
            w.setWarns(w.warns + 1)
            await ctx.send(f'Has recibido {w.warns} advertencias {user.mention} por {message}.')
            return

    w = Warn(user.id, user.name, 1, message)
    Warn.peopleWarned.append(w)
    await ctx.send(f'Has recibido una advertencia {user.mention} por {message}.')


@bot.command(name='request', help='Despliega la informacion de una o varias personas. e:[!lh request @{*user,..., users}]')
@commands.has_role('Moderador')
async def request(ctx, *users: discord.User):
    for user in users:
        await ctx.send(f'```{user.profile}```')


@bot.command(name='id', help='Obten la ID de una o varias personas. e:[!lh id @{*user,..., users}]')
@commands.has_role('Moderador')
async def getid(ctx, *users: discord.User):
    for user in users:
        await ctx.send(f'```ID: {user.id}```')


@bot.command(name='listv', help='Despliega toda la informacion guardada de las personas verificadas. (SOLO MODERADOR). e:[!lh listv]')
@commands.has_role('Moderador')
async def listVerify(ctx):
    for v in Verified.verifieds:
        await ctx.send(f'```ID: {v.id}\n' +
                       f'User: {v.user}\n' +
                       f'Genero: {v.gender}\n' +
                       f'Pais: {v.country}\n```')


@bot.command(name='warns', help='Ver todas las advertencias de una o varias personas. e:[!lh warns @{*user,..., users}]')
@commands.has_role('Moderador')
async def warns(ctx, *users: discord.User):
    for u in users:
        for w in Warn.peopleWarned:
            if u.id == w.id:
                await ctx.send(f'```Usuario: {u.name}\n' +
                               f'Avisos: {w.warns}\n' +
                               f'Ultimo motivo: {w.message}```')
            else:
                pass


@bot.command(name='listw', help='Ver todas las advertencias de todas las personas. e:[!lh listw]')
@commands.has_role('Moderador')
async def listWarns(ctx):
    for w in Warn.peopleWarned:
        await ctx.send(f'```Usuario: {w.user}\n' +
                       f'Avisos: {w.warns}\n' +
                       f'Ultimo motivo: {w.message}```')


@bot.command(name='underage')
@commands.has_role('Moderador')
async def underage(ctx, user, message):
    pass


@bot.command(name='listu')
@commands.has_role('Moderador')
async def listUnderages(ctx, *users):
    pass


@bot.command(name='save', help='Comando para guardar la informacion a disco. (SOLO DESARROLLADOR).')
@commands.has_role('Moderador')
async def save(ctx):
    listVerifieds = Verified.verifieds
    listWarns = Warn.peopleWarned

    data = {'id': [i.id for i in listVerifieds],
            'usuario': [i.user for i in listVerifieds],
            'genero': [i.gender for i in listVerifieds],
            'country': [i.country for i in listVerifieds]}
    f = open('files/people_verified.json', 'w')
    f.write(str(data).replace("'", '"'))
    f.close()

    data = {'id': [i.id for i in listWarns],
            'usuario': [i.user for i in listWarns],
            'avisos': [i.warns for i in listWarns],
            'ultima_razon': [i.message for i in listWarns]}
    f = open('files/people_warned.json', 'w')
    f.write(str(data).replace("'", '"'))
    f.close()

    #df = pd.DataFrame(data, columns=['id', 'usuario', 'genero', 'country'])
    # df.to_csv('verified.csv')
    await ctx.send("Se ha guardado la informacion correctamente.")


@bot.command(name='sum', help='Suma una serie de numeros.')
async def sum(ctx, *nums: float):
    z = 0
    for n in nums:
        z = z + n
    await ctx.send(z)


@bot.command(name='res', help='Resta una serie de numeros.')
async def res(ctx, *nums: float):
    z = 0
    for n in nums:
        z = z - n
    await ctx.send(z)


@bot.command(name='mul', help='Multiplica una serie de numeros.')
async def mul(ctx, *nums: float):
    if len(nums) > 100:
        await ctx.send("No creo que necesites tantos numeros...")
    z = 1
    for n in nums:
        z = z * n
    await ctx.send(z)


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Bienvenido {member.name}, espero este servidor sea para ti!'
    )


@bot.event
async def on_ready():
    with open('files/people_verified.json') as file:
        verifieds = json.load(file)

        for i in range(len(verifieds['id'])):
            v = Verified(verifieds['id'][i],
                         verifieds['usuario'][i],
                         verifieds['genero'][i],
                         verifieds['country'][i])
            Verified.verifieds.append(v)
        file.close()

    with open('files/people_warned.json') as file:
        verifieds = json.load(file)

        for i in range(len(verifieds['id'])):
            v = Verified(verifieds['id'][i],
                         verifieds['usuario'][i],
                         verifieds['avisos'][i],
                         verifieds['ultima_razon'][i])
            Verified.verifieds.append(v)
        file.close()

    print(f'{bot.user.name} estoy en funcionamiento.')


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
