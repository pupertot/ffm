from ff_espn_api import League
import requests
import json
from iterateDictionary import *

league_id = 509804
year = 2020
swid = '{81B9F363-5ED4-4FFD-A35C-047FCEE83965}'
espn_s2 = 'AEC2WwjnHbF3KZlA3y%2BIV5khPQnzTaJRAHULLiU3Fd5HyB%2BqC2xQjvnYaqLdk0wKcHCdhBD%2F4jsQAGDNxUIrHvi972xrv5SJpU7O5oRWhJbaUlbX5%2F7TijXjerUf3Z3RRslvffNBGW1rwGA4rUCrf%2F0bDNt2od5wRENw%2FXUwfq810%2FRJXOJeJhFuGoxxd0FE%2BfBB57pQ6Y2JUn6ET7vA3e9DOxi%2F%2BLonwA19XYgBu82b2heV57GFZNXV29cEUGlZmwnAioIcrF2bmS8PAANfdwlFukzNd6byTUInUa050vanJw%3D%3D'
#league = League(league_id, year, espn_s2=espn_s2, swid=swid)
#print(league.teams)

url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/" + str(year) + "/segments/0/leagues/" + str(league_id)
print(url)      
params = {
            'view': 'mTeam'
        } 
resp = requests.get(url, params = params,
                 cookies={"swid": swid,
                          "espn_s2": espn_s2})

print(resp)
data = resp.json()
print(data)
#members = data['members']
#print(members[0]['displayName'])
#print(len(members))
    