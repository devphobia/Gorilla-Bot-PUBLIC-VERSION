# imports

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands.errors import CommandInvokeError
import cogs._json
from random import randint
import re
from fun_classes.shuffler import Shuffler
import time

# Cog composta inteiramente por comandos para diversão e lazer dos membros (dados, sorteio, coisas bobas...)
# This cog only contains commands made to entertain (dice, shuffling, other stuff...)

class FunCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Evento de inicialização que confirma se a cog foi carregada
    # Event that triggers if the cog has been sucessfully loaded
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun Command Cog loaded\n======")

    # Comando que mostra o seu nível de gorilagem
    # Command that displays your GORILLA POWER

    @commands.command(name= "gorillapower", 
    description = "Displays your level of GORILLA POWER.")
    async def gorillapower(self, ctx):
        await ctx.send(gorilla_power_calculator())

    # Comando que rola dados
    # Command that rolls dice
    
    @commands.command(name="roll", description="Rolls die.")
    async def roll(self, ctx, throws, dice):
        dice_num = re.findall(r'd(.+)', dice)
        if throws.isnumeric() == True:
            rolls = []
            for i in range(int(throws)):
                rolls.append(randint(1, int(dice_num[0])))
            await ctx.send(f":game_die: {ctx.message.author.mention} rolled {throws} {dice}: {rolls} = **{sum(rolls)}**")

    # Commandos e subcommandos de sorteio
    # Commands and subcommands for drawing lots (shuffling)
    

    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error, IndexError):
                await ctx.send("The gorilla can't roll that much.")
        else:
            await ctx.send("Use the following format so the command may work: **.g roll [number of rolls] d[faces of the die]**. :gorilla:")

    @commands.group()
    async def shuffle(self, ctx):
        global shuffler
        if ctx.invoked_subcommand is None:
            await ctx.send("Add something to the shuffle box by typing **.g shuffle add [name]** and shuffle what's in the box using **.g shuffle time**.")

    @shuffle.command()
    async def add(self, ctx):
        print(ctx.message.content)
        element = ctx.message.content.replace(".g shuffle add ", "")
        elements = element.split(", ")

        for i in elements:
            shuffler.add_element(i)

        print(shuffler.elements)

        await ctx.send(f"{element} added to the shuffle box.")

    @shuffle.command()
    async def time(self, ctx):
        if len(shuffler.elements) != 0:
            await ctx.send("DRAWING LOTS")
            for i in range(3):
                await ctx.send("*SHLACK SHLACK SHLACK*")
                time.sleep(1)
            
            await ctx.send(f"**Winner:** {shuffler.random_element()} :star2:")
            shuffler.clear()
        else:
            await ctx.send("The shuffle box is empty.")

# Função que calcula propriamente o nível de gorilagem e é utilizada no comando acima
# Function that actually calculates your GORILLA POWER

def gorilla_power_calculator():
    percentage = randint(0, 100)

    answer = f"Your GORILLA POWER is at {percentage}%!"

    answers = [
        " That's pretty weak, not gonna lie...",
        " You're a little ape-like now, but just a little.",
        " I'm starting to feel the chimp inside you! :monkey:",
        " You're at orangutan levels of GORILLA POWER! :orangutan:",
        " You've reached GORILLA levels of GORILLA POWER! :gorilla:",
        " You're now at maximum GORILLA POWER output! You've gone APE MODE! :gorilla: :orangutan: :monkey: "
    ]
    
    if percentage == 0:
        answer += answers[0]
    elif percentage <= 25:
        answer += answers[1]
    elif percentage <= 50:
        answer += answers[2]
    elif percentage <= 75:
        answer += answers[3]
    elif percentage != 100:
        answer += answers[4]
    else:
        answer += answers[5]

    return answer


# Cog setup

def setup(bot):
    bot.add_cog(FunCommands(bot))

# Criação de uma variável para o sorteador

shuffler = Shuffler()