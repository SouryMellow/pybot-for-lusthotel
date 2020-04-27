import os
import discord
import json

from discord.ext import commands
from dotenv import load_dotenv

from Admin import *
from Custom import *
from Extra import *
from Save import *

from Verified import *
from Warn import *
from Underage import *

load_dotenv()
bot = commands.Bot(command_prefix='!lh ')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Bienvenido {member.name}, espero este servidor sea para ti!')
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


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(f'hola xd')

if __name__ == "__main__":
    bot.add_cog(Admin(bot))
    bot.add_cog(Custom(bot))
    bot.add_cog(Extra(bot))
    bot.add_cog(Save(bot))

    print("Conectando al servidor...")
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
