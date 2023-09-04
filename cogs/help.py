from typing import Any, List, Mapping, Optional
import discord
import os
from discord import SelectOption
from discord.ext import commands, tasks
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import Command, Group
from tokens import *
from discord.ui import View, Select


class MyHelp(commands.MinimalHelpCommand):
    def __init__(self):
        attributes = {
            
        'cooldown': commands.CooldownMapping.from_cooldown(1, 15.0, commands.BucketType.user)
        }
        super().__init__(command_attrs=attributes)
        
    #*error checks    
    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)
        
    
    
    #help command when a command is added   
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
    
    
    #help command when a cog name is inserted
    async def send_cog_help(self, cog):
        embed= discord.Embed(
            title=f"{cog.qualified_name} commands",
            color=discord.Color.blue()
        )
        
        cog_commands = cog.get_commands()
        
        Command_list = []
        for commands in cog_commands:
            holder = f"`{commands.name}`"
            if commands.description:
                holder += f"-{commands.description}"
            Command_list.append(holder)
        
            
        embed.add_field(name=f"commands for {cog.qualified_name}", value='\n'.join(Command_list))
        embed.set_footer(text="For more info for specific commands use !help (command)")#footer for command parameters
        
        channel = self.get_destination()
        await channel.send(embed=embed)
        
        
    #full help command (called if nothing else is added to the command)
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Command Group List")
        for cog, commands in mapping.items():
            visible_commands= [command for command in commands if not command.hidden]
            command_count = len(visible_commands)
            
            if command_count > 0:
                cog_name = getattr(cog, "qualified_name", "No Category")
                if cog_name == "No Category" or cog_name == "OyasuHelp":
                    pass
                else:
                    embed.add_field(name=cog_name , value=f"{command_count} commands\n `!help {cog_name}`", inline=False)
                
        
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
    #commands.HiddenAttribute()(OyasuHelp)
    await bot.add_cog(OyasuHelp(bot))