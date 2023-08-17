import discord
from discord.ext import commands
from tokens import *

import requests
import json

class Lol(commands.Cog):
    def __init__(self, client):
        self.client = client
       
    #TODO finish adding all the messages from the old command to the new one    
    @commands.command() 
    async def leagueprofile(self, ctx, summonername:str, region = "na1"):
        regions = ["BR1","EUN1","EUW1","JP1","KR","LA1","LA2","NA1","OC1","PH2","RU","SG2","TH2","TR1","TW2","VN2"]
        if region.lower() not in regions:
            raise commands.BadArgument("region not found")
        
        summonerid = self.get_summonerid(summonername, region)
        if summonerid == None:
            ctx.send(f"player {summonername} not found.")
        else:
            ...
            
             
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
        ranked_solo = {}
        ranked_flex = {}
        ranked_flex_message = "unranked"
        ranked_solo_message = "unranked"
        response = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoneriD}?api_key={RIOT_KEY}")
        
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
        
        
    #TODO create the mastery function and allow it to have name conversion   
    def get_champname(self)
    
    def get_mastery(self, summonerid, region):
        mastery = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoneriD}?api_key={RIOT_KEY}")
        
    
        
        

    
        
    #  FIXME clean this up. remake the command using normal functions to avoid long term confusion   
    @commands.command()
    async def leagueprofile(self, ctx, summonername: str, region: str):
        regions = ["BR1","EUN1","EUW1","JP1","KR","LA1","LA2","NA1","OC1","PH2","RU","SG2","TH2","TR1","TW2","VN2"]
        
        # getting data for summoner name, profile icon id, level, and account idea for further inspection
        summonerinfolink = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonername.replace(' ','%20')}?api_key={RIOT_KEY}")
        player_info= summonerinfolink.json()
        player_pfp = player_info["profileIconId"]
        player_level = player_info["summonerLevel"]
        summoneriD = player_info["id"]
        ranked_solo = {}
        ranked_flex = {}
        ranked_flex_message = "unranked"
        ranked_solo_message = "unranked"
        summonerrankinfo = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoneriD}?api_key={RIOT_KEY}")
        #done
        

        mastery = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoneriD}?api_key={RIOT_KEY}")
        """get back to this to allow the site to update at the date you choose"""
        champ_info = requests.get("https://ddragon.leagueoflegends.com/cdn/13.15.1/data/en_US/champion.json")
        champ_stats = {"champname":[], "championids":[], "masterylvl":[], "masterypoints":[]}
        
        for i in mastery.json():
            if len(champ_stats["championids"]) == 3:
                break
    
            elif "championId" in i.keys():
                champ_stats["championids"].append(i["championId"])
                champ_stats["masterylvl"].append(i["championLevel"])
                champ_stats["masterypoints"].append(i["championPoints"])
                #create a counter that only allows the loop to go 3 times
                
        
        
        for j in champ_stats["championids"]:
            for k in champ_info:
        #find champ number and take its name and replace said id with said name
                if "key" in k.keys():
                    if k["key"] == champ_stats["championids"][j]: 
                        champ_stats["champname"].append(k["name"])
                

        masterystring = f"{champ_stats['champname'][0]} M{champ_stats['masterylvl'][0]} {champ_stats['masterypoints'][0]} \n\
            {champ_stats['champname'][1]} M{champ_stats['masterylvl'][1]} {champ_stats['masterypoints'][1]} \n\
                {champ_stats['champname'][2]} M{champ_stats['masterylvl'][2]} {champ_stats['masterypoints'][2]}"
                
                
                
        
            
            
            
            
        
                
                
            
            
        
        
        
        
        
        
        
        #the embed message for the player stats and all its parameters
        embed_message = discord.Embed(title=f"Profile for {summonername}")
        embed_message.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/13.15.1/img/profileicon/{player_pfp}.png")
        embed_message.add_field(name="Summoner level" , value=player_level, inline= False)
        embed_message.add_field(name="Ranked Solo/Duo", value=ranked_solo_message, inline=False)
        embed_message.add_field(name="Ranked Flex", value=ranked_flex_message,inline=False)
        embed_message.add_field(name="Top champions", value=masterystring,inline=False)
        embed_message.add_field(name="Recent Games", value=...,inline=False)
        embed_message.add_field(name="Last Game", value=...,inline=False)
        
        await ctx.send(embed = embed_message)
        
        
            
    @leagueprofile.error
    async def leagueprofile_error(self,ctx):
        ...
        
    
    @commands.command()
    async def patchnotes(self, ctx):
        link = "https://na1.api.riotgames.com/lol/patches"
        response = requests.get(link, params={'api_key': RIOT_KEY})
        most_recent_patch = response.json()[0]
        patchnotes = most_recent_patch["notes"]
        
        print(patchnotes)
    
    
    @commands.command
    async def lolpatchnotes():
        ...    
           
    
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Lol is ready.")
        
        
        
        
        
async def setup(client):
    await client.add_cog(Lol(client))