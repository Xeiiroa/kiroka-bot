import discord
from discord.ext import commands
from tokens import *
import requests
import json
import datetime

from ossapi import Ossapi

class Osu(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Osu is ready.")
        
    #gets users osu stats    
    @commands.command()
    async def osustats(self, ctx, playername):
        
        profile = self.get_profile(playername)
        
        
        
        if profile == None:
            print("n")
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
                
                print(profile)
                print("\n")
                print(profile['playtime'])
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
   
   
    @commands.command()
    async def recentplay(self, ctx, playername):
        key = OSU_KEY
        base_url = "https://osu.ppy.sh/api"
        endpoint = "/get_user_recent"
        params = {
        "k": key,
        "u": playername,  # Replace with the player's username
        "limit": 1,       # Number of recent plays to retrieve
        }
        
        response = requests.get(base_url + endpoint, params=params)
        
        
        if response.status_code == 200: #if link is found
            if len(response.json()) > 0:
                most_recent_play = response.json()[0]
                print("Beatmap ID:", most_recent_play["beatmap_id"])
                print("Score:", most_recent_play["score"])
                print("Max Combo:", most_recent_play["maxcombo"])
                print("Rank:", most_recent_play["rank"])
                #possibly more when i check the link
            else:
                print("No recent plays found for the player.")
        else:
            print("Failed to retrieve recent play information.")
    
    @commands.command()
    async def topplays(self, ctx, playername):
        base_url = "https://osu.ppy.sh/api"
        endpoint = "/get_user_best"
        params = {
        "k": OSU_KEY,
        "u": playername,  # Replace with the player's username
        "limit": 3,       # Number of top plays to retrieve
        }
        
        response = requests.get(base_url + endpoint, params=params)
        
        if response.status_code == 200:
   
            if len(response.json) > 0:
                for index, top_play in enumerate(response.json()):
                    print(f"Top Play {index + 1}:")
                    print("Beatmap ID:", top_play["beatmap_id"])
                    print("Score:", top_play["score"])
                    print("Max Combo:", top_play["maxcombo"])
                    print("Rank:", top_play["rank"])
                    # Add more fields as needed
                    print()
            else:
                print("No top plays found for the player.")
        else:
            print("Failed to retrieve top play information.")
    
        
    def get_profile(self, playername):
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
            #TODO append these things to the dict and return them
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
        
        
    #get the count for ranks acheived (100 s ranks, 400 a ranks, etc)
    def get_ranks(self, playername):
        ranks={}
        url = "https://osu.ppy.sh/api/get_user"
        params = {
            "k": OSU_KEY,
            "u": playername
        }
        response = requests.get(url, params=params)
        data=response.json()
        
        ranks['silv_ss'] = data[0]['count_rank_ssh']
        ranks['silv_s'] = data[0]['count_rank_sh']
        ranks['ss']  = data[0]['count_rank_ss']
        ranks['s']  = data[0]['count_rank_s']
        ranks['a']  = data[0]['count_rank_a']
        
        return ranks    
       
        
        
        
        
        
async def setup(client):
    await client.add_cog(Osu(client))