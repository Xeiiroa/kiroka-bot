import discord
from discord.ext import commands
from tokens import *
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get



class Admin(commands.Cog):
    def __init__ (self, client):
        self.client = client
        
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin is ready.")
        
    #kick command
    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        await member.kick(reason=reason)
        await ctx.send(f"user {member} has been kicked.")
    
    #kick error check    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("you're too low in the hierarchy to do that lol.")
            
    
    
    
    #ban command        
    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        await member.ban(reason=reason)
        await ctx.send(f"user {member} has been banned.")
    
    #ban errorcheck    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("you're too low in the hierarchy to do that lol.")
      
      
    
    
    
    #unban command        
    @commands.command()
    @commands.guild_only()
    @has_permissions(administrator=True)
    async def unban(self, ctx, member: discord.Member, *, reason=None):
        
        banned_users = await ctx.guild.bans()
        print(banned_users)
        member_name, member_descriminator = member.split("#")
        print(member_name)
        
        for ban_entry in banned_users:
            user = ban_entry.user
            
        if (user.name, user.discriminaror )  == (member_name, member_descriminator):
            await ctx.guild.unban(user) 
            await ctx.send(f"Unbanned {user.mention}")
            return
        
    @unban.error
    async def unban_error(self, ctx, error):    
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You dont have permission to unban people")
            
    
    
    
    
    #addrole command
    @commands.command(pass_context = True)
    @commands.has_permissions(manage_roles = True)   
    async def addrole(self, ctx, user: discord.Member, *, role: discord.Role):
    
        if role in user.roles:
            await ctx.send(f"{user.mention} already has the role {role}")
        else:
            await user.add_roles(role)
            await ctx.send(f"{user.mention} now has the role {role}")
    
    #addrole errorcheck        
    @addrole.error
    async def role_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("you do not have permissions to assign that role.")        
    
    
    
    
        
    #remove roles from a user
    @commands.command(pass_context = True)
    @commands.has_permissions(manage_roles = True)   
    async def removerole(self, ctx, user: discord.Member, *, role: discord.Role):
    
        if role not in user.roles:
            await ctx.send(f"{user.mention} does not have the role {role}.")
        else:
            await user.remove_roles(role)
            await ctx.send(f"{user.mention} no longer has the role {role}.")
            
    @removerole.error
    async def role_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("you do not have permissions to assign that role.") 
        
    
        


async def setup(client):
    await client.add_cog(Admin(client))
    