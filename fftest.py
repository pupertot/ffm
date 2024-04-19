from ff_espn_api import League
import requests
import json
import pydash

#https://fantasy.espn.com/apis/v3/games/ffl/seasons/2020/segments/0/leagues/509804?view=mMatchup&view=mMatchupScore&scoringPeriodId=0

urlBase = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/"
league_id = 509804
year = 2020
swid = '{81B9F363-5ED4-4FFD-A35C-047FCEE83965}'
espn_s2 = 'AEC2WwjnHbF3KZlA3y%2BIV5khPQnzTaJRAHULLiU3Fd5HyB%2BqC2xQjvnYaqLdk0wKcHCdhBD%2F4jsQAGDNxUIrHvi972xrv5SJpU7O5oRWhJbaUlbX5%2F7TijXjerUf3Z3RRslvffNBGW1rwGA4rUCrf%2F0bDNt2od5wRENw%2FXUwfq810%2FRJXOJeJhFuGoxxd0FE%2BfBB57pQ6Y2JUn6ET7vA3e9DOxi%2F%2BLonwA19XYgBu82b2heV57GFZNXV29cEUGlZmwnAioIcrF2bmS8PAANfdwlFukzNd6byTUInUa050vanJw%3D%3D'
#league = League(league_id, year, espn_s2=espn_s2, swid=swid)
#print(league.teams)

#url = urlBase + str(year) + "/segments/0/leagues/" + str(league_id) 
#"?view=mMatchup&view=mMatchupScore&scoringPeriodId=0"
url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2020/segments/0/leagues/509804?view=mMatchup&view=mMatchupScore&scoringPeriodId=0"
print(url)      
#params = {
#            'view': 'mMatchup',
#            'view': 'mMatchupScore&scoringPeriodId=0'            
#        } 
#resp = requests.get(url, params = params,
#                 cookies={"swid": swid,
#                          "espn_s2": espn_s2})
resp = requests.get(url, 
                 cookies={"swid": swid,
                 "espn_s2": espn_s2})

respJson = resp.json()
schedule = respJson.get("schedule")
#matchup = pydash.filter_(schedule, {'matchupPeriodId' : 2})
matchup = schedule

print("\nList of keys:")
for x, y in respJson.items():
  print(x, ":", type(respJson[x]))
  

print("\nList of keys1:")
for i in range(len(matchup)):
  print("")
  for x, y in matchup[i].items():
    #print(x, " : ",type(y))
    #if isinstance(y,dict):
    if x == 'away':
      for a, b in y.items():
        if isinstance(b,dict):       #i think this isn't getting the roster because of the filter above on matchupperiodid
          print(a)
    #  awayTeamScore = y.get("totalPoints")
    #  print("Away score:", awayTeamScore)
    #if x == 'home':
      #
    #  homeTeamScore = y.get("totalPoints")
    #  print("Home score: ", homeTeamScore)
    #if x == 'winner':
    #  print("Winner: ",y)


    




#schedMap = pydash.map_(schedule2)


#with open('jsonfile.txt','w') as outfile:
#  json.dump(schedule3, outfile)


#data = resp.json()
#print(data)
#members = data['members']
#print(members[0]['displayName'])
#print(len(members))
    