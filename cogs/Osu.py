import discord
from discord.ext import commands
from tokens import *
import requests
import json

from ossapi import Ossapi

class Osu(commands.Cog):
    def __init__(self, client):
        self.client = client
        api = Ossapi(OSU_CLIENT_ID, OSU_SECRET)
        api_key=OSU_KEY
        
     
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Osu is ready.")
        
        
    @commands.command()
    async def osustats(self, ctx, playername):
        profilelink = (f"https://osu.ppy.sh/api/get_user")
        params = {
            "k": OSU_KEY,
            "u": playername
        }
    
    
        response = requests.get(profilelink, params=params)
        
        if response.status_code == 200:
            player_data = response.json()[0]
            #theres more links in this but i have to print the actual json file which i need my pc for
            print("Player ID:", player_data["user_id"])
            print("Player Username:", player_data["username"])
            print("Player Country:", player_data["country"])
        
    
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
        
        #TODO append these things to the dict and return them
        """
        #userid, 
        # playcount, 
        # rankedscore, 
        # totalscore, 
        # country, 
        # globalrank, 
        # countryrank, 
        # level(remove all decimal points)
        # pp(remove all decimal points)
        # accuracy(remove all decimal points besides the last 2)
        # playtime(default is in seconds so ill have to use datetime to change it to days hours min)
        """
        
        #*remember that the userid is what leads to the playerlink so you can hyperlink it to the embed link later on
        stats += ...
        
    #get the count for ranks acheived (100 s ranks, 400 a ranks, etc)
    def get_ranks(self, playername):
        stats={}
        url = "https://osu.ppy.sh/api/get_user"
        params = {
            "k": OSU_KEY,
            "u": playername
        }
        response = requests.get(url, params=params)
        data=response.json()
        
        #TODO append these things to the dict and return them
        """
        #silver ss ranks
        #ss ranks
        #silver s ranks
        #s ranks
        #a ranks
        """
        
        
        
        
        
        
async def setup(client):
    await client.add_cog(Osu(client))