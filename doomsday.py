import requests
import time
import datetime
from flask import Flask, jsonify, g, request
from flask_restful import Resource, reqparse, Api
from World import World
from Universe import Universe

doomsday = Flask(__name__)
api = Api(doomsday)

@doomsday.before_request
def start_timer():
    g.start = time.time()

@doomsday.after_request
def after_request(response):
    currentTime = time.time()
    reqTime = round(currentTime - g.start, 6) 
    print(str(request.path) + ' - Elapsed time: ' + str(reqTime))   
    return response

newUniverse = Universe()

# Adds a new world to the universe.
# The only parameter (row_list) is the list of rows that will be used to create the initial state of the world.
# The only acceptable characters in this parameter are ':', '.', ' ', 'T', and the row delimiter ','.
#
class Create_World(Resource):               

    def post(self):                    
        parser = reqparse.RequestParser()
        parser.add_argument('row_list', type=str, help='Comma delimited list of rows, with the first row being ground level and the rest stacking upwards from there.')  
        args = parser.parse_args()                
        retVal = {}
        responseText = None

        if args['row_list'] == None:            
            return {'404: ': 'No row list provided.'}

        else:      
            rows = args['row_list']                  
            for x in range(0, len(rows)):                
                if rows[x] not in '. :T,':
                    responseText = 'Invalid character(s) in row list'
                    retVal = {'404: ': responseText}
                    break                
                
            if retVal != {}:
                return retVal
            else:
                newWorldId = newUniverse.add_world(args['row_list'])     
                #display initial and end states of the world in the terminal                                           
                print(newUniverse.worlds[newWorldId].__format__('start', 'newline'))
                print('\n')                
                print(newUniverse.worlds[newWorldId].__format__('end', 'newline'))
                return {200: 'Success!', 'WorldID': newWorldId}

# Returns a list of world IDs that exist in the current universe
#
class List_Worlds(Resource):

    def get(self):
        worldList = {'200': 'Success!', 'WorldIDs': []}
        for world in newUniverse.worlds:            
            worldList['WorldIDs'].append(world)
        return jsonify(worldList)

# Adds a new row to the top of the world.   The entities in this row are dropped automatically into their proper places in the world.
# Parameters:
#   worldId <int> - ID of the world you want to add a row to.
#   row <string> - A list of '.', ':', ' ', and/or 'T' characters to add to the top of the world.   
#       The width of the new row must match the width of the world you are updating.
#
class Add_Row(Resource):

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('worldId', type=str, help='ID of the world you want to add a row to.')  
        parser.add_argument('row', type=str, help='The row you want to add to the top of the world.')  
        args = parser.parse_args()                
        retVal = {}
        responseText = None

        worldId = args['worldId']
        if worldId == None or newUniverse.worlds.get(worldId, 'missing') == 'missing':
            responseText = 'Invalid world ID.'
            retVal = {'404: ': responseText}
        
        else:
            row = args['row']            
            if len(row) != newUniverse.worlds[worldId].width:
                responseText = 'Width of row does not match width of existing world.'
                retVal = {'400: ': responseText}
            else:
                for x in range(0, len(row)):                
                    if row[x] not in '. :T':
                        responseText = 'Invalid character(s) in row'
                        retVal = {'400: ': responseText}
                        break                        
            
        if retVal != {}:
            return retVal        
        else:            
            newUniverse.worlds[worldId].add_row(row)
            newUniverse.worlds[worldId].set_end_state()
            text = 'Success? Call Show_World for world ' + str(worldId) + ' to find out.'
            return {'200: ': text}

# Returns textual representation of the world.  Always shows the current end state.
# Parameters:
#   worldId <int> - ID of the world you want to display.
#   strFormat <string> - Determines the format of the textual string that is returned.   Options:
#       'html' - Rows are separated by '<br>'
#       'url' - Rows are separated by '%0A' and spaces are represented by '%20'
#       'raw' - The end/initial state is returned as-is, which is a comma delimited list of '.', ':', ' ', and/or 'T' characters.
#       'newline' - Rows are separated by '\n'
#
class Show_World(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('worldId', type=str, help='ID of the world you want to receive a textual representation of.')          
        parser.add_argument('strFormat', type=str, help='Format of the text that is returned.  Options:  newline, url, raw, or html   (default: raw)')          
        args = parser.parse_args()                
        retVal = {}
        responseText = None

        worldId = args['worldId']
        strFormat = args['strFormat']

        if strFormat == None:
            strFormat = 'raw'

        if worldId == None or newUniverse.worlds.get(worldId, 'missing') == 'missing':
            responseText = 'Invalid world ID.'
            retVal = {'404: ': responseText}        
        
        if retVal != {}:
            return retVal        
        else:                                  
            #display initial and end states of the world in the terminal
            print(newUniverse.worlds[worldId].__format__('start', 'newline'))
            print('\n')
            print(newUniverse.worlds[worldId].__format__('end', 'newline'))            

            return newUniverse.show_world(worldId, 'end', strFormat)
            
# Deletes provided world from the Universe
# Parameters:
#   worldId <int> - ID of the world you want to delete.
class Delete_World(Resource):        
    
    def delete(self):        
        parser = reqparse.RequestParser()
        parser.add_argument('worldId', type=str, help='ID of the world you want to delete.')          
        args = parser.parse_args()                
        retVal = {}
        responseText = None

        worldId = args['worldId']
        if worldId == None or newUniverse.worlds.get(worldId, 'missing') == 'missing':
            responseText = 'Invalid world ID.'
            retVal = {'404: ': responseText}        
        
        if retVal != {}:
            return retVal
        
        else:
            del newUniverse.worlds[worldId]
            if newUniverse.worlds.get(worldId, 'missing') == 'missing':
                responseText = 'World ' + str(worldId) + ' was sucessfully deleted.'
                return {'200: ': responseText}
            else:                
                return {'400: ': 'World could not be deleted.'}

# 'Method not supported' (or other errors) returned if a specific URI is not used.
class Invalid_Req(Resource):        
    
    def get(self):        
        return {'405': 'Method not supported.'}

    def post(self):        
        return {'405': 'Method not supported.'} 

    def put(self):        
        return {'405': 'Method not supported.'}

    def delete(self):        
        return {'405': 'Method not supported.'}  


api.add_resource(Invalid_Req, '/')
api.add_resource(Create_World, '/Create_World')
api.add_resource(List_Worlds, '/List_Worlds')
api.add_resource(Add_Row, '/Add_Row')
api.add_resource(Delete_World, '/Delete_World')
api.add_resource(Show_World, '/Show_World')

if __name__=='__main__':        
    doomsday.run()