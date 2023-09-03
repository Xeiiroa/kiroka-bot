from typing import Any, List, Mapping, Optional
import discord
import os
from discord import SelectOption
from discord.ext import commands, tasks
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import Command, Group
from tokens import *
from discord.ui import View, Select
#create help passing
#create help command
#hiding owner commands or owner cog in general and cogs like help
#add cooldown to avoid spam

#on help command
#Show the categories and how many commands there are
#when a group or command is called return the infor for it
#check if command.hidden is true or false


class MyHelp(commands.MinimalHelpCommand):
    def __init__(self):
        attributes = {
            # Todo increase time to 1 in 15 seconds when
        'cooldown': commands.CooldownMapping.from_cooldown(2, 5.0, commands.BucketType.user)
        }
        super().__init__(command_attrs=attributes)
        
    #*error checks    
    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)
        
    #*bad argument check if they sent wrong name
        
    async def send_command_help(self, command):
            embed= discord.Embed(
                title=command.name,
                color=discord.Color.blue()
                )
            #check for parameters
            parameters= command.clean_params
            if parameters:
                parameter_names = list(parameters.keys())
                arguments = '\n'.join(parameter_names)
                embed.add_field(name="Arguments", value=arguments, inline=False)
            embed.add_field(name="Description", value=command.description)
            
            alias = command.aliases
            if alias:
                embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
            
            channel = self.get_destination()
            await channel.send(embed=embed)
    
    #TODO 
    #since i have one group per cog i can just call the other one for this
    #or just copy paste the code from one to another depending on if it looks differfent        
    async def send_cog_help(self, cog):
        embed= discord.Embed(
            title=f"{cog.qualified_name} commands",
            color=discord.Color.blue()
        )
        
        cog_commands = cog.get_commands()
        
        Command_list = []
        for commands in cog_commands:
            holder = f"`{commands.name}`-{commands.description}"
            Command_list.append(holder)
        
            
        embed.add_field(name=f"commands for {cog.qualified_name}", value='\n'.join(Command_list))
        embed.set_footer(text="For more info for specific commands use !help (command)")#footer for command parameters
        
        channel = self.get_destination()
        await channel.send(embed=embed)
        
        
        
    

    #TODO
    #This is the full help command, create a screen that Displays the names of each cog that isnt hidden and how many commands there are
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Command List")
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
        
        channel = self.get_destination()
        await channel.send(embed=embed)
        
#Help command
#todo
#create aliases for help commands, help, commands, 
class OyasuHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #attributes=
        help_command=MyHelp()
        help_command.cog=self
        bot.help_command=help_command
    
    
    
        
    
    
    
    
    
    
    
    

async def setup(bot):
    await bot.add_cog(OyasuHelp(bot))