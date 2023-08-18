import discord
from discord.ext import commands
from tokens import *

import requests
import json

class Lol(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #returns the users league stats  
    @commands.command() 
    async def leagueprofile(self, ctx, summonername:str, region = "na1"):
        regions = ["BR1","EUN1","EUW1","JP1","KR","LA1","LA2","NA1","OC1","PH2","RU","SG2","TH2","TR1","TW2","VN2"]
        if region.lower() not in regions:
            raise commands.BadArgument("region not found")
        
        summonerid = self.get_summonerid(summonername, region)
        if summonerid == None:
            await ctx.send(f"player {summonername} not found.")
        else:
            player_pfp = self.get_pfp(summonername, region)
            player_level = self.get_level(summonername, region)
            ranked_solo, ranked_flex = self.get_rank(summonername, region)
            top_champions = self.get_mastery(summonerid, region)
            
            embed_message = discord.Embed(title=f"{summonername}'s profile")
            embed_message.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/13.15.1/img/profileicon/{player_pfp}.png")
            embed_message.add_field(name="Summoner level" , value=player_level, inline= False)
            embed_message.add_field(name="Ranked Solo/Duo", value=ranked_solo, inline=False)
            embed_message.add_field(name="Ranked Flex", value=ranked_flex,inline=False)
            embed_message.add_field(name="Top champions", value=top_champions,inline=False)
            
            await ctx.send(embed = embed_message)
       
    
    #returns the most recent patch notes
    @commands.command()
    async def lolpatchnotes(self, ctx):
        version = self.get_latest_game_version()
        patch_url = f"https://na.leagueoflegends.com/en-us/news/game-updates/{version}-patch-notes/"

        embed = discord.Embed()
            
        embed = discord.Embed(
            title=f"**[patch {version.replace('.1', '')} notes3]{patch_url}**",
            description="The most recent patch notes for League of Legends",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    

    
    #utility functions
    def get_summonerid(self, summonername:str, region: str):
        response = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonername.replace(' ','%20')}?api_key={RIOT_KEY}")
        player_info = response.json()
        if response.status_code == 404:
            return None
        else:
            summoneriD = player_info["id"]
            return summoneriD
    
    
    def get_pfp(self, summonername:str, region: str):
        response = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonername.replace(' ','%20')}?api_key={RIOT_KEY}")
        player_info = response.json()
        player_pfp = player_info["profileIconId"]
        return player_pfp
    
    
    def get_level(self, summonername:str, region: str):
        response = requests.get((f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonername.replace(' ','%20')}?api_key={RIOT_KEY}"))
        player_info = response.json()
        player_level = player_info["summonerLevel"]
        return player_level
    
    def get_rank(self, summonerid, region):
        ranked_flex_message = "unranked"
        ranked_solo_message = "unranked"
        response = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerid}?api_key={RIOT_KEY}")
        
        for stats in response.json():
            if "RANKED_SOLO_5x5" in stats.values():
                total_games = stats["wins"] + stats["losses"]
                winrate = total_games / stats["wins"] * 100
                
                ranked_solo_message = f"{stats['tier']} {stats['rank']} {stats['leaguepoints']} LP \
                    {stats['wins']}W {stats['losses']}L {winrate}"
                
            
            if "RANKED_FLEX_SR" in stats.values():
                total_games = stats["wins"] + stats["losses"]
                winrate = total_games / stats["wins"] * 100
                
                ranked_solo_message = f"{stats['tier']} {stats['rank']} {stats['leaguepoints']} LP \
                    {stats['wins']}W {stats['losses']}L {winrate}"
                
        return ranked_solo_message, ranked_flex_message
    
    
    #gets the latest game version for request links  
    def get_latest_game_version(self):
        response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        data = response.json()
        
        if data:
            return data[0] #[0] is the most recent patch
        return '13.15.1'
    
    
    #returns a dict of all the champions with thier given ids and names together
    def get_champ_names(self):
        version = self.get_latest_game_version()
        response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json")
        data = response.json()
        champion_list = {champion['key']: champion['name'] for champion in data['data'].values()}
        return champion_list
        
    
    def get_mastery(self, summonerid, region):
        response = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerid}?api_key={RIOT_KEY}")
        mastery = response.json
        
        if len(mastery) == 0:
            return "no champions played"
        
        top_champs = mastery[:min(len(mastery), 3)] #get up to the top 3 champions info
        champion_info = []
        seperator = " "
        
        for champion in top_champs:
            champion_id = str(champion['championId'])
            champion_name = self.get_champ_name.get(champion_id, "champname")
            champion_info.append(f"{champion_name} M{champion['championLevel']} {champion['championPoints']}pts\n")
        
        newchampion_info = seperator.join(champion_info)    
        return newchampion_info
    
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Lol is ready.")
        
        
        
        
        
async def setup(client):
    await client.add_cog(Lol(client))