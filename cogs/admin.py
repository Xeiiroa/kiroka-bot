import discord
from discord.ext import commands
from tokens import *
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get



class Admin(commands.Cog):
    def __init__ (self, client):
        self.client = client
        
    def has_mute_permission(ctx):
        member = ctx.author
        for role in member.roles:
            if role.permissions.mute_members:
                return True
        return False
    
    def has_deafen_permission(ctx):
        member = ctx.author
        for role in member.roles:
            if role.permissions.deafen_members:
                return True
        return False

        
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
        
    
    """has potential to be better"""    
    #text mute
    @commands.command()
    @commands.has_permissions(mute_members=True)
    async def txtmute(ctx, member: discord.Member):
        txtmuted_role = discord.utils.get(ctx.guild.roles, name='TextMuted')
        
        #checking if theres a textmuted rule and if there isnt making one
        if not txtmuted_role:
            txtmuted_role = await ctx.guild.create_role(name="TextMuted")
            
        #checking if the user has the textmuted role and sending an error message if they do    
        if txtmuted_role in member.roles:
            await ctx.send(f"{member.mention} is already text muted")
        else:
            for channel in ctx.guild.text_channels:
                member_permission = channel.permission_for(member)
                
                if not member_permission.send_messages:
                    continue
                
                member_permission.update(send_messages=False)
                
                #applying the permission change
                await channel.set_permissions(member, overwrite=member_permission)
        
            await ctx.send(f'{member.mention} has been text muted.')
        
    @txtmute.error
    async def txtmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("you dont have the permissions to mute someone in text")
                
            
    #text unmute command        
    @commands.command()
    @commands.has_permissions(mute_members=True)
    async def unmutetxt(ctx, member: discord.Member):
        txtmuted_role = discord.utils.get(ctx.guild.roles, name='TextMuted')
        
        if txtmuted_role in member.roles:
            for channel in ctx.guild.text_channels:
                
                member_permission = channel.permissions_for(member)
                
                if member_permission.send_messages:
                    continue
                
                member_permission.update(send_messages=True)
                
                await channel.set_permission(member, overwrite=member_permission)
                
            await ctx.send(f"{member.mention} is now able to send messages again")
            
        else:
            await ctx.send(f"{member.mention} isn't muted")
            
    #voice mute command  
    #jist checking if the user is in a voice and if so mute them
          
    @commands.command()
    @commands.check(has_mute_permission)
    async def mute(self, ctx, member: discord.Member):
        if member.voice:
            if member.voice.mute:
                await ctx.send("they're is already muted")
            else:
                await member.edit(mute=True)
                await ctx.send(f"{member.mention} has been voice muted.")
        else:
            await ctx.send(f'{member.mention} is not in a voice channel.')
            
    #unmute command
    #jist checking the user is mute and if they are unmuting them        
    @commands.command()
    @commands.check(has_mute_permission)
    async def unmute(self, ctx, member: discord.Member):
        if member.voice.mute:
            await member.edit(mute=False)
            await ctx.send(f"{member.mention} has been unmuted.")
        else:
            await ctx.send(f"{member.mention} isnt muted")
            
    @commands.command()
    @commands.check(has_deafen_permission)
    async def deafen(self,ctx, member: discord.Member):
        if member.voice:
            if member.voice.deaf:
                await ctx.send("Theyre already deafened")
            else: 
                await member.edit(deafen=True)
                await ctx.send(f"{member.mention} has been deafened.")
        else:
            await ctx.send(f"{member.mention} is not in a voice channel")
            
    @commands.command()
    @commands.check(has_deafen_permission)
    async def undeafen(self, ctx, member: discord.Member):
        if member.voice.deaf:
            await member.edit(deafen=False)
            await ctx.send(f"{member.mention} has been undeafened.") 
        else:
            await ctx.send(f"they arent deafened")   
        
    #purge command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, count: int):
        await ctx.channel.purge(limit=count)
        await ctx.send(f"{count} message(s) deleted")
            
                    
        
    

async def setup(client):
    await client.add_cog(Admin(client))
    