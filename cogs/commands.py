# imports

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import platform
import datetime
import cogs._json
import re

# Esta cog contém comandos utilitários e voltados aos moderadores do servidor
# This cog mainly contains utility commands and commands that are to be used by the server moderators/administrators

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Evento de inicialização que confirma se a cog foi carregada
    # Event that triggers if the cog has been sucessfully loaded

    @commands.Cog.listener()
    async def on_ready(self):
        print("Command Cog loaded\n======")
    
    # Commando que printa todos os membros do servidor para se certificar que o bot possui visibilidade deles
    # Command that prints all guild users so that it is assured that the bot has access to the guilds information

    @commands.command()
    async def members(self, ctx):
        for member in ctx.guild.members:
            print(member.id)

    # Comando que envia algumas informações úteis do bot como: criador, colaborador, versão, etc
    # Command that sends some useful information from this bot

    @commands.command()
    async def stats(self, ctx):
        server_count = len(self.bot.guilds)
        member_count = len(set(self.bot.get_all_members()))

        embed = discord.Embed(title=f"{self.bot.user.name} Stats :gorilla:", description="-"*20, colour=discord.Colour(0x546e7a), timestamp=ctx.message.created_at)


        embed.add_field(name="Gorilla Version:", value=self.bot.version)
        embed.add_field(name="Servers:", value=server_count)
        embed.add_field(name="Users:", value=member_count)
        embed.add_field(name="Creator:", value="<@!726289058916990996>")
        embed.add_field(name="Collaborator:", value="<@!153367952463364096>", inline=True)

        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)
    
    
    # Repete o que o usuário fala
    # Repeats what the user says

    @commands.command()
    async def echo(self, ctx, *, message=None):
        message = message or "Use the following format so the command may work: **.g echo [message that you want the gorilla to say]**. :gorilla:"
        await ctx.send(message)

# Cog setup

def setup(bot):
    bot.add_cog(Commands(bot))