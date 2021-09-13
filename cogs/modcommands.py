import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import cogs._json
from random import randint
import re
import time


class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Mod Command Cog loaded\n======")
    
    # Deixa o bot offline (só pode ser usado pelo "dono" do bot)
    # Stops the bot from running (can only be used by the bot's owner)

    @commands.command(aliases=["disconnect", "close", "killgorilla"])
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(f"AWOOGA! AWOOGA! FAREWELL.")
        await self.bot.logout()
    
    # Chuta um usuário para fora do servidor (o usuário que utiliza este comando precisa de permissões de ban)
    # Kicks an user from the server (the user inputting this command needs the ban_members permission)

    @has_permissions(kick_members=True)
    @commands.command()
    async def exile(self, ctx, member):
        member_id = re.findall(r'^<@!(.+)>$', member)
        
        for member in ctx.guild.members:
            if [f'{member.id}'] == member_id:
                true_member = member
        await ctx.send(f"**{true_member.name}** has been exiled from the server. :skull:")
        await ctx.guild.kick(true_member)
    
    # Manda o usuário para a blacklist
    # Blacklists the user

    @has_permissions(kick_members=True)
    @commands.command()
    async def blacklist(self, ctx, user: discord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send("You cannot blacklist yourself.")
            return
            
        elif user.id not in self.bot.blacklisted_users:   
            self.bot.blacklisted_users.append(user.id)
            data = cogs._json.read_json("blacklist")
            data["blacklistedUsers"].append(user.id)
            cogs._json.write_json(data, "blacklist")

            await ctx.send(f"{user.mention} added to the blacklist.")
        else:
            await ctx.send("This person is already blacklisted.")

    @blacklist.error
    async def blacklist_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Member not found! :x:")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("Use the following format so the command may work: **.g blacklist [user mention]**. :gorilla:")
        else:
            await ctx.send("An error has occurred! :warning:")
            raise error
            


    # Retira o usuário da blacklist
    # Unblacklists the user
    
    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def pardon(self, ctx, user: discord.Member):
        self.bot.blacklisted_users.remove(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        cogs._json.write_json(data, "blacklist")

        await ctx.send(f"{user.mention} can now use GorillaBot again. :white_check_mark:")

    # Manda uma mensagem de erro caso o usuário tente tirar uma pessoa que não está na blacklist
    # Sends an error message if the user tries to unblacklist someone that isn't blacklisted
    
    @pardon.error
    async def pardon_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("This person is not blacklisted. :x:")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("Use the following format so the command may work: **.g pardon [user mention]**. :gorilla:")
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("Member not found. :x:")
        else:
            await ctx.send("An error has occurred! :warning:")
            raise error

def setup(bot):
    bot.add_cog(ModCommands(bot))