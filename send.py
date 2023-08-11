import requests
import json
from tokens import *

#mastery link
response = requests.get(f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/cSZjp1ioggKc8fTHM867W7QVFWYKtIoVyse8MrxWpBvDjOzxvh1uXHvy3g?api_key={RIOT_KEY}")

#champ comparison
champ_info = requests.get("https://ddragon.leagueoflegends.com/cdn/13.15.1/data/en_US/champion.json")


#list of dictionaries to hold values for the 3 champs
champ_stats = {"championids":[], "masterylvl":[], "masterypoints":[]}


for i in response.json():
    if len(champ_stats["championids"]) == 3:
        break
    elif "championId" in i.keys():
        champ_stats["championids"].extend(str(i["championId"]))
        print(len)(champ_stats["championids"])
