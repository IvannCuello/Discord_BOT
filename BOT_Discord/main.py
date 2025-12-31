import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

#Importamos el Token con los permisos del BOT
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

#Llamado a otorgar los permisos
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#Variable a BOT
bot = commands.Bot(command_prefix='!', intents=intents)

secret_role = "Rol"

 #¿Que quiero que haga el BOT?
#atraves de la función "bot.event" podemos agregar 
#distintas funciones

@bot.event  #Activamos el BOT en el servidor (aparecera en línea en nuestro servidor)
async def on_ready():
    print(f"Estoy en línea, {bot.user.name}")  


@bot.event  #"Event" para generar un mensaje de Bienvenido
async def on_member_join(member):
    await member.send(f"Bienvenido {member.name}")

@bot.event  #"Event" para responder y generar mensajes
async def on_message(message):
    if message.author == bot.user:
        return

    #if "partido" in message.content.lower():
      #  await message.channel.send(f"{message.author.mention} - si hay!")

    await bot.process_commands(message) #Con esta función el BOT siempre responderá

#Agregar comandos
#Comando para responder mensaje "!"
@bot.command()
async def hello (ctx):
    await ctx.send(f"hello {ctx.author.mention}!")

''' Enviar Mensajes '''
@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"Has dicho: {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("Esta es la réplica de tu mensaje") 

'''Comando para asignar y sacar roles'''
@bot.command(name="assign")
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} fue asignado a {secret_role}")
    else:
        await ctx.send("El rol no existe")


@bot.command(name="remove")
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} fue sacado de {secret_role}")
    else:
        await ctx.send("El rol no existe")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)