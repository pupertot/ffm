import requests
import json
#import restart
#from restart import RESTArt, Resource
from flask import Flask
from flask_restful import Resource, reqparse, Api 
from league import League

ffApp = Flask(__name__)
api = Api(ffApp)

swid = '{81B9F363-5ED4-4FFD-A35C-047FCEE83965}'
espn_s2 = 'AEC2WwjnHbF3KZlA3y%2BIV5khPQnzTaJRAHULLiU3Fd5HyB%2BqC2xQjvnYaqLdk0wKcHCdhBD%2F4jsQAGDNxUIrHvi972xrv5SJpU7O5oRWhJbaUlbX5%2F7TijXjerUf3Z3RRslvffNBGW1rwGA4rUCrf%2F0bDNt2od5wRENw%2FXUwfq810%2FRJXOJeJhFuGoxxd0FE%2BfBB57pQ6Y2JUn6ET7vA3e9DOxi%2F%2BLonwA19XYgBu82b2heV57GFZNXV29cEUGlZmwnAioIcrF2bmS8PAANfdwlFukzNd6byTUInUa050vanJw%3D%3D'

#need to make league ID and cookies (above) automatically sent to the API call at some point
#testLeague = League(509804,2020,espn_s2,swid)
#test_bs = testLeague.box_scores(14)

#sidebet_players = []
#posParam = []
#consider_multiple = 0
#winnar = ""
#losar = ""

#sbList[1] = ['QB']
#sbList[2] = ['RB']
#sbList[3] = ['WR']
#sbList[4] = ['TE']
#sbList[5] = ['RB/WR/TE']
#sbList[6] = ['D/ST']
#sbList[7] = ['K']
#sbList[9] = ['QB', 'D/ST']
#sbList[10] = ['RB', 'RB']
#sbList[11] = ['WR', 'WR']
#sbList[12] = ['TE', 'RB/WR/TE']
#sbList[14] = ['BE']
#highest scoring team ['QB', 'RB', 'WR', 'TE' 'RB/WR/TE', 'D/ST', 'K']

"""debug = 0
if debug == 1:
    for bs in test_bs:    
        for boxp in bs.home_lineup:
            for boxpos in posParam:                
                if boxp.slot_position == boxpos:
                    sidebet_players.append(boxp)
        for boxp in bs.away_lineup:        
            for boxpos in posParam:                
                if boxp.slot_position == boxpos:
                    sidebet_players.append(boxp)

    if len(posParam) == 1 and consider_multiple != 1:
        best = sorted(sidebet_players, key=lambda x: x.points, reverse=True)
        worst = sorted(sidebet_players, key=lambda x: x.points)
        print("WINNAR: \n" + str(best[0]) + " " + str(best[0].current_team))
        bleh = list(filter(lambda x: x.team_id == best[0].current_team, testLeague.teams))
        bleh2 = list(filter(lambda x: x.team_id == worst[0].current_team, testLeague.teams))
        print((bleh)[0].owner)
        print("LOSAR: \n" + str(worst[0]) + " " + str(worst[0].current_team))
        print((bleh2)[0].owner)
    else:
        teamList = {}
        scoreList = {}
        teamForScore = {}
        totals = []
        for bteam in testLeague.teams:
            teamList[bteam.team_id] = []
            scoreList[bteam.team_id] = 0
    
        for boxp in sidebet_players:        
            teamList[boxp.current_team].append(boxp)
    
        for team in teamList:
            for p in teamList[team]:
                scoreList[team] += p.points
        
        for team in scoreList:
            teamForScore[scoreList[team]] = team

        for team in scoreList:
            totals.append(scoreList[team])

        best = sorted(totals, reverse=True)
        worst = sorted(totals)
        winnar = teamForScore[best[0]]
        losar = teamForScore[worst[0]]

        posString = ""
        for pos in posParam:
            posString = posString + " " + pos

        print("Winner is " + testLeague.get_team_data(winnar).owner + ' with ' + str(best[0]) + " points for sidebet:  Best" + posString)
        for player in teamList[winnar]:
            print(player)
        print("\n")
        print("Loser is " + testLeague.get_team_data(losar).owner + ' with ' + str(worst[0]) + " points for sidebet:  Worst" + posString)
        for player in teamList[losar]:
            print(player)
"""

#Returns list of teams, rosters, and owners for given league and year
class Team_List(Resource):   
    parser = reqparse.RequestParser()
    parser.add_argument('leagueID', type=int, help='ID of your fantasy football league')
    parser.add_argument('leagueYear', type=int, help='Year in which your fantasy league takes place')    
        
    #Defining the get method
    def get(self):        
        args = self.parser.parse_args()        
        retVal = {}
        keyError = None

        for arg in args:                    
            if args[arg] == None:
                keyError = 'You are the worst'
                retVal = {'Error: ': keyError}
        
        if keyError == None:
            testLeague = League(args['leagueID'],args['leagueYear'],espn_s2,swid)
            for team in testLeague.teams:
                retVal[team.team_id] = {}
                retVal[team.team_id]['owner'] = team.owner
                retVal[team.team_id]['teamName'] = team.team_name
                retVal[team.team_id]['roster'] = {}
                for player in team.roster:
                    retVal[team.team_id]['roster'][player.playerId] = player.name
            
            return retVal
        else:
            return retVal

#Returns the team and owner with the highest score for the given league, year, week, and positions.
class Get_Winner(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('leagueID', type=int, help='ID of your fantasy football league')
    parser.add_argument('leagueYear', type=int, help='Year in which your fantasy league takes place')
    parser.add_argument('positionList', type=str, help='List of positions to include in the score calculation')
    parser.add_argument('allowRepetition', type=int, help='Whether or not (1 or 0) all players for a given position should be totaled, or just the best one')
    parser.add_argument('leagueWeek', type=int, help='NFL week to use for score calculations')
    parser.add_argument('bestOrWorst', type=int, help='Whether to return the best (0) or worst (1) performer for given position(s)')   
    parser.add_argument('tiebreakerPos', type=str, help='The position to use as the tiebreaker.  For now, only "most points" is used for the given position')   

    #Defining the get method
    def get(self):        
        args = self.parser.parse_args()        
        retVal = {}
        sidebet_players = []
        tb_players = []
        posParam = []
        tbParam = ""
        winnar = ""
        losar = ""

        for arg in args:                               
            if args[arg] == None and arg != 'tiebreakerPos':
                keyError = 'You are the worst'
                retVal = {'Error: ': keyError}
        
        testLeague = League(args['leagueID'],args['leagueYear'],espn_s2,swid)
        test_bs = testLeague.box_scores(args['leagueWeek'])

        tbParam = args['tiebreakerPos']
        posParamOrig = args['positionList']
        posParam = posParamOrig.split(',')        
        consider_multiple = args['allowRepetition']
        
        for bs in test_bs:    
            for boxp in bs.home_lineup:
                for boxpos in list(posParam):                    
                    if boxp.slot_position == boxpos:
                        sidebet_players.append(boxp)
                    if tbParam != None and tbParam == boxpos:
                        tb_players.append(boxp)
            for boxp in bs.away_lineup:        
                for boxpos in list(posParam):
                    if boxp.slot_position == boxpos:
                        sidebet_players.append(boxp)
                    if tbParam != None and tbParam == boxpos:
                        tb_players.append(boxp)
        #
        # add logic for tiebreaker using tb_players list
        #                 
        if consider_multiple != 1:
            pointsList = []
            for sbp in sidebet_players:
                pointsList.append(sbp.points)            
            best = sorted(sidebet_players, key=lambda x: x.points, reverse=True)
            worst = sorted(sidebet_players, key=lambda x: x.points)
            winningOwner = list(filter(lambda x: x.team_id == best[0].current_team, testLeague.teams))
            losingOwner = list(filter(lambda x: x.team_id == worst[0].current_team, testLeague.teams))
            if args['bestOrWorst'] == 0:
                val = (best)[0].points        
                if pointsList.count(val) > 1:
                    retVal['Positions Considered'] = []
                    retVal['Positions Considered'] = posParam
                    retVal['Winning Players'] = None                    
                    retVal['Winning Team'] = "Multiple teams tied with " + str(val) + " points."
                    retVal['Winning Owner'] = None
                    retVal['Points'] = (best)[0].points
                else:                
                    retVal['Positions Considered'] = []
                    retVal['Positions Considered'] = posParam
                    retVal['Winning Player'] = str(best[0].name)
                    retVal['Winning Team'] = (winningOwner)[0].team_name
                    retVal['Winning Owner'] = (winningOwner)[0].owner
                    retVal['Points'] = (best)[0].points
            else:    
                val = (worst)[0].points        
                if pointsList.count(val) > 1:
                    retVal['Positions Considered'] = []
                    retVal['Positions Considered'] = posParam
                    retVal['Winning Players'] = None                    
                    retVal['Winning Team'] = "Multiple teams tied with " + str(val) + " points."
                    retVal['Winning Owner'] = None
                    retVal['Points'] = (worst)[0].points
                else:              
                    retVal['Positions Considered'] = []
                    retVal['Positions Considered'] = posParam
                    retVal['Winning Player'] = str(worst[0].name)
                    retVal['Winning Team'] = (losingOwner)[0].team_name
                    retVal['Winning Owner'] = (losingOwner)[0].owner            
                    retVal['Points'] = (worst)[0].points
        else:
            teamList = {}
            scoreList = {}
            teamForScore = {}
            totals = []
            for bteam in testLeague.teams:
                teamList[bteam.team_id] = []
                scoreList[bteam.team_id] = 0
        
            for boxPlayer in sidebet_players:                        
                teamList[boxPlayer.current_team].append(boxPlayer)
                scoreList[boxPlayer.current_team] += boxPlayer.points
            
            for team in scoreList:
                teamForScore[scoreList[team]] = team
                totals.append(scoreList[team])

            best = sorted(totals, reverse=True)
            worst = sorted(totals)
            winnar = teamForScore[best[0]]
            losar = teamForScore[worst[0]]

            if args['bestOrWorst'] == 0:
                if best.count(best[0]) > 1:
                    retVal['Positions Considered'] = []
                    retVal['Positions Considered'] = posParam
                    retVal['Winning Players'] = None                    
                    retVal['Winning Team'] = "Multiple teams tied with " + str(best[0]) + " points."
                    retVal['Winning Owner'] = None
                    retVal['Points'] = best[0]                    
                else:                    
                    retVal['Positions Considered'] = []
                    retVal['Positions Considered'] = posParam
                    retVal['Winning Players'] = []
                    for player in teamList[winnar]:
                        retVal['Winning Players'].append(str(player.name) + " - " + str(player.points) + " points")                
                    retVal['Winning Team'] = testLeague.get_team_data(winnar).team_name
                    retVal['Winning Owner'] = testLeague.get_team_data(winnar).owner
                    retVal['Points'] = best[0]
            else:
                if worst.count(worst[0]) > 1:
                    retVal['Positions Considered'] = []
                    retVal['Positions Considered'] = posParam
                    retVal['Winning Players'] = None                    
                    retVal['Winning Team'] = "Multiple teams tied with " + str(worst[0]) + " points."
                    retVal['Winning Owner'] = None
                    retVal['Points'] = worst[0]
                else:
                    retVal['Positions Considered'] = []
                    retVal['Positions Considered'] = posParam
                    retVal['Winning Players'] = []
                    for player in teamList[losar]:
                        retVal['Winning Players'].append(str(player.name) + " - " + str(player.points) + " points")                
                    retVal['Winning Team'] = testLeague.get_team_data(losar).team_name
                    retVal['Winning Owner'] = testLeague.get_team_data(losar).owner
                    retVal['Points'] = worst[0]

        return retVal

class Invalid_Req(Resource):    
    #Defining the get method
    def get(self):        
        return {'Bad Request': 'Invalid request.  GFY'}    

#Adding the URIs to the api
api.add_resource(Invalid_Req, '/')
api.add_resource(Get_Winner, '/Get_Winner')
api.add_resource(Team_List, '/Team_List') 

#run the applications
if __name__=='__main__':        
    ffApp.run()