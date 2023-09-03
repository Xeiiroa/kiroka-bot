import discord
from discord.ext import commands
from tokens import *
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get



class Admin(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot
        
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin is ready.")
    
    @commands.is_owner()    
    @commands.command()
    async def sssync(self,ctx):
        await self.tree.sync()
        
    
    #error check for all commands that require permissions
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f"Error type: {type(error).__name__}")
        print(f"Command name: {ctx.command}")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("you don't have the proper permissions to use this command")
        
    #kick command
    @commands.command(name="kick", description="Remove a user from the server")
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        await member.kick(reason=reason)
        await ctx.send(f"user {member} has been kicked.")
    
    
    #ban command        
    @commands.command(name="ban", description="Remove a user from the server")
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        await member.ban(reason=reason)
        await ctx.send(f"user {member} has been banned.")
        
    
    #addrole command
    @commands.command(name="addrole", description="Give the mentioned user a role", pass_context = True)
    @commands.has_permissions(manage_roles = True)   
    async def addrole(self, ctx, user: discord.Member, *, role: discord.Role):
    
        if role in user.roles:
            await ctx.send(f"{user.mention} already has the role {role}")
        else:
            await user.add_roles(role)
            await ctx.send(f"{user.mention} now has the role {role}")
    
    
    #remove role command
    @commands.command(name="removerole", description="Remove a role from the mentioned user", pass_context = True)
    @commands.has_permissions(manage_roles = True)   
    async def removerole(self, ctx, user: discord.Member, *, role: discord.Role):
    
        if role not in user.roles:
            await ctx.send(f"{user.mention} does not have the role {role}.")
        else:
            await user.remove_roles(role)
            await ctx.send(f"{user.mention} no longer has the role {role}.")
            
    
    #todo 
    #! Create aliases for mutetxt and unmute text  
    #text mute
    @commands.command(name="mutetxt", description="Take a users ability to send messages away")
    async def mutetxt(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.mute_members:
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(member, send_messages=False)
            await ctx.send(f"{member.mention} has been text muted")
        else:
            await ctx.send("you don't have the proper permissions to use this command")
             
            
    #text unmute command        
    @commands.command(name="unmutetxt", description="Give the mentioned user ability to send messages")
    async def unmutetxt(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.mute_members:
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(member, send_messages=True)
            await ctx.send(f"{member.mention} has been unmuted")
        else:
            await ctx.send("you don't have the proper permissions to use this command")
            
        
      
            
    #voice mute command         
    @commands.command(name="mute", description="Mutes mentioned user if in a voice channel")
    async def mute(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.mute_members:
            if member.voice:
                if member.voice.mute:
                    await ctx.send("they're is already muted")
                else:
                    await member.edit(mute=True)
                    await ctx.send(f"{member.mention} has been voice muted.")
            else:
                await ctx.send(f'{member.mention} is not in a voice channel.')
        else:
            await ctx.send("you don't have the proper permissions to use this command")
                    
            
    #unmute command
    #jist checking the user is mute and if they are unmuting them        
    @commands.command(name="unmute", description="Unmutes mentioned user")
    async def unmute(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.mute_members:
            if member.voice.mute:
                await member.edit(mute=False)
                await ctx.send(f"{member.mention} has been unmuted.")
            else:
                await ctx.send(f"{member.mention} isnt muted")
        else:
            await ctx.send("you don't have the proper permissions to use this command")
            
    #deafen                    
    @commands.command(name="deafen", description="takes mentioned users ability to hear if in a voice channel")
    async def deafen(self,ctx, member: discord.Member):
        if ctx.author.guild_permissions.deafen_members:
            if member.voice:
                if member.voice.deaf:
                    await ctx.send(f"{member.mention} is already deafened")
                else: 
                    await member.edit(deafen=True)
                    await ctx.send(f"{member.mention} has been deafened.")
            else:
                await ctx.send(f"{member.mention} is not in a voice channel")
        else:
            await ctx.send("you don't have the proper permissions to use this command")    
      
    @commands.command(name="undeafen", description="Undeafens mentioned user")
    async def undeafen(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.deafen_members:
            if member.voice.deaf:
                await member.edit(deafen=False)
                await ctx.send(f"{member.mention} has been undeafened.") 
            else:
                await ctx.send(f"they arent deafened")
        else:
            await ctx.send("you don't have the proper permissions to use this command")
              
        
    #purge command
    @commands.hybrid_command(name="purge", description="deletes messages in voice channel when given a number")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, count: int):
        await ctx.channel.purge(limit=count)
        await ctx.send(f"{count} message(s) deleted")
        
    #rename command    
    @commands.command(name="rename", description="Changes mentioned users nickname")
    @commands.has_permissions(manage_nicknames=True)
    async def rename(self, ctx, member: discord.Member, *, new_name: str):
        await member.edit(nick=new_name)
        await ctx.send(f"{member.mention}'s nickname has been updated")
        
    

async def setup(bot):
    await bot.add_cog(Admin(bot))
    