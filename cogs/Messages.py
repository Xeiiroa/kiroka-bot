import discord
from discord.ext import commands
from tokens import *

from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions

class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client
     
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Messages is ready.")
        
    #purge command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, count: int):
        await ctx.channel.purge(limit=count)
        await ctx.send(f"{count} message(s) deleted")
        
        
async def setup(client):
    await client.add_cog(Messages(client))