import os
import discord
import random
import json

from Verified import *
from Warn import *
from Underage import *

from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
bot = commands.Bot(command_prefix='!lh ')

#
# admin functions
#
@bot.command(name='kick', help='Expulsa a uno o mas usuarios del servidor')
@commands.has_any_role('Moderador', 'Soporte')
async def ban(ctx, *users: discord.User):
    for u in users:
        await ctx.guild.kick(u)


@bot.command(name='ban', help='Banea a uno o mas usuarios del servidor')
@commands.has_any_role('Moderador', 'Soporte')
async def ban(ctx, *users: discord.User):
    for u in users:
        await ctx.guild.ban(u)


@bot.command(name='unban', help='Desbanea a uno o mas usuarios del servidor')
@commands.has_any_role('Moderador', 'Soporte')
async def ban(ctx, *users: discord.User):
    for u in users:
        await ctx.guild.unban(u)


@bot.command(name='roleid', help='Obten ID y nombre de un rol en un server.')
async def rolid(ctx, role: discord.Role):
    await ctx.send(f'id: {role.id}, name: {role.name}')


#
# custom functions
#
@bot.command(name='jail', help='Encarcela a un usuario.')
@commands.has_any_role('Moderador', 'Soporte')
async def jail(ctx, *users: discord.Member):
    for u in users:
        newRoles = u.roles
        rol = ctx.guild.get_role(701492794618937434)
        for r in newRoles:
            if r.id == rol.id:
                newRoles.remove(ctx.guild.get_role(701492794618937434))
                break

        await u.edit(roles=newRoles)
        await u.add_roles(ctx.guild.get_role(701337981751132172))
        await ctx.send(f'{u.mention} encarcelado.')


@bot.command(name='verify', help='Verifica a un usuario. (SOLO VERIFICADOR).')
@commands.has_any_role('Verificador')
async def verify(ctx, user: discord.User, gender, country):
    for v in Verified.verifieds:
        if v.id == user.id:
            await ctx.send(f'```{user.name} ya esta verificado.```')
            return

    p = Verified(user.id, user.name, gender, country)
    Verified.verifieds.append(p)

    await ctx.send(f'```{p.user} verificado correctamente.```')


@bot.command(name='warn', help='Pon una advertencia a una persona. (SOLO MODERADOR).')
@commands.has_any_role('Moderador', 'Soporte')
async def warn(ctx, user: discord.User, message="mal comportamiento"):
    for w in Warn.peopleWarned:
        if w.id == user.id:
            x = w.warns + 1
            w.setWarn(x)
            await ctx.send(f'Has recibido {w.warns} advertencias {user.mention} por {message}.')
            return

    w = Warn(user.id, user.name, 1, message)
    Warn.peopleWarned.append(w)
    await ctx.send(f'Has recibido una advertencia {user.mention} por {message}.')


@bot.command(name='request', help='Despliega la informacion de una o varias personas.')
@commands.has_any_role('Moderador', 'Soporte')
async def request(ctx, *users: discord.Member):
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


@bot.command(name='id', help='Obten la ID de una o varias personas.')
@commands.has_any_role('Moderador', 'Soporte')
async def getid(ctx, *users: discord.User):
    for user in users:
        await ctx.send(f'```ID: {user.id}```')


@bot.command(name='listv', help='Despliega toda la informacion guardada de las personas verificadas. (SOLO MODERADOR).')
@commands.has_any_role('Moderador', 'Soporte')
async def listVerify(ctx):
    for v in Verified.verifieds:
        await ctx.send(f'```ID: {v.id}\n' +
                       f'User: {v.user}\n' +
                       f'Genero: {v.gender}\n' +
                       f'Pais: {v.country}\n```')


@bot.command(name='warns', help='Ver todas las advertencias de una o varias personas.')
@commands.has_any_role('Moderador', 'Soporte')
async def warns(ctx, *users: discord.User):
    for u in users:
        for w in Warn.peopleWarned:
            if u.id == w.id:
                await ctx.send(f'```Usuario: {u.name}\n' +
                               f'Avisos: {w.warns}\n' +
                               f'Ultimo motivo: {w.message}```')
            else:
                pass


@bot.command(name='listw', help='Ver todas las advertencias de todas las personas.')
@commands.has_any_role('Moderador', 'Soporte')
async def listWarns(ctx):
    for w in Warn.peopleWarned:
        await ctx.send(f'```Usuario: {w.user}\n' +
                       f'Avisos: {w.warns}\n' +
                       f'Ultimo motivo: {w.message}```')


@bot.command(name='underage', help='Agrega a un usuario a la lista de menores de edad.')
@commands.has_any_role('Moderador', 'Soporte')
async def underage(ctx, user: discord.User, evidence="Menor de edad."):
    for u in Underage.underages:
        if u.id == user.id:
            await ctx.send("Ya esta en la lista de menores de edad.")
            return

    u = Underage(user.id, user.name, evidence)
    Underage.underages.append(u)
    await ctx.send(f'Ha sido agregado {user.mention} a la lista de menores de edad.')


@bot.command(name='listu', help='Muestra la lista de todos los menores de edad registrados.')
@commands.has_any_role('Moderador', 'Soporte')
async def listUnderages(ctx):
    for u in Underage.underages:
        await ctx.send('```' +
                       f'ID: {u.id}\n' +
                       f'Usuario: {u.user}\n' +
                       f'Evidencia: {u.evidence}\n' +
                       '```')


#
# special custom
#
@bot.command(name='habla')
async def none(ctx, *msg):
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


@bot.command(name='spank')
async def spank(ctx):
    await ctx.send(SPANK_GIF)


@bot.command(name='sour')
async def sour(ctx):
    await ctx.send(SOUR)


@bot.command(name='moch')
async def sour(ctx):
    await ctx.send('Te odio')


@bot.command(name='buitre')
async def buitre(ctx):
    await ctx.send("Buitre = Persona que solo busca acosar a alguien y apenas interactua.")


@bot.command(name='md')
async def md(ctx):
    await ctx.send('MD = Mensaje Directo.')


@bot.command(name='dm')
async def md(ctx):
    await ctx.send('DM = Direct Message.')


@bot.command(name='info')
async def info(ctx):
    await ctx.send('Want to help me? : https://github.com/SouryMellow/pybot-for-lusthotel')

#
# save
#
@bot.command(name='save', help='Comando para guardar la informacion a disco. (SOLO DESARROLLADOR).')
@commands.has_any_role('Soporte', 'DevSour')
async def save(ctx):
    listVerifieds = Verified.verifieds
    listWarns = Warn.peopleWarned
    listUnderages = Underage.underages

    a = {'id': [i.id for i in listVerifieds],
         'usuario': [i.user for i in listVerifieds],
         'genero': [i.gender for i in listVerifieds],
         'country': [i.country for i in listVerifieds]}
    f = open('files/people_verified.json', 'w')
    f.write(str(a).replace("'", '"'))
    f.close()

    del a
    del listVerifieds

    b = {'id': [i.id for i in listWarns],
         'usuario': [i.user for i in listWarns],
         'avisos': [i.warns for i in listWarns],
         'ultima_razon': [i.message for i in listWarns]}
    f = open('files/people_warned.json', 'w')
    f.write(str(b).replace("'", '"'))
    f.close()

    del b
    del listWarns

    c = {'id': [i.id for i in listUnderages],
         'usuario': [i.user for i in listUnderages],
         'evidencia': [i.evidence for i in listUnderages]}
    f = open('files/people_underage.json', 'w')
    f.write(str(c).replace("'", '"'))
    f.close()

    del c
    del listUnderages
    await ctx.send("Se ha guardado la informacion correctamente.")

#
# extra functions
#
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

#
# discord functions
#
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Bienvenido {member.name}, espero este servidor sea para ti!'
    )
    print("New member!")


@bot.event
async def on_ready():
    print("Leyendo archivos")
    with open('files/people_verified.json') as file:
        verifieds = json.load(file)
        print("Leyendo archivo people_verified.json")
        for i in range(len(verifieds['id'])):
            a = Verified(verifieds['id'][i],
                         verifieds['usuario'][i],
                         verifieds['genero'][i],
                         verifieds['country'][i])
            Verified.verifieds.append(a)
        file.close()
    print("Terminado...")

    with open('files/people_warned.json') as file:
        warned = json.load(file)
        print("Leyendo archivo people_warned.json")
        for i in range(len(warned['id'])):
            b = Warn(warned['id'][i],
                     warned['usuario'][i],
                     warned['avisos'][i],
                     warned['ultima_razon'][i])
            Warn.peopleWarned.append(b)
        file.close()
    print("Terminado...")

    with open('files/people_underage.json') as file:
        underage = json.load(file)
        print("Leyendo archivo people_underage.json")
        for i in range(len(underage['id'])):
            c = Underage(underage['id'][i],
                         underage['usuario'][i],
                         underage['evidencia'][i])
            Underage.underages.append(c)
        file.close()
    print("Terminado...")

    print(f'{bot.user.name} estoy en funcionamiento.')


@bot.event
async def on_error(event, *args, **kwargs):
    with open('files/err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    SOUR = os.getenv('SOUR')
    SPANK_GIF = os.getenv('SPANK_GIF')
    print("Conectando al servidor...")
    bot.run(TOKEN)
