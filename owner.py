#* Owner only commands
import discord
from discord import app_commands
from discord.ext import commands, Greedy, Context
from tokens import *
from typing import Any, Literal, Optional, Type


import os
import asyncio

from discord.ext.commands.bot import PrefixType, _default
from discord.ext.commands.help import HelpCommand

#import tokens
from tokens import *


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
    ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.client.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.client.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.client.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.client.tree.clear_commands(guild=ctx.guild)
                await ctx.client.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.client.tree.sync()
            
            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
        

async def setup(bot):
    await bot.add_cog(Owner(bot))