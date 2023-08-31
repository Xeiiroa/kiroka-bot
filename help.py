import discord
from discord.ext import commands, tasks
from tokens import *
from discord.ui import View, Select


class HelpSelect(Select):
    def __init__(self, client: commands.Bot):
        super().__init__(
            placeholder="Select a category",
            options=[
                discord.SelectOption(
                    label=cog_name, description=cog.__doc__
                ) for cog_name, cog in client.cogs.items() if cog.__cog_commands and cog_name not in ['Jishaku']
            ]
        )
        
        self.client=client
        
    async def callback(self, interaction: discord.Interaction) -> None:
        cog = self.client.get_cog(self.values[0])
        assert cog
        
        commands_mixer = []
        for i in cog.walk_commands():
            commands_mixer.append(i)
            
        for i in cog.walk_app_commands():
            commands_mixer.append(i)
            
        embed = discord.Embed(
            title=f"{cog.__cog_name__} Commands",
            desctiption='\n'.join(
                f"**{command.name}**: '{command.description}'"
                for command in commands_mixer
            )
        ) 
        
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


class Help(commands.Cog):
    def __init__(self, client):
        self.client= client

    @commands.hybrid_command(name="help", description="Shows list of commands")
    async def help(self, ctx: commands.Context):
        #default window
        embed=discord.Embed(
            title="Help command",
            description="This is the help command"
        )
        
        view = View().add_item(HelpSelect(self.client))
        await ctx.send(embed=embed, view=view)
        
    @commands.hybrid_command(name='test', description='This is the test command')
    async def test(self, ctx: commands.Context):
        await ctx.send(10)
        
async def setup(client):
    await client.add_cog(Help(client))