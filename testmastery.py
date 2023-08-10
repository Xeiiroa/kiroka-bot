import requests
import json
from tokens import *

#get champ id 
#find the mastery rank of said champion
#find mastery number




#compare champ id to champ name
#replace champ id with name



response = requests.get(f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/cSZjp1ioggKc8fTHM867W7QVFWYKtIoVyse8MrxWpBvDjOzxvh1uXHvy3g?api_key={RIOT_KEY}")
champ_info = requests.get("https://ddragon.leagueoflegends.com/cdn/13.15.1/data/en_US/champion.json")




#individual dicts
#a list of dicts

#append each of the stats unless the length of a key is 3 or the for loop ends
#for champs in champion ids
    #go through the file and compare the keys to the champ name and swap it out
champ_stats = [{"championids":[], "masterylvl":[], "masterypoints":[]}]
finalchampholder = []

for i in response.json():
    if len(champ_stats["championids"]) == 3:
        break
    
    if "championId" in i.keys():
        champ_stats["championids"] += i["championId"]
        champ_stats["masterylvl"] += i["championLevel"]
        champ_stats["masterypoints"] += i["championPoints"]
        
        
for j in champ_stats["championids"]:
    for k in champ_info:
        #find champ number and take its name and replace said id with said name
        if "key" in j.keys():
            # if key(champion id number = j(also champ id number))
            if "key" == j:
                #print(j (test))
                print(j)
    
                """ what i actually want to do with it"""
                #update champ_stats["championids"][j] for k["name"]  (k[name] is the champions name)
                
                
                
                #after that just iterate over each part of the dict likely using a for loop
                
                
                #for i in range len(champ_stats["championids"]):
                    
                    #champ_stats["championids"][i].append to a list or create a string out of it and add said string to a list
                    
                    #ex: exstring=f"{champ_stats["championids"][i]} M{champ_stats["masterylvl"][i]} {champ_stats["masterypoints"][i]}pts
                    #exlist.append(exstring) 
                    #after that i can just print the list by index and add a\n after finding a way to remove the brackets
                    
                    #sort by champion(each champion has their own index already so just add the indexes of each to a list)

                
    
        
    
        
    
    
    
    
        
        
     
     

    
   
    
        
        
    
    
    
    
    
    
    
    