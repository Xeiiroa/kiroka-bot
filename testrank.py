import requests
import json
from tokens import *

league =[
    {
        "leagueId": "f179bc4d-a061-48fa-a00f-6311e08c42e9",
        "queueType": "RANKED_FLEX_SR",
        "tier": "SILVER",
        "rank": "I",
        "summonerId": "FJt96ydgID9T37q6TOoNBHWmGVoDAVM53zk-zgMBo6Q3g_ZYaj9XCYK8hQ",
        "summonerName": "YellowRedBull",
        "leaguePoints": 40,
        "wins": 5,
        "losses": 5,
        "veteran": False,
        "inactive": False,
        "freshBlood": False,
        "hotStreak": False
    },
    {
        "leagueId": "2f130419-9968-43af-9acb-8a4edb2a8ae4",
        "queueType": "RANKED_SOLO_5x5",
        "tier": "GOLD",
        "rank": "III",
        "summonerId": "FJt96ydgID9T37q6TOoNBHWmGVoDAVM53zk-zgMBo6Q3g_ZYaj9XCYK8hQ",
        "summonerName": "YellowRedBull",
        "leaguePoints": 78,
        "wins": 53,
        "losses": 51,
        "veteran": False,
        "inactive": False,
        "freshBlood": False,
        "hotStreak": True
    },
    {
        "queueType": "CHERRY",
        "summonerId": "FJt96ydgID9T37q6TOoNBHWmGVoDAVM53zk-zgMBo6Q3g_ZYaj9XCYK8hQ",
        "summonerName": "YellowRedBull",
        "leaguePoints": 0,
        "wins": 29,
        "losses": 42,
        "veteran": False,
        "inactive": False,
        "freshBlood": False,
        "hotStreak": True
    }
]

ranked_solo = []
ranked_flex = {}


url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/FJt96ydgID9T37q6TOoNBHWmGVoDAVM53zk-zgMBo6Q3g_ZYaj9XCYK8hQ?api_key={RIOT_KEY}"
response = requests.get(url)

#loops over each dict
for i in response.json():
    if "RANKED_SOLO_5x5" in i.values():
        ranked_solo.append(i["tier"])
        ranked_solo.append(i["rank"])
        ranked_solo.append(i["leaguePoints"])
    if "RANKED_FLEX_SR" in i.values():
        ranked_flex["rank"] = i["rank"]
        
        
    
    


print(f"Ranked solo stats = {ranked_solo}")    
print(f"Ranked flex stats = {ranked_flex['rank']}")    
            


        
#use index to find the id 
#learned in riot api with python p3 3:21
        
#if queutype = rankedsolo
#append rank to ranked stats

#if ranked stats = None print unranked        
        



#add api code onto file 




