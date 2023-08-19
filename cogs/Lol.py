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
    async def lolstats(self, ctx, summonername:str, region = "na1"):
        regions = ["br1","eun1","euw1","jp1","kr","la1","la2","na1","oc1","ph2","ru","sg2","th2","tr1","tw2","vn2"]
        if region.lower() not in regions:
            await ctx.send("non-valid region provided" + "\n" + "list of valid regions:" + "\n" +
                           "br1, eun1, euw1, jp1, kr, la1, la2, na1, oc1, ph2, ru, sg2, th2, tr1, tw2, vn2")
        
        summonerid = self.get_summonerid(summonername, region)
        if summonerid == None:
            await ctx.send(f"player {summonername.title()} not found.")
        else:
            version = self.get_latest_game_version()
            player_pfp = self.get_pfp(summonername, region)
            player_level = self.get_level(summonername, region)
            ranked_solo, ranked_flex = self.get_rank(summonerid, region)
            top_champions = self.get_mastery(summonerid, region)
            
      
            embed = discord.Embed(
                title=f"{summonername.title()}'s stats- lvl {player_level}",
                color=discord.Color.blue()
            )
            
            
            embed.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{player_pfp}.png")
            
            
            embed.add_field(name="Top champions", value=top_champions, inline=True)
            embed.add_field(name="Ranked Solo/Duo", value=ranked_solo, inline=False)
            embed.add_field(name="Ranked Flex", value=ranked_flex, inline=False)
            
            await ctx.send(embed=embed)
       
    
    #returns the most recent patch notes
    @commands.command()
    async def lolpatchnotes(self, ctx):
        version = self.get_latest_game_version()
        version = version[:-2].replace('.', '-')
        patch_url = f"https://www.leagueoflegends.com/en-us/news/game-updates/patch-{version}-notes/"

        embed = discord.Embed(
            title=f"Patch {version.replace('-','.')} notes",
            description="The most recent patch notes for League of Legends",
            url=patch_url,
            color=discord.Color.blue()   
        )
        await ctx.send(embed=embed)
    

    
    # ? qutility functions
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
                winrate = (stats["wins"] / total_games) * 100 if total_games > 0 else 0
                winrate =("%d" % winrate)
                winrate = f"{winrate}%"
                
                ranked_solo_message = f"{stats['tier']} {stats['rank']} {stats['leaguePoints']}LP \n{stats['wins']}W {stats['losses']}L {winrate}"
                
            
            if "RANKED_FLEX_SR" in stats.values():
                total_games = stats["wins"] + stats["losses"]
                winrate = (stats["wins"] / total_games) * 100 if total_games > 0 else 0
                winrate =("%d" % winrate)
                winrate = f"{winrate}%"
                
                ranked_solo_message = f"{stats['tier']} {stats['rank']} {stats['leaguePoints']}LP \n{stats['wins']}W {stats['losses']}L {winrate}"
                
        return ranked_solo_message, ranked_flex_message
    
    
    #gets the latest game version for request links  
    def get_latest_game_version(self):
        response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        data = response.json()
        
        if data:
            return data[0] #[0] is the most recent patch
        return '13.16.1'
    
    
    #returns a dict of all the champions with thier given ids and names together
    def get_champ_names(self):
        version = self.get_latest_game_version()
        response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json")
        data = response.json()
        #? idk
        champion_list = {champion['key']: champion['name'] for champion in data['data'].values()}
        return champion_list
        
    
    def get_mastery(self, summonerid, region):
        url=f"https://{region.lower()}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerid}?api_key={RIOT_KEY}"
        headers = {'X-Riot-Token': RIOT_KEY}
        response = requests.get(url, headers=headers)
        mastery = response.json()
        
        if len(mastery) == 0:
            return "no champions played"
        
        top_champs = mastery[:min(len(mastery), 3)] #get up to the top 3 champions info
        champion_info = []
        seperator = " "
        
        for champion in top_champs:
            champion_id = str(champion['championId'])
            champion_name = self.get_champ_names().get(champion_id)
            champion_info.append(f"{champion_name} M{champion['championLevel']} {champion['championPoints']} pts\n")
        
        newchampion_info = seperator.join(champion_info)    
        return newchampion_info
    
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Lol is ready.")
        
        
        
        
        
async def setup(client):
    await client.add_cog(Lol(client))