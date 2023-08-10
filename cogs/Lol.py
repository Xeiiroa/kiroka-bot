import discord
from discord.ext import commands
from tokens import *

import requests
import json

class Lol(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        
        
    @commands.command
    async def leagueprofile(self, ctx, summonername: str, region: str):
        regions = ["BR1","EUN1","EUW1","JP1","KR","LA1","LA2","NA1","OC1","PH2","RU","SG2","TH2","TR1","TW2","VN2"]
        
        # getting data for summoner name, profile icon id, level, and account idea for further inspection
        summonerinfolink = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonername.replace(' ','%20')}?api_key={RIOT_KEY}")
        player_info= summonerinfolink.json()
        player_pfp = player_info["profileIconId"]
        player_level = player_info["summonerLevel"]
        summoneriD = player_info["id"]
        
        
        #getting data for summoners ranked stats
        ranked_solo = {}
        ranked_flex = {}
        ranked_flex_message = "unranked"
        ranked_solo_message = "unranked"
        summonerrankinfo = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoneriD}?api_key={RIOT_KEY}")
        rank_info = summonerrankinfo.json()
        for stats in summonerrankinfo.json():
            if "RANKED_SOLO_5x5" in stats.values():
                ranked_solo["ranknum"] = stats["rank"]
                ranked_solo["division"] = stats["tier"]
                ranked_solo["lp"] = stats["leaguePoints"]
                ranked_solo["wins"] = stats["wins"]
                ranked_solo["losses"] = stats["losses"]

                games_ranked_solo = stats["wins"] + stats["losses"]
                ranked_solo["winrate"] = games_ranked_solo / stats["wins"] * 100
                
                ranked_solo_message = f"{ranked_solo['division']} {ranked_solo['ranknum']} {ranked_solo['lp']} LP \n \
                    {ranked_solo['wins']}W {ranked_solo['losses']}L {ranked_solo['winrate']} "
                
            if "RANKED_FLEX_SR" in stats.values():
                ranked_flex["ranknum"] = stats["rank"]
                ranked_flex["division"] = stats["tier"]
                ranked_flex["lp"] = stats["leaguePoints"]
                ranked_flex["wins"] = stats["wins"]
                ranked_flex["losses"] = stats["losses"]

                games_ranked_flex = stats["wins"] + stats["losses"]
                ranked_solo["winrate"] = games_ranked_flex / stats["wins"] * 100
                
                ranked_flex_message = f"{ranked_flex['division']} {ranked_flex['ranknum']} {ranked_flex['lp']} LP \n \
                    {ranked_flex['wins']}W {ranked_flex['losses']}L {ranked_flex['winrate']} "
            
            
            
        #getting champion mastery information
        mastery = requests.get(f"")    
            

                
            
        
        
        
        
        
        
        
        
        mastery = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoneriD}")
        player_mastery = mastery.json()
        champdict={"championid": [], "masterylevel": [], "masterypoints": [] }
        for i in player_mastery(3):
            if i == "championId":
                champdict["championid"].extend([player_mastery["championId"]])
            elif i == "championLevel":
                champdict["masterylevel"].extend(player_mastery["championLevel"])
            elif i == "championPoints":
                champdict["masterypoints"].extend(player_mastery["championPoints"])
            #create a counter that only allows the loop to go 3 times
            
            
        
                
                
            
            
        
        
        
        
        
        
        
        #the embed message for the player stats and all its parameters
        embed_message = discord.Embed(title=f"Profile for {summonername}")
        embed_message.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/13.15.1/img/profileicon/{player_pfp}.png")
        embed_message.add_field(name="Summoner level" , value=player_level, inline= False)
        embed_message.add_field(name="Ranked Solo/Duo", value=ranked_solo_message, inline=False)
        embed_message.add_field(name="Ranked Flex", value=ranked_flex_message,inline=False)
        embed_message.add_field(name="Top champions", value=...,inline=False)
        embed_message.add_field(name="Recent Games", value=...,inline=False)
        embed_message.add_field(name="Last Game", value=...,inline=False)
        
        await ctx.send(embed = embed_message)
        
        
            
    @leagueprofile.error
    async def leagueprofile_error(self,ctx):
        ...
        
    
    
    @commands.command
    async def lolpatchnotes():
        ...    
           
    
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Lol is ready.")
        
        
        
        
        
async def setup(client):
    await client.add_cog(Lol(client))