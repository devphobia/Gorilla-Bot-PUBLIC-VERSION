# imports

import discord
from discord.ext import commands
import json
from pathlib import Path
import logging
import os

# Definindo o caminho para a pasta principal
# Setting current working directory path

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n=====")

# Carregando TOKEN e configuração do bot.
# Loading bot's token and setting up bot's configuration

intents = discord.Intents.default()
intents.members = True
secret_file = json.load(open(cwd+"/bot_config/secrets.json"))
bot = commands.Bot(intents=intents, command_prefix=".g ", case_insensitive=True)
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

# Criando variável para lista negra de usuários e informando a versão do bot
# Creating a variable for the blacklisted users and setting up bot's version

bot.blacklisted_users = []
bot.cwd = cwd

bot.version = "0.6.0"

# Evento de inicialização que confirma se o bot foi iniciado e está online
# Event that triggers when the code is started and the bot goes online

@bot.event
async def on_ready():
    print(f"=====\nGorilogged as: {bot.user.name} : {bot.user.id}\n")

# Evento que é ativado a cada mensagem que é mandada por algum usuário
# Event that triggers ON MESSAGE.

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    
    # Checa se o usuário está na lista negra, e caso estiver, impede-o de utilizar qualquer comando do bot
    # Verifies if the user inputting the message is blacklisted and makes so he can't use any commands from this bot

    if message.author.id in bot.blacklisted_users:
        return
    
    await bot.process_commands(message)

# Carrega as cogs da pasta cogs caso o arquivo bot seja o arquivo principal
# If this is the main file (not imported) it will load all the cogs needed for the bot to work.

if __name__ == "__main__":
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.run(bot.config_token)

