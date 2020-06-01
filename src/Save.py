import discord

from discord.ext import commands
from Verified import *
from Warn import *
from Underage import *

bot = commands.Bot(command_prefix='!lh ')


class Save(commands.Cog):
    @bot.command(name='save', help='Comando para guardar la informacion a disco')
    @commands.has_any_role('Soporte', 'DevSour', 'Concierge del Hotel')
    async def save(self, ctx):
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
