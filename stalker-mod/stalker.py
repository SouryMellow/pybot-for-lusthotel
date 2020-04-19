import os
import discord
import random
import time
import json

from Person import *

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.content.lower() == 'hola':
        sayHi(message)
    stalk(message)


@client.event
async def on_ready():
    readFile()
    pass


async def sayHi(message: discord.Message):
    saludo = ['hola', 'aloh', 'aloha', 'Hola', 'HOla', 'HOLa', 'HOLA', 'holA',
              'hoLA', 'hOLA', 'hello', 'hi', 'Hello', 'Hallo', 'marhabaan',
              'barev', 'geia', 'sannu', 'aloha', 'namaste', 'nyob zoo', 'saluton',
              'merhaba', 'salam', 'pryvit', 'Ola', 'Salut', 'hei', 'kaixo', 'tere',
              'zdravo', 'ahoj']
    await message.channel.send('**' + random.choice(saludo) + '**')


def stalk(message: discord.Message):
    addInformationUser(message)
    saveToFile()


def addInformationUser(message: discord.Message):
    for p in Person.persons:
        if p.id == message.author.id:
            t = time.strftime("%H:%M:%S")
            x = p.messages + 1
            p.setMessages(x)
            p.setMessage(f'{t}: {message.content}')
            del t
            del x
            return
    t = time.strftime("%H:%M:%S")
    p = Person(message.author.id, message.author.name,
               [f'{t}: {message.content}'], 1)
    Person.persons.append(p)
    del t
    del p


def readFile():
    with open('stalker.json', encoding="utf-8") as file:
        persons = json.load(file)
        for i in range(len(persons['id'])):
            a = Person(persons['id'][i],
                       persons['user'][i],
                       persons['message'][i],
                       persons['messages'][i])
            Person.persons.append(a)
            del a
        del persons
        file.close()
    print("Listo para la accion!")


def saveToFile():
    listPerson = Person.persons

    a = {'id': [i.id for i in listPerson],
         'user': [i.user for i in listPerson],
         'message': [i.message for i in listPerson],
         'messages': [i.messages for i in listPerson]}
    f = open('stalker.json', 'w', encoding="utf-8")
    f.write(str(a).replace("'", '"'))
    f.close()
    del a
    del f
    del listPerson


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)
