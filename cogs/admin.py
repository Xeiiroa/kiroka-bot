import discord
from discord.ext import commands
from tokens import *
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get

#this class contains all basic default functions
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    """
    Kick and ban commands

    checks if the user sending the message has the ability to kick people

    passes in the user thats being kicked

    giving a reason as to why the user is being kicked

    as well as error checking for if the user in question cant kick others
    """
    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason = None):
        await member.kick(reason=reason)
        await ctx.send(f"User {member} has been kicked")
        
        
    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Youre to low in the hierarchy to do that lol. step up" + "https://wompampsupport.azureedge.net/fetchimage?siteId=7575&v=2&jpgQuality=100&width=700&url=https%3A%2F%2Fi.ytimg.com%2Fvi%2Fl3HMALfodb8%2Fhqdefault.jpg")
            

    @commands.command
    @has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason = None):
        await member.ban(reason=reason)
        await ctx.send(f"Damn, you really wont be missed {member}")
        
        
    @kick.error
    async def ban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("No" + "https://media.tenor.com/vUs9lHbfbWIAAAAC/ha-ha-simpsons.gif")
         
    @commands.command()
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
    
    
    #didnt finish    
    @commands.command()
    @has_permissions(administrator=True)
    async def banlist(self, ctx):
        ...
    
    
    #give user roles
    @commands.command(pass_context = True)
    @commands.has_permissions(manage_roles = True)   
    async def addrole(self, ctx, user: discord.Member, *, role: discord.Role):
    
        if role in user.roles:
            await ctx.send(f"{user.mention} already has the role {role}")
        else:
            await user.add_roles(role)
            await ctx.send(f"{user.mention} now has the role {role}")
            
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
        
                
    
def setup(bot):
    bot.add_cog(Admin(bot))