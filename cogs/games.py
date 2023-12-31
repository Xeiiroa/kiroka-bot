#file to hold game related commands
import discord
from discord.ext import commands
from tokens import *
from discord.ui import Select
from typing import Literal

import requests
import json
import datetime

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Games is ready.")
    
    #*LEAGUE OF LEGENDS COMMANDS
    
    
    #returns the users league stats  
    @commands.hybrid_command(name="lolstats", description="gives basic info of a given league player")
    async def lolstats(self, ctx, summonername:str, region: Literal["EUN1","EUW1","JP1","KR","NA1","RU"]):
        regions = ["EUN1","EUW1","JP1","KR","NA1","RU"]
        if region.lower() not in regions:
            await ctx.send("non-valid region provided" + "\n" + "list of valid regions:" + "\n" +
                           "EUN1, EUW1, JP1, KR, NA1, RU")
        
        summonerid = self.get_summonerid(summonername, region)
        if summonerid == None:
            await ctx.send(f"player {summonername.title()} not found.")
        else:
            version = self.get_latest_game_version_lol()
            player_pfp = self.get_pfp_lol(summonername, region)
            player_level = self.get_level_lol(summonername, region)
            ranked_solo, ranked_flex = self.get_rank_lol(summonerid, region)
            top_champions = self.get_mastery_lol(summonerid, region)
            
      
            embed = discord.Embed(
                title=f"{summonername.title()}'s stats- lvl {player_level}",
                color=discord.Color.blue()
            )
            
            
            embed.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{player_pfp}.png")
            
            embed.add_field(name="Ranked Solo/Duo", value=ranked_solo, inline=True)
            embed.add_field(name="Top champions", value=top_champions, inline=True)
            embed.add_field(name="Ranked Flex", value=ranked_flex, inline=False)
            
            await ctx.send(embed=embed)
       
    
    #returns the most recent patch notes for lol
    @commands.hybrid_command(name="lolpatchnotes", description="Gives the url to league of legends most recent patch")
    async def lolpatchnotes(self, ctx):
        version = self.get_latest_game_version_lol()
        version = version[:-2].replace('.', '-')
        patch_url = f"https://www.leagueoflegends.com/en-us/news/game-updates/patch-{version}-notes/"

        embed = discord.Embed(
            title=f"Patch {version.replace('-','.')} notes",
            description="The most recent patch notes for League of Legends",
            url=patch_url,
            color=discord.Color.blue()   
        )
        await ctx.send(embed=embed)
        
    
    #* OSU! COMMANDS
    
    #gets users osu stats    
    @commands.hybrid_command(name="osustats", description="Gives the stats of an osu player")
    async def osustats(self, ctx, playername):
        profile = self.get_profile_osu(playername)
        if profile == None:
            await ctx.send(f"player, {playername} not found")
        else:
            try:   
                player_url = f"https://osu.ppy.sh/users/{profile['userid']}"
                avatar_url=f"https://a.ppy.sh/{profile['userid']}"
                
                embed = discord.Embed(
                    title=f"{playername}'s stats for Osu!",
                    url=player_url,
                    color=discord.Color.blue()
                )
                
                
                embed.set_thumbnail(url=avatar_url)
                
                embed.add_field(name="Level", value=profile['level'], inline=False)
                embed.add_field(name="Rank", value=f"{profile['rank']}", inline=False)
                embed.add_field(name="PP", value=profile['pp'], inline=False)
                embed.add_field(name="Accuracy", value=profile['accuracy'], inline=False)
                embed.add_field(name="Score", value=f"Ranked Score: {profile['rscore']}\nTotal Score: {profile['tscore']}", inline=False)
                embed.add_field(name="Playtime", value=f"{profile['playtime']} ({profile['playcount']}Plays)", inline=False)


                await ctx.send(embed=embed)
            except Exception as e:
                print(f"An error occurred: {e}")
    
    
                
    #*Valorant commands
    
    @commands.hybrid_command(name="valorantpatchnotes", description="Gives the url to Valorant's most recent patch")
    async def valpatchnotes(self, ctx, region="na"):
        regions = ["ap","br","eu","kr","latam","na","esports"]
        if region.lower() not in regions:
            await ctx.send("non-valid region provided" + "\n" + "valid regions include: ap, br, eu, kr, latam, na")
        else:
            version = self.get_latest_game_version_val(region)
            patch_url=f"https://playvalorant.com/en-us/news/game-updates/valorant-patch-notes-{version}/"
            
            embed = discord.Embed(
                title=f"Valorant Patch {version.replace('-', '.')} notes",
                color=discord.Color.blue(),
                description="The most recent patch notes for Valorant",
                url=patch_url
            )
            await ctx.send(embed=embed)
            
            
            
    #* VALORANT UTILITY FUNCTIONS
    
    def get_latest_game_version_val(self, region):
        url=f"https://{region}.api.riotgames.com/val/content/v1/contents"
        headers = {
            "X-Riot-Token": RIOT_KEY
        }
        response = requests.get(url, headers=headers)
        data = response.json()
    
        _, version = data['version'].split("-")
        if version.startswith("0"):
            return version[1:].replace(".", "-")
        else:
            return version.replace(".", "-")



    #* OSU! UTILITY FUNCTIONS

    def get_profile_osu(self, playername):
        stats = {}
        url = "https://osu.ppy.sh/api/get_user"
        params = {
            "k": OSU_KEY,
            "u": playername
        }
        response = requests.get(url, params=params)
        data=response.json()
        
        if data == []:
            return None
        
        else:
            
            stats['userid'] = data[0]['user_id']
            stats['playcount'] = f"{int(data[0]['playcount']):,}"
            stats['rscore'] = f"{int(data[0]['ranked_score']):,}"
            stats['tscore'] = f"{int(data[0]['total_score']):,}"
            stats['country'] = data[0]['country']
            stats['rank'] =  f"Global:{int(data[0]['pp_rank']):,}\n{data[0]['country']} Rank:{int(data[0]['pp_country_rank']):,}"
            stats['level'] = ("%d" % float(data[0]["level"]))
            stats['pp'] = "{:,}".format(round(float(data[0]['pp_raw'])))
            stats['accuracy'] = f"{float(data[0]['accuracy']): .2f}"
            
            
            playtime_seconds = int(data[0]['total_seconds_played'])
            days, remainder = divmod(playtime_seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, _ = divmod(remainder, 60)
    
            stats['playtime'] = f"{days}D {hours}H {minutes}M"
            
            return stats


    #* LEAGUE UTILITY FUNCTIONS
    def get_summonerid(self, summonername:str, region: str):
        response = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonername.replace(' ','%20')}?api_key={RIOT_KEY}")
        player_info = response.json()
        if response.status_code == 404:
            return None
        else:
            summoneriD = player_info["id"]
            return summoneriD
    
    
    def get_pfp_lol(self, summonername:str, region: str):
        response = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonername.replace(' ','%20')}?api_key={RIOT_KEY}")
        player_info = response.json()
        player_pfp = player_info["profileIconId"]
        return player_pfp
    
    
    def get_level_lol(self, summonername:str, region: str):
        response = requests.get((f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonername.replace(' ','%20')}?api_key={RIOT_KEY}"))
        player_info = response.json()
        player_level = player_info["summonerLevel"]
        return player_level
    
    def get_rank_lol(self, summonerid, region):
        ranked_emojis={"IRON": "<:Iron:1146489440332685382>",
                       "BRONZE": "<:Bronze:1146489123109093406>", 
                       "SILVER": "<:Silver:1146489422905356368>",
                       "GOLD": "<:Gold:1146489457378328696>",
                       "PLATINUM": "<:Platinum:1146489471399891004>",
                       "EMERALD": "<:Emerald:1146492847143518379>",
                       "DIAMOND": "<:Diamond:1146489492732133417>",
                       "MASTER": "<:Master:1146489508414640128>",
                       "GRANDMASTER": "<:Master:1146489520334831716>",
                       "CHALLENGER": "<:Challenger:1146489530644451409>"}
        
        ranked_flex_message = "unranked"
        ranked_solo_message = "unranked"
        response = requests.get(f"https://{region.lower()}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerid}?api_key={RIOT_KEY}")
        
        for stats in response.json():
            if "RANKED_SOLO_5x5" in stats.values():
                total_games = stats["wins"] + stats["losses"]
                winrate = (stats["wins"] / total_games) * 100 if total_games > 0 else 0
                winrate =("%d" % winrate)
                winrate = f"{winrate}%"
                
                
                
                ranked_solo_message = f"{ranked_emojis[stats['tier']]}{stats['tier']} {stats['rank']}{ranked_emojis[stats['tier']]}\n {stats['leaguePoints']}LP \n{stats['wins']}W {stats['losses']}L {winrate}"
                
            
            if "RANKED_FLEX_SR" in stats.values():
                total_games = stats["wins"] + stats["losses"]
                winrate = (stats["wins"] / total_games) * 100 if total_games > 0 else 0
                winrate =("%d" % winrate)
                winrate = f"{winrate}%"
                
                ranked_flex_message = f"{ranked_emojis[stats['tier']]}{stats['tier']} {stats['rank']}{ranked_emojis[stats['tier']]}\n {stats['leaguePoints']}LP \n{stats['wins']}W {stats['losses']}L {winrate}"
                
        return ranked_solo_message, ranked_flex_message
    
    
    #gets the latest game version for request links  
    def get_latest_game_version_lol(self):
        response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        data = response.json()
        
        if data:
            return data[0] #[0] is the most recent patch
        return '13.16.1'
    
    
    #returns a dict of all the champions with thier given ids and names together
    def get_champ_names_lol(self):
        version = self.get_latest_game_version_lol()
        response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json")
        data = response.json()
        #? idk
        champion_list = {champion['key']: champion['name'] for champion in data['data'].values()}
        return champion_list
        
    
    def get_mastery_lol(self, summonerid, region):
        mastery_emojis={4: "<:M4:1146491370677227591>",
                        5: "<:M5:1146491359595872296>",
                        6: "<:M6:1146491139860471881>",
                        7: "<:M7:1146491152770543686>"}
        
        url=f"https://{region.lower()}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerid}?api_key={RIOT_KEY}"
        headers = {'X-Riot-Token': RIOT_KEY}
        response = requests.get(url, headers=headers)
        mastery = response.json()
        
        if len(mastery) == 0:
            return "no champions played"
        
        top_champs = mastery[:min(len(mastery), 5)] #get up to the top 5 champions info
        champion_info = []
        seperator = " "
        
        for champion in top_champs:
            champion_id = str(champion['championId'])
            champion_name = self.get_champ_names_lol().get(champion_id)
        
            if champion["championLevel"] < 4:
                champion_info.append(f"{champion_name} M{champion['championLevel']} {champion['championPoints']}pts\n")
            else:
                champion_info.append(f"{mastery_emojis[champion['championLevel']]} {champion_name} {champion['championPoints']}pts\n")
        
        newchampion_info = seperator.join(champion_info)    
        return newchampion_info
    


async def setup(bot):
    await bot.add_cog(Games(bot))