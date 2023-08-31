import discord
from discord.ext import commands
from tokens import *
import requests, json

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    @commands.hybrid_command(name="animeinfo", description="Gives the information of a given anime", with_app_command=True)
    async def animeinfo(self, ctx, *, anime_title):
        info = self.get_info(anime_title)
        
        if info == None:
            await ctx.send(f"Anime {anime_title} was not found")
            
        else:
            embed = discord.Embed(
                title=f"information for {info['title']}",
                description=info['description'].replace("<br><br>", ""),
                #might change to beige or black
                color=discord.Color.blue()
            )
            
            embed.set_thumbnail(url=info['cover_image'])
            embed.add_field(name="Episodes", value=info['episodes'])
            embed.add_field(name="Genres",value=info['genres']) 
            embed.add_field(name="Status", value=info['status'].capitalize(),inline=False)
            
            
            #!
            '''if info['sequels']:
                embed.add_field(name="Other Seasons", value=info['sequels'])'''
            
            
            
            await ctx.send(embed=embed)
            
            
        
        
        
    #* Utility functions
    def get_info(self, anime_title):
        info = {}
        base_url = "https://graphql.anilist.co"

        #TODO customize query to allow exclusive sequel (and maybe prequel search)
        # using sequel = true is an option to try
        query = '''
        query ($anime_title: String) {
        Media(search: $anime_title, type: ANIME) {
            title {
            romaji
            english
            }
            description(asHtml: false)
            episodes
            genres
            averageScore
            status
            coverImage {
            large
            }
            relations {
            edges {
                node {
                title {
                    romaji
                }
                type
                }
            }
            }
        }
        }
        '''

        variables = {
            "anime_title": anime_title
        }

        
        response = requests.post(base_url, json={'query': query, 'variables': variables})
        data = response.json()
        
        if 'errors' in data:
            return None
        
        else:
            anime_data = data['data']['Media']
            info['title'] = anime_data['title']['romaji']
            info['description'] = anime_data['description']
            info['episodes'] = anime_data['episodes']
            info['genres'] = ', '.join(anime_data['genres'])
            info['cover_image'] = anime_data['coverImage']['large']
            info['status'] = anime_data['status']
            
            
            relations = anime_data['relations']['edges']
            related_seasons = [f"{rel['node']['title']['romaji']} ({rel['node']['type']})" for rel in relations if rel['node']['type'] == 'SEQUEL']
            season_sep="\n"

            #if theres any related seasons add them in list format
            if related_seasons:
                info['sequels'] = season_sep.join(related_seasons)
                
            return info
        
        
async def setup(bot):
    await bot.add_cog(Anime(bot))